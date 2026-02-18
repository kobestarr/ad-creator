#!/bin/bash
# List all Oktopost drafts for AI Value Accelerator campaign

ACCOUNT_ID="001kzy8780tsd6r"
API_KEY="7eb1835c181a410318218ed488c3b3366880fa3cab61e2.8211728517532831326880fa3cab6250.41127073"

echo "=== OKTOPOST DRAFTS - AI VALUE ACCELERATOR ==="
echo ""
curl -s -u "$ACCOUNT_ID:$API_KEY" \
  "https://api.oktopost.com/v2/message?campaignId=002g5m4amrtu2xs&_count=50" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Total drafts: {data.get(\"Total\", 0)}\n')
for item in data.get('Items', []):
    created = item.get('Created', 'Unknown')[:10]
    network = item.get('Network', 'Unknown')
    status = item.get('Status', 'Unknown')
    msg_id = item.get('Id', 'Unknown')
    preview = item.get('Message', 'No message')[:60].replace(chr(10), ' ')
    print(f'{created} | {network:10} | {status:8} | {msg_id}')
    print(f'  {preview}...')
    print()
"

echo ""
echo "=== DIRECT LINK TO MANAGE (use API) ==="
echo "Message IDs above can be retrieved/modified via API."
echo "Check Oktopost UI at: https://app.oktopost.com/campaign"
