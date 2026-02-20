# BluprintX → Oktopost Integration

## Connected & API Confirmed Working ✅

| Field | Value |
|-------|-------|
| Account ID | 001kzy8780tsd6r |
| Account Name | Bluprintx |
| API Status | Active (confirmed Feb 20, 2026) |
| Auth Method | Basic Auth (Account ID + API Key) |
| Default Campaign | AI Value Accelerator (002g5m4amrtu2xs) |

## Available Campaigns

| Campaign ID | Name |
|-------------|------|
| 002g5m4amrtu2xs | AI Value Accelerator |
| 002586p3bofvpua | 2026-01 Native Posts |
| 002yfxw3pc8r77l | 2025-12 Native Posts |
| ... | (more campaigns available) |

## Scripts

### Post Single Message
```bash
python3 /root/clawd/scripts/post-to-oktopost.py \
  --text "Your post content here" \
  --network LinkedIn \
  --campaign 002g5m4amrtu2xs
```

### Post from CSV (Claude's content table)
```bash
python3 /root/clawd/scripts/post-to-oktopost.py \
  --csv content_table.csv \
  --campaign 002g5m4amrtu2xs
```

### Interactive Mode
```bash
python3 /root/clawd/scripts/post-to-oktopost.py --interactive
```

## Workflow

1. **Claude skill** generates content table (24 posts/week)
2. **Export CSV** from Claude's output
3. **Run script** to post all as drafts
4. **Review** in Oktopost
5. **Publish** manually when ready

## Networks Supported
- LinkedIn ✅
- Instagram ✅
- Twitter ✅

## Key Features
- All posts saved as **DRAFTS** (never live)
- Supports multiple networks
- Maps platform from Claude's table to Oktopost network
- Adds leader name prefix for personal posts (Phil, AT, Lee)

## API Notes (from Oktopost Support, Feb 2026)

- `campaignId` is **required** when listing messages — no global list endpoint
- `IsAppMessage: 1` = created for app use, no visibility impact on API
- Only `IsAppMessage: 0` + `IsBoardMessage: 1` has visibility constraints in UI
- Alternative ID lookup: `/v2/message/005xxx` (ID in URL path)
- Delete endpoint needs further testing (was reported as returning success without deleting)

---

*Created: 2026-02-01*
*Updated: 2026-02-20 — API confirmed working, integration unblocked*
