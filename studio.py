import os
import re
import numpy as np
import textwrap
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

def create_text_image(text, fontsize=45, color='white', size=(1080, 1920)):
    """
    Creates a transparent subtitle image using Pillow.
    """
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Load Font (Try bold for better visibility)
    try:
        font = ImageFont.truetype("arialbd.ttf", fontsize)
    except IOError:
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", fontsize)
        except:
            font = ImageFont.load_default()

    # 2. Auto-wrap text
    # Smaller font (45px) allows ~35 chars per line
    chars_per_line = 35 
    wrapped_text = textwrap.fill(text, width=chars_per_line)

    # 3. Calculate Text Size
    try:
        bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback for older Pillow versions
        text_w, text_h = draw.textsize(wrapped_text, font=font)
    
    # 4. Position: Bottom Center (Subtitle Zone)
    x = (size[0] - text_w) / 2
    y = (size[1] * 0.80) - (text_h / 2) 

    # 5. Draw Text with Outline
    stroke_width = 3
    draw.text((x, y), wrapped_text, font=font, fill=color, 
              stroke_width=stroke_width, stroke_fill='black', align='center')
    
    return np.array(img)

# --- THIS IS THE FUNCTION YOUR APP IS LOOKING FOR ---
def create_short_with_subtitles(audio_path, video_paths, script, topic):
    print("\n✂️  Assembling Video...")
    
    # 1. Setup Audio
    if not audio_path or not os.path.exists(audio_path):
        print("❌ Error: Audio file missing.")
        return None

    audio = AudioFileClip(audio_path)
    target_duration = audio.duration
    
    # 2. Setup Video Clips
    clips = []
    if not video_paths:
        print("⚠️ No videos found. Creating black background.")
        color_clip = ColorClip(size=(1080, 1920), color=(0,0,0), duration=target_duration)
        clips.append(color_clip)
    else:
        for v in video_paths:
            try:
                clip = VideoFileClip(v)
                # Resize to cover 1080x1920
                if clip.h < 1920:
                    clip = clip.resize(height=1920)
                # Center Crop
                clip = clip.crop(x1=clip.w/2 - 540, width=1080, height=1920)
                clips.append(clip)
            except Exception as e:
                print(f"⚠️ Skipped bad clip {v}: {e}")

    # Concatenate clips
    if clips:
        # method='compose' is crucial for handling different resolutions safely
        final_video = concatenate_videoclips(clips, method="compose")
    else:
        final_video = ColorClip(size=(1080, 1920), color=(0,0,0), duration=target_duration)

    # Loop or Trim to match Audio
    if final_video.duration < target_duration:
        final_video = final_video.fx(vfx.loop, duration=target_duration)
    else:
        final_video = final_video.subclip(0, target_duration)
    
    # 3. Generate Subtitles (Pillow)
    print("📝 Generating Subtitles...")
    # Split script into sentences
    sentences = [s.strip() for s in re.split(r'[.!?]', script) if s.strip()]
    subtitle_clips = []
    
    if len(sentences) > 0:
        time_per_sentence = target_duration / len(sentences)
        for i, text in enumerate(sentences):
            # Generate image with clean font size (45)
            img_array = create_text_image(text, fontsize=45, size=(1080, 1920))
            
            # Create Clip
            txt_clip = ImageClip(img_array).set_duration(time_per_sentence).set_start(i * time_per_sentence)
            subtitle_clips.append(txt_clip)

    # 4. Composite
    # Combine video + subtitles + audio
    final_composite = CompositeVideoClip([final_video] + subtitle_clips).set_audio(audio)
    
    # Output File
    safe_topic = "".join([c for c in topic if c.isalnum() or c in (' ', '_')]).rstrip().replace(" ", "_")
    if not os.path.exists("output"):
        os.makedirs("output")
        
    output_file = os.path.join("output", f"{safe_topic}_FINAL.mp4")
    
    final_composite.write_videofile(
        output_file, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac", 
        preset="ultrafast",
        threads=4,
        logger='bar'
    )
    
    return output_file