# VPS Access Requirements

**Created:** 2026-02-01  
**Status:** NEEDED FOR AUTOMATION SCRIPTS

---

## What I Currently Have

✅ **Local Access:**
- Working directory: `/root/clawd`
- Can create scripts in `/root/clawd/`
- Can execute scripts locally
- Docker access (see running containers)

✅ **VPS Discovered:**
- IP: 72.62.134.99
- n8n running at: http://127.0.0.1:5678
- Traefik reverse proxy running

❌ **What I Need:**

---

## Priority 1: n8n API Access

**Needed to:** Control n8n programmatically, import workflows, create credentials

**Options:**

### Option A: n8n Basic Auth
```json
{
  "n8n_url": "http://127.0.0.1:5678",
  "n8n_user": "admin@email.com",
  "n8n_password": "password123"
}
```

### Option B: n8n API Key
```json
{
  "n8n_url": "http://127.0.0.1:5678",
  "n8n_api_key": "your-n8n-api-key"
}
```

**Where to find:** n8n Settings → API

---

## Priority 2: SSH Access (Optional but Recommended)

**Needed to:** 
- Deploy scripts to run as background services
- Set up cron jobs
- Access logs
- Manage Docker containers

**Required:**
```json
{
  "vps_host": "72.62.134.99",
  "vps_user": "ubuntu",
  "vps_password": "OR",
  "vps_ssh_key": "/path/to/private/key"
}
```

**Alternative:** Use existing n8n environment if it has docker/exec permissions

---

## Priority 3: Make.com API (If Using Make)

**Needed to:** Control Make.com scenarios programmatically

**Required:**
```json
{
  "make_api_key": "your-make-api-key",
  "make_org_id": "your-org-id"
}
```

---

## What I Can Build WITHOUT Full VPS Access

### Local Scripts (Can Build Now)
1. **Python scripts** - Run manually or via cron
2. **Node.js scripts** - Run manually or via cron
3. **API clients** - For UniScribe, n8n (if API key provided)
4. **Data processing scripts** - Transform/format data

### Examples I Can Build Today
```bash
# Python script for UniScribe transcription
python /root/clawd/scripts/transcribe-podcast.py --url YOUTUBE_URL

# Node.js script for job scraping
node /root/clawd/scripts/job-scraper.js --query "remote salesforce"

# Bash script for daily automation
bash /root/clawd/scripts/daily-balance-check.sh
```

### Cron Integration (I Can Create Entries)
```bash
# I can create cron entries like:
# 0 8 * * * python /root/clawd/scripts/morning-briefing.py
# 0 17 * * * python /root/clawd/scripts/afternoon-checkin.py
```

---

## What I CANNOT Build Without Credentials

❌ **n8n workflow imports** (need API key)  
❌ **Make.com scenario triggers** (need API key)  
❌ **SSH-based deployments** (need SSH access)  
❌ **Docker container management** (need permissions)  

---

## Recommendations

### For Immediate Progress
1. **Give me n8n API key** → I can build workflows programmatically
2. **Give me SSH access** → I can deploy as services

### For Quick Wins (No Credentials Needed)
1. Build **Python/Node.js scripts** that run from `/root/clawd/`
2. Set up **cron jobs** to run scripts daily
3. Scripts can call UniScribe API directly (you have subscription)

---

## Script Examples I Can Build

### 1. Podcast Transcription Script
```python
# /root/clawd/scripts/transcribe-podcast.py
import requests

def transcribe_youtube(url):
    response = requests.post(
        'https://api.uniscribe.co/api/v1/transcriptions/youtube',
        headers={'X-API-Key': 'YOUR_KEY'},
        json={'url': url, 'language_code': 'en'}
    )
    return response.json()
```

### 2. Job Application Automation
```python
# /root/clawd/scripts/job-apply.py
import apify
import openai

def scrape_and_apply():
    # Scrape jobs
    # Research companies
    # Generate personalized cover letter
    # Save to Google Sheets
```

### 3. Morning Briefing Script
```python
# /root/clawd/scripts/morning-briefing.py
def generate_briefing():
    # Check emails
    # Check calendar
    # Generate checklist
    # Send to user
    # Send sanitized version to wife
```

---

## Summary

**What I Need (Priority Order):**

| Priority | Item | Enables |
|----------|------|---------|
| 1 | n8n API Key | Programmatic workflow creation |
| 2 | SSH Access | Service deployment, cron management |
| 3 | Make.com API | Control Make scenarios |

**What I Can Do NOW:**
- Build Python/Node.js scripts in `/root/clawd/`
- Create cron job entries
- Call APIs directly (UniScribe, etc.)
- Process data, generate reports

---

*Created: 2026-02-01*
*Ready for credentials*
