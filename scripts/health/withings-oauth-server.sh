#!/bin/bash
# Withings OAuth Server - Captures code automatically

echo "🌐 Starting Withings OAuth Server..."
echo "1. Opening authorization URL..."
echo ""

# Generate auth URL
AUTH_URL=$(/root/clawd/scripts/withings.sh auth-url 2>/dev/null | grep "https://" | head -1)

echo "Auth URL: $AUTH_URL"
echo ""
echo "2. Starting callback server on port 8888..."
echo ""

# Start a simple server to capture the callback
# The server will write the code to a file when received

cat > /tmp/withings_server.py << 'PYEOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import sys

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if 'code' in params:
            code = params['code'][0]
            with open('/tmp/withings_code.txt', 'w') as f:
                f.write(code)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authorization Complete!</h1><p>Code captured. You can close this.</p></body></html>")
            sys.exit(0)

server = HTTPServer(('localhost', 8888), Handler)
print("Server running on http://localhost:8888")
server.handle_request()
PYEOF

python3 /tmp/withings_server.py &
SERVER_PID=$!
sleep 1

echo "3. Please visit this URL NOW:"
echo ""
echo "$AUTH_URL"
echo ""
echo "4. Authorize quickly (30 seconds)"
echo ""
echo "5. The code will be captured automatically"
echo ""
echo "Waiting for authorization..."

# Wait for code file
TIMEOUT=0
while [ ! -f /tmp/withings_code.txt ] && [ $TIMEOUT -lt 35 ]; do
    sleep 1
    TIMEOUT=$((TIMEOUT + 1))
done

if [ -f /tmp/withings_code.txt ]; then
    CODE=$(cat /tmp/withings_code.txt)
    echo ""
    echo "✅ Code received: $CODE"
    echo ""
    /root/clawd/scripts/withings.sh complete_auth "$CODE"
else
    echo "❌ Timeout - code expired"
fi

kill $SERVER_PID 2>/dev/null
