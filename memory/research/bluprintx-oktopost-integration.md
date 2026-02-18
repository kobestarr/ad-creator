# BluprintX → Oktopost Integration

## Connected ✅

| Field | Value |
|-------|-------|
| Account ID | 001kzy8780tsd6r |
| Account Name | Bluprintx |
| Status | Connected |
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

---

*Created: 2026-02-01*
