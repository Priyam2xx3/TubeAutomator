import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

def upload_to_youtube(video_path, title, description):
    print("🚀 Connecting to YouTube...")
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    
    # Check for secrets file
    if not os.path.exists('client_secret.json'):
        raise FileNotFoundError("client_secret.json not found. Cannot upload.")
        
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = build("youtube", "v3", credentials=credentials)

    print(f"☁️  Uploading {title}...")
    
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title[:100], # YouTube limit
                "description": description[:5000],
                "tags": ["Shorts", "AI", "Tech"],
                "categoryId": "28" # Science & Tech
            },
            "status": {
                "privacyStatus": "private", # Start private to be safe
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"    Progress: {int(status.progress() * 100)}%")
            
    video_id = response.get('id')
    return f"https://youtu.be/{video_id}"