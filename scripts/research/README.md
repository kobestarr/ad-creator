# Research Transcription System

For: YouTube tutorials, idea extraction, project research, blueprint building

## Quick Start

### Transcribe a Research Video

```bash
python /root/clawd/scripts/research/transcribe-video.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --title "Nick Saraev n8n Automation Tutorial" \
  --tags "automation,n8n,research" \
  --output /root/clawd/research/transcriptions \
  --wait
```

## What It Creates

For each research video:

```
/root/clawd/research/transcriptions/
└── Nick_Saraev_n8n_Automation_Tutorial_20260201_160000/
    ├── transcript.txt    (full text - 200KB+ for 1hr video)
    ├── summary.txt       (AI summary - ~3 paragraphs)
    ├── outline.md        (structured outline)
    ├── insights.md       (key takeaways extracted)
    ├── full.json         (complete API response)
    └── meta.json         (metadata + file paths)
```

## Tags System

Use tags to organize research:

| Tag | Use For |
|-----|---------|
| `automation` | n8n, Make.com, workflow tools |
| `n8n` | n8n-specific tutorials |
| `make` | Make.com tutorials |
| `salesforce` | Bluprintx client work |
| `job-search` | OE strategy videos |
| `marketing` | Content, outreach, SEO |
| `research` | General research |
| `podcast` | Ultimate Football Heroes |

## Integration with Nick Saraev's Methods

This system is designed to capture Nick Saraev's blueprints:

1. **Transcribe** → Get full transcript
2. **Extract** → Pull out workflow steps
3. **Implement** → Build using his methods
4. **Iterate** → Customize for your needs

## Research Index

All transcriptions are indexed in `_index.json`:

```json
{
  "research": [
    {
      "title": "Nick Saraev n8n Tutorial",
      "url": "https://youtube.com/watch?v=...",
      "tags": ["automation", "n8n"],
      "transcribed_at": "2026-02-01T16:00:00Z"
    }
  ],
  "last_updated": "2026-02-01T16:00:00Z"
}
```

## Daily Research Workflow

Add to crontab for automated research collection:

```bash
# Run daily at 8 AM
0 8 * * * python /root/clawd/scripts/research/daily-research-check.py
```

## Requirements

- Python 3.8+
- `requests` library: `pip install requests`
- UniScribe API key (stored in `/root/.credentials/uniscribe.json`)

## Security

✅ API key stored in secure location  
✅ File permissions: 600 (owner only)  
✅ No hardcoded credentials  
✅ Encrypted at rest potential

---

*Build the empire, one research video at a time.*
