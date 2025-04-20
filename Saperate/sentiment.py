from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(title, description):
    sentiment_result = sentiment_model(f"{title} {description}")[0]['label']
    if any(keyword in f"{title} {description}".lower() for keyword in ["alert", "crisis", "emergency", "warning", "evacuate", "disaster", "rescue", "urgent", "breaking"]):
        return 'emergency'
    return 'emergency' if sentiment_result == 'NEGATIVE' else 'neutral' if sentiment_result == 'NEUTRAL' else 'no emergency'
