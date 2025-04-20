from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import logging
import secrets
from Connect import get_database
from au import announce_news, announce_login_success, announce_login_error, announce_registration_error, announce_registration_success, stop_news_announcement , announce_message
from datetime import datetime
from chatbot import get_bot_response
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
logging.basicConfig(level=logging.INFO)
    
users, news_collection, processed_news_collection, annouced_news, annoucement_tracker = get_database()

def group_news(news_items):
    """Group news items by category for display purposes."""
    grouped = {}
    for news in news_items:
        category = news.get('class', 'Uncategorized')
        grouped.setdefault(category, []).append(news)
    return grouped

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.find_one({'username': username, 'password': password})
        if user:
            session['user_id'] = str(user['_id'])
            flash("Login successful!", "success")
            announce_login_success()
            return redirect(url_for('home'))
        announce_login_error()
        flash("Invalid username or password", "error")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        if users.find_one({'username': username}):
            return jsonify({'error': 'User already exists'}), 400
        users.insert_one({'username': username, 'password': password})
        announce_registration_success()
        flash("Registration successful! Please log in.", "success")
        return jsonify({'success': True}), 200
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    latest_news = list(processed_news_collection.find().sort("date", -1))
    
    selected_cat = request.args.get('cat')
    if selected_cat:
        latest_news = [
            news for news in latest_news 
            if news.get("class", "").upper() == selected_cat.upper()
        ]
        
    grouped_news = group_news(latest_news)
    
    announcement_message = None
    if latest_news:
        latest_news_item = latest_news[0]
        latest_date_str = latest_news_item.get("date")
        if latest_date_str:
            try:
                latest_date_obj = datetime.strptime(latest_date_str, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                logging.error(f"Error converting date: {e}")
                latest_date_obj = None

            announcement_message = f"Breaking News: {latest_news_item.get('title', 'No Title')}"
            last_announced_str = session.get("last_announced_time")
            last_announced_time = datetime.fromisoformat(last_announced_str) if last_announced_str else None
            if latest_date_obj and (not last_announced_time or latest_date_obj > last_announced_time):
                session["last_announced_time"] = latest_date_obj.isoformat()
        else:
            announcement_message = "Breaking News: No date available."
    else:
        announcement_message = "No breaking news at the moment."
    
    return render_template('index.html', grouped_news=grouped_news, announcement_message=announcement_message)

@app.route('/announce', methods=['GET'])
def announce_endpoint():
    """Endpoint to trigger announcement after the page loads.
       If a category (cat) parameter is provided, announce the latest news for that category.
    """
    cat = request.args.get('cat')
    if cat:
        filtered_news = list(processed_news_collection.find(
            {"class": {"$regex": f"^{cat}$", "$options": "i"}}
        ).sort("date", -1))
    else:
        filtered_news = list(processed_news_collection.find().sort("date", -1))
    
    if filtered_news:
        latest_news_item = filtered_news[0]
        announce_news([latest_news_item])
        return jsonify({"status": "success", "message": "Announcement triggered"}), 200
    else:
        return jsonify({"status": "error", "message": "No news available"}), 404

@app.route('/pause_announcement', methods=['POST'])
def pause_announcement():
    """Endpoint to pause the news announcement."""
    stop_news_announcement()
    return jsonify({"status": "success", "message": "Announcement paused"}), 200

@app.route('/get_bot_response', methods=['POST'])
def get_bot_response_endpoint():
    query = request.form.get('query')
    if not query:
        return jsonify({"response": "No query provided."})
    response = get_bot_response(query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)