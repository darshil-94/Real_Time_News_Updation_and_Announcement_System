# Real-Time News Updation

A voice-interactive news update system that scrapes, processes, and announces the latest news in real time, allowing users to request, filter, and interact using voice commands.

## Table of Contents

- [Introduction](#introduction)

- [ScreenShots](#screenshots)

- [Features](#features)

- [Architecture & Tech Stack](#architecture--tech-stack)

- [Installation](#installation)

- [Configuration](#configuration)

- [Usage](#usage)

- [Contributing](#contributing)

- [License](#license)

- [Contact](#contact)

---

## Introduction

"Real-Time News Updation" is a smart voice assistant designed to keep you informed with the latest news headlines and detailed articles through automated voice announcements. It integrates web scraping, Large Language Models , and speech synthesis/recognition to deliver an interactive news experience.

Key goals:

- Continuously fetch and store news in a database.
- Automatically announce breaking and new headlines.
- Allow users to query and filter news by category or keywords.
- Provide a seamless voice-driven interface for updates.

---
## ScreenShots

![Log_in](https://github.com/user-attachments/assets/2e63871f-ab7c-4f36-bc8e-072d04c43d23)

![Home_page_1](https://github.com/user-attachments/assets/bca8f012-9028-4b84-a828-ddaf447c1ccf)

![Home_page_2](https://github.com/user-attachments/assets/603995d7-6445-4555-b4e3-4f98c708ce59)

![Chat_bot](https://github.com/user-attachments/assets/7a1acb62-4f84-47cc-bd6d-f7be3377db3d)


---
## Features

1. **Automated News Scraping**
   - Periodically scrape headlines and descriptions from configured news sources.
2. **MongoDB Storage**
   - Store and index articles in a `news` collection for fast retrieval.
3. **LLM Processing**
   - Classify news into 8 categories using a fine-tuned BERT (bert-base-uncase) model .
   - Analyze sentiment and generate concise summaries using pre-trained BERT.
4. **Voice Announcements**
   - Synthesize and play the latest  new updates on login or when new articles arrive.
   - Format: "The news is from [Category], the title is [Title], and the description is [Description]."
5. **Interactive Voice Bot**
   - Recognize user voice queries (e.g., "Give me sports news") and respond with relevant headlines.
   - Support contextual follow‑ups (e.g., "What about that story you just announced?").
6. **User Authentication**
   - Greet users by name on login/registration/logout via voice.
7. **Context-Aware Suggestions**
   - Based on recent news, provide related recommendations.

---

## Architecture & Tech Stack

- **Backend**: Python, FastAPI
- **Database**: MongoDB
- **Web Scraping**: request\_html
- **LLM Models**: PyTorch (fine‑tuned BERT)
- **Voice**: Google Text-to-Speech (gTTS) , SpeechRecognition
- **Frontend (Dashboard)**: html , css , javascript
- **Chatbot:** Llama3 + RAG (My database News)



---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/real-time-news-updation.git
   cd real-time-news-updation
   ```

2. **Create a virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows

   pip install -r requirements.txt
   ```

3. **Setup MongoDB**

   - Install or start a MongoDB instance (locally or cloud).
   - Update your connection string in the `.env` file (see [Configuration](#configuration)).

4. **Run the application**

   ```bash
   python app.py
   ```

---

## Configuration

Copy the template and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```
MONGODB_URI=mongodb+srv://<user>:<pass>@cluster0.mongodb.net/newsdb
SCRAPE_INTERVAL_MINUTES=15
VOICE_LANGUAGE=en-US
```

---

## Usage

- **Automated mode:** On startup, the service scrapes news and announces the latest headlines via speakers.
- **Voice commands:**
  - "Give me technology news" → lists or announces tech headlines.
  - "Summarize the last business article" → reads out a summary.
  - "What did you announce earlier?" → revisits recent news content.

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to your branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

---

## License

This project is licensed under the D&P License.

---

## Contact

Darshil Patel – [darshilpatel.ds9472@gmail.com](mailto\:darshilpatel.ds9472@gmail.com)\
Project Link: [https://github.com/darshil94/Real\_Time\_News\_Updation\_and\_Announcement\_System](https://github.com/darshil94/Real_Time_News_Updation_and_Announcement_System)

