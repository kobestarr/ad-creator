#!/usr/bin/env python3
"""
BluprintX Content → Oktopost Draft Poster
Parses Claude's content table and posts to Oktopost as drafts.

Usage:
    python post-to-oktopost.py --csv content.csv
    python post-to-oktopost.py --text "Post content here" --network LinkedIn --campaign 002g5m4amrtu2xs
    python post-to-oktopost.py --interactive
"""

import json
import sys
import csv
import argparse
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import base64
import os

# Load credentials
CRED_FILE = os.path.expanduser("~/.clawdbot/oktopost_credentials.json")
with open(CRED_FILE) as f:
    CREDS = json.load(f)

ACCOUNT_ID = CREDS["account_id"]
API_KEY = CREDS["api_key"]
BASE_URL = CREDS["base_url"]

def post_message(message, network="LinkedIn", campaign_id="002g5m4amrtu2xs", status="draft"):
    """Post a message to Oktopost as draft."""
    auth_string = f"{ACCOUNT_ID}:{API_KEY}"
    auth_bytes = auth_string.encode('utf-8')
    auth_header = base64.b64encode(auth_bytes).decode('utf-8')
    
    url = f"{BASE_URL}/message"
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = urlencode({
        "network": network,
        "campaignId": campaign_id,
        "message": message,
        "status": status
    }).encode('utf-8')
    
    req = Request(url, data=data, headers=headers, method="POST")
    try:
        with urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('Result'):
                msg_id = result.get('Message', {}).get('Id', 'Unknown')
                print(f"  ✅ {network}: Posted (ID: {msg_id})")
                return msg_id
            else:
                print(f"  ❌ {network}: Failed - {result}")
                return None
    except Exception as e:
        print(f"  ❌ {network}: Error - {e}")
        return None

def post_from_csv(csv_file, campaign_id="002g5m4amrtu2xs"):
    """Parse CSV and post all drafts."""
    print(f"\n📤 Posting from {csv_file} to campaign {campaign_id}...\n")
    
    posts_created = 0
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = row.get('Status', '').strip().lower()
            if status != 'briefed':
                continue
                
            content = row.get('Final_Copy', '').strip()
            platform = row.get('Platform', '').strip()
            account = row.get('Account', '').strip()
            date = row.get('Publish_Date', '').strip()
            
            if not content or not platform:
                continue
            
            # Map platform to Oktopost network
            network_map = {
                'LinkedIn': 'LinkedIn',
                'Instagram': 'Instagram', 
                'Twitter': 'Twitter'
            }
            network = network_map.get(platform)
            if not network:
                continue
            
            # Add account reference if leader post
            if account not in ['BPX', 'BluprintX']:
                content = f"[{account}]\n\n{content}"
            
            print(f"  {date} | {account} | {platform}")
            print(f"    Preview: {content[:80]}...")
            
            msg_id = post_message(content, network, campaign_id, "draft")
            if msg_id:
                posts_created += 1
    
    print(f"\n✅ Created {posts_created} draft posts!")

def post_interactive():
    """Interactive mode - enter content manually."""
    print("\n📝 INTERACTIVE POST MODE")
    print("Enter content to post as draft (Ctrl+C to exit)\n")
    
    while True:
        try:
            content = input("Content: ")
            network = input("Network (LinkedIn/Instagram/Twitter) [LinkedIn]: ") or "LinkedIn"
            campaign = input(f"Campaign ID [002g5m4amrtu2xs]: ") or "002g5m4amrtu2xs"
            
            print(f"\n📤 Posting to {network}...")
            post_message(content, network, campaign, "draft")
            print()
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break

def post_single(content, network="LinkedIn", campaign_id="002g5m4amrtu2xs"):
    """Post single message."""
    print(f"\n📤 Posting single message to {network}...")
    post_message(content, network, campaign_id, "draft")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post content to Oktopost as drafts")
    parser.add_argument("--csv", help="CSV file with content table")
    parser.add_argument("--text", help="Single message to post")
    parser.add_argument("--network", default="LinkedIn", help="Network for single post")
    parser.add_argument("--campaign", default="002g5m4amrtu2xs", help="Campaign ID")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        post_interactive()
    elif args.csv:
        post_from_csv(args.csv, args.campaign)
    elif args.text:
        post_single(args.text, args.network, args.campaign)
    else:
        parser.print_help()
        print("\n📌 Example: python post-to-oktopost.py --csv week_content.csv --campaign 002g5m4amrtu2xs")
        print("📌 Example: python post-to-oktopost.py --text 'Hello world' --network LinkedIn")
