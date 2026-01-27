#!/usr/bin/env node

/**
 * Google Drive Setup Wizard
 *
 * Interactive CLI for configuring Google Drive OAuth 2.0 authentication
 * Detects credentials, runs OAuth flow, and tests connection
 */

const readline = require('readline');
const path = require('path');
const fs = require('fs').promises;
const fsSync = require('fs');
const os = require('os');
const {
  findCredentials,
  loadCredentials,
  findTokensPath,
  saveTokens,
  createOAuth2Client
} = require('./utils/google-drive');
const { google } = require('googleapis');

// Colors for terminal
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  red: '\x1b[31m'
};

function log(msg, color = 'reset') {
  console.log(colors[color] + msg + colors.reset);
}

function logBanner() {
  console.log('\n' + colors.bright + '═'.repeat(60));
  console.log('  GOOGLE DRIVE SETUP WIZARD');
  console.log('═'.repeat(60) + colors.reset + '\n');
}

function logSection(title) {
  console.log('\n' + colors.bright + title + colors.reset + '\n');
}

function logSuccess(msg) {
  console.log(colors.green + '✅ ' + msg + colors.reset);
}

function logError(msg) {
  console.log(colors.red + '❌ ' + msg + colors.reset);
}

function logWarning(msg) {
  console.log(colors.yellow + '⚠️  ' + msg + colors.reset);
}

function logInfo(msg) {
  console.log(colors.cyan + '💡 ' + msg + colors.reset);
}

/**
 * Prompt user for input
 */
function ask(question, defaultVal = '') {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    const prompt = defaultVal
      ? `${question} [${defaultVal}]: `
      : `${question}: `;

    rl.question(prompt, (answer) => {
      rl.close();
      resolve(answer.trim() || defaultVal);
    });
  });
}

/**
 * Find and validate credentials
 */
async function setupCredentials() {
  logSection('Step 1: Locate OAuth 2.0 Credentials');

  log('Looking for Google Cloud OAuth credentials...');

  // Try to auto-detect credentials
  const credentialsPath = await findCredentials();

  if (credentialsPath) {
    logSuccess(`Found credentials: ${credentialsPath}`);

    const useExisting = await ask('Use these credentials? (y/n)', 'y');

    if (useExisting.toLowerCase() === 'y') {
      return credentialsPath;
    }
  }

  // Prompt for manual path
  logWarning('No credentials found or user wants to specify different credentials');
  logInfo('You can download OAuth credentials from:');
  log('  https://console.cloud.google.com/apis/credentials', 'dim');
  console.log('');

  const manualPath = await ask('Enter path to credentials JSON file');

  if (!manualPath || !fsSync.existsSync(manualPath)) {
    logError('Credentials file not found');
    process.exit(1);
  }

  // Validate credentials format
  try {
    await loadCredentials(manualPath);
    logSuccess('Credentials file is valid');
  } catch (error) {
    logError(`Invalid credentials: ${error.message}`);
    process.exit(1);
  }

  // Copy to config directory
  const configDir = path.join(__dirname, '../config');
  const configPath = path.join(configDir, 'google-drive-credentials.json');

  try {
    if (!fsSync.existsSync(configDir)) {
      await fs.mkdir(configDir, { recursive: true });
    }

    await fs.copyFile(manualPath, configPath);
    logSuccess(`Credentials copied to: ${configPath}`);
    return configPath;
  } catch (error) {
    logWarning(`Could not copy credentials: ${error.message}`);
    return manualPath;
  }
}

/**
 * Run OAuth flow
 */
