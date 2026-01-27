/**
 * Google Drive Integration
 *
 * Handles file uploads to Google Drive using OAuth 2.0 authentication
 * Supports credential auto-detection, token refresh, and folder management
 */

const { google } = require('googleapis');
const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');
const os = require('os');

// Try to load keytar for secure token storage, fallback to file if unavailable
let keytar;
try {
  keytar = require('keytar');
} catch (error) {
  keytar = null;
}

const KEYCHAIN_SERVICE = 'ad-creator';
const KEYCHAIN_ACCOUNT = 'google-drive-tokens';

// Folder ID cache to minimize API calls
const folderCache = new Map();

/**
 * Find credentials file in multiple locations
 * @returns {Promise<string|null>} - Path to credentials file
 */
async function findCredentials() {
  const possiblePaths = [
    // Environment variable
    process.env.GOOGLE_DRIVE_CREDENTIALS,
    // Project config directory
    path.join(__dirname, '../../config/google-drive-credentials.json'),
    // User home directory
    path.join(os.homedir(), '.ad-intel', 'google-drive-credentials.json')
  ];

  // Only auto-discover in Downloads folder if explicitly enabled (security best practice)
  if (process.env.ALLOW_AUTO_DISCOVER_CREDENTIALS === 'true') {
    const downloadCreds = await findClientSecretInDownloads();
    if (downloadCreds.length > 0) {
      console.warn('⚠️  WARNING: Auto-discovery of credentials in Downloads folder is enabled.');
      console.warn('   This is a security risk. Set ALLOW_AUTO_DISCOVER_CREDENTIALS=false to disable.');
    }
    possiblePaths.push(...downloadCreds);
  }

  for (const credPath of possiblePaths) {
    if (credPath && fsSync.existsSync(credPath)) {
      try {
        const content = await fs.readFile(credPath, 'utf8');
        JSON.parse(content); // Validate JSON
        return credPath;
      } catch (error) {
        // Invalid JSON, continue to next
      }
    }
  }

  return null;
}

/**
 * Auto-detect client_secret_*.json files in Downloads folder
 * SECURITY NOTE: This should only be enabled via ALLOW_AUTO_DISCOVER_CREDENTIALS=true
 * @returns {Promise<Array<string>>} - Array of potential credential paths
 */
async function findClientSecretInDownloads() {
  const downloadsDir = path.join(os.homedir(), 'Downloads');

  try {
    const files = await fs.readdir(downloadsDir);
    const clientSecrets = files
      .filter(f => f.startsWith('client_secret_') && f.endsWith('.json'))
      .map(f => path.join(downloadsDir, f));
    return clientSecrets;
  } catch (error) {
    return [];
  }
}

/**
 * Load credentials from file
 * @param {string} credentialsPath - Path to credentials JSON
 * @returns {Promise<object>} - Credentials object
 */
async function loadCredentials(credentialsPath) {
  try {
    const content = await fs.readFile(credentialsPath, 'utf8');
    const credentials = JSON.parse(content);

    // Support both 'installed' and 'web' OAuth app types
    if (!credentials.installed && !credentials.web) {
      throw new Error('Invalid credentials format. Expected "installed" or "web" key.');
    }

    return credentials;
  } catch (error) {
    throw new Error(`Failed to load credentials: ${error.message}`);
  }
}

/**
 * Find tokens file
 * @returns {string|null} - Path to tokens file
 */
function findTokensPath() {
  const possiblePaths = [
    process.env.GOOGLE_DRIVE_TOKENS,
    path.join(os.homedir(), '.ad-intel', 'google-drive-tokens.json'),
    path.join(__dirname, '../../tokens.json')
  ];

  for (const tokenPath of possiblePaths) {
    if (tokenPath && fsSync.existsSync(tokenPath)) {
      return tokenPath;
    }
  }

  // Return default path for saving new tokens
  return path.join(os.homedir(), '.ad-intel', 'google-drive-tokens.json');
}

