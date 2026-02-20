# Oktopost UI/API Issue

## Problem
API-created messages didn't appear in Oktopost UI campaign message view.

## Root Cause
**RESOLVED (Feb 20, 2026)** — Oktopost support (Jason) confirmed the `campaignId` filter works correctly. The original issue was likely a typo or transient problem on our end. Support tested the same endpoint and retrieved 27 messages successfully.

## Original Symptoms
- `/v2/message?campaignId=xxx` → Returned 0 messages
- `/v2/message?ids=xxx` → Returned messages correctly

## Resolution
Contacted Oktopost support. Jason confirmed:
1. **`campaignId` filter works** — required parameter for listing messages
2. **`IsAppMessage: 1` has no effect** on API visibility. Only `IsAppMessage: 0` + `IsBoardMessage: 1` affects UI visibility
3. **No special workflow/board needed** — messages should appear automatically
4. **`_count` alone won't work** — `campaignId` is mandatory when listing messages
5. **Alternative ID lookup:** `https://api.oktopost.com/v2/message/005000000000000` (ID in URL path)

## Status: RESOLVED
- ✅ Messages created via API work correctly
- ✅ Messages can be retrieved by ID
- ✅ Messages can be listed by campaign (`campaignId` filter works)
- ✅ API-created messages visible in UI

## API Reference (Confirmed Working)
```
# Create message
POST https://api.oktopost.com/v2/message
  campaignId=xxx&network=LinkedIn&message=xxx

# List by campaign (REQUIRED)
GET https://api.oktopost.com/v2/message?campaignId=xxx

# Get by ID (two methods)
GET https://api.oktopost.com/v2/message?ids=005xxx
GET https://api.oktopost.com/v2/message/005xxx
```

---

*Documented: 2026-02-01*
*Resolved: 2026-02-20*
