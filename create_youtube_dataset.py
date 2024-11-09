import requests
from dotenv import load_dotenv
import os
import pandas as pd
import time

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_channel_id(channel_name):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "q": channel_name,
        "type": "channel",
        "part": "id"
    }
    response = requests.get(search_url, params=params)
    return response.json()["items"][0]["id"]["channelId"]

def get_channel_videos(channel_id):
    videos_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": 50,
        "type": "video"
    }
    
    response = requests.get(videos_url, params=params)
    return response.json()["items"]

# Define your channels and their types
channels_data = [
    # Add more channels as needed
]

channels_data = [
    # English Informative Channels
    {"name": "Khan Academy", "is_informative": 1},
    {"name": "Y Combinator", "is_informative": 1},
    {"name": "TED", "is_informative": 1},
    {"name": "National Geographic", "is_informative": 1},
    {"name": "SciShow", "is_informative": 1},
    {"name": "Crash Course", "is_informative": 1},
    {"name": "MIT OpenCourseWare", "is_informative": 1},
    {"name": "BBC News", "is_informative": 1},
    {"name": "The Economist", "is_informative": 1},
    {"name": "Veritasium", "is_informative": 1},
    {"name": "PBS NewsHour", "is_informative": 1},
    {"name": "Financial Times", "is_informative": 1},
    
    # English Non-Informative Channels
    {"name": "PewDiePie", "is_informative": 0},
    {"name": "MrBeast", "is_informative": 0},
    {"name": "Markiplier", "is_informative": 0},
    {"name": "Logan Paul", "is_informative": 0},
    {"name": "KSI", "is_informative": 0},
    {"name": "Dude Perfect", "is_informative": 0},
    {"name": "James Charles", "is_informative": 0},
    {"name": "David Dobrik", "is_informative": 0},
    {"name": "Sidemen", "is_informative": 0},
    {"name": "Surfing With Noz", "is_informative": 0},
    
    # French Informative Channels
    {"name": "Arte", "is_informative": 1},
    {"name": "France 24", "is_informative": 1},
    {"name": "Le Monde", "is_informative": 1},
    {"name": "Data Gueule", "is_informative": 1},
    {"name": "Science Étonnante", "is_informative": 1},
    {"name": "E-penser", "is_informative": 1},
    {"name": "Doc Seven", "is_informative": 1},
    {"name": "Nota Bene", "is_informative": 1},
    
    # French Non-Informative Channels
    {"name": "Squeezie", "is_informative": 0},
    {"name": "Cyprien", "is_informative": 0},
    {"name": "Norman", "is_informative": 0},
    {"name": "Amixem", "is_informative": 0},
    {"name": "Tibo InShape", "is_informative": 0},
    {"name": "Léna Situations", "is_informative": 0},
    {"name": "Michou", "is_informative": 0},
    {"name": "Domingo", "is_informative": 0},
    {"name": "Inoxtag 2.0", "is_informative": 0}
]

# Create empty lists to store data
all_titles = []
all_labels = []

# Collect data from each channel
for channel in channels_data:
    try:
        print(f"Processing channel: {channel['name']}")
        channel_id = get_channel_id(channel['name'])
        videos = get_channel_videos(channel_id)
        
        # Extract titles and add to lists
        for video in videos:
            title = video["snippet"]["title"]
            all_titles.append(title)
            all_labels.append(channel['is_informative'])
        
        # Add a delay to avoid hitting API rate limits
        time.sleep(1)
        
    except Exception as e:
        print(f"Error processing {channel['name']}: {str(e)}")
        continue

# Create DataFrame
df = pd.DataFrame({
    'title': all_titles,
    'is_informative': all_labels
})

# Save to CSV
df.to_csv('youtube_titles_dataset.csv', index=False)
print(f"Dataset created with {len(df)} videos")