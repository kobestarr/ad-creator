# UniScribe API Research - Complete Technical Analysis

**Research Date:** 2026-02-01  
**Source:** https://www.uniscribe.co/docs  
**Status:** BETA (may change)

---

## 🎯 EXECUTIVE SUMMARY

UniScribe provides a full REST API for audio/video transcription with:
- **Transcription** (audio/video → text)
- **Summarization** (auto-generated summaries)
- **Mind Maps** (outline in markdown)
- **Speaker Diarization** (identify multiple speakers)
- **YouTube Integration** (direct video URL transcription)
- **Webhook Support** (async notifications)
- **90+ Languages**

**Pricing:** Requires active subscription or LTD plan (free users cannot access API)

---

## 📊 WHAT YOU CAN DO WITH THE API

### Core Capabilities

| Capability | Description | Output |
|------------|-------------|--------|
| **Transcription** | Audio/video → text | Full text with timestamps |
| **Summarization** | Auto-generate summary | ~1-3 paragraph summary |
| **Mind Maps** | Auto-generate outline | Markdown outline structure |
| **Speaker Diarization** | Identify speakers | Speaker labels (A, B, C...) |
| **Subtitles** | Generate SRT/VTT | Subtitles with timestamps |
| **Word-Level Timing** | Per-word timestamps | Start/end for each word |

---

## 🔗 API ENDPOINTS REFERENCE

### Base URL
```
https://api.uniscribe.co
```

### Authentication
```
Header: X-API-Key: your_api_key
```

### Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/files/upload-url` | Get pre-signed upload URL |
| PUT | (upload_url) | Upload file directly |
| POST | `/api/v1/transcriptions` | Create transcription |
| POST | `/api/v1/transcriptions/youtube` | Transcribe YouTube video |
| GET | `/api/v1/transcriptions` | List all transcriptions |
| GET | `/api/v1/transcriptions/{id}` | Get transcription details |
| GET | `/api/v1/transcriptions/{id}/status` | Check status only |

---

## 📤 DETAILED ENDPOINT SPECS

### 1. Upload File (Recommended)

**Step 1: Get Upload URL**
```
POST /api/v1/files/upload-url
Content-Type: application/json
X-API-Key: your_api_key

{
  "filename": "my-audio.mp3",
  "file_size": 1048576,
  "upload_expires_in": 3600,
  "download_expires_in": 1800
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "upload_url": "https://r2.cloudflare.com/bucket/...mp3?X-Amz-Signature=...",
    "download_url": "https://r2.cloudflare.com/bucket/...mp3?X-Amz-Signature=...",
    "file_key": "12345-abc123def456.mp3"
  }
}
```

**Step 2: Upload File**
```
PUT {upload_url}
Content-Type: audio/mpeg
--binary @my-audio.mp3
```

**Step 3: Create Transcription**
```
POST /api/v1/transcriptions
Content-Type: application/json
X-API-Key: your_api_key

{
  "file_key": "12345-abc123def456.mp3",
  "filename": "my-audio.mp3",
  "language_code": "en",
  "transcription_type": "transcript",
  "enable_speaker_diarization": false,
  "webhook_url": "https://your-webhook.com"
}
```

---

### 2. From External URL

```
POST /api/v1/transcriptions
Content-Type: application/json
X-API-Key: your_api_key

{
  "file_url": "https://your-storage.com/audio.mp3",
  "filename": "my-audio.mp3",
  "language_code": "en",
  "transcription_type": "transcript",
  "enable_speaker_diarization": false
}
```

---

### 3. From YouTube

```
POST /api/v1/transcriptions/youtube
Content-Type: application/json
X-API-Key: your_api_key

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "language_code": "en",
  "transcription_type": "transcript",
  "enable_speaker_diarization": false,
  "webhook_url": "https://your-webhook.com"
}
```

---

### 4. Check Status

```
GET /api/v1/transcriptions/{id}/status
X-API-Key: your_api_key
```

**Status Values:**
- `queued` - Waiting to process
- `preprocessing` - Downloading/preparing
- `processing` - Transcribing
- `completed` - Done
- `failed` - Error

---

### 5. Get Results

```
GET /api/v1/transcriptions/{id}
X-API-Key: your_api_key
```

**Response includes:**
```json
{
  "data": {
    "id": "1234567890",
    "filename": "audio.mp3",
    "status": "completed",
    "duration": 120.5,
    "language_code": "en",
    "result": {
      "text": "Full transcription text...",
      "summary": "Generated summary...",
      "outline": "# 1. Introduction\n# 2. Main Points...",
      "segments": [
        {
          "start": 0.0,
          "end": 5.2,
          "text": "Hello, this is a sample",
          "speaker": "A",
          "words": [
            {"start": 0.0, "end": 0.8, "text": "Hello"}
          ]
        }
      ]
    }
  }
}
```

---

## 🎛️ PARAMETERS

