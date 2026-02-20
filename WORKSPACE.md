# Clawd Workspace

## Primary Goal

**Clear GBP 100,045.43 debt by February 2027** (12-month window)

Build automated income systems across entities. Target: GBP 4,624/month after expenses.

---

## Folder Map

```
clawd/
├── AGENTS.md              # How agents boot and operate
├── SOUL.md                # Identity (Robyn)
├── USER.md                # Who you're helping (Kobi)
├── MEMORY.md              # Long-term curated memory
├── WORKSPACE.md           # This file - master index
├── TOOLS.md               # Tool notes (SSH, voice, etc.)
├── IDEAS.md               # Active ideas list
│
├── entities/              # Business entities
│   ├── ksd/               # KSD - local outreach (NEW REVENUE)
│   ├── bluprintx/         # Main client - PROTECT THIS
│   ├── stripped-media/     # Content/creative business
│   ├── dealflow-media/     # Future venture
│   ├── personal/           # Personal projects + Mylo
│   └── clients/            # Future clients
│
├── scripts/               # Automation scripts
│   ├── health/            # Withings, Strava integration
│   ├── social/            # Oktopost posting tools
│   ├── briefings/         # Morning/weekly briefing generators
│   ├── podcast/           # Podcast transcription
│   └── linkedin/          # LinkedIn scraper, URL cleaner, job scraper
│
├── memory/                # All memory (version controlled)
│   ├── daily/             # Daily logs: YYYY-MM-DD.md
│   ├── research/          # Topic research notes
│   ├── plans/             # Strategy & game plans
│   ├── integrations/      # API & service integration notes
│   └── briefings/         # Morning briefing research
│
├── docs/                  # Strategy & business documents
├── shared/                # Cross-entity shared code (outreach-core)
├── modules/               # Utility modules (credentials-loader)
├── research/              # Research artifacts, templates
├── references/            # Brand/tone reference material
└── podcast/               # Podcast transcriptions
```

---

## Satellite Repos (Standalone Tools)

These live on the VPS as subdirectories but have their own GitHub repos:

| Tool | VPS Path | GitHub Repo | Purpose |
|------|----------|-------------|---------|
| Ad Intel | ~/clawd/ad-intel/ | kobestarr/ad-intel | LinkedIn ad scraper |
| Ad Creator | ~/clawd/ad-creator/ | kobestarr/ad-creator-engine | Ad generation engine |
| Transcription | ~/clawd/transcription-automation/ | kobestarr/transcription-automation | Podcast/video transcription + parasite SEO |

These are gitignored from the main clawd repo.

---

## Entity Quick Reference

| # | Entity | Folder | Purpose | Debt Impact |
|---|--------|--------|---------|-------------|
| 1 | Personal | entities/personal/ | Personal projects, Mylo | - |
| 2 | **KSD** | entities/ksd/ | **Local outreach - NEW REVENUE** | GBP 4,000-8,000/mo |
| 3 | Stripped Media | entities/stripped-media/ | Content/creative | Existing income |
| 4 | Deal Flow Media | entities/dealflow-media/ | Future venture | Future income |
| 5 | **Bluprintx** | entities/bluprintx/ | **Main client - PROTECT** | Main income |
| 6 | Clients | entities/clients/ | Future clients | Future income |

---

## Script Index

### Health (scripts/health/)
| Script | What it does |
|--------|-------------|
| withings-health-check.py | Fetch Withings health data |
| strava-analysis.py | Analyze Strava activity data |
| refresh-withings-token.py | Refresh Withings OAuth token |
| refresh-strava-token.py | Refresh Strava OAuth token |
| withings-reauthorize.py | Full Withings re-auth flow |

### Social (scripts/social/)
| Script | What it does |
|--------|-------------|
| post-to-oktopost.py | Post content to Oktopost as draft |
| generate-and-post.py | Generate content and post to Oktopost |
| list-oktopost-drafts.sh | List current Oktopost drafts |

### Briefings (scripts/briefings/)
| Script | What it does |
|--------|-------------|
| morning-briefing.sh | Generate morning briefing |
| weekly-briefing.sh | Generate weekly summary |
| asana-briefing.sh | Pull Asana task updates |
| daily-balance-check.sh | Check financial balances |

### LinkedIn (scripts/linkedin/)
| Script | What it does |
|--------|-------------|
| linkedin_url_cleaner.py | Clean LinkedIn URLs |
| linkedin-job-scraper/ | Full job scraping pipeline |

---

## Integration Status

| Service | Status | Scripts | Notes |
|---------|--------|---------|-------|
| Withings | Active | scripts/health/withings-* | User ID: 14711398 |
| Strava | Active | scripts/health/strava-* | Poynton 10k training |
| Oktopost | Active | scripts/social/ | API confirmed working (Feb 2026) - campaignId filter works, was likely a typo |
| Asana | Active | scripts/briefings/asana-* | PAT-based access |
| FreeAgent | Research | memory/integrations/ | Financial tracking |

---

## Agent Spawn Template

```
Label: [Entity] [Project] [Task Type]
Model: [appropriate model]
Task: |
  Context:
  - Primary goal: Clear GBP 100k debt by Feb 2027
  - Working on: [Entity] / [Project]
  
  Read these first:
  - /root/clawd/SOUL.md
  - /root/clawd/AGENTS.md
  - /root/clawd/MEMORY.md
  - /root/clawd/WORKSPACE.md
  
  Deliverables:
  - [Specific task requirements]
  - Save to: /root/clawd/entities/[entity]/[project]/
```

---

## Git Workflow

- **Main repo:** `kobestarr/clawd` — commit with entity prefix: `[KSD] Add outreach automation`
- **Satellite repos:** Commit independently to their own repos
- **Memory:** Auto-committed during heartbeats
- **Flow:** VPS → GitHub → Local (~/Development/clawd/ as backup)

---

*Last Updated: 2026-02-20*
*Primary Goal: Clear GBP 100,045.43 debt by February 2027*
