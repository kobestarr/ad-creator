#!/usr/bin/env python3
"""
Exchange Withings authorization code for tokens
Usage: python3 withings-exchange-code.py <authorization_code> [redirect_uri]
"""
import json
import requests
import os
import sys
import hmac
import hashlib
import time

CREDENTIALS_FILE = '/root/.credentials/withings.json'
ENV_FILE = '/root/.credentials/.env'

def get_env_var(key):
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if line.startswith(f'{key}='):
                    return line.split('=', 1)[1].strip()
    return os.getenv(key)

def get_nonce(client_id, client_secret):
    timestamp = str(int(time.time()))
    sig_string = f'getnonce,{client_id},{timestamp}'
    signature = hmac.new(client_secret.encode(), sig_string.encode(), hashlib.sha256).hexdigest()
    
    params = {
        'action': 'getnonce',
        'client_id': client_id,
        'timestamp': timestamp,
        'signature': signature
    }
    
    response = requests.post('https://wbsapi.withings.net/v2/signature', data=params, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 0:
            return data.get('body', {}).get('nonce')
    return None

def exchange_code_for_tokens(client_id, client_secret, code, redirect_uri):
    nonce = get_nonce(client_id, client_secret)
    if not nonce:
        print('ERROR: Failed to get nonce')
        return None
    
    timestamp = str(int(time.time()))
    sig_parts = ['requesttoken', client_id, nonce]
    sig_string = ','.join(sig_parts)
    signature = hmac.new(client_secret.encode(), sig_string.encode(), hashlib.sha256).hexdigest()
    
    params = {
        'action': 'requesttoken',
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'code': code,
        'redirect_uri': redirect_uri,
        'nonce': nonce,
        'timestamp': timestamp,
        'signature': signature
    }
    
    response = requests.post('https://wbsapi.withings.net/v2/oauth2', data=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 0:
            return data.get('body', {})
    
    print(f'ERROR: {response.status_code} - {response.text}')
    return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 withings-exchange-code.py <authorization_code> [redirect_uri]')
        print('Example: python3 withings-exchange-code.py abc123 http://localhost:3000')
        sys.exit(1)
    
    code = sys.argv[1]
    redirect_uri = sys.argv[2] if len(sys.argv) > 2 else 'http://localhost:3000'
    
    client_id = get_env_var('WITHINGS_CLIENT_ID')
    client_secret = get_env_var('WITHINGS_CLIENT_SECRET')
    
    if not all([client_id, client_secret]):
        print('ERROR: Missing client credentials')
        sys.exit(1)
    
    print('Exchanging authorization code for tokens...')
    tokens = exchange_code_for_tokens(client_id, client_secret, code, redirect_uri)
    
    if tokens:
        creds = {
            'access_token': tokens.get('access_token'),
            'refresh_token': tokens.get('refresh_token'),
            'expires_in': tokens.get('expires_in', 10800),
            'user_id': tokens.get('userid', '14711398')
        }
        
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(creds, f, indent=2)
        
        print('\n✅ SUCCESS! Tokens saved to credentials file')
        print(f'   Access token expires in: {creds["expires_in"]/3600:.1f} hours')
        print(f'   User ID: {creds["user_id"]}')
        print(f'   Refresh token: {creds["refresh_token"][:20]}...')
    else:
        print('\n❌ Failed to exchange code for tokens')
        sys.exit(1)
