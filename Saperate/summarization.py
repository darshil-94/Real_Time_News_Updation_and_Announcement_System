from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    summary = summarizer(text, max_new_tokens=60, min_length=2, do_sample=False)

    return summary[0]['summary_text']