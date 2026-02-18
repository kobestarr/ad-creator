# Twiggy Content Automation Research (Instagram → WordPress)

**Research Date:** 2026-02-01  
**Status:** Not Started

---

## Goal

Automated pipeline that:
1. Monitors Twiggy's Instagram posts
2. Scrapes post content and images
3. Researches context (premieres, magazines, launches)
4. Creates blog post on Twiggy's WordPress site
5. Adds additional context and value

---

## Components

### 1. Instagram Monitoring
**Options:**
- **Apify Instagram scraper** - Can monitor profiles, extract posts
- **IFTTT** - Simple notifications for new posts
- **Manual** - Check regularly

**Data to extract:**
- Post text/caption
- Images/videos
- Hashtags
- Engagement (likes, comments)
- Timestamp

### 2. Context Research
**For each post, research:**
- Event mentioned (premiere, launch, interview)
- Publication coverage
- Related news
- Background context

**Sources:**
- Google search for event/mentioned item
- News sites
- Magazine websites
- Event calendars

### 3. Content Enrichment
**Add to original post:**
- Event details (date, location, attendees)
- Links to related coverage
- Additional photos from event
- Historical context (if recurring event)
- Quotes from interviews

### 4. WordPress Publishing
**Options:**
- **WordPress REST API** - Programmatically create posts
- **IFTTT** - Simple auto-post (limited customization)
- **Manual** - Copy-paste, then edit

**Post format:**
- Title: Based on post topic
- Content: Original post + enriched context
- Featured image: From Instagram
- Categories: Appropriate for Twiggy's site
- Tags: Event type, people, publications

---

## Workflow Design

```
Step 1: MONITOR
├── Apify Instagram scraper runs daily
├── Detects new Twiggy posts
└── Extracts post data + images

Step 2: RESEARCH
├── For event-related posts:
│   ├── Search for event details
│   ├── Find related coverage
│   └── Gather additional context
└── For simple posts: Skip to publish

Step 3: ENRICH
├── Combine original post + research
├── Add links to sources
├── Include additional images
└── Write connecting narrative

Step 4: PUBLISH
├── Use WordPress REST API
├── Create draft post
└── Notify (don't auto-publish - human review)

Step 5: REVIEW
├── Human reviews draft
├── Edits/approves
└── Publishes
```

---

## Tools Required

| Tool | Purpose | Cost |
|------|---------|------|
| Apify Instagram Scraper | Monitor & extract Instagram | $49+/month |
| OpenClaw/Claude | Research + content enrichment | Existing |
| WordPress REST API | Publish to WordPress | Free |
| Google Search | Context research | Free (Perplexity) |

---

## Example: Premiere Post

**Original Instagram Post:**
```
Twiggy ✨ on Instagram: "Had the most wonderful evening at the [Event Name] last night! So honored to be among such incredible women. More photos coming soon... 📸"
```

**Enriched Blog Post:**
```
Title: Twiggy Shines at [Event Name] 2026

Body:
[Embed original Instagram post]

Context:
The [Event Name] took place last night at [Location], celebrating [purpose]. Twiggy was among the honored guests...

[Add 3-5 paragraphs of context:]
- What is the event?
- Who else attended?
- Why is it significant?
- Previous years/background

[Embed additional photos if available]
[Link to event coverage]
[Link to Twiggy's previous appearances]

Tags: Events, [Event Name], [Year], Red Carpet
```

---

## Considerations

### Instagram Terms of Service
- Automated scraping may violate ToS
- Use carefully, consider legal review
- May need to use official API if available

### WordPress Integration
- Need admin access to Twiggy's WordPress
- REST API must be enabled
- Test with drafts before full automation

### Content Quality
- Must add value beyond just reposting
- Human review required before publishing
- Maintain Twiggy's brand voice

---

## Next Steps

1. [ ] Confirm access to Twiggy's WordPress admin
2. [ ] Research Instagram API vs scraping options
3. [ ] Set up Apify Instagram scraper (free tier trial)
4. [ ] Test extraction on existing posts
5. [ ] Build context research prompt
6. [ ] Set up WordPress REST API connection
7. [ ] Create end-to-end workflow
8. [ ] Test with 5 posts, review quality
9. [ ] Move to production (with human review)

---

*Note: Research not started - placeholder for future work.*
