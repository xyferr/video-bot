# 🎥 Video Search and Upload Bot

A Python-based asynchronous bot that searches for videos on Instagram, monitors a directory for new video files, uploads them to a server using APIs, and manages local file cleanup. 

## 🌟 Features
- **Search & Download**: Finds videos on Instagram based on keywords and downloads them.
- **Directory Monitoring**: Watches the `/videos` folder for new `.mp4` files.
- **Asynchronous Upload**: Efficiently uploads videos to a server using pre-signed URLs.
- **Post Creation**: Creates a post on the server after upload.
- **Auto Cleanup**: Deletes videos locally after successful uploads.

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- An Instagram account for video search
- A valid `Flic-Token` for API authentication
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Environment Variables
- Create a .env file in the project root and add:
  ```bash
  FLIC_TOKEN=your_flic_token_here
    ```
### 3. Run the Bot
  ```bash
  python main.py
```

---

## 📂 Project Structure
```bash
video-bot/
├── main.py                # Entry point for the bot
├── upload.py              # Handles video uploads
├── create_post.py         # Manages post creation after upload
├── requirements.txt       # Project dependencies
├── README.md              # Documentation
└── .env                   # Environment variables
```
---

## 📋 How It Works
- Video Search:
Searches for Instagram videos using hashtags (e.g., "Motivational").
Requires Instagram login for access.
- Directory Monitoring:
Watches /videos for .mp4 files.
- Asynchronous Upload:
Fetches pre-signed upload URLs.
Uploads files to the server.
- Post Creation:
Sends video metadata to the server API.
- Cleanup:
Deletes videos from local storage after successful uploads