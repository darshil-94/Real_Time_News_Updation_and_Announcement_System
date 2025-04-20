import json
import logging
import time
from requests_html import HTMLSession
from datetime import datetime, timedelta
import pytz
from Connect import get_database

logging.basicConfig(level=logging.INFO)

users, news_collection, processed_news_collection, annouced_news, annoucement_tracker = get_database()

def parse_relative_time(time_str):
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)
    time_str = time_str.lower().strip()
    try:
        if "min" in time_str:
            minutes = int(time_str.split()[0])
            return now - timedelta(minutes=minutes)
        if "hour" in time_str or "hr" in time_str:
            hours = float(time_str.split()[0])
            return now - timedelta(hours=hours)
        if "day" in time_str:
            days = int(time_str.split()[0])
            return now - timedelta(days=days)
    except Exception as e:
        logging.error(f"Error parsing relative time '{time_str}': {e}")
        return None
    return None

def standardize_date(date_str):
    tz = pytz.timezone("Asia/Kolkata")
    if not date_str or not date_str.strip():
        logging.warning(f"Unexpected date format: {date_str}")
        return None

    date_str = date_str.strip()
    if "ago" in date_str.lower():
        return parse_relative_time(date_str)
    else:
        try:
            dt = datetime.strptime(date_str, "%d %b %Y")
            return tz.localize(dt)
        except Exception as e:
            logging.warning(f"Unexpected date format: {date_str}")
            return None

def fetch_and_parse(config):
    session = HTMLSession()
    url = config["url"]
    source_name = config.get("source_name", url)
    logging.info(f"Fetching news from {url} ...")
    response = session.get(url)
    
    if response.status_code != 200:
        logging.error(f"Failed to fetch {url} with status code: {response.status_code}")
        return []
    
    news_list = []
    container_selector = config.get("Container", None)
    
    if container_selector:
        # Using the container to limit the scope for each news item.
        containers = response.html.find(container_selector)
        for container in containers:
            title_elem = container.find(config["Title"], first=True)
            title = title_elem.text if title_elem else "N/A"
            
            desc_elem = container.find(config["Description"], first=True)
            description = desc_elem.text if desc_elem else "N/A"
            
            date_elem = container.find(config["Date"], first=True)
            date = date_elem.text if date_elem else "N/A"
            
            # Standardize the date format if available
            if date != "N/A":
                standardized_date = standardize_date(date)
                if standardized_date:
                    date = standardized_date.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    date = "N/A"
            
            news_item = {
                "source": source_name,
                "title": title,
                "description": description,
                "date": date,
                "url": url
            }
            news_list.append(news_item)
    else:
        # When no container is provided, assume elements exist in parallel.
        title_elems = response.html.find(config["Title"])
        desc_elems = response.html.find(config["Description"])
        date_elems = response.html.find(config["Date"])
        count = min(len(title_elems), len(desc_elems), len(date_elems))
        
        for i in range(count):
            title = title_elems[i].text if i < len(title_elems) else "N/A"
            description = desc_elems[i].text if i < len(desc_elems) else "N/A"
            date = date_elems[i].text if i < len(date_elems) else "N/A"
            
            # Standardize the date if possible
            if date != "N/A":
                standardized_date = standardize_date(date)
                if standardized_date:
                    date = standardized_date.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    date = "N/A"
                    
            news_item = {
                "source": source_name,
                "title": title,
                "description": description,
                "date": date,
                "url": url
            }
            news_list.append(news_item)
    
    return news_list

def main():
    # Load JSON configuration from web.json
    with open("web.json", "r", encoding="utf-8") as f:
        config_data = json.load(f)
    
    complete_news = []
    incomplete_news = []
    
    # Process each website's configuration
    for config in config_data["websites"]:
        news_items = fetch_and_parse(config)
        for item in news_items:
            # Check if any of title, description, or date is missing (i.e. "N/A")
            if item["title"] == "N/A" or item["description"] == "N/A" or item["date"] == "N/A":
                incomplete_news.append(item)
            else:
                complete_news.append(item)
    
    # Filter out duplicates by checking if an article with the same title and url exists.
    unique_news = []
    duplicate_count = 0
    for item in complete_news:
        if news_collection.find_one({"title": item["title"], "url": item["url"]}):
            duplicate_count += 1
            continue
        unique_news.append(item)
    
    if unique_news:
        result_complete = news_collection.insert_many(unique_news)
        logging.info(f"Inserted {len(result_complete.inserted_ids)} unique news articles into the 'news' collection.")
    else:
        logging.info("No new unique news articles to insert.")
    
    # Write items with missing fields to incomplete_news.txt
    with open("incomplete_news.txt", "w", encoding="utf-8") as incomplete_file:
        for item in incomplete_news:
            incomplete_file.write(f"Source: {item['source']}\n")
            incomplete_file.write(f"URL: {item['url']}\n")
            incomplete_file.write(f"Title: {item['title']}\n")
            incomplete_file.write(f"Description: {item['description']}\n")
            incomplete_file.write(f"Date: {item['date']}\n")
            incomplete_file.write("=" * 80 + "\n\n")
    
    logging.info(f"Skipped {duplicate_count} duplicate articles.")

if __name__ == "__main__":
    while True:
        logging.info("Starting a new fetch cycle.")
        main()
        logging.info("Fetch cycle completed. Sleeping for 20 minutes.")
        time.sleep(1200)  