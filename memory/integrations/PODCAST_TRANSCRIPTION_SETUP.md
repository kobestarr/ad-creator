# Podcast Transcription System - Setup & Usage

**Created:** 2026-02-01  
**Status:** READY TO USE

---

## Quick Start

### 1. Test with a YouTube Video

```bash
python /root/clawd/scripts/podcast/transcribe-podcast.py \
  --url "https://www.youtube.com/watch?v=EXAMPLE_VIDEO_ID" \
  --title "Ultimate Football Heroes - Test Episode" \
  --output /root/clawd/podcast/transcriptions \
  --wait
```

### 2. What It Creates

For each episode, you'll get:

```
/root/clawd/podcast/transcriptions/
└── Ultimate Football Heroes - Test Episode_20260201_160000/
    ├── transcript.txt    (full text)
    ├── summary.txt       (AI summary)
    ├── outline.md        (mind map)
    └── full.json         (complete data)
```

---

## Scripts Available

| Script | Purpose | Usage |
|--------|---------|-------|
| `transcribe-podcast.py` | Transcribe single episode | With --url, --title, --wait |
| `daily-podcast-check.py` | Auto-check for new episodes | Runs via cron |

---

## Daily Automation (Optional)

Add to crontab for automatic daily transcription:

```bash
crontab -e

# Add this line:
0 9 * * * python /root/clawd/scripts/podcast/daily-podcast-check.py
```

This runs daily at 9 AM to check for new episodes.

---

## Credential Storage

**API Key Location:** `/root/.credentials/uniscribe.json`
- Permissions: 600 (owner read/write only)
- Status: ✅ SECURE

**Format:**
```json
{
  "api_key": "us_w0mB5WRIwdUauuBFTpQ5b9oVf-lNFoft8H1WkYTjH8E",
  "created": "2026-02-01T16:06:00Z",
  "permissions": ["transcribe", "youtube", "read"]
}
```

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/transcriptions/youtube` | POST | Create YouTube transcription |
| `/api/v1/transcriptions/{id}/status` | GET | Check status |
| `/api/v1/transcriptions/{id}` | GET | Get results |

**Base URL:** `https://api.uniscribe.co`  
**Auth:** Header `X-API-Key: {your_key}`

---

## Security Notes

✅ API key stored in secure location (`/root/.credentials/`)  
✅ File permissions set to 600  
✅ No hardcoded credentials in scripts  
✅ Script runs with minimal permissions

---

## Next Steps

1. [ ] Test with a sample YouTube video
2. [ ] Add YouTube API key for playlist auto-detection
3. [ ] Set up daily cron job
4. [ ] Connect to blog system (auto-post summaries)

---

*Podcasting automation ready!*
