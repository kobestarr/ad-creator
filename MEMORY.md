# MEMORY.md - Durable Knowledge

## About the Human

- Works with a Gary Vee-style founder (energetic, B2B thought leader)
- Company: Bluprintx (Salesforce partner, AI/consultancy)
- Based: Poynton, East Cheshire (near Manchester)
- Timezone: GMT/BST (UK)

## About the Projects

### Ad Intelligence Tool
- GitHub: https://github.com/kobestarr/ad-intel
- Scrapes LinkedIn ads for competitor research
- Stores data in Google Drive: `Ad Intelligence/Projects/Bluprintx/`
- Captures screenshots of ads
- Multi-keyword, date range, company exclusion supported

### Google Drive Skill
- Location: `/usr/lib/node_modules/clawdbot/skills/google-drive/`
- Supports: upload, list, download, delete, switch accounts
- OAuth 2.0 with 11 Google APIs enabled

## Technical Notes

### LinkedIn Ad Library
- URL: https://www.linkedin.com/ad-library/search
- Only shows company logos, not full ad creatives
- Screenshot capture implemented for visual content
- Date filtering works with `&date=YYYY-MM-DD,YYYY-MM-DD`

### Reddit Ads API
- Docs: https://ads-api.reddit.com/docs/v3/
- Credentials portal: https://business.reddithelp.com/s/article/authenticate-your-developer-application
- Still needs credential testing

## Preferences

- Prefers testing credentials before building features
- Uses WhatsApp for communication
- Values systematic, step-by-step approach
- Likes organized folder structures with clear naming

## Key Files

- `/root/clawd/memory/daily/YYYY-MM-DD.md` - Daily logs
- `/root/clawd/IDENTITY.md` - My identity (Robyn 🦊)
- `/root/clawd/SOUL.md` - My personality
- `/root/clawd/USER.md` - User preferences

## Overemployed Strategy (Feb 2026)

### UK-Specific OE Requirements
- **Fully remote jobs ONLY** (hybrid makes OE impossible)
- **Separate hardware** (J1 laptop for J1, J2 for J2)
- **Separate calendars** (no overlapping meetings)
- **HMRC doesn't care** (multiple PAYE jobs are legal, just pay correct taxes)
- **Watch out:** Contract clauses may restrict additional employment

### OE Resources
- **Subreddits:** r/overemployed (~200K members), r/OveremployedUK (private)
- **Website:** overemployed.com + Discord community
- **Job Boards:** RemoteJobMatching.com, LinkedIn Easy Apply, We Work Remotely

### Strategy
- Apply to 10-20 remote jobs/day minimum
- Use AI automation for personalized applications
- Track all applications in Google Sheets
- Build systems for maximum productivity

---

## Job Scraping Automation (Nick Saraev Methods)

### Who Is Nick Saraev?
- **n8n Creator:** https://n8n.io/creators/nicksaraev/
- **YouTube:** https://www.youtube.com/@nicksaraev
- **Reputation:** "Only guy that builds good automations"
- **Proven Results:** $72K/month using his automation methods

### Key n8n Workflows (FREE Templates)
1. **Cold Email Icebreaker Generator**
   - Link: https://n8n.io/workflows/5388-cold-email-icebreaker-generator-with-apify-gpt-4-and-website-scraping/
   - Results: 5-10% reply rates (vs 1-2% standard)
   - Cost: ~$150/month

2. **Personalized Upwork Proposals** - https://n8n.io/workflows/6174-automate-personalized-upwork-proposals-with-gpt-4-google-docs-and-mermaid-diagrams/

3. **LinkedIn Connection Requests** - https://n8n.io/workflows/4803-personalized-linkedin-connection-requests-with-apollo-gpt-4-apify-and-phantombuster/

### The Icebreaker Method
1. **Multi-page scraping** (not just homepage)
2. **AI analyzes** each page for insights
3. **Generate personalized** icebreakers
4. **Recipients think** you spent hours researching manually
5. **Result:** 5-10% response rates

### Applied to Job Applications
- Research company deeply before applying
- Generate personalized cover letters
- Reference specific initiatives/news
- Stand out from generic applications

