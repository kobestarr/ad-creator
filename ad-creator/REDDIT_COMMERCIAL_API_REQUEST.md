# Reddit Commercial API Access Request

**Submission Form**: https://support.reddithelp.com/hc/en-us/requests/new?ticket_form_id=14868593862164

---

## Application Details

### Company/Organization Information
- **Company Name**: Bluprintx
- **Website**: https://bluprintx.com
- **Contact Email**: [Your business email]
- **Reddit Username**: padelpickle

### Application Information
- **App Name**: Bluprintx Ad Tool
- **App ID (Client ID)**: 2JkGff3iDSuUFeqAFDhaDA
- **Current Status**: Approved for Ads API, requesting Native API access

---

## Use Case Description

### Purpose
We are building a marketing automation tool that creates and manages Reddit advertising campaigns for our clients. Our tool reads ad copy from Google Sheets, creates Reddit posts with that content, and then promotes those posts via Reddit's Ads API.

### Current Workflow (Manual)
1. Marketing team writes ad copy variations in Google Sheets
2. **Manual step**: Create posts on Reddit with this content (time-consuming, error-prone)
3. Use Ads API to promote these posts (automated)

### Desired Workflow (Automated)
1. Marketing team writes ad copy variations in Google Sheets
2. **Automated**: Tool creates posts on Reddit using Native API
3. **Automated**: Tool creates ads promoting those posts using Ads API

### Business Value
- **Time savings**: Eliminate manual post creation for multiple ad variations
- **Consistency**: Ensure exact ad copy from approved sheets is used in posts
- **Scale**: Support multiple clients with high-volume campaigns
- **Accuracy**: Reduce human error in transcribing ad copy to Reddit

---

## Technical Implementation

### APIs Required
1. **Ads API** (Already approved and working)
   - Scopes: `adsread`, `adsedit`, `adsconversions`, `history`
   - Purpose: Create and manage ad campaigns

2. **Native API** (Requesting approval)
   - Scopes: `identity`, `submit`, `mysubreddits`
   - Purpose: Programmatically create posts with client-approved ad copy

### Architecture
- Node.js backend tool
- OAuth 2.0 authentication for both APIs
- Google Sheets integration for ad copy input
- Automated post creation → ad promotion pipeline

### Code Repository
- GitHub: https://github.com/kobestarr/ad-creator
- Open source implementation
- Built with security and Reddit's API best practices

---

## Volume Estimates

### Current Scale
- **Client**: Bluprintx (primary client)
- **Campaigns per month**: 5-10
- **Posts per campaign**: 10-20 variations (headlines × body × CTAs)
- **Total posts per month**: 50-200

### Growth Projection (Next 12 months)
- **Additional clients**: 3-5
- **Total posts per month**: 200-500

### Rate Limiting Compliance
- We respect Reddit's rate limits
- Batch operations with delays between requests
- No spam or low-quality content
- All posts are genuine marketing content for real businesses

---

## Content Standards

### Quality Commitment
- All posts created are legitimate marketing content
- No spam, manipulation, or policy violations
- Posts follow subreddit rules and Reddit's content policy
- Human oversight: Marketing teams approve all ad copy before automation runs

### Subreddit Targeting
- Focus on business/professional subreddits (e.g., r/salesforce, r/marketing)
- Respect community guidelines
- Only post where advertising is permitted

### Transparency
- Posts are clearly branded (Bluprintx branding visible)
- No attempt to deceive users about sponsored content
- All posts are promoted as paid ads (via Ads API)

---

## Compliance

### Reddit Policies
- We have read and agree to comply with:
  - Reddit's API Terms of Service
  - Responsible Builder Policy
  - Advertising Policy
  - Content Policy

### Data Usage
- No scraping or data collection beyond our own posts
- No user data harvesting
- Only authenticate our own accounts
- Secure credential storage (OAuth tokens in encrypted storage)

### Monitoring
- We log all API activity
- Monitor for errors or policy violations
- Quick response to any Reddit concerns

---

## Commercial Context

### Business Model
- Marketing automation SaaS for B2B companies
- Clients pay for campaign management services
- Reddit ads are part of multi-platform advertising strategy
- We are Reddit Ads API customers (spending advertising budget)

### Why Reddit?
- Our clients target professional audiences on Reddit
- Reddit Ads API provides excellent ROI
- Automation reduces campaign setup time
- Native API access would complete our workflow automation

---

## References

- **Reddit Ads Account**: a2_i5qw2u3t9aca
- **Existing App**: "Bluprintx Ad Tool" (Ads API approved)
- **Documentation Followed**: https://ads-api.reddit.com/docs/, https://www.reddit.com/dev/api/
- **Technical Challenge Summary**: See CHALLENGE_SUMMARY.md in our repository

---

## Additional Information

### Timeline
- Development complete, pending Native API approval
- Can begin operations immediately upon approval

### Support Needs
- None expected - our team has experience with Reddit's Ads API
- Will reach out to developer support if issues arise

### Questions for Reddit
1. Is there a production testing phase before full approval?
2. Are there any additional compliance requirements for commercial post creation?
3. Should we implement additional rate limiting beyond standard API limits?

---

**Submission Date**: [Fill in when submitting]
**Contact for Questions**: [Your email]