async function runOAuthFlow(credentialsPath) {
  logSection('Step 2: Authorize with Google');

  // Load credentials and create OAuth client
  const credentials = await loadCredentials(credentialsPath);
  const oauth2Client = createOAuth2Client(credentials);

  // Generate authorization URL
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: ['https://www.googleapis.com/auth/drive.file'],
    prompt: 'consent' // Force to get refresh token
  });

  console.log(colors.bright + '📋 AUTHORIZATION REQUIRED' + colors.reset);
  console.log('');
  log('Copy this URL and open it in your browser:', 'cyan');
  console.log('');
  console.log(colors.bright + authUrl + colors.reset);
  console.log('');
  log('After authorizing, Google will show you an authorization code.', 'dim');
  log('Copy that code and paste it below.', 'dim');
  console.log('');

  // Get authorization code from user
  const code = await ask('Enter authorization code');

  if (!code) {
    logError('No authorization code provided');
    process.exit(1);
  }

  // Exchange code for tokens
  try {
    log('Exchanging authorization code for access tokens...', 'dim');

    const { tokens } = await oauth2Client.getToken(code);

    logSuccess('Successfully obtained access tokens');

    // Save tokens
    const tokensPath = findTokensPath();
    const tokensDir = path.dirname(tokensPath);

    if (!fsSync.existsSync(tokensDir)) {
      await fs.mkdir(tokensDir, { recursive: true });
    }

    await saveTokens(tokensPath, tokens);
    logSuccess(`Tokens saved to: ${tokensPath}`);

    return { oauth2Client, tokens };
  } catch (error) {
    logError(`Authorization failed: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Test Google Drive connection
 */
async function testConnection(oauth2Client, tokens) {
  logSection('Step 3: Test Connection');

  try {
    log('Testing Google Drive API access...', 'dim');

    // Set credentials
    oauth2Client.setCredentials(tokens);
    const drive = google.drive({ version: 'v3', auth: oauth2Client });

    // Try to create root folder
    log('Creating "Ad Intelligence" folder...', 'dim');

    // Check if folder already exists
    const searchResponse = await drive.files.list({
      q: "name='Ad Intelligence' and mimeType='application/vnd.google-apps.folder' and trashed=false",
      fields: 'files(id, name)',
      spaces: 'drive'
    });

    let folderId;
    if (searchResponse.data.files && searchResponse.data.files.length > 0) {
      folderId = searchResponse.data.files[0].id;
      logSuccess('Found existing "Ad Intelligence" folder');
    } else {
      const folderResponse = await drive.files.create({
        requestBody: {
          name: 'Ad Intelligence',
          mimeType: 'application/vnd.google-apps.folder'
        },
        fields: 'id, name'
      });

      folderId = folderResponse.data.id;
      logSuccess('Created "Ad Intelligence" folder in Google Drive');
    }

    // List some files to verify access
    log('Verifying read access...', 'dim');

    await drive.files.list({
      pageSize: 5,
      fields: 'files(id, name)'
    });

    logSuccess('Google Drive API is working correctly');

    return true;
  } catch (error) {
    logError(`Connection test failed: ${error.message}`);
    return false;
  }
}

/**
 * Display success message and next steps
 */
function showSuccessMessage() {
  logSection('Setup Complete!');

  logSuccess('Google Drive integration is now configured');
  console.log('');

  console.log(colors.bright + 'Configuration Files:' + colors.reset);
  console.log(`  📁 Credentials: config/google-drive-credentials.json`);
  console.log(`  🔑 Tokens: ${path.join(os.homedir(), '.ad-intel', 'google-drive-tokens.json')}`);
  console.log('');

  console.log(colors.bright + 'Next Steps:' + colors.reset);
  console.log('  1. Run a search with the project flag:');
  console.log('');
  console.log(colors.cyan + '     node src/cli/index.js search "AI agents" -c US -p MyProject --limit 5' + colors.reset);
  console.log('');
  console.log('  2. Your screenshots and data will upload to:');
  console.log(colors.dim + '     Google Drive → Ad Intelligence → Projects → MyProject →' + colors.reset);
  console.log(colors.dim + '     Data → LinkedIn → ads → screenshots/' + colors.reset);
  console.log('');

  logInfo('Tokens will auto-refresh when expired. No need to re-authorize.');
  console.log('');
}

/**
 * Main setup function
 */
async function setup() {
  logBanner();

  log('This wizard will configure Google Drive integration for ad-intel.');
  log('You will need OAuth 2.0 credentials from Google Cloud Console.', 'dim');
  console.log('');

  logInfo('Prerequisites:');
  log('  • Google Cloud project with Drive API enabled', 'dim');
  log('  • OAuth 2.0 Client ID credentials (Desktop app)', 'dim');
  log('  • Downloaded client_secret_*.json file', 'dim');
  console.log('');

  const proceed = await ask('Ready to begin? (y/n)', 'y');

  if (proceed.toLowerCase() !== 'y') {
    log('\nSetup cancelled.', 'yellow');
    process.exit(0);
  }

  try {
    // Step 1: Find/validate credentials
    const credentialsPath = await setupCredentials();

    // Step 2: Run OAuth flow
    const { oauth2Client, tokens } = await runOAuthFlow(credentialsPath);

    // Step 3: Test connection
    const testPassed = await testConnection(oauth2Client, tokens);

    if (!testPassed) {
      logWarning('Connection test had issues, but tokens are saved');
      logWarning('Try running a search to verify uploads work');
    }

    // Show success message
    showSuccessMessage();
  } catch (error) {
    logError(`Setup failed: ${error.message}`);
    console.error(error);
    process.exit(1);
  }
}

// Run setup if executed directly
if (require.main === module) {
  setup().catch(error => {
    logError('Unexpected error:');
    console.error(error);
    process.exit(1);
  });
}

module.exports = { setup };
