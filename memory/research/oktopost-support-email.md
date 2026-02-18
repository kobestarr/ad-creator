# Oktopost Support Email - API Issues

---

**Subject:** Multiple API Bugs - Messages Created Via API Not Visible, Delete Returns Success But Doesn't Delete

---

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

**Impact:**
- Messages are created successfully via API
- But cannot be listed by campaign
- This means API-created messages don't appear in the campaign message UI
- I cannot build automation around listing/managing campaign messages

---

**ISSUE #2: Delete API Returns Success But Doesn't Delete Messages**

When I try to delete a message, the API returns success but the message still exists.

**Steps to Reproduce:**

1. Create a test message (ID: 005uknajp2x6f7j)
```
POST https://api.oktopost.com/v2/message
campaignId=002g5m4amrtu2xs
network=LinkedIn
message="Test delete"

Response: {"Result":true,"Message":{"Id":"005uknajp2x6f7j"}}
```

2. Try to delete the message:
```
DELETE https://api.oktopost.com/v2/message/005uknajp2x6f7j

Response: {"Result":true}
```

3. Verify if deleted - MESSAGE STILL EXISTS:
```
GET https://api.oktopost.com/v2/message?ids=005uknajp2x6f7j

Response: {"Result":true,"Items":[{"Id":"005uknajp2x6f7j","CampaignId":"002g5m4amrtu2xs","Network":"LinkedIn","Message":"Test delete"}],"Total":1}
```

**Impact:**
- Delete API appears to work (returns success)
- But messages are NOT actually deleted
- This causes test messages to accumulate
- I cannot clean up test data

---

**Additional Observations:**

- Messages created via API have `IsAppMessage: 1` flag
- Messages created via UI have `IsAppMessage: 0` flag
- This flag might be affecting visibility or behavior

---

**Questions:**

1. Is the `campaignId` filter on `/v2/message` broken?
2. Why does the Delete API return success but not actually delete messages?
3. Is the `IsAppMessage` flag causing messages to be filtered or hidden?
4. Is there a different endpoint I should use for listing API-created messages?
5. Are messages and posts different entities that require different API calls?

I've been testing this for several hours and the behavior is consistent. I'm happy to provide more details, do a screenshare, or jump on a call.

Thanks for your help,
Kobi
Bluprintx
kobi.omenaka@bluprintx.com

