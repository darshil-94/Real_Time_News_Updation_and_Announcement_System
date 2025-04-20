from pymongo import MongoClient
import urllib.parse

def get_database():
    username = ""
    password = ""
    
    encoded_username = urllib.parse.quote_plus(username)
    encoded_password = urllib.parse.quote_plus(password)
    
    connection_string = (
        "mongodb+srv://{encoded_username}:{encoded_password}@realtimeupdate.7tmbf.mongodb.net/?retryWrites=true&w=majority&appName=RealTimeUpdate"
    )
    
    client = MongoClient(connection_string, serverSelectionTimeoutMS=30000)

    db = client['Real_Time_Updattion']
    
    users = db['users']
    news = db['news']
    processed_news = db['processed_news']
    announced_news = db['announced_news']  
    announcement_tracker = db['announcement_tracker'] 
    
    return users, news, processed_news, announced_news, announcement_tracker

if __name__ == "__main__":
    try:
        collections = get_database()
        print("✅ Connection established and collections accessed successfully!")
    except Exception as e:
        print("❌ Error connecting to MongoDB:", e)
