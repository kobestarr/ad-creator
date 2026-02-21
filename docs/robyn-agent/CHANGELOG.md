# Robyn Agent - Changelog

## [1.0.0] - 2026-02-21 - Initial Build

### Context
Robyn (the AI agent persona defined in SOUL.md) had no actual messaging capability — briefing scripts existed but nothing delivered messages to Kobi. This release creates a Node.js service that connects Robyn to Slack for both scheduled briefings and two-way conversation.

### Added

**Core Service (`robyn-agent/`)**
- `index.js` — Entry point. Starts briefing scheduler and optionally Slack Bolt for two-way chat. Graceful shutdown handling.
- `package.json` — Dependencies: `@slack/bolt`, `@anthropic-ai/sdk`, `node-cron`, `dotenv`
- `ecosystem.config.js` — PM2 deployment config (auto-restart, log rotation, 256MB memory limit)
- `.env.example` — Template for all environment variables across all phases

**Briefing System**
- `core/briefing-runner.js` — Wraps existing bash/python briefing scripts via `child_process.execFile()` with 30-second timeout. Maps briefing types (`morning`, `standup`, `lunch`, `eod`, `weekly`) to script paths.
- `config/schedules.js` — 4 cron jobs in Europe/London timezone:
  - 6:35 AM daily — Morning briefing (weather, Strava, Withings, countdowns)
  - 9:30 AM Mon-Fri — Daily standup (Asana tasks)
  - 12:35 PM Mon-Fri — Lunchtime check (bank balances)
  - 5:30 PM Mon-Fri — End of day (Asana + bank balances)

**Slack Integration (`channels/slack.js`)**
- Webhook posting for one-way briefings (Phase 1, active now)
- Block Kit formatting with header, content section, and context footer
- Slack Bolt with Socket Mode for two-way chat (Phase 2, needs bot tokens)
- Direct message handler — routes through Claude API with full persona context
- @mention handler — responds in-thread when Robyn is mentioned
- Bot message loop prevention

**AI & Persona**
- `core/claude.js` — Anthropic SDK wrapper. `chat()` for two-way conversation (Sonnet), `formatBriefing()` for adding Robyn's voice to raw script output (Haiku). Graceful fallback to raw output if no API key.
- `core/persona.js` — Reads SOUL.md, IDENTITY.md, USER.md, AGENTS.md, MEMORY.md on startup. Caches for 5 minutes. Injects today's daily log from `memory/daily/YYYY-MM-DD.md`. Adds channel-specific formatting instructions (Slack mrkdwn vs WhatsApp formatting).
- `core/conversation.js` — JSON-file conversation history. 50-message sliding window per channel. One file per channel in `robyn-agent/memory/conversations/` (gitignored).

**Configuration**
- `config/channels.js` — Runtime channel config populated from environment variables
- `.gitignore` updated — Added `robyn-agent/memory/conversations/` to exclude chat history

### Tested
- **Slack webhook delivery** — Message appeared in Slack channel (Feb 21, 2026)
- **Briefing script execution** — `morning-briefing.sh` produced 1,082 chars (weather 10.2C, running window, Strava, sun times, countdowns)
- **Persona loader** — All 5 identity files loaded, 22,854-char system prompt generated
- **Dependency install** — 139 packages, 0 vulnerabilities

### Not Yet Active (Needs Tokens/Config)
- Two-way Slack chat (needs `SLACK_BOT_TOKEN` + `SLACK_APP_TOKEN` from Slack App)
- Claude-powered responses (needs `ANTHROPIC_API_KEY`)
- Claude briefing formatting (needs `ANTHROPIC_API_KEY`)
- VPS deployment (needs `git pull` + `npm install` + PM2 start)

### Architecture Decisions
- **Node.js over Python** — Matches existing codebase patterns, best Slack Bolt SDK, first-class Anthropic SDK
- **Socket Mode over Events API** — No public URL needed for Slack, just outbound WebSocket
- **Standalone service over n8n** — Two-way chat needs persistent WebSocket connections and conversation state management, which n8n handles poorly
- **JSON files over database** — Solo developer, greppable, fits existing `memory/` architecture
- **Existing scripts wrapped, not rewritten** — `briefing-runner.js` calls bash/python via `execFile()`, preserving all current integrations (Strava, Withings, Asana, Starling Bank, Open-Meteo)

### Files Created
```
robyn-agent/
├── package.json              (21 lines)
├── package-lock.json         (1,637 lines)
├── .env.example              (22 lines)
├── ecosystem.config.js       (21 lines)
├── index.js                  (94 lines)
├── core/briefing-runner.js   (52 lines)
├── core/claude.js            (46 lines)
├── core/persona.js           (87 lines)
├── core/conversation.js      (50 lines)
├── channels/slack.js         (151 lines)
├── config/schedules.js       (36 lines)
└── config/channels.js        (18 lines)

Total: 13 files, 2,238 lines
```

### Files Modified
- `.gitignore` — Added `robyn-agent/memory/conversations/`
