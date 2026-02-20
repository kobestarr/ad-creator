# Oktopost Support Email - API Issues

## Status: RESOLVED (Feb 20, 2026)

---

**Subject:** Multiple API Bugs - Messages Created Via API Not Visible, Delete Returns Success But Doesn't Delete

---

### Email Sent (Feb 1, 2026)

Hi Oktopost Support,

I'm trying to automate posting content to Oktopost using your API and have discovered multiple issues I can't find documented anywhere.

**What I'm Trying to Do:**

I'm building an automation system for Bluprintx that generates social media content and posts it to Oktopost as drafts for manual review.

**My Setup:**
- Account: Bluprintx (Account ID: 001kzy8780tsd6r)
- Campaign: "AI Value Accelerator" (Campaign ID: 002g5m4amrtu2xs)
- Using Basic Auth with Account ID and API key

---

**ISSUE #1: Cannot List Messages by Campaign**

When I create messages via the API, they appear to be created successfully. However, I cannot list these messages by campaign - the endpoint returns 0 messages even when messages exist.

**Steps to Reproduce:**

1. Create a message:
```
POST https://api.oktopost.com/v2/message
campaignId=002g5m4amrtu2xs
network=LinkedIn
message="Test message"

Response: {"Result":true,"Message":{"Id":"005xxx","CampaignId":"002g5m4amrtu2xs","Status":"default"}}
```

2. Try to list messages by campaign:
```
GET https://api.oktopost.com/v2/message?campaignId=002g5m4amrtu2xs&_count=100

Response: {"Result":true,"Items":[],"Total":0}
```

3. Try to list ALL messages:
```
GET https://api.oktopost.com/v2/message?_count=100

Response: {"Result":false,"Errors":{"api":{"message":"You must send either of the mandatory parameters: campaignId\\ids"}}}
```

4. HOWEVER, I CAN retrieve the message by ID:
```
GET https://api.oktopost.com/v2/message?ids=005xxx

Response: {"Result":true,"Items":[{"Id":"005xxx","CampaignId":"002g5m4amrtu2xs","Network":"LinkedIn","Status":"default","IsAppMessage":1}],"Total":1}
```

---

**ISSUE #2: Delete API Returns Success But Doesn't Delete Messages**

When I try to delete a message, the API returns success but the message still exists.

---

### Support Response (Jason @ Oktopost, Feb 20, 2026)

**On campaignId filter returning 0 results:**
> "I'm not sure why you're not getting any results. I tested it on my end, and it's showing me 27 Messages. Are you sure there isn't a typo somewhere on your end?"

**On `_count` alone not working:**
> "This endpoint requires the CampaignId parameter to list Messages, so this doesn't surprise me."

**On `IsAppMessage: 1`:**
> "It only has visibility constraints if that's 0 and 'IsBoardMessage: 1' and only in the Oktopost UI for the Campaign."

**Answers to specific questions:**
1. **campaignId filter works** — it is required to list messages. Alternative: message ID in URL path (`/v2/message/005xxx`)
2. **Messages should show in UI** — likely was a typo causing the original issue
3. **IsAppMessage: 1 does NOT affect API visibility**
4. **No different endpoint needed**
5. **No workflow/board assignment needed**

---

### Resolution

The `campaignId` filter works as expected. The original issue was likely a typo or transient problem. Confirmed working via Postman with 200 OK response returning items.

**Integration status changed:** Blocked → Active

---

*Email sent: 2026-02-01*
*Response received: 2026-02-20*
*Status: RESOLVED*
