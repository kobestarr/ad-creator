# Bluprintx LinkedIn Job Scraper → Hiring Manager Finder
**Handover Document - Stage 2: Contact Discovery**

## 🎯 Project Overview
We've built a LinkedIn job scraper that identifies companies hiring for Salesforce roles. The next critical stage is finding the actual hiring managers and their contact details for sales outreach.

## ✅ What We've Built (Stage 1 Complete)

### Core Technology Stack
- **LinkedIn Job Scraper**: Apify actor-based system ($0.35/1K jobs)
- **Data Processing**: Clean URLs, deduplication, formatting
- **Output**: Google Sheets with clean job data
- **Filters**: Company size, seniority, location, salary ranges
- **Cost**: Extremely efficient at ~$0.02 per search

### Current Data Output
Each job entry contains:
- Clean job posting URL (no tracking parameters)
- Company name and LinkedIn company URL
- Job title and description
- Location and posting date
- Employment type and experience level

## 🚀 Stage 2: Hiring Manager Discovery

### The Problem We're Solving
"We know Salesforce is hiring Administrators, but WHO is the actual hiring manager? The person with budget authority?"

### Target Contact Types (Priority Order)
1. **Hiring Manager** - Direct budget authority (Primary target)
2. **Department Head** - Functional leader (Secondary)
3. **Talent Acquisition** - Recruiter working role (Tertiary)
4. **HR Business Partner** - Strategic HR contact (Backup)

## 🔧 Technical Implementation Options

### Option A: N8N Workflow (Recommended)
Build on your existing n8n infrastructure:
```
Job Data → LinkedIn Company Search → Employee Search → 
Title Filtering → Contact Extraction → Email Finding → 
Validation → CRM Export
```

### Option B: Apollo.io Integration
Leverage Apollo's contact database:
```
Company Name → Apollo Search → Role Filtering → 
Email/Phone Extraction → Verification → Export
```

### Option C: Hunter.io + LinkedIn
Combine email finding with LinkedIn data:
```
Company Domain → Hunter Email Finder → LinkedIn Cross-reference → 
Title Matching → Contact Validation
```

## 📊 Contact Finding Strategy

### LinkedIn Search Parameters
```
Company: [From Job Scraper]
Title Contains: ("Head of" OR "Director of" OR "VP of" OR "Manager") AND 
("Salesforce" OR "CRM" OR "Technology" OR "Digital")
Location: [Same as job location]
```

### Priority Title Keywords
**Tier 1 (Hiring Managers):**
- "Head of Salesforce"
- "Director of CRM Technology" 
- "VP of Digital Transformation"
- "Salesforce Practice Lead"

**Tier 2 (Department Heads):**
- "IT Director"
- "Technology Director" 
- "Digital Director"
- "CRM Manager"

**Tier 3 (Recruitment):**
- "Talent Acquisition"
- "Recruiter" + Salesforce
- "HR Business Partner"

## 🎯 Bluprintx-Specific Targeting

### Ideal Prospect Profile
- **Company Size**: 50-1000 employees (sweet spot for consulting)
- **Industry**: Professional services, technology, financial services
- **Location**: UK-based (primary market)
- **Role**: Salesforce Administrator/Developer/Consultant hiring
- **Budget Signal**: Multiple Salesforce roles = serious investment

### Contact Quality Scoring
```
Score 10: Hiring Manager + Verified Email + Direct Phone
Score 8: Department Head + Verified Email  
Score 6: Recruiter + Verified Email
Score 4: Any contact + Verified Email
Score 2: Contact found but unverified
```

## 🔍 Data Enrichment Process

### Step 1: Company Research
```
Input: Company Name from Job Scraper
Process: LinkedIn Company Search → Domain extraction → Industry/Size validation
Output: Company domain, employee count, industry, key decision makers
```

### Step 2: Contact Discovery  
```
Input: Company domain + target titles
Process: LinkedIn Sales Navigator → Apollo.io → Hunter.io
Output: Contact list with names, titles, LinkedIn URLs
```

### Step 3: Email Finding
```
Input: Contact names + company domain
Process: Hunter.io → Apollo.io → Email pattern matching
Output: Email addresses with confidence scores
```

### Step 4: Phone Numbers
```
Input: Contact emails + LinkedIn URLs  
Process: Apollo.io → ZoomInfo → Direct dial finding
Output: Phone numbers with line type (mobile/direct/office)
```

