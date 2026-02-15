import streamlit as st
import os
import google_brain
import studio
import uploader
import platform
import subprocess

def open_file_locally(path):
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.call(("open", path))
        else:
            subprocess.call(("xdg-open", path))
    except Exception as e:
        print(f"Cannot open file: {e}")

st.set_page_config(page_title="TubeAutomator Pro", page_icon="🎥")
st.title("🎥 TubeAutomator Pro: AI Shorts Factory")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ Settings")
    duration = st.slider("Video Duration (seconds)", min_value=15, max_value=60, value=30)
    upload_enabled = st.checkbox("Upload to YouTube?", value=False)
    if upload_enabled and not os.path.exists("client_secret.json"):
        st.error("Missing client_secret.json!")

# --- MAIN INTERFACE ---
topic = st.text_input("Enter Video Topic (e.g., 'Life on Mars'):")

if st.button("Generate Video"):
    if not topic:
        st.warning("Please enter a topic.")
    else:
        status = st.empty()
        
        # 1. ASSETS GENERATION
        status.info(f"Step 1/3: Writing Script & Downloading Videos ({duration}s)...")
        script, audio_path, video_paths = google_brain.generate_full_assets(topic, duration)
        
        if not audio_path:
            st.error("Generation Failed. Check API Keys.")
            st.stop()
            
        st.success(f"Assets Ready! ({len(video_paths)} videos downloaded)")
        st.text_area("Generated Script", script, height=100)
        
        # 2. VIDEO EDITING
        status.info("Step 2/3: Editing, Stitching & Adding Subtitles...")
        final_video_path = studio.create_short_with_subtitles(audio_path, video_paths, script, topic)
        
        st.success("✅ Render Complete!")
        st.video(final_video_path)
        open_file_locally(final_video_path)
        
        # 3. YOUTUBE UPLOAD
        if upload_enabled:
            status.info("Step 3/3: Uploading to YouTube Shorts...")
            try:
                video_title = f"{topic} #Shorts"
                link = uploader.upload_to_youtube(final_video_path, video_title, script)
                st.success(f"🚀 Upload Successful! [Watch Here]({link})")
            except Exception as e:
                st.error(f"Upload Failed: {e}")