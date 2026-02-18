# Podcast Transcription Scripts

## Quick Start

### Transcribe a Single Episode

```bash
python /root/clawd/scripts/podcast/transcribe-podcast.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --title "Ultimate Football Heroes - Episode 1" \
  --output /root/clawd/podcast/transcriptions \
  --wait
```

### Set Up Daily Automatic Check

Add to crontab:

```bash
# Run daily at 9 AM
0 9 * * * python /root/clawd/scripts/podcast/daily-podcast-check.py
```

## Output Files

For each episode, the following files are created:

| File | Description |
|------|-------------|
| `{title}_YYYYMMDD_HHMMSS_transcript.txt | Full transcription text |
| `{title}_YYYYMMDD_HHMMSS_summary.txt | Auto-generated summary |
| `{title}_YYYYMMDD_HHMMSS_outline.md | Mind map / outline (Markdown) |
| `{title}_YYYYMMDD_HHMMSS_full.json | Complete API response |

## Configuration

Edit `/root/clawd/scripts/podcast/daily-podcast-check.py`:
- Set `PODCAST_CHANNEL_ID` or `PODCAST_PLAYLIST_URL`
- Add YouTube API key for full automation

## Requirements

- Python 3.8+
- requests library: `pip install requests`
- UniScribe API key (stored in `/root/.credentials/uniscribe.json`)
