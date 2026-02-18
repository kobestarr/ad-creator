#!/usr/bin/env python3
"""
Generate BluprintX content and post to Oktopost drafts.
Uses brand references and tone guidelines to create posts.
"""

import json
import sys
import os
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import base64

# Load credentials
CRED_FILE = os.path.expanduser("~/.clawdbot/oktopost_credentials.json")
with open(CRED_FILE) as f:
    CREDS = json.load(f)

ACCOUNT_ID = CREDS["account_id"]
API_KEY = CREDS["api_key"]
BASE_URL = CREDS["base_url"]

# Default holding image for Instagram
DEFAULT_IG_MEDIA_ID = "026dgnkgcc9furg"

def post_message(message, network="LinkedIn", campaign_id="002g5m4amrtu2xs", status="draft", media_id=None):
    """Post a message to Oktopost as draft."""
    auth_string = f"{ACCOUNT_ID}:{API_KEY}"
    auth_bytes = auth_string.encode('utf-8')
    auth_header = base64.b64encode(auth_bytes).decode('utf-8')
    
    url = f"{BASE_URL}/message"
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "network": network,
        "campaignId": campaign_id,
        "message": message,
        "status": status
    }
    
    # Add media for Instagram (parameter is "media" not "mediaId")
    if network == "Instagram" and media_id:
        data["media"] = media_id
    
    data_encoded = urlencode(data).encode('utf-8')
    
    req = Request(url, data=data_encoded, headers=headers, method="POST")
    try:
        with urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('Result'):
                msg_id = result.get('Message', {}).get('Id', 'Unknown')
                return True, msg_id
            return False, result
    except Exception as e:
        return False, str(e)

# Generate content for THIS week (Mon-Fri next 5 days)
today = datetime.now()
days_ahead = 7 - today.weekday() if today.weekday() < 7 else 0
if days_ahead == 0: days_ahead = 7
next_monday = today + timedelta(days=days_ahead)

posts = []

# ============ MONDAY - TOFU ============
monday = next_monday
posts.append({
    "date": monday.strftime("%Y-%m-%d"),
    "platform": "LinkedIn",
    "account": "BPX",
    "funnel": "TOFU",
    "content": """AI is moving from experiment to measurable business value. 26% of companies have already made that leap.

The gap between AI pilots and AI profits is closing fast.

What is holding your organisation back from the 26%?

Not technology. Not data.

It is the gap between strategy and execution.

Your next idea is waiting. The question is: how fast can you push it into reality?

#AITransformation #DigitalTransformation #BluprintX"""
})

posts.append({
    "date": monday.strftime("%Y-%m-%d"),
    "platform": "Twitter",
    "account": "BPX",
    "funnel": "TOFU",
    "content": """26% of companies have scaled AI from pilot to production.

The other 74% are still experimenting.

What separates the winners from the experimenters?

It is not technology. It is strategy.

#AI #DigitalTransformation

1/2"""
})

posts.append({
    "date": monday.strftime("%Y-%m-%d"),
    "platform": "Instagram",
    "account": "BPX",
    "funnel": "TOFU",
    "content": """26% of companies have scaled AI successfully.

The rest are still in pilot mode.

What separates the winners from the experimenters?

It is not technology. It is strategy.

Your next idea is waiting. How fast can you push it into reality?

#AITransformation #DigitalTransformation #BluprintX""",
    "media_id": DEFAULT_IG_MEDIA_ID
})

# ============ TUESDAY - MOFU ============
tuesday = next_monday + timedelta(days=1)
posts.append({
    "date": tuesday.strftime("%Y-%m-%d"),
    "platform": "LinkedIn",
    "account": "BPX",
    "funnel": "MOFU",
    "content": """Most AI projects fail not because of the technology, but because they skip the strategy phase.

You cannot optimise what you have not designed.

Here is what winning teams do differently:

1. They define success metrics BEFORE they build
2. They identify the one business outcome that matters
3. They build for adoption, not just implementation

The fastest path to AI value is a strategy-first approach.

What outcome are you optimising for?"""
})

posts.append({
    "date": tuesday.strftime("%Y-%m-%d"),
    "platform": "Twitter",
    "account": "BPX",
    "funnel": "MOFU",
    "content": """Most AI projects fail because they skip the strategy phase.

You cannot optimise what you have not designed.

What is your single business outcome? #AI

2/2"""
})

