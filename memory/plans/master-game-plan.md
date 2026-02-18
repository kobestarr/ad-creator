# MASTER GAME PLAN - All Projects

**Last Updated:** 2026-02-01  
**Primary Goal:** Clear £100,045.43 debt by February 2027

---

## PHASE 1: CORE INFRASTRUCTURE (This Week)

### 1.1 Morning Briefing System ⭐ PRIORITY
**Goal:** Reduce daily cognitive load

**Components:**
- [ ] School management integration
- [ ] Meal planning system
- [ ] Financial digest (Freeagent + Starling)
- [ ] Health/fitness (Strava + TrainerRoad + Withings)
- [ ] Media tracking
- [ ] Daily priorities

**What I can build now:**
- [ ] Briefing template structure
- [ ] Financial API integration (exists, expand)
- [ ] Health API connection framework

**API Needs:**
- None additional (financial APIs exist)

**User Input Needed:** Brain dump on school/meal systems

---

### 1.2 Financial Tracking Expansion
**Goal:** Complete debt payoff visibility

**Current State:**
- ✅ Freeagent connected (Stripped Media)
- ✅ Starling connected (KSD + Stripped Media)
- ⏳ KSD specific data access

**What I can build now:**
- [ ] Weekly debt payoff digest
- [ ] Cash flow forecasting
- [ ] Payment due reminders
- [ ] Visual dashboard

**API Needs:**
- Freeagent: Already have tokens (need KSD-specific access)

---

### 1.3 Job Board Scraping Pipeline ⭐ HIGH INCOME
**Goal:** £5,000-15,000/month recurring revenue

**Research:** Complete ✅

**What I can build now:**
- [ ] Apify job scraper setup guide
- [ ] CaptainData enrichment workflow
- [ ] Outreach email templates
- [ ] Spreadsheet CRM template

**API Needs:**
| Service | Purpose | Cost | Action |
|---------|---------|------|--------|
| Apify | Job scraping | $49+/mo | Create account |
| CaptainData | Data enrichment | Credits | Create account |
| Hunter.io | Email finding | $49+/mo | Create account |

---

## PHASE 2: CONTENT & SEO (Next 2 Weeks)

### 2.1 Parasite SEO System (LinkedIn + Reddit)
**Goal:** Fast traffic, lead generation

**Research:** Complete ✅

**What I can build now:**
- [ ] Content calendar (12 topics)
- [ ] SEO-optimized article templates
- [ ] LinkedIn posting workflow (approval required)
- [ ] Reddit monitoring setup (Redreach.ai)

**API Needs:**
| Service | Purpose | Cost | Action |
|---------|---------|------|--------|
| Redreach.ai | Reddit monitoring | $97+/mo | Optional - research first |

**Posting:** NO - user approval only

---

### 2.2 Content Repurposing Pipeline
**Goal:** One content piece → 10+ outputs

**What I can build now:**
- [ ] Template system for repurposing
- [ ] Platform-specific formatting rules
- [ ] Scheduling workflow (Oktopost exists)

**API Needs:**
- None - uses existing Oktopost

---

### 2.3 Substack Strategy
**Goal:** Build email list, eventual paid subscriptions

**Research:** Complete ✅

**What I can build now:**
- [ ] Content repurposing to Substack
- [ ] Newsletter templates
- [ ] Growth strategy

**API Needs:**
- Substack: Free, just need account creation

---

## PHASE 3: INCOME STREAMS (This Month)

### 3.1 Twine Freelance Profile
**Goal:** £75-150/hour freelance work

**Research:** Complete ✅

**What I can build now:**
- [ ] KSD portfolio page structure
- [ ] Productized offer template
- [ ] Profile optimization checklist

**API Needs:**
- Twine: Free, just need profile setup

---

### 3.2 GHL Communities Setup
**Goal:** Community building + affiliate income

**Research:** Complete ✅

**What I can build now:**
- [ ] Community structure design
- [ ] Course outline template
- [ ] Affiliate strategy

**API Needs:**
| Service | Purpose | Cost | Action |
|---------|---------|------|--------|
| GoHighLevel | Community platform | $97-497/mo | Free trial available |

---

### 3.3 KSD Local Outreach Service
**Goal:** £4,000-8,000/month recurring

