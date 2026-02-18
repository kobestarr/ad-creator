#!/usr/bin/env python3
"""
Fetch Withings Weight Data - Robust Version
Uses OAuth 2.0 authentication with auto-refresh on failure
"""
import json
import requests
import os
import subprocess
import time
from datetime import datetime

CREDENTIALS_FILE = '/root/.credentials/withings.json'
ENV_FILE = '/root/.credentials/.env'
LOG_FILE = '/var/log/withings-data.log'
REFRESH_SCRIPT = '/root/clawd/scripts/refresh-withings-token.py'
MAX_RETRIES = 3
RETRY_DELAY = 5

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

def refresh_token():
    """Attempt to refresh the token"""
    try:
        log('Attempting to refresh token...')
        result = subprocess.run(['python3', REFRESH_SCRIPT], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            log('Token refresh successful')
            return True
        else:
            log(f'Token refresh failed: {result.stderr[:200]}')
            return False
    except Exception as e:
        log(f'Error running refresh script: {str(e)}')
        return False

def fetch_withings_data(retry_count=0):
    try:
        # Read credentials
        if not os.path.exists(CREDENTIALS_FILE):
            log('ERROR: Credentials file not found')
            return False
            
        with open(CREDENTIALS_FILE, 'r') as f:
            withings = json.load(f)
        
        # Get OAuth credentials
        client_id = get_env_var('WITHINGS_CLIENT_ID')
        client_secret = get_env_var('WITHINGS_CLIENT_SECRET')
        access_token = withings.get('access_token')
        user_id = withings.get('user_id', '14711398')
        
        if not all([client_id, client_secret, access_token]):
            log('ERROR: Missing Withings credentials')
            return False
        
        # Calculate date range (last 30 days)
        end_date = int(datetime.now().timestamp())
        start_date = int((datetime.now().timestamp() - 30*24*60*60))
        
        # Withings API v2 endpoint - OAuth 2.0
        url = 'https://wbsapi.withings.net/v2/measure'
        params = {
            'action': 'getmeas',
            'userid': user_id,
            'startdate': start_date,
            'enddate': end_date,
            'category': 1  # Weight category
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        log(f'Fetching Withings data for user {user_id} (last 30 days)...')
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status')
            if status == 0:  # Success
                measures = data.get('body', {}).get('measuregrps', [])
                if measures:
                    log(f'SUCCESS: Found {len(measures)} weight measurements')
                    # Show last 5 measurements
                    for m in measures[-5:]:
                        weight = None
                        for measure in m.get('measures', []):
                            if measure.get('type') == 1:  # Weight
                                weight = measure.get('value', 0) * 10**-measure.get('unit', 0)
                                break
                        if weight:
                            date = datetime.fromtimestamp(m.get('date', 0))
                            log(f'  {date.strftime("%Y-%m-%d %H:%M")}: {weight:.1f} kg')
                    return True
                else:
                    log('No measurements found in last 30 days')
                    return True
            elif status == 277 or status == 401:
                log(f'Token expired or invalid (status {status}) - attempting refresh...')
                if refresh_token():
                    # Retry with new token
                    if retry_count < MAX_RETRIES:
                        log(f'Retrying fetch after token refresh ({retry_count + 1}/{MAX_RETRIES})...')
                        time.sleep(RETRY_DELAY)
                        return fetch_withings_data(retry_count + 1)
                    else:
                        log('Max retries reached after token refresh')
                        return False
                else:
                    log('Token refresh failed, cannot fetch data')
                    return False
            else:
                error_msg = data.get('error', 'Unknown')
                log(f'ERROR: Withings API status {status}: {error_msg}')
                if retry_count < MAX_RETRIES and status >= 500:  # Retry on server errors
                    log(f'Retrying fetch ({retry_count + 1}/{MAX_RETRIES})...')
                    time.sleep(RETRY_DELAY * (retry_count + 1))
                    return fetch_withings_data(retry_count + 1)
                return False
        elif response.status_code == 401:
            log('HTTP 401 Unauthorized - attempting token refresh...')
            if refresh_token():
                if retry_count < MAX_RETRIES:
                    log(f'Retrying fetch after token refresh ({retry_count + 1}/{MAX_RETRIES})...')
                    time.sleep(RETRY_DELAY)
                    return fetch_withings_data(retry_count + 1)
            return False
        else:
            log(f'ERROR: HTTP {response.status_code}: {response.text[:200]}')
            if retry_count < MAX_RETRIES and response.status_code >= 500:
                log(f'Retrying fetch ({retry_count + 1}/{MAX_RETRIES})...')
                time.sleep(RETRY_DELAY * (retry_count + 1))
                return fetch_withings_data(retry_count + 1)
            return False
            
    except requests.exceptions.RequestException as e:
        log(f'Network error: {str(e)}')
        if retry_count < MAX_RETRIES:
            log(f'Retrying fetch ({retry_count + 1}/{MAX_RETRIES})...')
            time.sleep(RETRY_DELAY * (retry_count + 1))
            return fetch_withings_data(retry_count + 1)
        return False
    except Exception as e:
        log(f'ERROR: {str(e)}')
        import traceback
        log(traceback.format_exc())
        return False

if __name__ == '__main__':
    success = fetch_withings_data()
    exit(0 if success else 1)
