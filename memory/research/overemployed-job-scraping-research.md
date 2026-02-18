# Overemployed Strategy & Job Scraping Automation Research

**Research Date:** 2026-02-01  
**Status:** COMPLETE

---

## PART 1: OVEREMPLOYED (OE) STRATEGY

### What Is Overemployed?

**Overemployed (OE)** = Working multiple full-time remote jobs simultaneously without employers knowing.

**Key Subreddits:**
- r/overemployed - Main community (~200K+ members)
- r/OveremployedUK - UK-focused private community
- overemployed.com - Main website with Discord community

---

### UK-Specific OE Considerations

**Tax & Legal (HMRC):**
- ✅ HMRC doesn't care as long as you pay correct taxes
- ✅ Multiple PAYE jobs are legal
- ⚠️ Most contracts have clauses restricting additional employment
- ⚠️ Reference checks can be an issue (past employers)

**Critical Requirements for UK OE:**
1. **Fully Remote Jobs Only** - Hybrid makes OE very difficult
2. **Separate Hardware** - J1 laptop for J1 only, J2 laptop for J2 only
3. **Separate Calendars** - No overlapping meeting times
4. **Tax Code Management** - Second job typically uses BR code
5. **LinkedIn Separation** - Separate accounts or hidden from search

**Success Factors from UK OEers:**
- Software/tech roles work best (remote-friendly, high demand)
- Part-time contracts in 2018-2023 worked well
- Current job market (2025) is harder - more competition
- Age can be a factor (42+ mentioned as harder)
- Geographic restrictions (many US-only remote jobs)

**Challenges Reported:**
- Job market saturation in 2024-2025
- Reference checks with past employers
- Companies wanting on-site presence
- Time zone coordination for overlapping jobs

---

### OE Process Overview

**Finding Remote Jobs:**
- RemoteJobMatching.com - Searches multiple remote boards at once
- LinkedIn Easy Apply - High volume applications
- We Work Remotely, Remote OK, FlexJobs
- Company career pages directly

**Application Strategy:**
- Apply to 10-20 jobs/day minimum
- Focus on fully remote positions
- Use AI tools for applications (covered below)
- Automate where possible

---

## PART 2: NICK SARAEV'S JOB SCRAPING & AUTOMATION METHODS

### Who Is Nick Saraev?

**n8n Creator Profile:** https://n8n.io/creators/nicksaraev/
**YouTube:** https://www.youtube.com/@nicksaraev

**Tagline:** "I make money with automation & teach others how they can too"

**Reputation in Automation Community:**
- "Nick Saraev is the only guy I've seen that actually builds good automations" - Reddit
- Known for practical, revenue-generating workflows
- Generated $72K/month using his automation methods

---

### Nick Saraev's n8n Workflows (Relevant to Job Scraping)

#### 1. **Personalized Upwork Proposals with GPT-4**
**Workflow:** Automate personalized Upwork proposals
**Components:** Google Docs, GPT-4, Mermaid diagrams
**Link:** https://n8n.io/workflows/6174-automate-personalized-upwork-proposals-with-gpt-4-google-docs-and-mermaid-diagrams/
**Views:** 2,889

**What it does:**
- Scrapes Upwork job postings
- Generates personalized proposals using GPT-4
- Creates custom diagrams for each proposal
- Saves to Google Docs

**RELEVANCE:** Can be adapted for job applications

---

#### 2. **Cold Email Icebreaker Generator with Apify, GPT-4 & Website Scraping**
**Workflow:** Deep personalization system for cold outreach
**Components:** Apollo.io, Apify, GPT-4, Google Sheets
**Link:** https://n8n.io/workflows/5388-cold-email-icebreaker-generator-with-apify-gpt-4-and-website-scraping/
**Views:** 3,166

**What it does:**
- Apollo lead acquisition (500+ leads per search)
- Multi-page website scraping (not just homepage)
- AI content analysis of multiple pages
- Generates personalized icebreakers (5-10% reply rates)
- Outputs to Google Sheets

**Key Statistics:**
- Response rates: 5-10% (vs 1-2% for standard cold email)
- Monthly cost: ~$150 (Apollo + Apify + OpenAI)
- Build time: 3-4 hours
- Proven methodology: $72K/month agency revenue

**RELEVANCE:** EXCELLENT for job scraping + personalization

---

#### 3. **Personalized LinkedIn Connection Requests**
**Workflow:** LinkedIn outreach with Apollo, GPT-4, Apify, PhantomBuster
**Components:** Apollo, GPT-4, Apify, PhantomBuster, Google Sheets
**Link:** https://n8n.io/workflows/4803-personalized-linkedin-connection-requests-with-apollo-gpt-4-apify-and-phantombuster/
**Views:** 3,136

**RELEVANCE:** Can be adapted for LinkedIn job engagement

---

