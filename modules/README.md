# Modular Email Automation System

**Philosophy:** Build Once, Use Infinitely

Each module is reusable across multiple use cases. Configure parameters instead of rebuilding.

---

## Module Architecture

```
/root/clawd/modules/
├── README.md                          ← This file
├── email-scraper/                     ← Finds/extracts emails
│   ├── README.md
│   ├── linkedin-scraper.js
│   ├── website-scraper.js
│   └── apify-integration.js
├── email-enrichment/                  ← Adds context to leads
│   ├── README.md
│   ├── apollo-integration.js
│   ├── perplexity-research.js
│   └── company-enrichment.js
├── email-verification/                ← Validates email deliverability
│   ├── README.md
│   ├── zerobounce-integration.js
│   └── debounce-integration.js
├── email-sender/                      ← Sends with tracking
│   ├── README.md
│   ├── gmail-integration.js
│   ├── sendgrid-integration.js
│   └── tracking-pixel.js
└── email-followup/                    ← Automated sequences
    ├── README.md
    ├── behavior-tracker.js
    ├── sequence-builder.js
    └── engagement-scorer.js
```

---

## Use Cases

| Use Case | Modules Required | Target List |
|----------|-----------------|-------------|
| Journalist Outreach | Scraper → Enrichment → Verification → Sender → Follow-Up | Journalists, editors |
| Football Club Outreach | Scraper → Enrichment → Verification → Sender → Follow-Up | Clubs, academies, schools |
| Local Business Outreach | Scraper → Enrichment → Verification → Sender → Follow-Up | Plumbers, electricians, roofers |
| Salesforce Hiring Tracker | Scraper → Enrichment → Sender | Companies hiring Salesforce |
| Job Applications | Scraper → Enrichment → Sender | Hiring managers |
| Press Coverage | Scraper → Enrichment → Sender → Follow-Up | Media contacts |

---

## Configuration Example (football-outreach.json)

```json
{
  "campaign": "ultimate-football-heroes-podcast",
  "modules": {
    "scraper": {
      "source": "club-websites",
      "target_file": "/root/clawd/data/football-clubs.json"
    },
    "enrichment": {
      "fields": ["size", "age_groups", "location", "coach_name"]
    },
    "verification": {
      "provider": "zerobounce"
    },
    "sender": {
      "provider": "sendgrid",
      "template": "football-podcast-outreach",
      "from_name": "Robyn @ Ultimate Football Heroes"
    },
    "followup": {
      "sequence": [3, 7, 14],  // Days after initial
      "triggers": ["no_open", "no_response"]
    }
  }
}
```

---

## Running a Campaign

```bash
# Run full campaign
node /root/clawd/modules/run-campaign.js --config /root/clawd/modules/football-outreach.json

# Run individual modules
node /root/clawd/modules/email-scraper/index.js --source club-websites
node /root/clawd/modules/email-enrichment/index.js --input data/clubs.json
node /root/clawd/modules/email-verification/index.js --input data/enriched.json
node /root/clawd/modules/email-sender/index.js --input data/verified.json
node /root/clawd/modules/email-followup/index.js --input data/sent.json
```

---

## Testing Checklist

Before deploying new use case:
- [ ] Test scraper on 10 targets
- [ ] Verify enrichment accuracy
- [ ] Validate email deliverability
- [ ] Send test emails (check spam folder)
- [ ] Verify tracking works (open/click tracking)
- [ ] Test follow-up sequences
- [ ] Document configuration in campaign file

---

*Build Once, Use Infinitely*
