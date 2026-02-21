# Robyn Agent - Product Requirements Document

## Overview

Robyn is an AI-powered messaging agent for the clawd project. She delivers scheduled briefings and responds to two-way chat on Slack (and later WhatsApp), powered by Claude API with a persistent personality loaded from the clawd identity files.

## Status: Phase 1 Active (Slack Webhook Briefings)

---

## Problem Statement

Kobi needs a persistent AI assistant that proactively delivers scheduled briefings (health, finance, tasks, weather) and is available for on-demand conversation across messaging platforms. The existing briefing scripts produce output but have no delivery mechanism — no messages actually reach Kobi.

## Solution

A Node.js service (`robyn-agent/`) running on the VPS that:
1. **Delivers** 4 daily briefings to Slack on schedule (and later WhatsApp)
2. **Responds** to two-way chat messages with Robyn's personality via Claude API
3. **Wraps** existing briefing scripts — no rewrite needed
4. **Loads** identity from SOUL.md, AGENTS.md, USER.md, MEMORY.md, IDENTITY.md

## Users

| User | Interaction |
|------|-------------|
| Kobi Omenaka | Receives briefings, chats with Robyn |

## Architecture

```
VPS (72.62.134.99)
├── Traefik (existing reverse proxy)
├── n8n (existing, untouched)
└── robyn-agent (port 3141)
    ├── Slack Webhook ──────> #briefings channel (one-way, Phase 1)
    ├── Slack Bolt (Socket Mode) ──> two-way chat (Phase 2)
    ├── Express server ─────> WhatsApp webhook (Phase 3)
    ├── Claude API (Anthropic SDK)
    ├── Persona loader (SOUL.md, AGENTS.md, USER.md, etc.)
    ├── Conversation history (JSON files, 50-msg window)
    └── node-cron scheduler (4 daily briefings)
```

### Data Flow: Briefing Delivery
```
node-cron trigger (Europe/London timezone)
    |
    v
briefing-runner.js (executes existing bash/python scripts)
    |
    v
Raw script output (weather, strava, asana, bank balances)
    |
    v
[Optional] Claude Haiku formatting (adds Robyn's voice)
    |
    v
Slack webhook POST (Block Kit formatted message)
    |
    v
#briefings channel
```

### Data Flow: Two-Way Chat
```
User message in Slack (DM or @Robyn mention)
    |
    v
Slack Bolt (Socket Mode receives event)
    |
    v
persona.js (loads SOUL.md + AGENTS.md + USER.md + MEMORY.md + today's daily log)
    |
    v
conversation.js (retrieves last 50 messages for context)
    |
    v
claude.js (Anthropic SDK - Claude Sonnet with system prompt + history)
    |
    v
Response posted back to Slack
    |
    v
conversation.js (saves response to history)
```

## Technical Specifications

### Runtime

| Field | Value |
|-------|-------|
| Runtime | Node.js 18+ |
| Process Manager | PM2 |
| Location (VPS) | `/root/clawd/robyn-agent/` |
| Location (local) | `~/Development/clawd/robyn-agent/` |
| Port | 3141 (Phase 3 Express server) |

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `@slack/bolt` | ^4.1.0 | Slack Socket Mode + event handling |
| `@anthropic-ai/sdk` | ^0.39.0 | Claude API for chat + briefing formatting |
| `dotenv` | ^16.4.0 | Environment variable loading |
| `node-cron` | ^3.0.3 | Scheduled briefing triggers |

### Briefing Schedule

| Time (UK) | Name | Type | Data Sources |
|-----------|------|------|-------------|
| 6:35 AM | Morning Briefing | `morning` | Weather, Strava, Withings, sun times, countdowns |
| 9:30 AM (Mon-Fri) | Daily Standup | `standup` | Asana tasks, overdue items, project summary |
| 12:35 PM (Mon-Fri) | Lunchtime Check | `lunch` | Bank balances (KSD, Stripped Media) |
| 5:30 PM (Mon-Fri) | End of Day | `eod` | Asana tasks + bank balances |

### Briefing Scripts (Existing, Wrapped)

| Script | Path | Data |
|--------|------|------|
| Morning briefing | `scripts/briefings/morning-briefing.sh` | Open-Meteo weather, Strava API, Withings |
| Asana briefing | `scripts/briefings/asana-briefing.sh` | Asana tasks (PAT auth) |
| Balance check | `scripts/briefings/daily-balance-check.sh` | Starling Bank API (KSD + Stripped Media) |
| Weekly briefing | `scripts/briefings/weekly-briefing.sh` | Weekly weather + Strava summary |

### Persona System

The persona loader (`core/persona.js`) reads these files on startup and caches for 5 minutes:

