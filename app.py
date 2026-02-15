import streamlit as st
import os
import google_brain
import studio
import uploader

# --- ☁️ CLOUD COMPATIBILITY SETUP ☁️ ---
# This runs first to ensure the cloud server has your keys

# 1. Inject Environment Variables (API Keys)
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
if "PEXELS_API_KEY" in st.secrets:
    os.environ["PEXELS_API_KEY"] = st.secrets["PEXELS_API_KEY"]

# 2. Recreate client_secret.json (For YouTube Auth)
if "client_secret" in st.secrets:
    # We check if the file exists to avoid overwriting it constantly, 
    # but on cloud restart it's needed.
    with open("client_secret.json", "w") as f:
        f.write(st.secrets["client_secret"]["content"])

# 3. Recreate token.json (For YouTube Login Session)
if "token_json" in st.secrets:
    with open("token.json", "w") as f:
        f.write(st.secrets["token_json"]["content"])
# ---------------------------------------

st.set_page_config(page_title="TubeAutomator Pro", page_icon="🎥")
st.title("🎥 TubeAutomator Pro: AI Shorts Factory")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ Settings")
    duration = st.slider("Video Duration (seconds)", min_value=15, max_value=60, value=30)
    upload_enabled = st.checkbox("Upload to YouTube?", value=False)
    
    # Check if we are ready to upload
    if upload_enabled:
        if not os.path.exists("client_secret.json"):
            st.error("❌ Missing client_secret.json! Add it to Streamlit Secrets.")
        elif not os.path.exists("token.json"):
            st.warning("⚠️ No login token found. Authentication might fail on Cloud if not pre-authorized.")

# --- MAIN INTERFACE ---
topic = st.text_input("Enter Video Topic (e.g., 'Life on Mars'):")

if st.button("Generate Video"):
    if not topic:
        st.warning("Please enter a topic.")
    else:
        status = st.empty()
        
        # 1. ASSETS GENERATION
        status.info(f"Step 1/3: Writing Script & Downloading Videos ({duration}s)...")
        # google_brain might try to open files locally, but on cloud it just won't happen (no error usually)
        script, audio_path, video_paths = google_brain.generate_full_assets(topic, duration)
        
        if not audio_path:
            st.error("Generation Failed. Check API Keys.")
            st.stop()
            
        st.success(f"Assets Ready! ({len(video_paths)} videos downloaded)")
        with st.expander("View Script"):
            st.write(script)
        
        # 2. VIDEO EDITING
        status.info("Step 2/3: Editing, Stitching & Adding Subtitles...")
        final_video_path = studio.create_short_with_subtitles(audio_path, video_paths, script, topic)
        
        st.success("✅ Render Complete!")
        
        # Display Video Player
        st.video(final_video_path)
        
        # Add Download Button (Essential for Cloud)
        with open(final_video_path, "rb") as file:
            st.download_button(
                label="⬇️ Download Video",
                data=file,
                file_name=os.path.basename(final_video_path),
                mime="video/mp4"
            )
        
        # 3. YOUTUBE UPLOAD
        if upload_enabled:
            status.info("Step 3/3: Uploading to YouTube Shorts...")
            if not os.path.exists("token.json"):
                 st.error("❌ Cannot authenticate in Cloud mode without a pre-saved token.json in Secrets.")
            else:
                try:
                    video_title = f"{topic} #Shorts"
                    link = uploader.upload_to_youtube(final_video_path, video_title, script)
                    st.success(f"🚀 Upload Successful! [Watch Here]({link})")
                except Exception as e:
                    st.error(f"Upload Failed: {e}")