**Proposal:** Complete ✅

**What I can build now:**
- [ ] Lead sourcing workflow
- [ ] Outreach sequence templates
- [ ] CRM setup guide

**API Needs:**
- Same as Job Board Scraping (Apify, CaptainData)

---

## PHASE 4: AUTOMATION PROJECTS

### 4.1 Twiggy Content Automation
**Goal:** Automated blog posts from Instagram

**Research:** Placeholder ✅

**What I can build now:**
- [ ] Instagram monitoring workflow
- [ ] Context research automation
- [ ] WordPress draft creation

**API Needs:**
| Service | Purpose | Cost | Action |
|---------|---------|------|--------|
| Apify | Instagram scraping | $49+/mo | Trial first |
| WordPress REST API | Blog posting | Free | Get admin access |

**Posting:** NO - drafts only, human review required

---

### 4.2 Media Tracking System
**Goal:** Track TV/films, repurpose to blog

**Research:** Placeholder ⏳ (Low Priority)

**What I can build now:**
- [ ] Letterboxd integration guide
- [ ] Blog post templates
- [ ] Weekly export workflow

**API Needs:**
- Letterboxd: Free, just need account

---

## API ACCESS REQUIRED - COMPLETE LIST

### CRITICAL (For Core Work)

| # | Platform | Purpose | Cost | Get Credentials |
|---|----------|---------|------|-----------------|
| 1 | **Apify** | Job scraping, Instagram | $49+/mo | https://apify.com |
| 2 | **CaptainData** | Data enrichment | Credits | https://captaindata.io |
| 3 | **Hunter.io** | Email finding | $49+/mo | https://hunter.io |
| 4 | **Strava** | Activity tracking | Free | https://strava.com |
| 5 | **TrainerRoad** | Training sync | Free | https://trainerroad.com |
| 6 | **Withings** | Health metrics | Free | https://withings.com |

### MEDIUM PRIORITY

| # | Platform | Purpose | Cost | Get Credentials |
|---|----------|---------|------|-----------------|
| 7 | **GoHighLevel** | Communities | $97-497/mo | https://gohighlevel.com |
| 8 | **Redreach.ai** | Reddit monitoring | $97+/mo | https://redreach.ai |
| 9 | **WordPress (Twiggy)** | Blog posting | Free | Need admin access |

### LOW PRIORITY / NO CREDENTIALS NEEDED

| # | Platform | Purpose | Cost | Notes |
|---|----------|---------|------|-------|
| 10 | **Twine** | Freelance profile | Free | Just signup |
| 11 | **Substack** | Newsletter | Free | Just signup |
| 12 | **Letterboxd** | Media tracking | Free | Just signup |
| 13 | **Oktopost** | Social scheduling | Existing | Already connected |
| 14 | **Freeagent** | Accounting | Existing | Already connected |
| 15 | **Starling** | Banking | Existing | Already connected |

---

## AGENT TASK TEMPLATES

### Agent 1: Job Scraping Setup
```
Label: Job Board Scraping Setup
Task: Build complete job scraping and outreach pipeline.
Read: /root/clawd/memory/job-scraping-research.md
Deliverables:
1. Apify actor configuration guide
2. CaptainData enrichment workflow
3. Outreach email templates (3 variants)
4. Spreadsheet CRM template
Output: /root/clawd/ksd/local-outreach/job-scraping/
```

### Agent 2: Parasite SEO Content
```
Label: Parasite SEO Content Creator
Task: Create 12 SEO-optimized articles for LinkedIn.
Read: /root/clawd/memory/parasite-seo-research.md
Deliverables:
1. Article 1: "AI Automation for Marketing Agencies"
2. Article 2: "Case Study: 10x ROI with Automation"
3. Article 3-12: Based on keyword research
Format: Markdown, ready for review
Output: /root/clawd/ksd/parasite-seo/articles/
Rule: NO POSTING - drafts only for approval
```

### Agent 3: Morning Briefing System
```
Label: Morning Briefing System Builder
Task: Design and build morning briefing automation.
Read: /root/clawd/memory/morning-briefing-research.md
Deliverables:
1. Briefing template structure
2. Financial section (Freeagent/Starling)
3. Health section (Strava/TrainerRoad/Withings)
4. Priority ordering system
Output: /root/clawd/scripts/morning-briefing/
```