# ============ WEDNESDAY - MOFU ============
wednesday = next_monday + timedelta(days=2)
posts.append({
    "date": wednesday.strftime("%Y-%m-%d"),
    "platform": "LinkedIn",
    "account": "BPX",
    "funnel": "MOFU",
    "content": """Speed is the new currency in B2B.

The companies winning on AI are not the ones with the most sophisticated models.

They are the ones who move fastest from insight to action.

How fast can your organisation go from "we should try this" to "we are seeing results"?

If the answer is months, you have a problem.

If the answer is weeks, you are in the 26%."""
})

# ============ THURSDAY - BOFU ============
thursday = next_monday + timedelta(days=3)
posts.append({
    "date": thursday.strftime("%Y-%m-%d"),
    "platform": "LinkedIn",
    "account": "BPX",
    "funnel": "BOFU",
    "content": """The gap between AI investment and AI return is a strategy problem, not a technology problem.

Companies who move fastest from pilot to production share a common trait:

They know exactly what success looks like before they start.

No vague "explore AI potential" objectives.

Just one clear outcome, defined metrics, and a path to adoption.

Ready to close the gap between your AI pilots and AI profits?

Book a call: bluprintx.com/book-a-call"""
})

posts.append({
    "date": thursday.strftime("%Y-%m-%d"),
    "platform": "Instagram",
    "account": "BPX",
    "funnel": "BOFU",
    "content": """The gap between AI investment and AI return is a strategy problem.

What does success look like for your AI initiatives?

If you cannot answer that, you are not ready to scale.

Ready to close the gap?

Link in bio to book a call.

#AITransformation #ROI #BluprintX""",
    "media_id": DEFAULT_IG_MEDIA_ID
})

# ============ FRIDAY - TOFU-LIGHT ============
friday = next_monday + timedelta(days=4)
posts.append({
    "date": friday.strftime("%Y-%m-%d"),
    "platform": "LinkedIn",
    "account": "BPX",
    "funnel": "TOFU-Light",
    "content": """Quick thought on AI transformation:

It is not about the technology you choose.

It is about the problem you are solving.

Technology should solve problems, not create them.

That is the BluprintX approach. Strategy led, technology powered, AI optimised.

What problem are you solving this week?"""
})

# ============ LEADER POSTS (LinkedIn only) ============
posts.append({
    "date": monday.strftime("%Y-%m-%d"),
    "platform": "LinkedIn",
    "account": "Lee Hackett",
    "funnel": "TOFU",
    "content": """I have been thinking about the data vs. technology debate.

Everyone talks about AI. Few talk about what actually drives value.

Data beats algorithms. Every time.

The companies seeing real ROI from AI investments are not using better models.

They are using better data.

What is your data strategy? #ArtificialIntelligence #DataStrategy"""
})

posts.append({
    "date": wednesday.strftime("%Y-%m-%d"),
    "platform": "LinkedIn",
    "account": "Lee Hackett",
    "funnel": "MOFU",
    "content": """The fastest growing companies I have worked with have one thing in common.

They optimise for speed, not complexity.

When complexity builds, growth slows.

When systems align to deliver what customers need, speed returns.

Complexity is the enemy of growth. #GrowthStrategy #BusinessTransformation"""
})

posts.append({
    "date": thursday.strftime("%Y-%m-%d"),
    "platform": "LinkedIn",
    "account": "Lee Hackett",
    "funnel": "BOFU",
    "content": """Four phases to AI transformation:

1. Design - What does success look like?
2. Deliver - Build for adoption
3. Adopt - Get people using it
4. Grow - Expand across the organisation

Most companies skip phase 1.

That is why most AI projects never deliver value.

What is your phase? #AITransformation #DigitalTransformation"""
})

# Post all to Oktopost as drafts
print(f"\n{'='*60}")
print(f"GENERATING & POSTING BLUPRINTX CONTENT")
print(f"Week: {next_monday.strftime('%B %d')} - {friday.strftime('%d, %Y')}")
print(f"{'='*60}\n")

campaign_id = "002g5m4amrtu2xs"  # AI Value Accelerator
posted = 0
failed = 0

for post in posts:
    media_note = ""
    if post.get('media_id'):
        media_note = " [with holding image]"
    
    print(f"{post['date']} | {post['account']} | {post['platform']} | {post['funnel']}{media_note}")
    print(f"  Preview: {post['content'][:70]}...")
    
    success, result = post_message(
        post['content'], 
        post['platform'], 
        campaign_id, 
        "draft",
        post.get('media_id')
    )
    if success:
        posted += 1
        print(f"  ✅ Draft created\n")
    else:
        failed += 1
        print(f"  ❌ Failed: {result}\n")

print(f"\n{'='*60}")
print(f"COMPLETE: {posted} drafts created, {failed} failed")
print(f"{'='*60}")
print(f"\n📋 Review in Oktopost: https://app.oktopost.com/campaign/{campaign_id}/message")
