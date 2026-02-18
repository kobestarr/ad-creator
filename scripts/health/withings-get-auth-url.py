#!/usr/bin/env python3
"""
Generate Withings authorization URL with custom redirect_uri
Usage: python3 withings-get-auth-url.py <redirect_uri>
"""
import urllib.parse
import sys
import os

ENV_FILE = '/root/.credentials/.env'

def get_env_var(key):
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if line.startswith(f'{key}='):
                    return line.split('=', 1)[1].strip()
    return os.getenv(key)

if __name__ == '__main__':
    client_id = get_env_var('WITHINGS_CLIENT_ID')
    
    if len(sys.argv) < 2:
        print('Usage: python3 withings-get-auth-url.py <redirect_uri>')
        print('\nCommon redirect URIs:')
        print('  - http://localhost:3000')
        print('  - http://localhost:8080')
        print('  - https://yourdomain.com/callback')
        print('  - urn:ietf:wg:oauth:2.0:oob (for manual copy-paste)')
        print('\nThe redirect_uri MUST match what is configured in your Withings Developer Dashboard.')
        print('Check: https://developer.withings.com/dashboard/')
        sys.exit(1)
    
    redirect_uri = sys.argv[1]
    base_url = 'https://account.withings.com/oauth2_user/authorize2'
    
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': 'user.metrics,user.activity',
        'redirect_uri': redirect_uri,
        'state': 'withings_auth'
    }
    
    auth_url = f'{base_url}?{urllib.parse.urlencode(params)}'
    
    print('\n' + '='*70)
    print('WITHINGS AUTHORIZATION URL')
    print('='*70)
    print(f'\nRedirect URI: {redirect_uri}')
    print(f'\nAuthorization URL:\n')
    print(auth_url)
    print('\n' + '='*70)
    print('\nAfter authorization, you will be redirected to:')
    print(f'{redirect_uri}?code=XXXXX&state=withings_auth')
    print('\nCopy the code and run:')
    print(f'python3 /root/clawd/scripts/withings-exchange-code.py <code> {redirect_uri}')
