#!/usr/bin/env python3
"""
Withings API Health Check
Tests authentication, token validity, and API connectivity
"""
import json
import requests
import os
import subprocess
from datetime import datetime

CREDENTIALS_FILE = '/root/.credentials/withings.json'
ENV_FILE = '/root/.credentials/.env'
LOG_FILE = '/var/log/withings-health-check.log'
REFRESH_SCRIPT = '/root/clawd/scripts/refresh-withings-token.py'

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

def check_credentials():
    """Check if credentials exist"""
    log('=== Checking Credentials ===')
    client_id = get_env_var('WITHINGS_CLIENT_ID')
    client_secret = get_env_var('WITHINGS_CLIENT_SECRET')
    
    if not client_id:
        log('❌ WITHINGS_CLIENT_ID not found')
        return False
    if not client_secret:
        log('❌ WITHINGS_CLIENT_SECRET not found')
        return False
    
    log(f'✅ Client ID: {client_id[:20]}...')
    log(f'✅ Client Secret: {client_secret[:20]}...')
    
    if not os.path.exists(CREDENTIALS_FILE):
        log('❌ Credentials file not found')
        return False
    
    with open(CREDENTIALS_FILE, 'r') as f:
        creds = json.load(f)
    
    if not creds.get('access_token'):
        log('❌ No access_token in credentials file')
        return False
    if not creds.get('refresh_token'):
        log('❌ No refresh_token in credentials file')
        return False
    
    expires_in = creds.get('expires_in', 0)
    hours_remaining = expires_in / 3600 if expires_in > 0 else 0
    log(f'✅ Access token expires in: {hours_remaining:.1f} hours')
    log(f'✅ User ID: {creds.get("user_id", "N/A")}')
    
    return True

def check_api_connectivity():
    """Check if Withings API is reachable"""
    log('=== Checking API Connectivity ===')
    try:
        response = requests.get('https://wbsapi.withings.net/v2/measure', timeout=5)
        log(f'✅ API endpoint reachable (HTTP {response.status_code})')
        return True
    except requests.exceptions.RequestException as e:
        log(f'❌ API endpoint unreachable: {str(e)}')
        return False

def check_token_validity():
    """Check if current token is valid"""
    log('=== Checking Token Validity ===')
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            creds = json.load(f)
        
        access_token = creds.get('access_token')
        user_id = creds.get('user_id', '14711398')
        
        if not access_token:
            log('❌ No access token')
            return False
        
        # Try a simple API call
        url = 'https://wbsapi.withings.net/v2/measure'
        params = {
            'action': 'getmeas',
            'userid': user_id,
            'startdate': int(datetime.now().timestamp()) - 86400,  # Last 24 hours
            'enddate': int(datetime.now().timestamp()),
            'category': 1
        }
        headers = {'Authorization': f'Bearer {access_token}'}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 0:
                log('✅ Token is valid and working')
                return True
            elif data.get('status') == 277:
                log('❌ Token is invalid (status 277)')
                return False
            else:
                log(f'⚠️  Token check returned status {data.get("status")}')
                return False
        else:
            log(f'❌ Token check HTTP {response.status_code}')
            return False
    except Exception as e:
        log(f'❌ Error checking token: {str(e)}')
        return False

def test_refresh():
    """Test token refresh functionality"""
    log('=== Testing Token Refresh ===')
    try:
        result = subprocess.run(['python3', REFRESH_SCRIPT], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            log('✅ Token refresh script works')
            return True
        else:
            log(f'⚠️  Token refresh script returned code {result.returncode}')
            log(f'Output: {result.stdout[:200]}')
            return False
    except Exception as e:
        log(f'❌ Error testing refresh: {str(e)}')
        return False

def main():
    log('\n' + '='*50)
    log('Withings API Health Check')
    log('='*50)
    
    results = {
        'credentials': check_credentials(),
        'connectivity': check_api_connectivity(),
        'token_validity': check_token_validity(),
        'refresh': test_refresh()
    }
    
    log('\n' + '='*50)
    log('Health Check Summary')
    log('='*50)
    for check, passed in results.items():
        status = '✅ PASS' if passed else '❌ FAIL'
        log(f'{check.upper()}: {status}')
    
    all_passed = all(results.values())
    log('\n' + ('✅ ALL CHECKS PASSED' if all_passed else '❌ SOME CHECKS FAILED'))
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    exit(main())
