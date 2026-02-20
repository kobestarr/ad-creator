# Oktopost Integration

Automated social media content pipeline for BluprintX. Generates content with Claude AI and posts to Oktopost as drafts for human review.

## Status: Active

API confirmed working (Feb 20, 2026). All scripts operational.

## Quick Start

### Post a single message
```bash
python3 scripts/social/post-to-oktopost.py \
  --text "Your post content here" \
  --network LinkedIn \
  --campaign 002g5m4amrtu2xs
```

### Post from CSV (Claude's content table)
```bash
python3 scripts/social/post-to-oktopost.py \
  --csv content_table.csv \
  --campaign 002g5m4amrtu2xs
```

### Generate a full week + post
```bash
python3 scripts/social/generate-and-post.py
```

### List current drafts
```bash
bash scripts/social/list-oktopost-drafts.sh
```

### Interactive mode
```bash
python3 scripts/social/post-to-oktopost.py --interactive
```

## How It Works

```
Claude AI  -->  CSV/Text  -->  Python Script  -->  Oktopost API  -->  Oktopost UI  -->  Social Media
(generate)      (export)       (post drafts)       (create)          (review)          (publish)
```

1. Use the `bluprintx-social-content` Claude skill to generate 24 posts/week
2. Export content as CSV or copy text directly
3. Run `post-to-oktopost.py` to create drafts in Oktopost
4. Review and approve drafts in the Oktopost web UI
5. Oktopost publishes on schedule

## Weekly Content Volume

| Account | Posts/Week | Platforms | Days |
|---------|-----------|-----------|------|
| BluprintX (company) | 15 | LinkedIn, Instagram, Twitter | Mon-Fri |
| Phil Petrelli (CRO) | 3 | LinkedIn only | Mon, Wed, Thu |
| AT Trzaskus (VP Marketing) | 3 | LinkedIn only | Mon, Wed, Thu |
| Lee Hackett (CEO) | 3 | LinkedIn only | Mon, Wed, Thu |
| **Total** | **24** | | |

## Scripts

| Script | Purpose |
|--------|---------|
| `post-to-oktopost.py` | Post content as drafts (CSV, single, interactive) |
| `generate-and-post.py` | Generate template content + post to Oktopost |
| `list-oktopost-drafts.sh` | List all drafts in campaign |
| `oktopost-post-ui.js` | Playwright UI fallback (not preferred) |

## Configuration

Credentials stored at `~/.clawdbot/oktopost_credentials.json`:
```json
{
  "account_id": "001kzy8780tsd6r",
  "api_key": "YOUR_API_KEY",
  "base_url": "https://api.oktopost.com/v2"
}
```

## API Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/v2/message` | Create draft message |
| GET | `/v2/message?campaignId=xxx` | List messages by campaign |
| GET | `/v2/message?ids=xxx` | Get message by ID (query) |
| GET | `/v2/message/xxx` | Get message by ID (path) |
| DELETE | `/v2/message/xxx` | Delete message (needs testing) |

**Note:** `campaignId` is required when listing messages. There is no global list endpoint.

## Key Constraints

- All posts created as **DRAFTS** (never auto-published)
- Instagram posts require a media ID for images
- Lee Hackett content must use British English
- No em dashes in any content
- Carousels limited to 5 pages max

## Related Docs

- [PRD.md](PRD.md) - Full product requirements
- [ROADMAP.md](ROADMAP.md) - Development roadmap
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [BluprintX Integration Notes](../../memory/research/bluprintx-oktopost-integration.md)
- [Content Generation Skill](../../entities/bluprintx/references/SKILL.md)

---

*Last updated: 2026-02-20*
