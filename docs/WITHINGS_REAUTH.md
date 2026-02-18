# Withings Re-authorization Guide

## Problem: redirect_uri_mismatch

The redirect_uri you're using doesn't match what's configured in your Withings Developer Dashboard.

## Solution: Find Your Correct Redirect URI

1. **Go to Withings Developer Dashboard:**
   https://developer.withings.com/dashboard/

2. **Find your app** (Client ID: 6559b3aa742396c378c962301ca2dd54818e31d62c386c9a6131135094d3b718)

3. **Check the "Callback URL" or "Redirect URI" field**
   - This is what you MUST use exactly (case-sensitive, including http/https, port, path)

4. **Common redirect URIs:**
   - 
   - 
   - 
   -  (for manual copy-paste, no redirect)

## Steps to Re-authorize

### Step 1: Generate Authorization URL with Correct Redirect URI



Example:


### Step 2: Open the URL in Browser

Copy the authorization URL from Step 1 and open it in your browser.

### Step 3: Authorize and Get Code

- Log in to Withings
- Authorize the application
- You'll be redirected to your redirect_uri with a  parameter
- Copy the code value

**If using :**
- You'll see the code on the page instead of a redirect
- Copy it directly

### Step 4: Exchange Code for Tokens



Example:


## If You Need to Update Redirect URI in Dashboard

1. Go to https://developer.withings.com/dashboard/
2. Select your app
3. Edit the "Callback URL" field
4. Save changes
5. Use the new redirect_uri in the scripts above

## After Re-authorization

Once tokens are saved, the automated system will work:
- Token refresh: Every 2 hours
- Data fetch: Twice daily (6 AM & 6 PM)
- Health check: Daily at midnight
