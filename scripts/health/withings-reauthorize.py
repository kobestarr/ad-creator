#!/usr/bin/env python3
"""
Withings OAuth 2.0 Re-authorization Helper
Generates authorization URL and exchanges code for tokens
"""
import json
import requests
import os
import hmac
import hashlib
import time
import urllib.parse
from datetime import datetime

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
    """Get nonce from Withings API"""
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

def generate_auth_url(client_id, redirect_uri, state='withings_auth'):
    """Generate OAuth 2.0 authorization URL"""
    base_url = 'https://account.withings.com/oauth2_user/authorize2'
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': 'user.metrics,user.activity',
        'redirect_uri': redirect_uri,
        'state': state
    }
    return f'{base_url}?{urllib.parse.urlencode(params)}'

def exchange_code_for_tokens(client_id, client_secret, code, redirect_uri):
    """Exchange authorization code for access and refresh tokens"""
    # Get nonce first
    nonce = get_nonce(client_id, client_secret)
    if not nonce:
        print('ERROR: Failed to get nonce')
        return None
    
    timestamp = str(int(time.time()))
    
    # Signature: action,client_id,nonce (alphabetically sorted)
    sig_parts = ['requesttoken', client_id, nonce]
    sig_string = ','.join(sig_parts)
    signature = hmac.new(client_secret.encode(), sig_string.encode(), hashlib.sha256).hexdigest()
    
    params = {
        'action': 'requesttoken',
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
        'nonce': nonce,
        'timestamp': timestamp,
        'signature': signature
    }
    
    # Remove client_secret from request (not sent)
    request_params = {k: v for k, v in params.items() if k != 'client_secret'}
    
    response = requests.post('https://wbsapi.withings.net/v2/oauth2', data=request_params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 0:
            return data.get('body', {})
    
    print(f'ERROR: {response.status_code} - {response.text[:200]}')
    return None

def main():
    client_id = get_env_var('WITHINGS_CLIENT_ID')
    client_secret = get_env_var('WITHINGS_CLIENT_SECRET')
    
    if not all([client_id, client_secret]):
        print('ERROR: Missing client credentials')
        return
    
    print('\n=== Withings OAuth 2.0 Re-authorization ===\n')
    
    # Get redirect URI (common defaults)
    redirect_uri = input('Enter your redirect_uri (e.g., http://localhost:3000 or https://yourdomain.com/callback): ').strip()
    if not redirect_uri:
        redirect_uri = 'http://localhost:3000'
        print(f'Using default: {redirect_uri}')
    
    # Generate authorization URL
    auth_url = generate_auth_url(client_id, redirect_uri)
    print(f'\n1. Open this URL in your browser:\n\n{auth_url}\n')
    print('2. Authorize the application')
    print('3. After authorization, you will be redirected to your redirect_uri')
    print('4. Copy the "code" parameter from the redirect URL\n')
    
    code = input('Enter the authorization code from the redirect URL: ').strip()
    
    if not code:
        print('ERROR: No authorization code provided')
        return
    
    print('\nExchanging code for tokens...')
    tokens = exchange_code_for_tokens(client_id, client_secret, code, redirect_uri)
    
    if tokens:
        # Save tokens
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
    else:
        print('\n❌ Failed to exchange code for tokens')

if __name__ == '__main__':
    main()
