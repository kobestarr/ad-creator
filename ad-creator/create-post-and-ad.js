#!/usr/bin/env node

/**
 * Reddit Ad Creator - Full Pipeline
 *
 * Creates posts + ads from Google Sheets data
 *
 * Usage: node create-post-and-ad.js --client bluprintx --subreddit salesforce --headline "..." --body "..." --url "..."
 */

require('dotenv').config();

const { loadCredentials, getAdAccount } = require('./lib/reddit-api');
const { getAuthorizationUrl, exchangeCodeForToken, saveNativeTokens, getNativeAccessToken } = require('./lib/reddit-native-oauth');
const { createLinkPost } = require('./lib/reddit-native-posts');
const https = require('https');
const readline = require('readline');
const path = require('path');
const os = require('os');

const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  red: '\x1b[31m'
};

function log(msg, color = 'reset') {
  console.log(colors[color] + msg + colors.reset);
}

function logBanner() {
  console.log('');
  console.log('═'.repeat(60));
  log('  REDDIT POST + AD CREATOR', 'bright');
  console.log('═'.repeat(60));
  console.log('');
}

/**
 * Setup Reddit Native OAuth (run once)
 */
async function setupNativeOAuth(clientName) {
  log('Setting up Reddit Native API OAuth...', 'cyan');
  console.log('');

  const credentials = await loadCredentials(clientName);
  const state = Math.random().toString(36).substring(7);
  const authUrl = getAuthorizationUrl(state);

  log('Step 1: Authorize in browser', 'yellow');
  console.log('');
  console.log('Open this URL:');
  console.log(authUrl);
  console.log('');
  console.log('Click "Allow" to authorize.');
  console.log('');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  const code = await new Promise(resolve => {
    rl.question('Paste the authorization code from the redirect URL: ', resolve);
  });

  rl.close();

  log('Exchanging code for tokens...', 'cyan');
  const tokens = await exchangeCodeForToken(code);

  log('Saving tokens...', 'cyan');
  const tokenPath = await saveNativeTokens(clientName, {
    accessToken: tokens.accessToken,
    refreshToken: tokens.refreshToken,
    expiresAt: Date.now() + (tokens.expiresIn * 1000) - 60000,
    scope: tokens.scope
  });

  log(`Tokens saved to: ${tokenPath}`, 'green');
  console.log('');
  log('✅ Reddit Native OAuth setup complete!', 'green');
  console.log('');
}

/**
 * Create post and ad
 */
async function createPostAndAd(clientName, subreddit, title, body, landingPageUrl, adGroupId) {
  logBanner();

  // Check if native tokens exist
  const { loadNativeTokens, getNativeAccessToken } = require('./lib/reddit-native-oauth');
  const nativeTokens = await loadNativeTokens(clientName);

  if (!nativeTokens) {
    log('Reddit Native OAuth not configured.', 'red');
    log('Run: node create-post-and-ad.js --setup', 'yellow');
    console.log('');
    return;
  }

  const accessToken = await getNativeAccessToken(clientName);
  const credentials = await loadCredentials(clientName);
  const accountId = credentials.ad_account_id;

  // Step 1: Create post
  log('Step 1: Creating Reddit Post', 'yellow');
  console.log('');

  const post = await createLinkPost(accessToken, subreddit, title, landingPageUrl);

  log('✅ Post created!', 'green');
  console.log(`  Post ID: ${post.postId}`);
  console.log(`  URL: ${post.url}`);
  console.log('');

  // Step 2: Create ad promoting the post
  log('Step 2: Creating Ad', 'yellow');
  console.log('');

  const adData = {
    data: {
      name: `Ad: ${title.substring(0, 50)}...`,
      ad_group_id: adGroupId,
      post_id: post.fullName,
      click_url: landingPageUrl,
      configured_status: 'ACTIVE'
    }
  };

  const adReq = https.request({
    hostname: 'ads-api.reddit.com',
    path: `/api/v3/ad_accounts/${accountId}/ads`,
    method: 'POST',
    headers: {
      'User-Agent': 'ad-creator/2.0',
      'Authorization': `Bearer ${await require('./lib/reddit-api').getAccessToken(clientName)}`,
      'Content-Type': 'application/json'
    }
  }, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
      console.log(`  Status: ${res.statusCode}`);
      console.log(`  Response: ${data.substring(0, 500)}`);

      if (res.statusCode === 200 || res.statusCode === 201) {
        console.log('');
        log('═'.repeat(60));
        log('  ✅ POST + AD CREATED SUCCESSFULLY!', 'green');
        log('═'.repeat(60));
        console.log('');
        console.log(`  Post: ${post.url}`);
        console.log(`  Ad ID: ${JSON.parse(data).data?.id}`);
        console.log('');
      } else {
        console.log('');
        log('⚠️  Ad creation failed - post was created but ad may need manual creation', 'yellow');
        console.log('');
      }
    });
  });

  adReq.on('error', console.error);
  adReq.write(JSON.stringify(adData));
  adReq.end();
}

/**
 * Main CLI
 */
async function main() {
  const args = process.argv.slice(2);
  const setup = args.includes('--setup');
  const clientName = args.find(a => a.startsWith('--client='))?.split('=')[1] || 'bluprintx';
  const subreddit = args.find(a => a.startsWith('--subreddit='))?.split('=')[1] || 'salesforce';
  const title = args.find(a => a.startsWith('--title='))?.split('=')[1]?.replace(/_/g, ' ');
  const body = args.find(a => a.startsWith('--body='))?.split('=')[1]?.replace(/_/g, ' ') || '';
  const url = args.find(a => a.startsWith('--url='))?.split('=')[1];
  const adGroupId = args.find(a => a.startsWith('--adgroup='))?.split('=')[1];

  if (setup) {
    await setupNativeOAuth(clientName);
    return;
  }

  if (!title || !url) {
    logBanner();
    console.log('Usage:');
    console.log('');
    console.log('  # Setup OAuth (run once)');
    console.log('  node create-post-and-ad.js --setup --client bluprintx');
    console.log('');
    console.log('  # Create post + ad');
    console.log('  node create-post-and-ad.js --client bluprintx \\');
    console.log('    --subreddit salesforce \\');
    console.log('    --title "Your title here" \\');
    console.log('    --body "Your body here" \\');
    console.log('    --url https://example.com \\');
    console.log('    --adgroup 2423534574861646096');
    console.log('');
    return;
  }

  await createPostAndAd(clientName, subreddit, title, body, url, adGroupId);
}

main().catch(error => {
  console.error('Error:', error.message);
  process.exit(1);
});
