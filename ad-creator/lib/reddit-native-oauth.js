/**
 * Reddit Native API OAuth
 * 
 * Handles Reddit user authentication for creating posts (separate from Ads API)
 * 
 * OAuth Scopes needed:
 * - identity: Access user identity
 * - submit: Submit posts and comments
 * - mysubreddits: Access user's subreddits
 */

const https = require('https');
const fs = require('fs').promises;
const path = require('path');
const os = require('os');
const crypto = require('crypto');

const REDDIT_NATIVE_CONFIG = {
  clientId: process.env.REDDIT_NATIVE_CLIENT_ID,
  clientSecret: process.env.REDDIT_NATIVE_CLIENT_SECRET,
  redirectUri: process.env.REDDIT_NATIVE_REDIRECT_URI || 'http://localhost:3000/callback/reddit-native',
  userAgent: 'ad-creator/2.0 (Native API)',
  tokenUrl: 'https://www.reddit.com/api/v1/access_token',
  baseUrl: 'https://oauth.reddit.com',
};

// Scopes for post creation
const SCOPES = ['identity', 'submit', 'mysubreddits'];

/**
 * Generate authorization URL
 */
function getAuthorizationUrl(state) {
  const params = new URLSearchParams({
    client_id: REDDIT_NATIVE_CONFIG.clientId,
    response_type: 'code',
    state: state,
    redirect_uri: REDDIT_NATIVE_CONFIG.redirectUri,
    duration: 'permanent',
    scope: SCOPES.join(',')
  });

  return `https://www.reddit.com/api/v1/authorize?${params.toString()}`;
}

/**
 * Exchange authorization code for tokens
 */
async function exchangeCodeForToken(code) {
  return new Promise((resolve, reject) => {
    const auth = Buffer.from(`${REDDIT_NATIVE_CONFIG.clientId}:${REDDIT_NATIVE_CONFIG.clientSecret}`).toString('base64');

    const req = https.request({
      hostname: 'www.reddit.com',
      path: '/api/v1/access_token',
      method: 'POST',
      headers: {
        'User-Agent': REDDIT_NATIVE_CONFIG.userAgent,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `Basic ${auth}`
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode !== 200) {
          reject(new Error(`OAuth error: ${res.statusCode} - ${data}`));
          return;
        }

        try {
          const response = JSON.parse(data);
          if (response.error) {
            reject(new Error(`OAuth error: ${response.error}`));
          } else {
            resolve({
              accessToken: response.access_token,
              refreshToken: response.refresh_token,
              expiresIn: response.expires_in,
              scope: response.scope
            });
          }
        } catch (error) {
          reject(new Error(`Failed to parse OAuth response: ${error.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(`grant_type=authorization_code&code=${code}&redirect_uri=${REDDIT_NATIVE_CONFIG.redirectUri}`);
    req.end();
  });
}

/**
 * Refresh access token
 */
async function refreshAccessToken(refreshToken) {
  return new Promise((resolve, reject) => {
    const auth = Buffer.from(`${REDDIT_NATIVE_CONFIG.clientId}:${REDDIT_NATIVE_CONFIG.clientSecret}`).toString('base64');

    const req = https.request({
      hostname: 'www.reddit.com',
      path: '/api/v1/access_token',
      method: 'POST',
      headers: {
        'User-Agent': REDDIT_NATIVE_CONFIG.userAgent,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `Basic ${auth}`
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          resolve({
            accessToken: response.access_token,
            refreshToken: response.refresh_token || refreshToken,
            expiresIn: response.expires_in,
            scope: response.scope
          });
        } catch (error) {
          reject(new Error(`Failed to refresh token: ${error.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(`grant_type=refresh_token&refresh_token=${refreshToken}`);
    req.end();
  });
}

/**
 * Load native API tokens
 */
async function loadNativeTokens(clientName) {
  const tokenPath = path.join(os.homedir(), '.ad-creator', `reddit-native-${clientName}.json`);

  try {
    const content = await fs.readFile(tokenPath, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    return null;
  }
}

/**
 * Save native API tokens
 */
async function saveNativeTokens(clientName, tokens) {
  const tokenDir = path.join(os.homedir(), '.ad-creator');
  const tokenPath = path.join(tokenDir, `reddit-native-${clientName}.json`);

  await fs.mkdir(tokenDir, { recursive: true });
  await fs.writeFile(tokenPath, JSON.stringify(tokens, null, 2));

  return tokenPath;
}

/**
 * Get access token (with auto-refresh)
 */
async function getNativeAccessToken(clientName) {
  const tokens = await loadNativeTokens(clientName);

  if (!tokens) {
    throw new Error(`No native tokens for ${clientName}. Run: npm run setup:reddit-native`);
  }

  const now = Date.now();
  if (tokens.expiresAt && tokens.expiresAt > now) {
    return tokens.accessToken;
  }

  // Refresh if expired
  if (tokens.refreshToken) {
    const newTokens = await refreshAccessToken(tokens.refreshToken);
    const tokenData = {
      accessToken: newTokens.accessToken,
      refreshToken: newTokens.refreshToken,
      expiresAt: Date.now() + (newTokens.expiresIn * 1000) - 60000,
      scope: newTokens.scope
    };

    await saveNativeTokens(clientName, tokenData);
    return newTokens.accessToken;
  }

  throw new Error(`Tokens expired and no refresh token for ${clientName}`);
}

module.exports = {
  getAuthorizationUrl,
  exchangeCodeForToken,
  refreshAccessToken,
  loadNativeTokens,
  saveNativeTokens,
  getNativeAccessToken,
  SCOPES
};
