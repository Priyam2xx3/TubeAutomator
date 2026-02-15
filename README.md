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
## Project Structure

TubeAutomator/
├── app.py              # Main Streamlit Dashboard UI
├── google_brain.py     # AI Logic (Gemini), Audio (gTTS), Pexels Downloader
├── studio.py           # Video Editing & Subtitle Generation (MoviePy + Pillow)
├── uploader.py         # YouTube Data API Upload Logic
├── requirements.txt    # Python dependencies
├── .env                # API Keys (Hidden from Git)
├── client_secret.json  # Google OAuth Credentials (Hidden from Git)
└── output/             # Generated assets (MP3s, MP4s)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/TubeAutomator.git](https://github.com/YOUR_USERNAME/TubeAutomator.git)
cd TubeAutomator

