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

*Last updated: 2026-02-01* (Added ideas #11-19 from deep research session)

---

## NEW IDEAS (Research Complete - Awaiting Prioritization)

### 11. **Twine.net Freelance Strategy** (`#11`)
   - Platform: Twine.net - professional creative freelancers marketplace
   - Pricing: Free to post, 10% fee on first $10K, 5% thereafter
   - Strategy: Build portfolio, apply to projects, position as specialist
   - Opportunity: Leverage KSD skills for high-value freelance work
   - Status: Research complete
   - Priority: Medium
   - Research: `/root/clawd/memory/twine-research.md`

### 12. **Job Board Scraping & Outreach Automation** (`#12`)
   - Target: Upwork, LinkedIn, job boards for services you offer
   - Strategy: Scrape matching jobs → Auto-generate personalized outreach
   - Tools: Apify, Python scrapers, CaptainData for enrichment
   - Revenue: £5K-15K/month potential (based on Reddit/nick saraev methods)
   - Status: Research complete
   - Priority: High
   - Research: `/root/clawd/memory/job-scraping-research.md`

### 13. **Reddit Parasite SEO** (`#13`)
   - **NEW RESEARCH:** `/root/clawd/transcription-automation/reddit-parasite-seo/`
   - Use Reddit's DA 91 to rank content and get free traffic
   - Strategy: Create subreddit → Claude content → Quality control → Post consistently
   - Results: 25K visitors/month, 1,300+ leads/week (example)
   - Tools: Make.com auto-blogger, Claude, Proxies
   - 4-step process: Setup subreddit → Create content → QC → Measure
   - Key: Quality control critical (AI hallucinates!)
   - Status: Research started
   - Priority: High
   - Source: YouTube jMEhA3vhuuQ

### 14. **Substack Content Repurposing & Subscription Income** (`#14`)
   - Model: Paid newsletter subscriptions
   - Strategy: Repurpose existing content → Substack → Paid subscriptions
   - Examples: Creators earning 6-figures (Emily Atkin, Heated)
   - Multiple monetization: Subscriptions + sponsorships + affiliates
   - Status: Research complete
   - Priority: Medium
   - Research: `/root/clawd/memory/substack-research.md`

### 15. **GHL Communities for Community Building & Income** (`#15`)
   - Platform: GoHighLevel Communities feature
   - Features: Unlimited communities, course integration, subscription pricing
   - Monetization: Membership fees, course sales, affiliate commissions
   - Affiliate: 40% recurring commission on GHL referrals
   - Status: Research complete
   - Priority: Medium
   - Research: `/root/clawd/memory/ghl-communities-research.md`

### 16. **Morning Briefing & Daily Stand-up System** (`#16`)
   - Components:
     - School management (pickup/dropoff, emails, messages)
     - Meal prep & planning
     - Financial tracking digest
     - Health/fitness (Strava, TrainerRoad, Withings)
     - Media tracking (IMDb, Letterboxd watched/to-watch)
     - Daily priorities & focus areas
   - Goal: Reduce cognitive load, start each day clear
   - Status: Research started, deep dive needed
   - Priority: HIGH (user requested)
   - Research: `/root/clawd/memory/morning-briefing-research.md`

### 17. **Health & Fitness Integration (Strava + TrainerRoad + Withings)** (`#17`)
   - Integrations:
     - Strava: Activity syncing (runs, rides)
     - TrainerRoad: Cycling training plans, FTP sync
     - Withings: Weight, sleep, health metrics
   - Goal: Poynton 10k training tracking (March 8, 2026)
   - Morning briefing integration: Daily activity summary
   - Status: API research complete
   - Priority: HIGH (10k training)
   - Research: `/root/clawd/memory/health-fitness-research.md`

### 18. **Media Tracking System (IMDb + Letterboxd)** (`#18`)
   - Track: TV shows, films watching + want-to-watch
   - Integrations: IMDb, Letterboxd sync
   - Morning briefing: What's currently watching, progress
   - Content repurposing: Write reviews/posts for kobestarr.com
   - Status: Research not started
   - Priority: Low
   - Research: `/root/clawd/memory/media-tracking-research.md`

### 19. **Twiggy Content Automation (Instagram → WordPress)** (`#19`)
   - Monitor: Twiggy's Instagram posts
   - Process: Scrape post → Find context → Gather images
   - Output: Blog post on Twiggy's WordPress site
   - Context enrichment: Research premieres, launches, magazines
   - Goal: Automated content pipeline for official website
   - Status: Research not started
   - Priority: Medium
   - Research: `/root/clawd/memory/twiggy-automation-research.md`

---

## HIGH PRIORITY (User Requested Today)

1. **Morning Briefing Deep Dive** - Complete services mapping, brain dump
2. **Poynton 10k Tracking** - Confirm date (March 8, 2026?), set up Strava integration
3. **Job Board Scraping** - High income potential (£5-15K/month)

## Research Documents Created

- `/root/clawd/memory/twine-research.md`
- `/root/clawd/memory/job-scraping-research.md`
- `/root/clawd/memory/parasite-seo-research.md`
- `/root/clawd/memory/substack-research.md`
- `/root/clawd/memory/ghl-communities-research.md`
- `/root/clawd/memory/morning-briefing-research.md` (to be created)
- `/root/clawd/memory/health-fitness-research.md` (to be created)
- `/root/clawd/memory/media-tracking-research.md` (to be created)
- `/root/clawd/memory/twiggy-automation-research.md` (to be created)

## Agent-Ready Research Tasks

These research documents can be used by agents for deeper work:

**Agent Task: Morning Briefing System**
```
Label: Morning Briefing System Designer
Task: Design comprehensive morning briefing system.
Read: /root/clawd/memory/morning-briefing-research.md
Deliverable: System architecture, automation flows, priority matrix
```

**Agent Task: Twiggy Content Automation**
```
Label: Twiggy Content Automation
Task: Build Instagram scraper → WordPress blog post pipeline.
Read: /root/clawd/memory/twiggy-automation-research.md
Deliverable: Working automation script
```

### 20. **Reddit-Researcher** (`#20`)
   - Find validated startup ideas from Reddit communities
   - ICP lead generation from problem discussions
   - Replaces: Gummy Search (no longer exists)
   - Approach: PRAW + Apify scraper + OpenAI for pattern analysis
   - 4-step process: Find trending subreddits → Analyze problems/solutions → Find creators → Build MVP
   - Status: Research started (1 video)
   - Priority: High
   - Notes: Based on Greg's video process + $17K MRR from Reddit research

### 21. **PR Agency Website Services** (`#21`)
   - Pitch: "I built Twiggy's website, I can do the same for your clients"
   - Target ICPs: PR agencies, publicists, talent agencies
   - Service: Website builds + social media integration
   - Case study: Twiggy website
   - Status: Just created
   - Priority: High
   - Notes: Cold outreach opportunity, Reddit not involved
