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

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|--------|
| POST | `/v2/message` | Create a draft message | Confirmed working |
| GET | `/v2/message?campaignId=xxx` | List messages by campaign (required) | Confirmed working |
| GET | `/v2/message?ids=xxx` | Get message by ID (query param) | Confirmed working |
| GET | `/v2/message/xxx` | Get message by ID (URL path) | Confirmed working |
| DELETE | `/v2/message/xxx` | Delete message | Needs re-testing |

### Required Parameters (POST /v2/message)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| campaignId | string | Yes | Campaign to post to |
| network | string | Yes | LinkedIn, Instagram, Twitter |
| message | string | Yes | Post content |
| status | string | No | "draft" (default), "default" |
| media | string | No | Media ID for image posts (Instagram) |

### Message Response Schema

Confirmed via Postman (Feb 20, 2026). Response from `GET /v2/message?campaignId=xxx`:

```json
{
  "Result": true,
  "Items": [
    {
      "Id": "005uknajp2x6f7j",
      "Created": "2026-02-01 12:28:10",
      "Modified": "2026-02-01 12:49:15",
      "Status": "default",
      "Type": "image",
      "AccountId": "001kzy8780tsd6r",
      "CreatedBy": "00Ayqwys85oqx9e",
      "ModifiedBy": "00Ayqwys85oqx9e",
      "CampaignId": "002g5m4amrtu2xs",
      "Network": "Instagram",
      "Subject": "",
      "Message": "The gap between AI investment and AI return..."
    }
  ],
  "Total": 27
}
```

### Message Object Fields

| Field | Type | Description |
|-------|------|-------------|
| Id | string | Unique message ID (prefix `005`) |
| Created | datetime | Creation timestamp (UTC) |
| Modified | datetime | Last modification timestamp |
| Status | string | `default`, `draft`, etc. |
| Type | string | `image`, `text`, etc. |
| AccountId | string | Bluprintx account ID |
| CreatedBy | string | User ID who created the message |
| ModifiedBy | string | User ID who last modified |
| CampaignId | string | Parent campaign ID |
| Network | string | `LinkedIn`, `Instagram`, `Twitter` |
| Subject | string | Message subject (typically empty for social) |
| Message | string | Full post content |
| IsAppMessage | int | 1 = created for app use (normal), 0 = board-only |
| IsBoardMessage | int | 1 = board message (UI visibility constraint when IsAppMessage=0) |

### API Behaviour Notes (from Oktopost Support, Feb 2026)

These were confirmed directly by Jason at Oktopost via support ticket:

1. **`campaignId` is mandatory for listing** - There is no global `/v2/message` list. You must always provide `campaignId` or specific `ids`.
2. **`IsAppMessage: 1` is normal** - All API-created messages get this flag. It does NOT affect visibility in the API or UI.
3. **Visibility constraint** - Only when `IsAppMessage: 0` AND `IsBoardMessage: 1` are messages hidden from the campaign UI view. This does not apply to API-created messages.
4. **Two ID lookup methods** - Both `?ids=005xxx` (query param) and `/005xxx` (URL path) work for retrieving a single message.
5. **No workflow/board assignment needed** - Messages created via API appear in the campaign view automatically.

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

## Support & Escalation

| Contact | Channel | Reference |
|---------|---------|-----------|
| Oktopost Support (Jason) | Zendesk ticket | API issues, endpoint behaviour |
| Kobi Omenaka | kobi.omenaka@bluprintx.com | Account owner, pipeline operator |

## Issue History

| Date | Issue | Resolution |
|------|-------|------------|
| Feb 1, 2026 | `campaignId` filter returning 0 results | Resolved Feb 20 - was likely a typo. Support confirmed 27 messages visible. |
| Feb 1, 2026 | DELETE returning success without deleting | Still under investigation |
| Feb 1, 2026 | API messages not visible in campaign UI | Resolved - messages do appear, original test was flawed |

## Open Items

| Item | Status | Priority |
|------|--------|----------|
| Delete endpoint verification | Needs re-testing | Medium |
| Image/asset auto-upload to Oktopost | Not started | High |
| Scheduling via API (set publish date/time) | Research needed | Medium |
| Webhook for post status updates | Research needed | Low |
| CSV export from Claude skill (currently manual) | Manual process | Medium |
| End-to-end pipeline test (full 24 posts) | Ready to test | High |

---

*Created: 2026-02-20*
*Updated: 2026-02-20*
*Version: 1.2*
