# Oktopost UI/API Issue

## Problem
API-created messages don't appear in Oktopost UI campaign message view.

## Root Cause
Oktopost's `/v2/message` endpoint has a broken `campaignId` filter:
- `/v2/message?campaignId=xxx` → Returns 0 messages (BROKEN)
- `/v2/message?ids=xxx` → Returns messages correctly (WORKAROUND)

Messages ARE being created successfully, but cannot be listed by campaign via API or UI.

## Status
- ✅ Messages created via API work correctly
- ✅ Messages can be retrieved by ID
- ❌ Messages cannot be listed by campaign
- ❌ UI doesn't show API-created messages

## Workaround
1. Store message IDs when created
2. Retrieve by ID when needed: `/v2/message?ids=005xxx`
3. Contact Oktopost support about the campaignId filter bug

## Contact Oktopost Support
Report: "API-created messages don't appear in campaign message view. The /v2/message?campaignId endpoint returns 0 messages even when messages exist for that campaign. Messages can only be retrieved via /v2/message?ids=xxx"

## Impact
- Cannot list all messages in a campaign via API
- Cannot view API-created messages in standard UI view
- Manual workaround required (store IDs, retrieve by ID)

---

*Documented: 2026-02-01*
