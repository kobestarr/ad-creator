#!/usr/bin/env python3
"""
Research Transcription Script
For: YouTube tutorials, idea extraction, project research
Usage: python transcribe-video.py --url "YOUTUBE_URL" --title "Research Topic" --tags "tag1,tag2"
"""

import os
import json
import requests
import argparse
from datetime import datetime
from pathlib import Path
import re

CREDENTIALS_FILE = "/root/.credentials/uniscribe.json"

def load_credentials():
    with open(CREDENTIALS_FILE, 'r') as f:
        creds = json.load(f)
    return creds['api_key']

def extract_video_id(url):
    patterns = [r'v=([a-zA-Z0-9_-]{11})', r'youtube\.com/shorts/([a-zA-Z0-9_-]{11})', r'youtu\.be/([a-zA-Z0-9_-]{11})']
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def create_transcription(api_key, url, language="en"):
    base_url = "https://api.uniscribe.co/api/v1/transcriptions/youtube"
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
    payload = {"url": url, "language_code": language, "transcription_type": "transcript", "enable_speaker_diarization": False}
    response = requests.post(base_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code}")

def check_status(api_key, transcription_id):
    base_url = f"https://api.uniscribe.co/api/v1/transcriptions/{transcription_id}/status"
    headers = {"X-API-Key": api_key}
    return requests.get(base_url, headers=headers).json()

def get_results(api_key, transcription_id):
    base_url = f"https://api.uniscribe.co/api/v1/transcriptions/{transcription_id}"
    headers = {"X-API-Key": api_key}
    return requests.get(base_url, headers=headers).json()

def sanitize_filename(title):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', title)[:50]

def save_research(data, output_dir, title, tags, url):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    video_id = extract_video_id(url)
    safe_title = sanitize_filename(title)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    result = data.get('data', {}).get('result', {})
    transcript = result.get('text', '')
    summary = result.get('summary', '')
    outline = result.get('outline', '')
    
    metadata = {
        "title": title, "url": url, "video_id": video_id,
        "tags": tags.split(',') if tags else [],
        "transcribed_at": datetime.now().isoformat(),
        "duration_seconds": data.get('data', {}).get('duration', 0),
        "language": data.get('data', {}).get('language_code', 'en'),
        "files": {}
    }
    
    base_filename = f"{safe_title}_{timestamp}"
    
    # Transcript
    transcript_file = output_dir / f"{base_filename}_transcript.txt"
    with open(transcript_file, 'w') as f:
        f.write(f"# {title}\nURL: {url}\nVideo ID: {video_id}\nDate: {datetime.now().isoformat()}\nTags: {tags}\n{'='*60}\n\n{transcript}")
    metadata['files']['transcript'] = str(transcript_file)
    
    # Summary
    summary_file = output_dir / f"{base_filename}_summary.txt"
    with open(summary_file, 'w') as f:
        f.write(f"# {title}\n\n## Summary\n\n{summary}\n\n**Source:** {url}\n**Tags:** {tags}\n")
    metadata['files']['summary'] = str(summary_file)
    
    # Outline
    outline_file = output_dir / f"{base_filename}_outline.md"
    with open(outline_file, 'w') as f:
        f.write(f"# {title}\n\n**Tags:** {tags}\n**Source:** [{url}]({url})\n\n## Outline\n\n{outline}")
    metadata['files']['outline'] = str(outline_file)
    
    # Insights
    insights_file = output_dir / f"{base_filename}_insights.md"
    insights = []
    for line in outline.split('\n'):
        if line.startswith('#') and len(line.strip('# ')) > 3:
            insights.append(f"- 📌 {line.strip('# ').strip()}")
    with open(insights_file, 'w') as f:
        f.write(f"# {title} - Key Insights\n\n**Tags:** {tags}\n**Source:** [{url}]({url})\n\n## Key Takeaways\n\n" + "\n".join(insights))
    metadata['files']['insights'] = str(insights_file)
    
    # Full JSON
    json_file = output_dir / f"{base_filename}_full.json"
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    metadata['files']['full'] = str(json_file)
    
    # Metadata
    meta_file = output_dir / f"{base_filename}_meta.json"
    with open(meta_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    metadata['files']['meta'] = str(meta_file)
    
    # Update index
    index_file = output_dir / "_index.json"
    if index_file.exists():
        with open(index_file, 'r') as f:
            index = json.load(f)
    else:
        index = {"research": [], "last_updated": None}
    
    index['research'].append({"title": title, "url": url, "video_id": video_id, "tags": tags.split(',') if tags else [], "transcribed_at": datetime.now().isoformat()})
    index['last_updated'] = datetime.now().isoformat()
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)
    
    return metadata

def main():
    parser = argparse.ArgumentParser(description="Transcribe YouTube research videos")
    parser.add_argument("--url", required=True, help="YouTube URL")
    parser.add_argument("--title", required=True, help="Research topic title")
    parser.add_argument("--output", default="/root/clawd/research/transcriptions", help="Output directory")
    parser.add_argument("--language", default="en", help="Language code")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--wait", action="store_true", help="Wait for completion")
    
    args = parser.parse_args()
    
    print(f"🎬 Research Transcription: {args.title}")
    print(f"📎 URL: {args.url}")
    if args.tags:
        print(f"🏷️  Tags: {args.tags}")
    
    api_key = load_credentials()
    print("📤 Creating task...")
    result = create_transcription(api_key, args.url, args.language)
    transcription_id = result['data']['id']
    print(f"🆔 Task ID: {transcription_id}")
    
    if args.wait:
        import time
        print("⏳ Waiting...")
        while True:
            status = check_status(api_key, transcription_id)['data']['status']
            print(f"📊 {status}")
            if status == 'completed':
                break
            elif status == 'failed':
                raise Exception("Transcription failed")
            time.sleep(30)
        
        print("💾 Saving...")
        metadata = save_research(get_results(api_key, transcription_id), args.output, args.title, args.tags, args.url)
        print(f"\n✅ Saved to: {args.output}")
        for name, path in metadata['files'].items():
            print(f"   • {name}: {Path(path).name}")

if __name__ == "__main__":
    main()
