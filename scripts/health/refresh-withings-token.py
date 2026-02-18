#!/usr/bin/env python3
"""
Refresh Withings Token - Robust Version
Withings OAuth 2.0 requires HMAC SHA-256 signatures
Uses correct /v2/signature endpoint for getnonce
"""
import json
import requests
import os
import hmac
import hashlib
import time
from datetime import datetime

CREDENTIALS_FILE = '/root/.credentials/withings.json'
ENV_FILE = '/root/.credentials/.env'
LOG_FILE = '/var/log/withings-token-refresh.log'
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f'[{timestamp}] {message}\n'
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg)
    print(log_msg.strip())

def get_env_var(key):
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if line.startswith(f'{key}='):
                    return line.split('=', 1)[1].strip()
    return os.getenv(key)

def get_nonce(client_id, client_secret, retry_count=0):
    """Get nonce from Withings API - CORRECT ENDPOINT: /v2/signature"""
    try:
        timestamp = str(int(time.time()))
        # Signature: action,client_id,timestamp (comma-separated)
        sig_string = f'getnonce,{client_id},{timestamp}'
        signature = hmac.new(client_secret.encode(), sig_string.encode(), hashlib.sha256).hexdigest()
        
        params = {
            'action': 'getnonce',
            'client_id': client_id,
            'timestamp': timestamp,
            'signature': signature
        }
        
        # CORRECT ENDPOINT: /v2/signature (POST, not GET)
        response = requests.post('https://wbsapi.withings.net/v2/signature', data=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 0:
                nonce = data.get('body', {}).get('nonce')
                if nonce:
                    log(f'Got nonce successfully: {nonce[:10]}...')
                    return nonce
                else:
                    log(f'ERROR: No nonce in response: {json.dumps(data)}')
            else:
                error = data.get('error', 'Unknown')
                log(f'getnonce API error: status {data.get("status")}, error: {error}')
                if retry_count < MAX_RETRIES:
                    log(f'Retrying getnonce ({retry_count + 1}/{MAX_RETRIES})...')
                    time.sleep(RETRY_DELAY * (retry_count + 1))
                    return get_nonce(client_id, client_secret, retry_count + 1)
        else:
            log(f'getnonce HTTP {response.status_code}: {response.text[:200]}')
            if retry_count < MAX_RETRIES:
                log(f'Retrying getnonce ({retry_count + 1}/{MAX_RETRIES})...')
                time.sleep(RETRY_DELAY * (retry_count + 1))
                return get_nonce(client_id, client_secret, retry_count + 1)
        return None
    except requests.exceptions.RequestException as e:
        log(f'Network error getting nonce: {str(e)}')
        if retry_count < MAX_RETRIES:
            log(f'Retrying getnonce ({retry_count + 1}/{MAX_RETRIES})...')
            time.sleep(RETRY_DELAY * (retry_count + 1))
            return get_nonce(client_id, client_secret, retry_count + 1)
        return None
    except Exception as e:
        log(f'Unexpected error getting nonce: {str(e)}')
        import traceback
        log(traceback.format_exc())
        return None

def refresh_withings_token():
    try:
        # Read credentials
        if not os.path.exists(CREDENTIALS_FILE):
            log('ERROR: Credentials file not found')
            return False
            
        with open(CREDENTIALS_FILE, 'r') as f:
            withings = json.load(f)
        
        client_id = get_env_var('WITHINGS_CLIENT_ID')
        client_secret = get_env_var('WITHINGS_CLIENT_SECRET')
        refresh_token = withings.get('refresh_token')
        user_id = withings.get('user_id', '14711398')
        expires_in = withings.get('expires_in', 10800)
        
        if not all([client_id, client_secret]):
            log('ERROR: Missing client credentials')
            return False
        
        if not refresh_token:
            log('ERROR: No refresh_token available - token needs re-authorization')
            return False
        
        # Check if token needs refresh (refresh if < 1 hour remaining)
        # expires_in is in seconds, typically 10800 (3 hours)
        if expires_in > 3600:
            log(f'Token still valid for {expires_in/3600:.1f} hours, skipping refresh')
            return True
        
        log('Token needs refresh (expires soon or expired)')
        log('Getting nonce for token refresh...')
        nonce = get_nonce(client_id, client_secret)
        if not nonce:
            log('ERROR: Failed to get nonce after retries')
            return False
        
        log('Refreshing Withings token...')
        timestamp = str(int(time.time()))
        
        # Signature: action,client_id,nonce (alphabetically sorted, comma-separated)
        sig_parts = ['requesttoken', client_id, nonce]
        sig_string = ','.join(sig_parts)
        signature = hmac.new(client_secret.encode(), sig_string.encode(), hashlib.sha256).hexdigest()
        
        # Request parameters
        request_params = {
            'action': 'requesttoken',
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'refresh_token': refresh_token,
            'nonce': nonce,
            'timestamp': timestamp,
            'signature': signature
        }
        
        response = requests.post('https://wbsapi.withings.net/v2/oauth2', data=request_params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 0:
                body = data.get('body', {})
                new_access_token = body.get('access_token')
                new_refresh_token = body.get('refresh_token', refresh_token)
                new_expires_in = body.get('expires_in', 10800)
                new_user_id = body.get('userid', user_id)
                
                if not new_access_token:
                    log('ERROR: No access_token in refresh response')
                    return False
                
                # Update credentials
                withings['access_token'] = new_access_token
                withings['refresh_token'] = new_refresh_token
                withings['expires_in'] = new_expires_in
                withings['user_id'] = new_user_id
                
                with open(CREDENTIALS_FILE, 'w') as f:
                    json.dump(withings, f, indent=2)
                
                log(f'SUCCESS: Token refreshed (expires in {new_expires_in/3600:.1f} hours)')
                return True
            else:
                error = data.get('error', 'Unknown')
                log(f'Token refresh failed: status {data.get("status")}, error: {error}')
                log(f'Response: {json.dumps(data, indent=2)[:500]}')
                return False
        else:
            log(f'Token refresh HTTP {response.status_code}: {response.text[:200]}')
            return False
    except Exception as e:
        log(f'ERROR: {str(e)}')
        import traceback
        log(traceback.format_exc())
        return False

if __name__ == '__main__':
    success = refresh_withings_token()
    exit(0 if success else 1)