/**
 * Load tokens from keychain (secure storage)
 * @returns {Promise<object|null>} - Tokens object or null if not found
 */
async function loadTokensFromKeychain() {
  if (!keytar) {
    return null;
  }

  try {
    const tokenString = await keytar.getPassword(KEYCHAIN_SERVICE, KEYCHAIN_ACCOUNT);
    if (!tokenString) {
      return null;
    }
    return JSON.parse(tokenString);
  } catch (error) {
    console.warn('Failed to load tokens from keychain, falling back to file storage:', error.message);
    return null;
  }
}

/**
 * Save tokens to keychain (secure storage)
 * @param {object} tokens - Tokens object
 * @returns {Promise<boolean>} - True if successful
 */
async function saveTokensToKeychain(tokens) {
  if (!keytar) {
    return false;
  }

  try {
    await keytar.setPassword(KEYCHAIN_SERVICE, KEYCHAIN_ACCOUNT, JSON.stringify(tokens));
    return true;
  } catch (error) {
    console.warn('Failed to save tokens to keychain, falling back to file storage:', error.message);
    return false;
  }
}

/**
 * Load tokens from file (fallback method)
 * @param {string} tokensPath - Path to tokens JSON
 * @returns {Promise<object|null>} - Tokens object or null if not found
 */
