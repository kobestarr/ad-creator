#!/bin/bash
# Withings OAuth & Data Fetch Module
# Handles token refresh and data retrieval

CREDENTIALS_FILE="/root/.credentials/withings.json"
CLIENT_ID="6559b3aa742396c378c962301ca2dd54818e31d62c386c9a6131135094d3b718"
CLIENT_SECRET="26489fd97bb9b2d494898ac7a2f720a93b16e69a139fa45a2add37a201b9260d"
API_BASE="https://wbsapi.withings.net"

# Load credentials
load_credentials() {
  if [ -f "$CREDENTIALS_FILE" ]; then
    ACCESS_TOKEN=$(cat "$CREDENTIALS_FILE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
    REFRESH_TOKEN=$(cat "$CREDENTIALS_FILE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('refresh_token',''))")
    USER_ID=$(cat "$CREDENTIALS_FILE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('user_id',''))")
  fi
}

# Save credentials
save_credentials() {
  local access_token="$1"
  local refresh_token="$2"
  local user_id="$3"
  local expires_in="$4"
  
  cat > "$CREDENTIALS_FILE" << EOF
{
  "access_token": "$access_token",
  "refresh_token": "$refresh_token",
  "user_id": "$user_id",
  "expires_in": $expires_in,
  "saved_at": $(date +%s)
}
EOF
  echo "✅ Credentials saved"
}

# Check if token is expired
is_token_expired() {
  local saved_at=$(cat "$CREDENTIALS_FILE" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('saved_at',0))" 2>/dev/null || echo "0")
  local expires_in=$(cat "$CREDENTIALS_FILE" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('expires_in',10800))" 2>/dev/null || echo "10800")
  
  local now=$(date +%s)
  local expires_at=$((saved_at + expires_in))
  
  if [ "$now" -ge "$expires_at" ]; then
    return 0  # expired
  else
    return 1  # not expired
  fi
}

# Refresh token
refresh_token() {
  echo "🔄 Refreshing Withings token..."
  
  if [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_SECRET" ]; then
    echo "❌ Client credentials not configured"
    echo "📋 To fix:"
    echo "   1. Go to https://developer.withings.com"
    echo "   2. Create/select your app"
    echo "   3. Copy client_id and client_secret"
    echo "   4. Edit /root/clawd/scripts/withings.sh and fill in credentials"
    return 1
  fi
  
  RESPONSE=$(curl -s -X POST "$API_BASE/v2/oauth2" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "action=requesttoken" \
    -d "grant_type=refresh_token" \
    -d "client_id=$CLIENT_ID" \
    -d "client_secret=$CLIENT_SECRET" \
    -d "refresh_token=$REFRESH_TOKEN")
  
  STATUS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',999))" 2>/dev/null)
  
  if [ "$STATUS" -eq 0 ]; then
    NEW_ACCESS_TOKEN=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
    NEW_REFRESH_TOKEN=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('refresh_token',''))")
    NEW_EXPIRES_IN=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('expires_in',10800))")
    NEW_USER_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('userid',$USER_ID))")
    
    save_credentials "$NEW_ACCESS_TOKEN" "$NEW_REFRESH_TOKEN" "$NEW_USER_ID" "$NEW_EXPIRES_IN"
    echo "✅ Token refreshed successfully"
    ACCESS_TOKEN="$NEW_ACCESS_TOKEN"
    return 0
  else
    echo "❌ Token refresh failed: $RESPONSE"
    return 1
  fi
}

# Get weight data
get_weight() {
  load_credentials
  
  if [ -z "$ACCESS_TOKEN" ]; then
    echo "⚠️ No credentials. Re-authentication needed."
    echo "📋 Run: /root/clawd/scripts/withings.sh reauth"
    return 1
  fi
  
  # Check if expired
  if is_token_expired; then
    refresh_token || return 1
  fi
  
  # Fetch weight (last 30 days)
  START_DATE=$(date -d "30 days ago" +%Y-%m-%d)
  END_DATE=$(date +%Y-%m-%d)
  
  RESPONSE=$(curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
    "$API_BASE/v2/measure?action=getmeas&startdateymd=$START_DATE&enddateymd=$END_DATE&userid=$USER_ID")
  
  STATUS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',999))" 2>/dev/null)
  
  if [ "$STATUS" -eq 0 ]; then
    # Parse weight (type=1 for kg)
    WEIGHT=$(echo "$RESPONSE" | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('body',{}).get('measuregrps'):
    for m in d['body']['measuregrps']:
        for measure in m.get('measures',[]):
            if measure.get('type') == 1:  # weight in kg
                value=measure['value']
                unit=measure.get('unit',0)
                print(value / (10 ** unit))
                sys.exit(0)
    print('N/A')
else:
    print('N/A')
" 2>/dev/null)
    
    if [ "$WEIGHT" != "N/A" ]; then
      echo "${WEIGHT}kg"
    else
      echo "N/A (no weight data)"
    fi
  elif [ "$STATUS" -eq 401 ] || [ "$STATUS" -eq 277 ]; then
    # Token expired, try refresh
    refresh_token && get_weight
  else
    echo "❌ API error (status $STATUS)"
  fi
}

# Generate auth URL for re-authentication
generate_auth_url() {
  if [ -z "$CLIENT_ID" ]; then
    echo "❌ Client ID not configured"
    return 1
  fi
  
  local redirect_uri=$(python3 -c "import urllib.parse; print(urllib.parse.quote('http://localhost/callback'))")
  local state=$(date +%s)
  
  echo "🔗 Authorize at:"
  echo "https://account.withings.com/oauth2_user/authorize2?response_type=code&client_id=$CLIENT_ID&scope=user.metrics&redirect_uri=$redirect_uri&state=$state"
  echo ""
  echo "After auth, run: $0 complete_auth <authorization_code>"
}

# Complete OAuth flow
complete_auth() {
  local code="$1"
  
  if [ -z "$code" ]; then
    echo "Usage: $0 complete_auth <authorization_code>"
    return 1
  fi
  
  RESPONSE=$(curl -s -X POST "$API_BASE/v2/oauth2" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "action=requesttoken" \
    -d "grant_type=authorization_code" \
    -d "client_id=$CLIENT_ID" \
    -d "client_secret=$CLIENT_SECRET" \
    -d "code=$code" \
    -d "redirect_uri=http://localhost/callback")
  
  STATUS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',999))")
  
  if [ "$STATUS" -eq 0 ]; then
    ACCESS_TOKEN=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
    REFRESH_TOKEN=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('refresh_token',''))")
    EXPIRES_IN=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('expires_in',10800))")
    USER_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('userid',''))")
    
    save_credentials "$ACCESS_TOKEN" "$REFRESH_TOKEN" "$USER_ID" "$EXPIRES_IN"
    echo "✅ Authentication complete!"
  else
    echo "❌ Auth failed: $RESPONSE"
  fi
}

# Run command
case "${1:-get_weight}" in
  refresh)
    refresh_token
    ;;
  auth-url)
    generate_auth_url
    ;;
  complete_auth)
    complete_auth "$2"
    ;;
  reauth)
    generate_auth_url
    ;;
  get_weight)
    get_weight
    ;;
  *)
    echo "Usage: $0 {refresh|auth-url|complete_auth|reauth|get_weight}"
    ;;
esac