### Agent 4: Twiggy Automation
```
Label: Twiggy Content Automation
Task: Build Instagram → WordPress blog pipeline.
Read: /root/clawd/memory/twiggy-automation-research.md
Deliverables:
1. Instagram monitoring workflow
2. Context research automation
3. WordPress draft creation script
4. Human review workflow
Output: /root/clawd/twiggy/automation/
Rule: NO AUTO-POSTING - drafts only
```

### Agent 5: GHL Community Setup
```
Label: GHL Community Designer
Task: Design community structure for KSD.
Read: /root/clawd/memory/ghl-communities-research.md
Deliverables:
1. Community structure (free + paid tiers)
2. Course outline template
3. Membership pricing model
4. Affiliate strategy
Output: /root/clawd/ksd/ghl-community/
```

---

## APPROVAL WORKFLOW (No Auto-Posting)

### Rule: NOTHING POSTS WITHOUT APPROVAL

**Workflow:**
```
Agent creates content → Draft saved to folder → User reviews → User approves → THEN post
```

**Folders for drafts:**
- `/root/clawd/ksd/parasite-seo/drafts/` - LinkedIn/Reddit drafts
- `/root/clawd/twiggy/blog-drafts/` - Twiggy blog drafts
- `/root/clawd/ksd/outreach/emails/` - Outreach email drafts

**User Action Required:**
1. Check drafts folder
2. Review content
3. Approve (or request changes)
4. Then I can post (when authorized)

---

## PRIORITY MATRIX - WHAT TO BUILD FIRST

### Week 1 (This Week)
| Priority | Project | What I Can Build | Dependencies |
|----------|---------|------------------|--------------|
| 1 | Morning Briefing | Template, structure | User brain dump |
| 2 | Financial Tracking | Expand existing | API exists |
| 3 | Job Scraping | Agent task + templates | Apify account |

### Week 2
| Priority | Project | What I Can Build | Dependencies |
|----------|---------|------------------|--------------|
| 4 | Parasite SEO | Article templates | None |
| 5 | Content Repurposing | Template system | None |
| 6 | Health Integration | API framework | Strava/TrainerRoad |

### Week 3-4
| Priority | Project | What I Can Build | Dependencies |
|----------|---------|------------------|--------------|
| 7 | GHL Setup | Community design | GHL account |
| 8 | Twiggy Automation | Workflow design | WordPress access |
| 9 | Twine Profile | Portfolio structure | None |

---

## USER ACTION ITEMS

### Today
1. [ ] Brain dump: Morning briefing requirements
2. [ ] Create Apify account (https://apify.com)
3. [ ] Create CaptainData account (https://captaindata.io)
4. [ ] Create Hunter.io account (https://hunter.io)

### This Week
5. [ ] Set up Strava API access
6. [ ] Verify TrainerRoad data sharing
7. [ ] Confirm Withings → Strava sync
8. [ ] Get Twiggy WordPress admin access

### Next Week
9. [ ] Try GoHighLevel free trial
10. [ ] Create Twine profile (KSD)
11. [ ] Create Substack account
12. [ ] Create Letterboxd account

---

## SUCCESS CRITERIA

### By End of Week 1
- [ ] Morning briefing template ready
- [ ] Job scraping workflow designed
- [ ] All APIs researched and accounts created

### By End of Week 2
- [ ] Parasite SEO articles drafted (12)
- [ ] Health data flowing to briefing
- [ ] Financial tracking dashboard complete

### By End of Month
- [ ] Job scraping pipeline operational
- [ ] First parasite SEO content approved
- [ ] GHL community structure designed
- [ ] Twiggy automation workflow ready

---

## CURRENT STATE CHECKLIST

### Completed
- [x] Local Outreach PROPOSAL.md
- [x] Deep research on all topics
- [x] Research documents saved
- [x] Ideas board updated (19 ideas)
- [x] Workspace organization complete
- [x] Agent baseline requirements documented

### In Progress
- [ ] Morning briefing brain dump (waiting for user)
- [ ] API credential collection

### Not Started
- [ ] Agent spawning
- [ ] System building
- [ ] Content creation

---

*Master Game Plan - Updated 2026-02-01*
