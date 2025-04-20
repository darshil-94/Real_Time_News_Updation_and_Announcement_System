from Connect import get_database
from datetime import datetime
from Saperate.classification import classify_review
from Saperate.sentiment import analyze_sentiment
from Saperate.summarization import summarize_text
import logging
from transformers import BertForSequenceClassification, get_linear_schedule_with_warmup, BertTokenizer
from torch.optim import AdamW
import torch
import time

model_path = r"F:\Projects\Updated_Real_Time_News\Saperate\f_model\classification_bert_8_classes_initial_ep_equ_data.pth"
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

checkpoint = torch.load(model_path, map_location=torch.device('cpu'))

model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=8)
model.load_state_dict(checkpoint['model_state_dict'])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device) 

logging.basicConfig(level=logging.INFO)

users, news_collection, processed_news_collection, annouced_news, annoucement_tracker = get_database()

def process_news():
    cursor = news_collection.find({}, {"title": 1, "description": 1, "date": 1, "_id": 0})
    news_items = list(cursor)
    logging.info(f"Fetched {len(news_items)} news items for processing.")
    
    processed_items = []
    skipped_count = 0

    for item in news_items:
        title = item.get("title", "N/A")
        description = item.get("description", "")
        date = item.get("date", "N/A")
        
        if processed_news_collection.find_one({"title": title}):
            skipped_count += 1
            continue
        
        summary = summarize_text(description)
        classification = classify_review(title, description, model, tokenizer, device)
        sentiment = analyze_sentiment(title, description)
        
        processed_item = {
            "title": title,
            "summarization": summary,
            "date": date,
            "class": classification,
            "sentiment": sentiment,
            "date": date
        }
        processed_items.append(processed_item)
    
    if processed_items:
        result = processed_news_collection.insert_many(processed_items)
        logging.info(f"Inserted {len(result.inserted_ids)} processed news items into 'news_processed_collection'.")
    
    logging.info(f"Skipped {skipped_count} news items that were already processed.")

if __name__ == "__main__":
    while True:
        logging.info("Starting a new fetch cycle.")
        process_news()
        logging.info("Fetch cycle completed. Sleeping for 10 minutes.")
        time.sleep(300)
