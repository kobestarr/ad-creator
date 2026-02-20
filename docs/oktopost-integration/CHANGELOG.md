# Oktopost Integration - Changelog

## [1.2.0] - 2026-02-20 - PRD & Changelog Enriched

### Added to PRD
- **Full message response schema** — Documented all fields returned by the API (Id, Created, Modified, Status, Type, AccountId, CreatedBy, ModifiedBy, CampaignId, Network, Subject, Message, IsAppMessage, IsBoardMessage) based on confirmed Postman response
- **API behaviour notes** — 5 key rules confirmed by Oktopost support (Jason) including campaignId mandatory, IsAppMessage explained, visibility constraints, dual ID lookup methods, no workflow needed
- **Endpoint status column** — Each endpoint now shows confirmed working / needs testing
- **Support & escalation contacts** — Jason at Oktopost (Zendesk), Kobi as account owner
- **Issue history table** — Timeline of all reported issues and their resolutions
- **End-to-end pipeline test** added to open items (ready to test now that API is unblocked)

### Changed
- PRD version: 1.1 -> 1.2

---

## [1.1.0] - 2026-02-20 - API Unblocked

### Context
On Feb 1, 2026, Kobi reported that `GET /v2/message?campaignId=002g5m4amrtu2xs` was returning `{"Result":true,"Items":[],"Total":0}` despite messages being created successfully via `POST /v2/message`. A detailed support email was sent to Oktopost covering:
- The `campaignId` filter returning empty results
- DELETE endpoint returning success without actually deleting
- Questions about `IsAppMessage` flag affecting visibility

### Support Response (Jason @ Oktopost, Feb 20, 2026)
Jason tested the same endpoint and confirmed:
- **27 messages visible** in the AI Value Accelerator campaign
- The original 0-result issue was **likely a typo** on our end
- `campaignId` parameter is **required** — no global list exists
- `IsAppMessage: 1` is the **normal** flag for app-created messages and has no visibility impact
- Only `IsAppMessage: 0` + `IsBoardMessage: 1` hides messages from the campaign UI
- No special workflow or board assignment needed

### Verified via Postman
- `GET https://api.oktopost.com/v2/message?campaignId=002g5m4amrtu2xs` returns **200 OK** with 27 items (25.65 KB response, 428ms)
- Response includes full message objects with Id, Created, Modified, Status, Type, Network, Message content, and all metadata fields

### Resolved
- **API `campaignId` filter confirmed working** — Original issue was a typo, not a bug
- **`IsAppMessage: 1` clarified** — Normal behaviour, no visibility impact
- **Integration status: Blocked -> Active** across all project docs

### Updated Files
- `WORKSPACE.md` — Oktopost status: Blocked -> Active
- `memory/research/oktopost-ui-issue.md` — Marked RESOLVED with full support response
- `memory/research/oktopost-support-email.md` — Added Jason's response and resolution
- `memory/research/bluprintx-oktopost-integration.md` — Added API notes, updated status
- `memory/daily/2026-02-01.md` — Marked Oktopost blocker as resolved
- `memory/briefings/2026-02-05-morning-briefing-DEEP-DIVE.md` — Marked resolved
- `scripts/social/oktopost-post-ui.js` — Updated comment (API works, UI automation is fallback)

### New Documentation
- `docs/oktopost-integration/README.md` — Quick start guide
- `docs/oktopost-integration/PRD.md` — Full product requirements
- `docs/oktopost-integration/ROADMAP.md` — 6-phase development roadmap
- `docs/oktopost-integration/CHANGELOG.md` — This file
- `memory/daily/2026-02-20.md` — Daily log entry

### Still Open
- DELETE endpoint needs re-testing (reported as returning success without actually deleting, not addressed by support)

---

## [1.0.0] - 2026-02-01 - Initial Integration

### Added
- `scripts/social/post-to-oktopost.py` — Post content to Oktopost as drafts (single, CSV, interactive modes)
- `scripts/social/generate-and-post.py` — Generate full week of BluprintX content and post to Oktopost
- `scripts/social/list-oktopost-drafts.sh` — List current Oktopost drafts by campaign
- `scripts/social/oktopost-post-ui.js` — Playwright-based UI automation (created as workaround for suspected API bug)
- `memory/research/bluprintx-oktopost-integration.md` — Integration documentation
- `memory/research/oktopost-ui-issue.md` — Issue tracker for API problems
- `memory/research/oktopost-support-email.md` — Support correspondence

### Configuration
- Account: Bluprintx (001kzy8780tsd6r)
- Default Campaign: AI Value Accelerator (002g5m4amrtu2xs)
- Auth: Basic Auth (Account ID + API Key)
- Credentials: `~/.clawdbot/oktopost_credentials.json`
- Networks: LinkedIn, Instagram, Twitter

### Known Issues (at time of release)
- `campaignId` filter appeared to return 0 results (later resolved Feb 20 — was a typo)
- DELETE API appeared to return success without deleting (still under investigation)
- Created Playwright UI fallback script as workaround (no longer needed for primary use)
