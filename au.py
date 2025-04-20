import os
import pygame
from gtts import gTTS
import threading
import time

announcement_paused = threading.Event()

def announce_message(text, filename="announcement.mp3", lang="en", tld="com.au"):
    """
    Converts text to speech and plays the audio.
    """
    # Ensure the directory exists before saving the file.
    dir_name = os.path.dirname(filename)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    
    tts = gTTS(text, lang=lang, tld=tld)
    tts.save(filename)
    
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(70)

def stop_news_announcement():
    """Pauses the news announcements."""
    pygame.mixer.music.stop()

def resume_news_announcement():
    """Resumes news announcements if they were paused."""
    announcement_paused.clear()

def announce_login_success():
    announce_message("Login successful. Welcome back!", r"F:\Projects\Updated_Real_Time_News\audio\login_success.mp3")

def announce_registration_success():
    announce_message("Registration successful. You can now log in.", r"F:\Projects\Updated_Real_Time_News\audio\register_success.mp3")

def announce_registration_error():
    announce_message("Registration failed. The username might already be taken.", r"audio/register_error.mp3")

def announce_login_error():
    announce_message("Login failed. Please check your credentials.", r"F:\Projects\Updated_Real_Time_News\audio\login_error.mp3")

def announce_no_news_found():
    announce_message("Sorry, no news found.", "audio/no_news_found.mp3")

def announce_news(latest_news):
    if not latest_news:
        print("No new news found.")
        return
    for item in latest_news:
        text = (
            f"Class of the news: {item.get('class', 'No Title')}. "
            f"Sentiment of the news: {item.get('sentiment', 'No Sentiment')}. "
            f"Headline: {item.get('title', 'No Title')}. "
            f"Description: {item.get('summarization', 'No Description')}. "
            f"Time: {item.get('date', 'No Date')}."
        )
        filename = f"audio/news_{int(time.time())}.mp3"
        announce_message(text, filename)
    return filename

if __name__ == "__main__":
    announce_login_success()
    announce_login_error()
    announce_registration_success()