async function loadTokens(tokensPath) {
  try {
    if (!fsSync.existsSync(tokensPath)) {
      return null;
    }
    const content = await fs.readFile(tokensPath, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    return null;
  }
}

/**
 * Save tokens to file (fallback method)
 * @param {string} tokensPath - Path to save tokens
 * @param {object} tokens - Tokens object
 */
async function saveTokens(tokensPath, tokens) {
  try {
    const dir = path.dirname(tokensPath);

    // Ensure directory exists
    if (!fsSync.existsSync(dir)) {
      await fs.mkdir(dir, { recursive: true });
    }

    await fs.writeFile(tokensPath, JSON.stringify(tokens, null, 2));
  } catch (error) {
    throw new Error(`Failed to save tokens: ${error.message}`);
  }
}

/**
 * Load tokens with automatic fallback (keychain -> file)
 * @param {string} tokensPath - Path to tokens JSON (fallback)
 * @returns {Promise<object|null>} - Tokens object or null if not found
 */
async function loadTokensWithFallback(tokensPath) {
  // Try keychain first
  const keychainTokens = await loadTokensFromKeychain();
  if (keychainTokens) {
    return keychainTokens;
  }

  // Fallback to file storage
  return await loadTokens(tokensPath);
}

/**
 * Save tokens with automatic fallback (keychain -> file)
 * @param {string} tokensPath - Path to save tokens (fallback)
 * @param {object} tokens - Tokens object
 */
async function saveTokensWithFallback(tokensPath, tokens) {
  // Try keychain first
  const savedToKeychain = await saveTokensToKeychain(tokens);
  if (savedToKeychain) {
    return;
  }

  // Fallback to file storage
  await saveTokens(tokensPath, tokens);
}

/**
 * Create OAuth2 client
 * @param {object} credentials - Credentials object
 * @returns {object} - OAuth2 client
 */
function createOAuth2Client(credentials) {
  const creds = credentials.installed || credentials.web;

  return new google.auth.OAuth2(
    creds.client_id,
    creds.client_secret,
    creds.redirect_uris[0]
  );
}

/**
 * Authenticate with Google Drive
 * @returns {Promise<object>} - Authenticated drive instance
 */
async function authenticate() {
  // Find credentials
  const credentialsPath = await findCredentials();
  if (!credentialsPath) {
    throw new Error('Google Drive credentials not found. Run: npm run setup:gdrive');
  }

  // Load credentials
  const credentials = await loadCredentials(credentialsPath);
  const oauth2Client = createOAuth2Client(credentials);

  // Find and load tokens (with keychain fallback)
  const tokensPath = findTokensPath();
  const tokens = await loadTokensWithFallback(tokensPath);

  if (!tokens) {
    throw new Error('Google Drive tokens not found. Run: npm run setup:gdrive');
  }

  // Set credentials
  oauth2Client.setCredentials(tokens);

  // Check if token is expired and refresh if needed
  if (tokens.expiry_date && Date.now() >= tokens.expiry_date) {
    try {
      const { credentials: newTokens } = await oauth2Client.refreshAccessToken();
      await saveTokensWithFallback(tokensPath, newTokens);
      oauth2Client.setCredentials(newTokens);
    } catch (error) {
      throw new Error('Token refresh failed. Run: npm run setup:gdrive');
    }
  }

  return google.drive({ version: 'v3', auth: oauth2Client });
}

/**
 * Search for a folder by name and optional parent
 * @param {object} drive - Google Drive instance
 * @param {string} name - Folder name
 * @param {string} parentId - Parent folder ID (optional)
 * @returns {Promise<string|null>} - Folder ID or null
 */
async function searchFolder(drive, name, parentId = null) {
  try {
    let query = `name='${name}' and mimeType='application/vnd.google-apps.folder' and trashed=false`;

    if (parentId) {
      query += ` and '${parentId}' in parents`;
    }

    const response = await drive.files.list({
      q: query,
      fields: 'files(id, name)',
      spaces: 'drive'
    });

    if (response.data.files && response.data.files.length > 0) {
      return response.data.files[0].id;
    }

    return null;
  } catch (error) {
    console.error(`Error searching folder "${name}":`, error.message);
    return null;
  }
}

/**
 * Create a folder
 * @param {object} drive - Google Drive instance
 * @param {string} name - Folder name
 * @param {string} parentId - Parent folder ID (optional)
 * @returns {Promise<string>} - Created folder ID
 */
async function createFolder(drive, name, parentId = null) {
  try {
    const fileMetadata = {
      name: name,
      mimeType: 'application/vnd.google-apps.folder'
    };

    if (parentId) {
      fileMetadata.parents = [parentId];
    }

    const response = await drive.files.create({
      requestBody: fileMetadata,
      fields: 'id'
    });

    return response.data.id;
  } catch (error) {
    throw new Error(`Failed to create folder "${name}": ${error.message}`);
  }
}

/**
 * Get or create a folder
 * @param {object} drive - Google Drive instance
 * @param {string} name - Folder name
 * @param {string} parentId - Parent folder ID (optional)
 * @returns {Promise<string>} - Folder ID
 */
async function getOrCreateFolder(drive, name, parentId = null) {
  // Check cache first
  const cacheKey = `${name}:${parentId || 'root'}`;
  if (folderCache.has(cacheKey)) {
    return folderCache.get(cacheKey);
  }

  // Search for existing folder
  let folderId = await searchFolder(drive, name, parentId);

  // Create if doesn't exist
  if (!folderId) {
    folderId = await createFolder(drive, name, parentId);
  }

  // Cache the result
  folderCache.set(cacheKey, folderId);

  return folderId;
}

/**
 * Ensure entire folder path exists
 * @param {object} drive - Google Drive instance
 * @param {Array<string>} pathArray - Array of folder names
 * @returns {Promise<string>} - ID of final folder
 */
async function ensureFolderPath(drive, pathArray) {
  let parentId = null;

  for (const folderName of pathArray) {
    parentId = await getOrCreateFolder(drive, folderName, parentId);
  }

  return parentId;
}

/**
 * Auto-detect MIME type from file extension
 * @param {string} filePath - File path
 * @returns {string} - MIME type
 */
function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();

  const mimeTypes = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.json': 'application/json',
    '.txt': 'text/plain',
    '.pdf': 'application/pdf',
    '.html': 'text/html',
    '.csv': 'text/csv'
  };

  return mimeTypes[ext] || 'application/octet-stream';
}

