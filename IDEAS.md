# Ideas & Project Backlog

*A place to capture, list, and evaluate ideas*

---

## How to Use

**Add an idea:** Just share it with me, I'll add it here

**Evaluate an idea:** Ask me to "evaluate idea #X" and I'll assess:
- Feasibility
- Complexity
- Priority
- Dependencies

**Prioritize:** Ask me to "rank these" or "order by priority"

**Archive:** Completed or rejected ideas move to the bottom

---

## Ideas List

### Active Ideas

1. **Ad Intelligence Platform** (`#1`)
   - Multi-platform competitor ad analysis
   - Status: In progress (Slice 1: LinkedIn scraper)
   - Priority: High

2. **Scheduled Ad Collection** (`#2`)
   - Background job to collect ads periodically
   - Status: Not started
   - Priority: Medium

3. **LinkedIn Ads API Integration** (`#3`)
   - Connect to personal LinkedIn ad account
   - Monitor performance, start/stop campaigns, optimize ads
   - Status: Not started
   - Priority: Medium
   - Requires: LinkedIn Marketing API approval

4. **Skool Community Automation** (`#4`)
   - Read posts and comments from Skool communities
   - Automated posting (if API supports)
   - Status: Research needed
   - Priority: Low
   - Options: SkoolAPI (paid), Apify scraper, Zapier

5. **Token Usage Display** (`#5`)
   - Track and display token usage per session
   - Alerts at 1000, 2000, 3000, etc.
   - 80% context limit warning
   - Status: Not started
   - Priority: Low
   - Note: Nice to have, not blocking

6. **Asana Integration** (`#6`)
   - Sync tasks to Asana
   - Create tasks from ad discoveries
   - Log analysis as comments
   - Status: Not started
   - Priority: Medium
   - Requires: Asana Personal Access Token

7. **Trading Bot** (`#7`)
   - Crypto and/or Forex automated trading
   - Strategy execution, risk management
   - Status: Not started
   - Priority: Low
   - Warning: High risk, no profit guarantee
   - Requires: Exchange API keys, capital

8. **Lemlist Integration** (`#8`)
   - Automate cold email outreach to competitors
   - Multi-channel sequences (email, LinkedIn, WhatsApp, calls)
   - Track lead interactions and replies
   - Status: Not started
   - Priority: Low
   - Requires: Lemlist API key, account

9. **CaptainData Integration** (`#9`)
   - B2B data enrichment for companies found in ads
   - Contact information lookup (emails, phone numbers)
   - Intent signals and buyer profiles
   - CRM integration for enriched data
   - Status: Not started
   - Priority: Low
   - Requires: CaptainData API key, credit usage

10. **Podcast PR Relationship CRM** (`#10`)
    - Track journalist relationships for podcast PR
    - Research: Find press coverage of podcasts
    - Step 1: Use Playwright to scrape publication websites
      - Navigate to Deadline, BroadcastNow, PodNews, etc.
      - Extract editorial emails, journalist bylines, contact pages
    - Step 2: Enrich using CaptainData API
      - Find personal emails
      - Get LinkedIn profiles
      - Add phone numbers and social accounts
    - Step 3: Contact tracking system
      - Check if journalist is in contact history
      - If NEW → Generate intro email mentioning their recent article
      - If EXISTING → Ask: "Follow up via email or LinkedIn?"
    - Goal: Build journalist relationships for podcast promotion
    - Status: Not started
    - Priority: Medium
    - Requires: Playwright (free), CaptainData API (for enrichment)

---

### On Hold

*(Ideas waiting for dependencies or timing)*

---

### Completed

*(Done projects)*

---

### Rejected

*(Ideas decided against)*

---

*Last updated: 2026-01-26* (Added idea #10)
