# Oktopost Integration - Changelog

## [1.1.0] - 2026-02-20 - API Unblocked

### Resolved
- **API `campaignId` filter now confirmed working** - Oktopost support (Jason) confirmed the `/v2/message?campaignId=xxx` endpoint works correctly. Original issue was likely a typo or transient problem on our end.
- **`IsAppMessage: 1` clarified** - Has no effect on API visibility. Only `IsAppMessage: 0` + `IsBoardMessage: 1` affects UI visibility in campaigns.
- **Integration status changed from Blocked to Active** across all project docs.

### Updated
- `WORKSPACE.md` - Oktopost status: Blocked -> Active
- `memory/research/oktopost-ui-issue.md` - Marked as RESOLVED with support response details
- `memory/research/oktopost-support-email.md` - Added full support response from Jason
- `memory/research/bluprintx-oktopost-integration.md` - Added API notes from support, updated status
- `memory/daily/2026-02-01.md` - Marked Oktopost blocker as resolved
- `memory/briefings/2026-02-05-morning-briefing-DEEP-DIVE.md` - Marked Oktopost as resolved
- `scripts/social/oktopost-post-ui.js` - Updated comment (no longer "bypasses broken API")

### API Learnings (from Oktopost Support)
- `campaignId` is **required** when listing messages via `/v2/message`
- No global message list endpoint exists (must filter by campaign or IDs)
- Two ways to get a message by ID:
  - `GET /v2/message?ids=005xxx`
  - `GET /v2/message/005xxx`
- Delete endpoint still needs investigation (reported as returning success without actually deleting)

---

## [1.0.0] - 2026-02-01 - Initial Integration

### Added
- `scripts/social/post-to-oktopost.py` - Post content to Oktopost as drafts (single, CSV, interactive modes)
- `scripts/social/generate-and-post.py` - Generate full week of BluprintX content and post to Oktopost
- `scripts/social/list-oktopost-drafts.sh` - List current Oktopost drafts by campaign
- `scripts/social/oktopost-post-ui.js` - Playwright-based UI automation (fallback method)
- `memory/research/bluprintx-oktopost-integration.md` - Integration documentation
- `memory/research/oktopost-ui-issue.md` - Issue tracker for API problems
- `memory/research/oktopost-support-email.md` - Support correspondence

### Configuration
- Account: Bluprintx (001kzy8780tsd6r)
- Default Campaign: AI Value Accelerator (002g5m4amrtu2xs)
- Auth: Basic Auth (Account ID + API Key)
- Credentials: `~/.clawdbot/oktopost_credentials.json`
- Networks: LinkedIn, Instagram, Twitter

### Known Issues (at time of release)
- `campaignId` filter appeared to return 0 results (later resolved - was likely a typo)
- Delete API appeared to return success without deleting (still under investigation)
