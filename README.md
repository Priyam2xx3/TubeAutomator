# 🎥 TubeAutomator: AI Shorts Factory

**TubeAutomator** is a fully automated Python application that generates ready-to-upload YouTube Shorts using AI. It writes scripts, narrates audio, finds relevant stock footage, generates subtitles, and uploads the final video to your channel—all from a simple dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5-orange)
![MoviePy](https://img.shields.io/badge/Render-MoviePy-yellow)

---

## ✨ Features

* **🧠 AI Brain (Gemini 2.5):** Automatically generates engaging scripts optimized for short-form content.
* **🗣️ Human-like Voiceovers:** Converts text to speech using Google TTS.
* **🎬 Smart Video Search:** Fetches multiple dynamic stock videos from Pexels based on the script's context.
* **📝 Custom Subtitles:** Generates professional, outlined subtitles using **Pillow** (No ImageMagick required!).
* **✂️ Auto-Editing:** Stitches clips, loops video to match audio length, and composites layers automatically.
* **☁️ Direct Upload:** Authenticates with YouTube Data API v3 to upload your video as a Short instantly.
* **🖥️ Local Dashboard:** Easy-to-use Streamlit interface to control topic and duration.

---
## 📂 Project Structure

The project is organized into modular Python scripts to handle AI generation, media processing, and uploading separately.

```text
TubeAutomator/
│
├── app.py                  # 🚀 Main Streamlit Application (The User Interface)
├── google_brain.py         # 🧠 AI Logic: Handles Gemini API (Scripts), gTTS (Audio), & Pexels (Video Fetching)
├── studio.py               # 🎬 Video Editor: Uses MoviePy & Pillow to stitch video, audio, and subtitles
├── uploader.py             # ☁️ YouTube Uploader: Handles authentication and video uploading via YouTube Data API
│
├── requirements.txt        # 📦 Dependencies: List of all Python libraries required to run the app
├── .gitignore              # 🛡️ Security: Tells Git to ignore sensitive files (API keys, videos)
│
├── .env                    # 🔑 Secrets (Local Only): Stores GEMINI_API_KEY and PEXELS_API_KEY
├── client_secret.json      # 🔑 Secrets (Local Only): Google OAuth 2.0 credentials for YouTube API
├── token.json              # 🔑 Secrets (Auto-generated): Stores your personal YouTube login session
│
└── output/                 # 📂 Output Folder: Stores generated MP3s, MP4s, and final videos (Ignored by Git)
## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/TubeAutomator.git](https://github.com/YOUR_USERNAME/TubeAutomator.git)
cd TubeAutomator

