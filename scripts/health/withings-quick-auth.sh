#!/bin/bash
# Quick Withings Authorization Helper

echo ''
echo '============================================================'
echo 'WITHINGS QUICK RE-AUTHORIZATION'
echo '============================================================'
echo ''
echo 'You have two redirect URIs configured:'
echo '  1. http://localhost/callback'
echo '  2. http://localhost/test'
echo ''
echo 'Choose which one to use (1 or 2): '
read -r choice

if [ "$choice" = "1" ]; then
    REDIRECT_URI="http://localhost/callback"
elif [ "$choice" = "2" ]; then
    REDIRECT_URI="http://localhost/test"
else
    echo 'Invalid choice, using http://localhost/callback'
    REDIRECT_URI="http://localhost/callback"
fi

echo ''
echo 'Generating authorization URL for: '$REDIRECT_URI
echo ''
python3 /root/clawd/scripts/withings-get-auth-url.py "$REDIRECT_URI"
echo ''
echo 'After you get the authorization code, run:'
echo "python3 /root/clawd/scripts/withings-exchange-code.py <code> $REDIRECT_URI"