#### 4. **AI Premium Proposal Generator**
**Workflow:** High-end proposal generation
**Components:** OpenAI, Google Slides, PandaDoc
**Link:** https://n8n.io/workflows/4804-ai-premium-proposal-generator-with-openai-google-slides-and-pandadoc/
**Views:** 4,525

**RELEVANCE:** For high-value job applications or freelance proposals

---

### Nick Saraev's YouTube Content

**Channel:** https://www.youtube.com/@nicksaraev

**Key Videos/Playlists:**
1. "How to Master N8N Like Nick Saraev" series
   - Lesson 5: Website scraping with HTTP Request node
   - Building complete workflow automations
   
2. "I Deep-Personalized 1000+ Cold Emails Using THIS AI System (FREE TEMPLATE)"
   - Live build of the icebreaker generator
   - Shows exact prompting strategies
   - Explains $72K/month methodology

**YouTube Search Terms to Find His Content:**
- "Nick Saraev n8n tutorial"
- "Nick Saraev job automation"
- "Nick Saraev Upwork proposals"
- "Nick Saraev cold email"

---

### Bluprintx Service Opportunity: Salesforce Hiring Tracker

**Idea:** Monitor LinkedIn/Job Boards for companies hiring Salesforce talent → Outreach to those companies

**Process:**
1. **Monitor:** Apify LinkedIn Jobs scraper for "Salesforce" keywords
2. **Enrich:** Find hiring company details (size, industry, location)
3. **Research:** Perplexity search for company news/events
4. **Outreach:** Personalized email about their Salesforce hiring + Bluprintx services
5. **Track:** Google Sheets CRM

**Value Proposition:**
- Companies just hired/advertising Salesforce → have budget
- Recent hire = likely need more help
- Automation makes this scalable

---

## PART 3: JOB SCRAPING FOR OE APPLICATIONS

### Nick Saraev's Approach (Based on His Workflows)

**Core Components:**
1. **Lead Source:** Apollo.io (or LinkedIn, Indeed, etc.)
2. **Scraping:** Apify (multi-page website scraping)
3. **AI Processing:** GPT-4 for personalization
4. **Output:** Google Sheets (structured data)
5. **Automation:** n8n workflow (orchestration)

**The Icebreaker System (Key Insight):**
```
Multi-Page Scraping → AI Content Analysis → Personalized Opener
```

**Why It Works:**
- Scrapes MORE than just homepage
- AI analyzes multiple pages per prospect
- Generates non-obvious personalization
- Makes recipient think you did hours of manual research

**Application to Job Applications:**
- Same approach for job postings
- Research company deeply before applying
- Generate personalized cover letter
- Reference specific company initiatives/news

---

### Required Tools & Accounts

| Tool | Purpose | Cost | Link |
|------|---------|------|------|
| **Apollo.io** | Lead/contact database | $49+/mo | apollo.io |
| **Apify** | Web scraping | $49+/mo | apify.com |
| **n8n** | Workflow automation | Free (self-hosted) | n8n.io |
| **OpenAI API** | AI processing | Pay per token | openai.com |
| **Google Sheets** | CRM/Database | Free | google.com |

**Total Monthly Cost:** ~$150-200

---

### Job Scraping Workflow for OE

**Phase 1: Find Remote Jobs**
```
1. Use LinkedIn Easy Apply filters:
   - Remote only
   - Full-time
   - Your job title/keywords
   - Last 24 hours (fresh postings)

2. Export to Google Sheets via Apify
```

**Phase 2: Research Each Company**
```
For each job:
1. Scrape company website (multiple pages)
2. Search for recent news/events
3. Find company's pain points
4. Identify hiring manager name
```

**Phase 3: Personalize Application**
```
1. Generate personalized cover letter using AI
2. Reference specific company initiatives
3. Connect your experience to their needs
4. Send application
```

**Phase 4: Track & Follow Up**
```
1. Google Sheets for all applications
2. Track responses
3. Follow up on applications > 1 week old
4. Update status daily
```

---

## PART 4: NICK SARAEV BLUEPRINTS & TEMPLATES

### Available Templates (Free)

**From n8n.io:**
1. Cold Email Icebreaker Generator ⭐ (Most relevant)
2. Personalized Upwork Proposals
3. LinkedIn Connection Requests
4. AI Premium Proposal Generator
5. Competitive Ad Research & Image Generator

**To Access:**
1. Create free n8n.io account
2. Go to workflow link
3. Click "Use this workflow"
4. Configure with your credentials

### Custom Workflows to Build

**Workflow 1: Job Application Tracker**
```
Trigger: Apify LinkedIn Jobs scraper
→ Extract job details
→ Scrape company website
→ AI generate cover letter
→ Save to Google Sheets
→ Send application
```

