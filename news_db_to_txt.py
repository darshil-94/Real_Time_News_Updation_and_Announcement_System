import os
from dotenv import load_dotenv
from Connect import get_database
import time

load_dotenv()

users, news_collection, processed_news_collection, annouced_news, annoucement_tracker = get_database()

current_dir = os.path.dirname(os.path.abspath(__file__))
output_file_path = os.path.join(current_dir, "documents/news_data.txt")

existing_entries = set()
if os.path.exists(output_file_path):
    with open(output_file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        # Split entries using the separator (50 dashes).
        if content:
            entries = content.split("-" * 50)
            for entry in entries:
                cleaned = entry.strip()
                if cleaned:
                    existing_entries.add(cleaned)

with open(output_file_path, "a", encoding="utf-8") as f:
    for doc in news_collection.find():
        title = doc.get("title", "N/A")
        description = doc.get("description", "N/A")
        entry_text = f"Title: {title}\nDescription: {description}".strip()
        
        if entry_text in existing_entries:
            print("Duplicate found. Skipping entry.")
        else:
            f.write(f"Title: {title}\n")
            f.write(f"Description: {description}\n")
            f.write("-" * 50 + "\n")
            print("Process completed. Now wait for 20 mins.")
            existing_entries.add(entry_text)
            time.sleep(1200) 
        
print(f"Data has been written to {output_file_path}")