### Transcription Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `file_key` | conditional | string | Key from upload API |
| `file_url` | conditional | string | Public URL to file |
| `filename` | optional | string | Custom filename |
| `language_code` | required | string | e.g., "en", "es", "zh" |
| `transcription_type` | optional | string | "transcript" or "subtitle" |
| `enable_speaker_diarization` | optional | boolean | Identify speakers |
| `webhook_url` | optional | string | Notification webhook |

### File Requirements

| Constraint | Limit |
|------------|-------|
| File size | Max 5GB |
| Duration | Max 10 hours |
| Audio formats | mp3, m4a, wav, aac, ogg, opus, flac |
| Video formats | mp4, webm, mov |

---

## 🌐 LANGUAGE SUPPORT

**90+ languages including:**
- English (en), Spanish (es), French (fr), German (de)
- Chinese (zh), Japanese (ja), Korean (ko)
- All major European, Asian, African languages
- See full list in API docs

---

## 🔔 WEBHOOKS

UniScribe calls your webhook when transcription completes:

**Event: transcription.completed**
```json
{
  "event": "transcription.completed",
  "data": {
    "id": "1234567890",
    "filename": "audio.mp3",
    "status": "completed",
    "duration": 120.5
  }
}
```

**Event: transcription.failed**
```json
{
  "event": "transcription.failed",
  "data": {
    "id": "1234567890",
    "status": "failed",
    "error_message": "Failed to download file from URL"
  }
}
```

**Requirements:**
- Return HTTP 2xx
- Timeout: 30 seconds
- Header: User-Agent: UniScribe-Webhook/1.0

---

## 📈 RATE LIMITS

| Limit | Value |
|-------|-------|
| Requests per minute | 10 |
| Requests per day | 1000 |
| Max API keys | 5 per user |

---

## ❌ ERROR CODES

| Code | Meaning |
|------|---------|
| 40010001 | Invalid request parameters |
| 40141001 | Invalid API Key |
| 40341000 | No active subscription |
| 40345002 | Transcription permission denied |
| 40445001 | Transcription not found |
| 429 | Rate limit exceeded |

---

## 💰 PRICING REQUIREMENTS

**To access API:**
- ✅ Active subscription OR
- ✅ LTD (Lifetime Deal) plan
- ❌ Free users cannot use API
- ❌ One-time purchase users cannot use API

**Pricing Page Notes:**
- API Access mentioned in Korean pricing section
- Bulk transcription options available
- Team/enterprise options available

---

## 🔧 INTEGRATION EXAMPLES

### Python Example

```python
import requests

# Create transcription
response = requests.post(
    'https://api.uniscribe.co/api/v1/transcriptions',
    headers={'X-API-Key': 'your_api_key'},
    json={
        'file_url': 'https://example.com/audio.mp3',
        'filename': 'my-recording.mp3',
        'language_code': 'en',
        'webhook_url': 'https://your-app.com/webhook'
    }
)

transcription_id = response.json()['data']['id']

# Check status
status = requests.get(
    f'https://api.uniscribe.co/api/v1/transcriptions/{transcription_id}/status',
    headers={'X-API-Key': 'your_api_key'}
).json()

print(status)
```

### cURL Example

```bash
# Create transcription from URL
curl -X POST https://api.uniscribe.co/api/v1/transcriptions \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "file_url": "https://example.com/audio.mp3",
    "filename": "my-audio.mp3",
    "language_code": "en"
  }'

# Get results
curl -X GET https://api.uniscribe.co/api/v1/transcriptions/1234567890 \
  -H "X-API-Key: your_api_key"
```

### n8n Integration

**HTTP Request Node:**
- Method: POST
- URL: https://api.uniscribe.co/api/v1/transcriptions
- Headers: X-API-Key: your_api_key
- Body: JSON with file_url and webhook_url

**Webhook Node:**
- Listen for completion
- Process transcription results

---

## 🎯 USE CASES FOR YOUR BUSINESS

### 1. Podcast Transcription
- Transcribe Ultimate Football Heroes episodes
- Auto-generate show notes from summaries
- Create searchable episode database

### 2. Meeting Notes
- Transcribe client calls
- Auto-generate summaries
- Extract action items from outlines

### 3. Content Repurposing
- Transcribe video content
- Convert to blog posts (use summary + outline)
- Create social media clips

### 4. Interview Transcription
- Transcribe job interviews
- Auto-identify speakers
- Generate interview summaries

### 5. YouTube Content
- Transcribe existing videos
- Auto-generate captions
- Create blog posts from videos

---

## 📋 SUPPORT

- **Email:** support@uniscribe.co
- **Discord:** https://discord.com/invite/RJTaS28UWU

---

## 🚀 NEXT STEPS

1. [ ] Create UniScribe account
2. [ ] Upgrade to paid subscription (for API access)
3. [ ] Generate API key (Settings → API Keys)
4. [ ] Test with sample audio file
5. [ ] Build n8n workflow for podcast transcription

---

*Research Complete - 2026-02-01*
*Source: https://www.uniscribe.co/docs*