### Tools Required
| Tool | Purpose | Monthly Cost |
|------|---------|--------------|
| n8n | Workflow automation | FREE (self-hosted) |
| Apollo.io | Lead/contact database | $49+/mo |
| Apify | Web scraping | $49+/mo |
| OpenAI API | AI processing | $10-50/mo |

**Total Monthly Cost: ~$150-200**

### Bluprintx Service Opportunity: Salesforce Hiring Tracker
- Scrape LinkedIn for "Salesforce" job postings
- Target companies that just hired
- Outreach: "I noticed you just hired a Salesforce [role]..."
- Revenue: £500-1,000/month per client

---

## Commands

```bash
# Run ad intelligence scraper
cd /root/clawd/ad-intel
docker compose run --rm linkedin-search sh -c "node src/cli/index.js search 'keyword' -c US --limit 10"

# Google Drive skill
cd /usr/lib/node_modules/clawdbot/skills/google-drive
node src/index.js upload <file> --folder "Bluprintx"
```

---

## Code Review Process (Feb 2026)

### Git Hook Setup
- Location: `.git/hooks/post-push`
- Triggers on EVERY commit and push

### Two-Step Review Workflow

**STEP 1: Code Review (by Codex agent)**
- Uses: CODE_REVIEW_PROMPT.md
- Checks: Logging, Error Handling, TypeScript, Production Readiness, React/Hooks, Performance, Security, Architecture, Python specifics
- Output: List of issues found with severity levels

**STEP 2: Peer Review (by team lead - another model)**
- Uses: PEER_REVIEW_PROMPT.md
- Validates: Each Codex finding (verify code, explain invalid findings)
- Output: Confirmed issues + invalid findings + prioritized fix plan

### Key Prompt Files
- **CODE_REVIEW_PROMPT.md** - What Codex checks for (logging, error handling, TypeScript, security, architecture, etc.)
- **PEER_REVIEW_PROMPT.md** - How to validate Codex findings

### PEER_REVIEW_PROMPT.md Template (Use Before EVERY Review)

```
## Peer Review Analysis

### Findings Confirmed as VALID (Will Fix)
| Issue | Severity | Fix Plan |
|-------|----------|----------|
|       |          |          |

### Findings INVALIDATED (With Explanations)
| Finding | Why It's Invalid |
|---------|------------------|
|         |                  |

### Priority Action Plan
1. [HIGH] 
2. [MEDIUM] 
3. [LOW] 
```

### Critical Rules
1. **Use both prompts** - Every review must use CODE_REVIEW_PROMPT.md AND PEER_REVIEW_PROMPT.md
2. **Verify before accepting** - Check actual code, don't assume Codex is correct
3. **Explain invalid findings** - Clear reasoning, not dismissals
4. **Prioritize fixes** - Not all issues are equal
5. **Full workflow on EVERY push** - Code review → Peer review → Summary

---

## Health & Fitness Data (Feb 2026)

### Strava Integration
- **Credentials File:** `/root/.credentials/strava.json`
- **Athlete:** Kobi Ømenåk (Obi-5 RPR), Poynton
- **YTD Stats:** 28 runs (97.4km), 14 rides (469.3km)
- **Last Activity:** January 31, 2026 - Final Runauary run!!! (6.6km)
- **Morning Briefing:** Includes last activity + YTD summary

### Withings Integration
- **Credentials File:** `/root/.credentials/withings.json`
- **User ID:** 14711398 (correct - was incorrectly listed as 40194722)
- **Last Weight:** [REPLACE WITH CURRENT WEIGHT FROM APP.WITHINGS.COM/14711398/TIMELINE]
- **Morning Briefing:** Includes latest weight

### Morning Briefing Health Section Template
```
🏃 STRAVA:
- Last activity: [date] - [name] ([distance]km)
- YTD: [X] runs ([Y]km), [A] rides ([B]km)

⚖️ WITHINGS:
- Last weight: [W] kg ([date])
```

### Training Goals
- **Poynton 10k:** March 8, 2026
- **Progress Tracking:** Via Strava in daily briefings

