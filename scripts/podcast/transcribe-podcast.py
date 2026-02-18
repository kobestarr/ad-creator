#!/usr/bin/env python3
"""
UniScribe Podcast Transcription Script
For: Ultimate Football Heroes Podcast
Usage: python transcribe-podcast.py --url "YOUTUBE_URL" --output /path/to/output
"""

import os
import json
import requests
import argparse
from datetime import datetime
from pathlib import Path

# Load API key securely
CREDENTIALS_FILE = "/root/.credentials/uniscribe.json"

def load_credentials():
    """Load UniScribe API key from secure storage"""
    with open(CREDENTIALS_FILE, 'r') as f:
        creds = json.load(f)
    return creds['api_key']

def create_transcription(api_key, url, language="en"):
    """Create a YouTube transcription task"""
    base_url = "https://api.uniscribe.co/api/v1/transcriptions/youtube"
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": url,
        "language_code": language,
        "transcription_type": "transcript",
        "enable_speaker_diarization": False
    }
    
    response = requests.post(base_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

def check_status(api_key, transcription_id):
    """Check transcription status"""
    base_url = f"https://api.uniscribe.co/api/v1/transcriptions/{transcription_id}/status"
    
    headers = {"X-API-Key": api_key}
    
    response = requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Status Check Error: {response.status_code}")

def get_results(api_key, transcription_id):
    """Get completed transcription results"""
    base_url = f"https://api.uniscribe.co/api/v1/transcriptions/{transcription_id}"
    
    headers = {"X-API-Key": api_key}
    
    response = requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Results Error: {response.status_code}")

def save_results(data, output_dir, video_title):
    """Save transcription results to files"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{video_title}_{timestamp}"
    
    result = data.get('data', {}).get('result', {})
    
    # Save full transcript
    transcript_file = output_dir / f"{base_filename}_transcript.txt"
    with open(transcript_file, 'w') as f:
        f.write(f"Transcription: {video_title}\n")
        f.write(f"Date: {datetime.now().isoformat()}\n")
        f.write("=" * 50 + "\n\n")
        f.write(result.get('text', 'No transcript available'))
    print(f"✅ Saved transcript: {transcript_file}")
    
    # Save summary
    summary_file = output_dir / f"{base_filename}_summary.txt"
    with open(summary_file, 'w') as f:
        f.write(f"Summary: {video_title}\n")
        f.write(f"Date: {datetime.now().isoformat()}\n")
        f.write("=" * 50 + "\n\n")
        f.write(result.get('summary', 'No summary available'))
    print(f"✅ Saved summary: {summary_file}")
    
    # Save outline/mind map
    outline_file = output_dir / f"{base_filename}_outline.md"
    with open(outline_file, 'w') as f:
        f.write(f"# {video_title}\n\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        f.write("## Outline / Mind Map\n\n")
        f.write(result.get('outline', 'No outline available'))
    print(f"✅ Saved outline: {outline_file}")
    
    # Save JSON (full data)
    json_file = output_dir / f"{base_filename}_full.json"
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved full data: {json_file}")
    
    return {
        "transcript": str(transcript_file),
        "summary": str(summary_file),
        "outline": str(outline_file),
        "full": str(json_file)
    }

def main():
    parser = argparse.ArgumentParser(description="Transcribe podcast episodes using UniScribe")
    parser.add_argument("--url", required=True, help="YouTube URL of the podcast episode")
    parser.add_argument("--output", default="/root/clawd/podcast/transcriptions", help="Output directory")
    parser.add_argument("--language", default="en", help="Language code (default: en)")
    parser.add_argument("--title", required=True, help="Episode title for filenames")
    parser.add_argument("--wait", action="store_true", help="Wait for transcription to complete")
    
    args = parser.parse_args()
    
    print(f"🎙️ Starting transcription for: {args.title}")
    print(f"📎 URL: {args.url}")
    
    # Load API key
    api_key = load_credentials()
    print("✅ API key loaded")
    
    # Create transcription
    print("📤 Creating transcription task...")
    result = create_transcription(api_key, args.url, args.language)
    transcription_id = result['data']['id']
    print(f"🆔 Transcription ID: {transcription_id}")
    
    if args.wait:
        print("⏳ Waiting for transcription to complete...")
        import time
        
        while True:
            status_result = check_status(api_key, transcription_id)
            status = status_result['data']['status']
            print(f"📊 Status: {status}")
            
            if status == 'completed':
                break
            elif status == 'failed':
                error = status_result['data'].get('error_message', 'Unknown error')
                raise Exception(f"Transcription failed: {error}")
            else:
                time.sleep(30)  # Wait 30 seconds before checking again
        
        # Get results
        print("📥 Fetching results...")
        final_result = get_results(api_key, transcription_id)
        
        # Save all outputs
        print("💾 Saving results...")
        saved_files = save_results(final_result, args.output, args.title)
        
        print("\n✅ Transcription complete!")
        print(f"📁 Files saved to: {args.output}")
        for name, path in saved_files.items():
            print(f"   • {name}: {path}")
    else:
        print(f"✅ Transcription task created!")
        print(f"🆔 ID: {transcription_id}")
        print(f"💡 To check status: python {__file__} --check {transcription_id}")
        print(f"💡 To wait for completion: python {__file__} --url {args.url} --title \"{args.title}\" --wait")

if __name__ == "__main__":
    main()