## 📋 Output Specification

### Final Contact Record
```json
{
  "company_name": "Mango Analytics",
  "company_domain": "mango-analytics.com", 
  "company_size": "51-200",
  "company_linkedin": "https://linkedin.com/company/mango-analytics",
  "job_title_found": "Salesforce Administrator",
  "job_url": "https://linkedin.com/jobs/view/4368116790",
  
  "contact_name": "Sarah Johnson",
  "contact_title": "Head of Technology",
  "contact_linkedin": "https://linkedin.com/in/sarah-johnson-123",
  "contact_email": "s.johnson@mango-analytics.com",
  "contact_phone": "+1-614-555-0123",
  "contact_score": 8,
  "contact_priority": "Tier 1",
  
  "discovery_date": "2026-02-04",
  "email_verified": true,
  "phone_type": "direct",
  "notes": "Hiring for Salesforce Admin, reports to CTO"
}
```

## 🚀 Implementation Priority

### Phase 1: MVP (Week 1)
- [ ] Build n8n workflow for basic contact finding
- [ ] Test with 10-20 companies from job scraper
- [ ] Validate email accuracy rates
- [ ] Export to CSV for manual outreach

### Phase 2: Automation (Week 2)  
- [ ] Integrate with job scraper output
- [ ] Add email verification (NeverBounce/ZeroBounce)
- [ ] Build confidence scoring system
- [ ] Create CRM-ready export format

### Phase 3: Scale (Week 3)
- [ ] Batch processing for large job volumes
- [ ] Add phone number finding
- [ ] Implement quality scoring
- [ ] Build dashboard for tracking results

## 💰 Cost Considerations

### Tool Costs (Monthly)
- **Apollo.io**: $49/month (5K credits)
- **Hunter.io**: $49/month (1K searches) 
- **NeverBounce**: $0.01 per email verification
- **LinkedIn Sales Navigator**: $99/month (optional)

### Volume Planning
- **Target**: 100 qualified contacts per month
- **Cost per contact**: ~$0.50-1.50 (including tools + verification)
- **Break-even**: 1 consulting deal per 100 contacts = massive ROI

## 🔧 Technical Requirements

### Integration Points
```
Input: Google Sheets from Job Scraper
Processing: N8N workflow with API integrations
Output: Clean CSV + CRM integration ready
Monitoring: Success rates, bounce rates, contact quality
```

### API Integrations Needed
1. **LinkedIn API** (or Sales Navigator) - Company/employee data
2. **Apollo.io API** - Contact database access
3. **Hunter.io API** - Email finding
4. **NeverBounce API** - Email verification
5. **Google Sheets API** - Input/output integration

## 📊 Success Metrics

### Quality Metrics
- **Email accuracy**: >85% verified emails
- **Contact relevance**: >70% are actual decision makers
- **Data completeness**: >90% have email + title
- **Bounce rate**: <5% on verified emails

### Business Metrics  
- **Contacts per month**: 100+ qualified prospects
- **Response rate**: >15% to initial outreach
- **Meeting booking**: >5% of contacts
- **Deal conversion**: >1% of contacts to clients

## 🎯 Next Steps

### Immediate Actions
1. **Review n8n blueprint code** - understand current infrastructure
2. **Set up API accounts** - Apollo, Hunter, NeverBounce
3. **Build MVP workflow** - test with 10 companies
4. **Validate data quality** - manual review of first batch

### Questions for Implementation
1. **N8N infrastructure**: What's currently built and operational?
2. **API budget**: Monthly budget for contact finding tools?
3. **Volume expectations**: How many companies to process monthly?
4. **Quality vs quantity**: Prioritize perfect contacts or scale quickly?

## 📋 Handover Checklist

**For Next Developer:**
- [ ] Review existing n8n workflows and infrastructure
- [ ] Set up API accounts (Apollo, Hunter, NeverBounce)
- [ ] Build contact finding workflow (start with MVP)
- [ ] Test with small batch (10-20 companies)
- [ ] Validate email accuracy and contact quality
- [ ] Integrate with job scraper output
- [ ] Build export functionality for sales team
- [ ] Create monitoring dashboard

**Files/Resources Needed:**
- Current n8n workflow configurations
- API credentials for contact finding services
- Job scraper output format specification
- Sales team requirements and preferences
- CRM integration requirements

This handover provides the complete roadmap for turning job scraping data into actionable sales contacts for Bluprintx's consulting business.