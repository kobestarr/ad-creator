# Oktopost Integration - Product Requirements Document

## Overview

Automated social media content pipeline for BluprintX that generates content via Claude AI and publishes it to Oktopost as drafts for human review before going live.

## Status: Active (API Confirmed Working Feb 20, 2026)

---

## Problem Statement

BluprintX needs to produce 24 social media posts per week across multiple platforms (LinkedIn, Instagram, Twitter) and multiple voices (company account + 3 senior leaders). Manual creation and scheduling is time-consuming and inconsistent.

## Solution

An end-to-end pipeline that:
1. **Generates** content using Claude AI (via the `bluprintx-social-content` skill)
2. **Posts** content to Oktopost as drafts via API
3. **Enables** human review and approval in Oktopost UI
4. **Publishes** on schedule through Oktopost's native scheduling

## Users

| User | Role | Interaction |
|------|------|-------------|
| Kobi Omenaka | System builder / operator | Runs scripts, manages pipeline |
| BluprintX marketing team | Reviewers | Approve/edit drafts in Oktopost UI |
| Phil Petrelli (CRO) | Content voice | LinkedIn posts reviewed in his name |
| AT Trzaskus (VP Marketing) | Content voice | LinkedIn posts reviewed in his name |
| Lee Hackett (CEO) | Content voice | LinkedIn posts reviewed in his name |

## Architecture

```
Claude AI (content generation)
    |
    v
CSV / Direct text output
    |
    v
post-to-oktopost.py / generate-and-post.py
    |
    v
Oktopost API (POST /v2/message)
    |
    v
Oktopost UI (draft review & scheduling)
    |
    v
LinkedIn / Instagram / Twitter (published)
```

## Technical Specifications

### API Details

| Field | Value |
|-------|-------|
| Base URL | `https://api.oktopost.com/v2` |
| Auth | Basic Auth (Account ID : API Key) |
| Account ID | 001kzy8780tsd6r |
| Content-Type | `application/x-www-form-urlencoded` |

### Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/v2/message` | Create a draft message |
| GET | `/v2/message?campaignId=xxx` | List messages by campaign |
| GET | `/v2/message?ids=xxx` | Get message by ID |
| GET | `/v2/message/xxx` | Get message by ID (path) |
| DELETE | `/v2/message/xxx` | Delete message (needs testing) |

### Required Parameters (POST /v2/message)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| campaignId | string | Yes | Campaign to post to |
| network | string | Yes | LinkedIn, Instagram, Twitter |
| message | string | Yes | Post content |
| status | string | No | "draft" (default), "default" |
| media | string | No | Media ID for image posts (Instagram) |

### Campaigns

| Campaign ID | Name | Purpose |
|-------------|------|---------|
| 002g5m4amrtu2xs | AI Value Accelerator | Primary content campaign |
| 002586p3bofvpua | 2026-01 Native Posts | Monthly native posts |
| 002yfxw3pc8r77l | 2025-12 Native Posts | Archive |

## Content Volume

### Weekly Output (24 posts total)

**BluprintX Company (15 posts):**
- 5 days (Mon-Fri) x 3 platforms (LinkedIn, Instagram, Twitter)
- Funnel stages: TOFU, MOFU, MOFU, BOFU, TOFU-Light

**Senior Leaders (9 posts):**
- 3 leaders x 3 days (Mon, Wed, Thu) x LinkedIn only
- Phil Petrelli, AT Trzaskus, Lee Hackett

## Scripts

### post-to-oktopost.py
Primary posting tool with three modes:
- `--csv content.csv` — Batch post from CSV (Claude's content table output)
- `--text "content" --network LinkedIn` — Single post
- `--interactive` — Manual interactive mode

### generate-and-post.py
All-in-one content generation + posting. Generates a full week of template content and posts directly to Oktopost. Useful for quick content fills.

### list-oktopost-drafts.sh
Lists all draft messages in the AI Value Accelerator campaign. Used to verify posts were created correctly.

### oktopost-post-ui.js (Fallback)
Playwright-based browser automation. Posts content through the Oktopost web UI. Available as an alternative to the API method but not the preferred approach since API was confirmed working.

## Credential Storage

```
~/.clawdbot/oktopost_credentials.json
{
  "account_id": "001kzy8780tsd6r",
  "api_key": "...",
  "base_url": "https://api.oktopost.com/v2"
}
```

## Constraints

- All posts are created as **DRAFTS** — never published directly
- Instagram posts require a media ID (holding image available: `026dgnkgcc9furg`)
- Lee Hackett content must be in British English
- No em dashes in any content
- Carousels limited to 5 pages maximum
- `campaignId` is mandatory for listing messages (no global list)

## Success Metrics

| Metric | Target |
|--------|--------|
| Posts generated per week | 24 |
| Time from generation to Oktopost | < 5 minutes |
| Draft accuracy (no manual rewrite needed) | > 80% |
| Platform coverage | LinkedIn + Instagram + Twitter |
| API reliability | > 99% success rate |

## Open Items

| Item | Status | Priority |
|------|--------|----------|
| Delete endpoint verification | Needs testing | Medium |
| Image/asset auto-upload to Oktopost | Not started | High |
| Scheduling via API (not just drafts) | Research needed | Medium |
| Webhook for post status updates | Research needed | Low |
| CSV export from Claude skill | Manual process | Medium |

---

*Created: 2026-02-20*
*Version: 1.1*
