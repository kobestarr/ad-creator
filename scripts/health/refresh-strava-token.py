#!/usr/bin/env python3
"""
Automated Strava Token Refresh Script
Refreshes Strava access token before it expires
Runs via cron every 4 hours
"""
import json
import requests
import os
from datetime import datetime
from pathlib import Path

# Paths
CREDENTIALS_FILE = '/root/.credentials/strava.json'
ENV_FILE = '/root/.credentials/.env'
LOG_FILE = '/var/log/strava-token-refresh.log'

def log(message):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f'[{timestamp}] {message}\n'
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg)
    print(log_msg.strip())

def get_env_var(key):
    """Get environment variable from .env file"""
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if line.startswith(f'{key}='):
                    return line.split('=', 1)[1].strip()
    return os.getenv(key)

def refresh_token():
    """Refresh Strava access token"""
    try:
        # Read current credentials
        with open(CREDENTIALS_FILE, 'r') as f:
            strava = json.load(f)
        
        # Get client credentials
        client_id = get_env_var('STRAVA_CLIENT_ID')
        client_secret = get_env_var('STRAVA_CLIENT_SECRET')
        refresh_token = strava.get('refresh_token')
        
        if not all([client_id, client_secret, refresh_token]):
            log('ERROR: Missing credentials (client_id, client_secret, or refresh_token)')
            return False
        
        # Check if token is still valid (refresh if expires in < 1 hour)
        expires_at = strava.get('expires_at', 0)
        hours_until_expiry = (expires_at - datetime.now().timestamp()) / 3600
        
        if hours_until_expiry > 1:
            log(f'Token still valid for {hours_until_expiry:.1f} hours, skipping refresh')
            return True
        
        log('Refreshing Strava token...')
        
        # Refresh token
        response = requests.post('https://www.strava.com/oauth/token', data={
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Update credentials
            strava['access_token'] = data['access_token']
            strava['refresh_token'] = data.get('refresh_token', refresh_token)
            strava['expires_at'] = int(datetime.now().timestamp()) + data.get('expires_in', 21600)
            
            # Save updated credentials
            with open(CREDENTIALS_FILE, 'w') as f:
                json.dump(strava, f, indent=2)
            
            exp_time = datetime.fromtimestamp(strava['expires_at'])
            log(f'SUCCESS: Token refreshed! Expires: {exp_time}')
            return True
        else:
            log(f'ERROR: Token refresh failed: {response.status_code} - {response.text[:200]}')
            return False
            
    except Exception as e:
        log(f'ERROR: Exception during refresh: {str(e)}')
        return False

if __name__ == '__main__':
    success = refresh_token()
    exit(0 if success else 1)