/**
 * Upload a file to Google Drive with retry logic
 * @param {string} filePath - Absolute path to file
 * @param {object} options - Upload options
 * @param {string} options.name - File name in Drive
 * @param {string} options.folder - Folder path (e.g., "Data/LinkedIn/ads/screenshots")
 * @param {string} options.projectName - Project name for folder hierarchy
 * @param {string} [options.mimeType] - MIME type (auto-detected if not provided)
 * @returns {Promise<object>} - { success: boolean, name: string, id: string, error?: string }
 */
async function upload(filePath, options = {}) {
  const maxRetries = 3;
  let lastError = null;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await uploadWithoutRetry(filePath, options);
    } catch (error) {
      lastError = error;

      // Don't retry on authentication or file not found errors
      if (error.message.includes('credentials') ||
          error.message.includes('tokens') ||
          error.message.includes('ENOENT')) {
        break;
      }

      // Wait before retry with exponential backoff
      if (attempt < maxRetries) {
        const delay = Math.pow(2, attempt - 1) * 1000; // 1s, 2s, 4s
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  // All retries failed
  return {
    success: false,
    name: options.name || path.basename(filePath),
    id: null,
    error: lastError.message
  };
}

/**
 * Upload file without retry logic (internal)
 * @param {string} filePath - Absolute path to file
 * @param {object} options - Upload options
 * @returns {Promise<object>} - Upload result
 */
async function uploadWithoutRetry(filePath, options = {}) {
  // Validate file exists
  if (!fsSync.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }

  // Authenticate
  const drive = await authenticate();

  // Build full folder path
  const folderPathParts = ['Ad Intelligence', 'Projects'];

  if (options.projectName) {
    folderPathParts.push(options.projectName);
  }

  if (options.folder) {
    folderPathParts.push(...options.folder.split('/'));
  }

  // Ensure folder path exists
  const folderId = await ensureFolderPath(drive, folderPathParts);

  // Prepare file metadata
  const fileName = options.name || path.basename(filePath);
  const mimeType = options.mimeType || getMimeType(filePath);

  const fileMetadata = {
    name: fileName,
    parents: [folderId]
  };

  // Upload file
  const media = {
    mimeType: mimeType,
    body: fsSync.createReadStream(filePath)
  };

  const response = await drive.files.create({
    requestBody: fileMetadata,
    media: media,
    fields: 'id, name'
  });

  return {
    success: true,
    name: response.data.name,
    id: response.data.id
  };
}

/**
 * List files in a Google Drive folder
 * @param {string} folderId - Folder ID (defaults to root)
 * @param {object} options - List options
 * @param {number} [options.pageSize=100] - Max results
 * @param {string} [options.q] - Search query
 * @returns {Promise<Array>} - Array of file objects
 */
async function list(folderId = 'root', options = {}) {
  try {
    const drive = await authenticate();

    const query = options.q || `'${folderId}' in parents and trashed=false`;

    const response = await drive.files.list({
      q: query,
      pageSize: options.pageSize || 100,
      fields: 'files(id, name, mimeType, createdTime, modifiedTime, size)',
      orderBy: 'modifiedTime desc'
    });

    return response.data.files || [];
  } catch (error) {
    throw new Error(`Failed to list files: ${error.message}`);
  }
}

/**
 * Check if Google Drive is configured
 * @returns {Promise<boolean>} - True if configured
 */
async function checkConfiguration() {
  try {
    // Check for credentials
    const credentialsPath = await findCredentials();
    if (!credentialsPath) {
      return false;
    }

    // Check for tokens
    const tokensPath = findTokensPath();
    const tokens = await loadTokens(tokensPath);
    if (!tokens) {
      return false;
    }

    return true;
  } catch (error) {
    return false;
  }
}

module.exports = {
  upload,
  list,
  authenticate,
  checkConfiguration,
  findCredentials,
  loadCredentials,
  findTokensPath,
  loadTokens,
  saveTokens,
  loadTokensWithFallback,
  saveTokensWithFallback,
  createOAuth2Client
};
