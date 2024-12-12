! pip install requests beautifulsoup4 yt-dlp moviepy

import os
import re
import requests
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
from moviepy.editor import concatenate_videoclips, VideoFileClip

# Channel URL
CHANNEL_URL = "https://www.youtube.com/@isldictionary/videos"
SEARCH_WORDS = ["word1", "word2", "word3"]  # Replace with your search words

def fetch_video_links(channel_url):
    """Fetch all video links from the channel."""
    response = requests.get(channel_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch the channel page.")

    soup = BeautifulSoup(response.text, "html.parser")
    video_links = []

    for link in soup.find_all("a", href=True):
        if "/watch?v=" in link["href"]:
            video_links.append(f"https://www.youtube.com{link['href']}")

    return list(set(video_links))  # Remove duplicates

def filter_videos_by_keywords(video_links, keywords):
    """Filter video links by checking if the title matches any of the keywords."""
    filtered_links = []
    for link in video_links:
        video_title = link.split("v=")[-1]  # Extract video ID for simplicity
        if any(word.lower() in video_title.lower() for word in keywords):
            filtered_links.append(link)
    return filtered_links

def download_videos(video_links, output_folder="downloads"):
    """Download videos from YouTube."""
    os.makedirs(output_folder, exist_ok=True)
    ydl_opts = {
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "format": "bestvideo+bestaudio/best",
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_links)

def merge_videos(video_folder="downloads", output_file="merged_video.mp4"):
    """Merge all videos in the folder into a single video."""
    clips = []
    for file in os.listdir(video_folder):
        if file.endswith(".mp4"):
            clips.append(VideoFileClip(os.path.join(video_folder, file)))

    if clips:
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    # Step 1: Fetch all video links from the channel
    video_links = fetch_video_links(CHANNEL_URL)

    # Step 2: Filter videos by search keywords
    filtered_links = filter_videos_by_keywords(video_links, SEARCH_WORDS)

    # Step 3: Download the filtered videos
    download_videos(filtered_links)

    # Step 4: Merge downloaded videos
    merge_videos()