**Workflow 2: Company Research Automation**
```
Input: List of companies
→ Scrape website (multi-page)
→ AI analyze for pain points
→ Generate talking points
→ Output to Google Sheets
```

**Workflow 3: Application Follow-Up**
```
Trigger: Google Sheets row older than 7 days
→ Check job posting status
→ If still open → Send follow-up email
→ Update status
```

---

## PART 5: IMPLEMENTATION FOR BLUPRINTX

### Service 1: Salesforce Hiring Tracker

**Target:** Companies hiring Salesforce talent → Offer Bluprintx services

**Workflow:**
```
1. Apify LinkedIn Jobs scraper for "Salesforce"
2. Filter: Remote, Last 7 days, Full-time
3. Enrich company data (size, industry, location)
4. Perplexity research for recent news
5. Personalized outreach email
6. Track in Google Sheets CRM
7. Follow-up sequence
```

**Value Props:**
- "I noticed you just hired a Salesforce [role]..."
- Companies with budget (just spent on hiring)
- Likely need ongoing Salesforce support
- Scalable, automated outreach

---

### Service 2: Remote Job Scraping for OE Clients

**Target:** People wanting to work 2+ remote jobs

**Workflow:**
```
1. Monitor multiple job boards (LinkedIn, Indeed, etc.)
2. Scrape new postings daily
3. Filter by criteria (remote, salary, title)
4. Research each company
5. Generate personalized applications
6. Track in CRM
7. Auto-apply or prepare drafts
```

**Monetization:**
- Monthly subscription service
- Help clients get 2-3 remote jobs
- Ongoing support for OE maintenance

---

### Service 3: Job Application Automation

**Target:** Job seekers (could be white-label for Bluprintx)

**Features:**
- Daily job alerts matching criteria
- AI-personalized cover letters
- Auto-apply where possible
- Follow-up sequences
- Interview prep based on company research

---

## PART 6: REVENUE POTENTIAL

### Per-Service Estimates

| Service | Setup Fee | Monthly | Volume |
|---------|-----------|---------|--------|
| Salesforce Hiring Tracker | £2,000 | £500-1,000 | 5-10 clients |
| OE Job Scraping | £1,500 | £300-500 | 10-20 clients |
| Application Automation | £1,000 | £200-300 | 15-25 clients |

### Combined OE + Job Scraping Agency
- **Target:** £10K-20K/month recurring
- **Team:** You + automation
- **Scalability:** n8n handles volume

---

## PART 7: NEXT STEPS

### Immediate Actions

1. [ ] Create n8n.io account (free)
2. [ ] Import Nick Saraev's icebreaker workflow
3. [ ] Set up Apify LinkedIn Jobs scraper
4. [ ] Create Google Sheets CRM template
5. [ ] Build Salesforce Hiring Tracker workflow (test)

### This Week

1. [ ] Build Job Application Tracker workflow
2. [ ] Test with 10 job applications
3. [ ] Document process
4. [ ] Create service offering for Bluprintx

### This Month

1. [ ] Launch Salesforce Hiring Tracker service
2. [ ] Build OE Job Scraping service
3. [ ] Create content for potential clients
4. [ ] Get first 2-3 paying clients

---

## PART 8: KEY RESOURCES

### Nick Saraev Resources
- **n8n Profile:** https://n8n.io/creators/nicksaraev/
- **YouTube:** https://www.youtube.com/@nicksaraev
- **Cold Email Workflow:** https://n8n.io/workflows/5388-cold-email-icebreaker-generator-with-apify-gpt-4-and-website-scraping/
- **Upwork Proposal Workflow:** https://n8n.io/workflows/6174-automate-personalized-upwork-proposals-with-gpt-4-google-docs-and-mermaid-diagrams/

### OE Resources
- **Subreddit:** r/overemployed
- **UK Subreddit:** r/OveremployedUK (private)
- **Website:** overemployed.com
- **Discord:** overemployed.com/join-community/

### Tools & Pricing
- **n8n:** Free (self-hosted) or $20/mo (cloud)
- **Apollo.io:** $49+/mo
- **Apify:** $49+/mo
- **OpenAI:** Pay per token (~$10-50/mo for this use case)

---

## SUMMARY

### OE Strategy for You
1. Use job scraping to find remote jobs
2. Personalize applications using AI (Nick Saraev's method)
3. Apply to 10-20/day minimum
4. Track everything in Google Sheets
5. Build systems to maximize productivity

### Bluprintx Service Opportunity
1. Salesforce Hiring Tracker (high value)
2. OE Job Scraping (subscription model)
3. Application Automation (white-label potential)

### Key Insight
Nick Saraev's methods work because they:
- Research deeply (multi-page scraping)
- Personalize authentically (AI that sounds human)
- Scale efficiently (n8n automation)
- Generate real results ($72K/month proven)

---

*Research Complete - Ready for Implementation*
