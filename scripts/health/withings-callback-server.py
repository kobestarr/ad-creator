#!/usr/bin/env python3
# Simple HTTP server to capture Withings OAuth callback
# Run this, then visit auth URL, and the code will be captured automatically

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import sys

# Get the authorization URL from the bash script
import subprocess
result = subprocess.run(['/root/clawd/scripts/withings.sh', 'auth-url'], capture_output=True, text=True)
auth_url = None
for line in result.stdout.split('\n'):
    if 'https://account.withings.com' in line:
        auth_url = line.strip()
        break

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        
        if 'code' in params:
            code = params['code'][0]
            print(f"\n✅ AUTHORIZATION CODE RECEIVED:")
            print(f"{code}")
            print(f"\n📋 Now run:")
            print(f"/root/clawd/scripts/withings.sh complete_auth {code}")
            
            # Also save to file for automation
            with open('/tmp/withings_code.txt', 'w') as f:
                f.write(code)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authorization complete!</h1><p>Code captured. You can close this window.</p></body></html>")
            
            # Exit after capturing
            sys.exit(0)
        else:
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logging

if __name__ == '__main__':
    if not auth_url:
        print("❌ Could not generate auth URL")
        sys.exit(1)
    
    print("🌐 Withings OAuth Callback Server")
    print("=" * 40)
    print(f"\n1. Visit this URL:")
    print(f"{auth_url}")
    print(f"\n2. Authorize (you have ~30 seconds!)")
    print(f"\n3. Code will be captured automatically...")
    print(f"\n4. Then run:")
    print(f"/root/clawd/scripts/withings.sh complete_auth <code>")
    print(f"\n🚀 Starting server on http://localhost:8080...")
    
    server = HTTPServer(('localhost', 8080), CallbackHandler)
    server.handle_request()  # Handle one request then exit
