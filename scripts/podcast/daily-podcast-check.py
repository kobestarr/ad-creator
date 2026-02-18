#!/usr/bin/env python3
"""
Daily Podcast Transcription Check
Checks for new episodes and transcribes them automatically
"""

import os
import json
import requests
from datetime import datetime, timedelta

# Load credentials
def load_api_key():
    with open("/root/.credentials/uniscribe.json", 'r') as f:
        return json.load(f)['api_key']

# Configuration
PODCAST_CHANNEL_ID = "YOUR_CHANNEL_ID"  # YouTube channel ID
PODCAST_PLAYLIST_URL = "YOUR_PLAYLIST_URL"  # Or playlist URL

def get_latest_episodes(max_results=5):
    """Get latest episodes from YouTube playlist"""
    # This would use YouTube API - simplified for now
    return []

def should_transcribe(episode_id):
    """Check if episode already transcribed"""
    transcriptions_dir = "/root/clawd/podcast/transcriptions"
    if not os.path.exists(transcriptions_dir):
        return True
    
    for f in os.listdir(transcriptions_dir):
        if episode_id in f:
            return False
    return True

def run_daily_check():
    """Run daily check for new episodes"""
    api_key = load_api_key()
    
    print(f"📅 Daily Podcast Check - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    # TODO: Implement YouTube API integration
    # For now, this is a placeholder
    
    episodes = get_latest_episodes()
    
    if not episodes:
        print("ℹ️  No new episodes found (YouTube API not configured)")
        return
    
    new_count = 0
    for episode in episodes:
        if should_transcribe(episode['id']):
            print(f"🎙️  New episode: {episode['title']}")
            new_count += 1
            # Trigger transcription
            # os.system(f"python /root/clawd/scripts/podcast/transcribe-podcast.py --url {episode['url']} --title \"{episode['title']}\" --output /root/clawd/podcast/transcriptions")
    
    if new_count == 0:
        print("✅ No new episodes to transcribe")
    else:
        print(f"📤 Queued {new_count} episodes for transcription")

if __name__ == "__main__":
    run_daily_check()
