import os
import requests
import random
import time
import platform
import subprocess
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# Ensure output folder exists
output_folder = os.path.join(os.getcwd(), "output")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def open_file_locally(path):
    """Opens the file/folder using the system's default viewer"""
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.call(("open", path))
        else:
            subprocess.call(("xdg-open", path))
    except Exception as e:
        print(f"⚠️ Could not open file: {e}")

def get_clean_filename(topic, suffix, index=None):
    safe_topic = "".join([c for c in topic if c.isalnum() or c in (' ', '_')]).rstrip().replace(" ", "_")
    timestamp = int(time.time())
    if index is not None:
        return os.path.join(output_folder, f"{safe_topic}_{timestamp}_{index}_{suffix}")
    return os.path.join(output_folder, f"{safe_topic}_{timestamp}_{suffix}")

def get_model():
    """Robust Model Selector"""
    models = ["gemini-2.5-flash", "gemini-1.5-flash"]
    for m in models:
        try:
            model = genai.GenerativeModel(m)
            model.generate_content("test")
            return model
        except:
            continue
    return genai.GenerativeModel("gemini-pro")

def get_multiple_pexels_videos(query, topic, target_duration):
    """Downloads enough videos to cover the duration"""
    print(f"🎥 Searching Pexels for: {query}...")
    
    if not PEXELS_API_KEY:
        print("❌ PEXELS_API_KEY missing.")
        return []

    headers = {"Authorization": PEXELS_API_KEY}
    # Request more videos (15) to ensure we have enough diversity
    url = f"https://api.pexels.com/videos/search?query={query}&orientation=portrait&size=medium&per_page=15"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        if not data.get('videos'):
            return []
            
        video_paths = []
        current_duration = 0
        
        # Shuffle to get random variation
        available_videos = data['videos']
        random.shuffle(available_videos)

        for i, video_data in enumerate(available_videos):
            if current_duration >= target_duration:
                break
            
            # Find best quality MP4 link
            video_files = video_data['video_files']
            # Sort by quality (width) descending
            video_files.sort(key=lambda x: x['width'], reverse=True)
            
            # Pick the best one that isn't 4k (to save bandwidth), ideally 720p-1080p
            best_video = next((v for v in video_files if v['width'] <= 1080 and v['width'] >= 720), video_files[0])
            video_url = best_video['link']
            
            print(f"⬇️  Downloading clip {i+1} (ID: {video_data['id']})...")
            content = requests.get(video_url).content
            
            filename = get_clean_filename(topic, "clip.mp4", index=i)
            with open(filename, 'wb') as f:
                f.write(content)
            
            video_paths.append(filename)
            current_duration += video_data['duration']
            
        return video_paths

    except Exception as e:
        print(f"❌ Pexels Error: {e}")
        return []

def generate_full_assets(topic, duration_sec):
    open_file_locally(output_folder)
    print(f"♊ Gemini is planning a {duration_sec}s video on: {topic}...")
    
    model = get_model()

    # 1. Script tailored to duration
    # Approx 150 words per minute. For 30s, we need ~75 words.
    word_count = int((duration_sec / 60) * 140) 
    prompt = f"""
    Write a YouTube Shorts script about '{topic}'.
    - Target Length: Exactly {duration_sec} seconds (approx {word_count} words).
    - Format: Raw text only. Do not use **bold** or *italics*. Do not include [Visual Notes].
    - Content: Hook in the first sentence. Interesting facts.
    """
    try:
        response = model.generate_content(prompt)
        script_text = response.text.strip()
    except Exception as e:
        return f"Error: {e}", None, []

    # 2. Audio
    print("🗣️ Generating Voiceover...")
    tts = gTTS(text=script_text, lang='en', tld='us')
    audio_filename = get_clean_filename(topic, "audio.mp3")
    tts.save(audio_filename)
    open_file_locally(audio_filename)

    # 3. Video Search & Download
    search_prompt = f"Give me ONE broad search keyword for a Pexels stock video about: '{topic}'. Output ONLY the word."
    try:
        search_res = model.generate_content(search_prompt)
        search_term = search_res.text.strip().split()[0]
    except:
        search_term = topic 
    
    video_paths = get_multiple_pexels_videos(search_term, topic, duration_sec)

    return script_text, audio_filename, video_paths