| File | Purpose |
|------|---------|
| `SOUL.md` | Core personality, boundaries, vibe |
| `IDENTITY.md` | Name (Robyn), emoji (fox), creature type |
| `USER.md` | Kobi's details, preferences, schedule |
| `AGENTS.md` | Operational guidelines, platform formatting |
| `MEMORY.md` | Long-term curated memory |
| `memory/daily/YYYY-MM-DD.md` | Today's context (injected dynamically) |

System prompt size: ~22,000 characters (~5,500 tokens).

### Conversation History

- Storage: JSON files in `robyn-agent/memory/conversations/`
- Format: `[{role, content, timestamp}]`
- Window: Last 50 messages per channel (sliding)
- One file per channel: `slack-C0XXXXXXX.json`
- Gitignored (contains chat data)

### Claude API Usage

| Use Case | Model | Estimated Tokens/Call |
|----------|-------|----------------------|
| Two-way chat | `claude-sonnet-4-20250514` | ~6K input, ~500 output |
| Briefing formatting | `claude-haiku-4-5-20251001` | ~2K input, ~500 output |

### Environment Variables

```
# Phase 1 (active)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Phase 2 (needs setup)
ANTHROPIC_API_KEY=sk-ant-...
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...

# Phase 3 (future)
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
WHATSAPP_TO=whatsapp:+44...
```

## File Structure

```
robyn-agent/
├── package.json
├── .env.example
├── .env                         # Not committed (gitignored)
├── ecosystem.config.js          # PM2 deployment config
├── index.js                     # Entry point - scheduler + Bolt startup
├── core/
│   ├── briefing-runner.js       # Wraps existing bash/python scripts
│   ├── claude.js                # Anthropic SDK wrapper (chat + format)
│   ├── persona.js               # Loads identity files into system prompt
│   └── conversation.js          # Chat history manager (JSON files)
├── channels/
│   └── slack.js                 # Webhook posting + Bolt two-way chat
├── config/
│   ├── schedules.js             # Cron expressions for 4 briefings
│   └── channels.js              # Channel IDs, phone numbers from env
└── memory/conversations/        # Chat history (gitignored)
```

## Deployment

### VPS Setup
```bash
cd /root/clawd && git pull
cd robyn-agent && npm install
cp .env.example .env
# Edit .env with actual values
pm2 start ecosystem.config.js
pm2 save
pm2 startup   # auto-restart on VPS reboot
```

### PM2 Commands
```bash
pm2 logs robyn-agent       # View logs
pm2 restart robyn-agent    # Restart
pm2 stop robyn-agent       # Stop
pm2 monit                  # Monitor resources
```

## Constraints

- All briefing formatting is optional — raw script output is delivered if Claude API is unavailable
- Socket Mode means no public URL needed for Slack (outbound WebSocket only)
- Conversation history is local JSON files, not a database
- Persona files are read from the parent clawd directory (not copied)
- Briefing scripts run with 30-second timeout

## Cost Estimate

| Component | Cost |
|-----------|------|
| Slack | Free (Socket Mode, webhook) |
| Claude API (chat) | ~$0.50-2/day |
| Claude API (briefing formatting) | ~$0.10-0.30/day |
| Twilio WhatsApp (Phase 3) | ~$6/month |
| **Total** | **~$20-40/month** |

## Phases

| Phase | Status | Description |
|-------|--------|-------------|
| 1 - Slack Briefings | **Active** | Webhook delivery of 4 daily briefings |
| 2 - Slack Two-Way Chat | Needs tokens | Bolt Socket Mode + Claude API responses |
| 3 - WhatsApp Two-Way | Not started | Twilio webhook + Express server |
| 4 - Polish | Not started | Voice formatting, error handling, daily log injection |

## Verified

- Slack webhook delivery: tested Feb 21, 2026 (message appeared in channel)
- Briefing script execution: morning-briefing.sh produces 1,082 chars of weather/Strava/countdown data
- Persona loader: reads all 5 identity files, produces 22,854-char system prompt
- Conversation manager: creates/reads/writes JSON history files

## Open Items

| Item | Status | Priority |
|------|--------|----------|
| Create Slack App (Socket Mode) for two-way chat | Needs Kobi | High |
| Add ANTHROPIC_API_KEY to .env | Needs Kobi | High |
| Deploy to VPS via PM2 | Ready | High |
| WhatsApp via Twilio (Phase 3) | Not started | Medium |
| Strava token refresh (expired in briefing script) | Needs refresh | Medium |
| Briefing formatting with Robyn's voice (Haiku) | Ready when API key added | Low |
| Weekly briefing schedule (Saturday) | Not yet scheduled | Low |

---

*Created: 2026-02-21*
*Version: 1.0*
