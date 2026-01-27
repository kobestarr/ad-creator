#!/usr/bin/env node

/**
 * Ad Creative Generation Engine v2.0
 * 
 * Generates all combinations of ad creatives from:
 * - Images from Google Drive (siloed by ad group)
 * - Text variations from Google Sheets
 * - URL variations for A/B testing landing pages
 * 
 * Usage:
 *   node ad-creator.js
 *   (Will prompt for ad group, landing page URL, etc.)
 * 
 * Or with args:
 *   node ad-creator.js --ad-group "Agentforce-7-Lessons" --url "https://bluprintx.com/..."
 * 
 * ============================================================================
 * FOLDER STRUCTURE & SCALING NOTES
 * ============================================================================
 * 
 * CURRENT SETUP (Personal Use):
 * - Uses Google OAuth credentials from ~/.clawdbot/gdrive/
 * - Assumes: Bluprintx/Ads/Images/{AdGroup}/{SubTheme}
 * 
 * EXPECTED DRIVE FOLDER STRUCTURE:
 *   Bluprintx/
 *   └── Ads/
 *       └── Images/
 *           └── Agentforce-7-Lessons/
 *               └── Salesforce-Communities/
 *                   ├── Img-V1.png
 *                   ├── Img-V2.png
 *                   └── Img-V3.png
 * 
 * TO SCALE FOR MULTI-USER/TEAM USE:
 * 1. Service Account: Use a Google Cloud service account instead of OAuth
 *    - Create at: https://console.cloud.google.com/iam-admin/serviceaccounts
 *    - Share the target Drive folders with the service account email
 * 
 * 2. Folder Structure for Teams:
 *    Each user would have their own folder:
 *    - /{OrgName}/{UserName}/Ads/Images/{AdGroup}/{SubTheme}/
 * 
 * 3. Environment Variables (for production):
 *    - GOOGLE_SERVICE_ACCOUNT_EMAIL
 *    - GOOGLE_PRIVATE_KEY
 *    - DEFAULT_DRIVE_FOLDER_PATH
 * 
 * 4. For Client-Facing Use:
 *    - Users connect their own Google account via OAuth
 *    - Or provide a shared "Bluprintx" folder they can upload to
 *    - Clear instructions in UI: "Upload images to: Bluprintx/Ads/Images/{YourAdGroup}/"
 * 
 * ============================================================================
 */

const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');
const readline = require('readline');
const { google } = require('googleapis');
const { v4: uuidv4 } = require('uuid');
const { authenticate, checkConfiguration } = require('./src/utils/google-drive');

// We'll initialize drive and sheets after authentication
let drive, sheets;

// UI colors
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m'
};

function log(msg, color = 'reset') {
  console.log(colors[color] + msg + colors.reset);
}

console.log('');
console.log('════════════════════════════════════════════════════════════');
console.log('        🎨 Ad Creative Generation Engine v2.0');
console.log('════════════════════════════════════════════════════════════');
console.log('');

// Interactive prompts
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer.trim());
    });
  });
}

/**
 * Validate ad group name
 * @param {string} name - Ad group name to validate
 * @returns {string} - Validated and sanitized name
 * @throws {Error} - If validation fails
 */
function validateAdGroupName(name) {
  if (!name || typeof name !== 'string') {
    throw new Error('Ad group name is required');
  }
  
  const trimmed = name.trim();
  
  if (trimmed.length === 0) {
    throw new Error('Ad group name cannot be empty');
  }
  
  if (trimmed.length > 100) {
    throw new Error('Ad group name must be 100 characters or less');
  }
  
  // Allow alphanumeric, spaces, hyphens, and underscores
  if (!/^[a-zA-Z0-9\s\-_]+$/.test(trimmed)) {
    throw new Error('Ad group name contains invalid characters. Only letters, numbers, spaces, hyphens, and underscores are allowed.');
  }
  
  return trimmed;
}

/**
 * Validate URL format
 * @param {string} url - URL to validate
 * @returns {string} - Validated URL
 * @throws {Error} - If validation fails
 */
function validateUrl(url) {
  if (!url || typeof url !== 'string') {
    throw new Error('URL is required');
  }
  
  const trimmed = url.trim();
  
  if (trimmed.length === 0) {
    throw new Error('URL cannot be empty');
  }
  
  try {
    const urlObj = new URL(trimmed);
    // Only allow http and https protocols
    if (!['http:', 'https:'].includes(urlObj.protocol)) {
      throw new Error('URL must use http or https protocol');
    }
    return trimmed;
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error('Invalid URL format');
    }
    throw error;
  }
}

/**
 * Validate Google Sheet ID
 * @param {string} sheetId - Sheet ID to validate
 * @returns {string} - Validated sheet ID
 * @throws {Error} - If validation fails
 */
function validateSheetId(sheetId) {
  if (!sheetId || typeof sheetId !== 'string') {
    throw new Error('Sheet ID is required');
  }
  
  const trimmed = sheetId.trim();
  
  if (trimmed.length === 0) {
    throw new Error('Sheet ID cannot be empty');
  }
  
  // Google Sheet IDs are typically 44 characters, alphanumeric with hyphens/underscores
  // But we'll be lenient and just check for reasonable format
  if (!/^[a-zA-Z0-9_-]+$/.test(trimmed)) {
    throw new Error('Invalid sheet ID format. Sheet ID should contain only letters, numbers, hyphens, and underscores.');
  }
  
  return trimmed;
}

/**
 * Sanitize sheet name to prevent injection
 * @param {string} sheetName - Sheet name to sanitize
 * @returns {string} - Sanitized sheet name
 */
function sanitizeSheetName(sheetName) {
  if (!sheetName || typeof sheetName !== 'string') {
    return '';
  }
  
  // Remove any characters that could be used for injection
  // Allow alphanumeric, spaces, hyphens, underscores
  return sheetName.replace(/[^a-zA-Z0-9\s_-]/g, '').trim();
}

async function main() {
  // Check Google Drive configuration
  const isConfigured = await checkConfiguration();
  if (!isConfigured) {
    log('\n⚠️  Google Drive not configured\n', 'yellow');
    log('Run: npm run setup:gdrive\n', 'blue');
    log('Or manually set up OAuth at: https://console.cloud.google.com/apis/credentials\n', 'blue');
    process.exit(1);
  }

  // Authenticate and initialize Drive/Sheets clients
  try {
    const driveClient = await authenticate();
    drive = driveClient;

    // Get the auth client from drive instance
    const auth = drive.context._options.auth;
    sheets = google.sheets({ version: 'v4', auth: auth });

    log('✅ Google Drive authenticated\n', 'green');
  } catch (error) {
    log('\n❌ Authentication failed: ' + error.message + '\n', 'yellow');
    log('Run: npm run setup:gdrive\n', 'blue');
    process.exit(1);
  }

  log('📋 Step 1: Configuration\n', 'cyan');

  // Get ad group name with validation
  let adGroup;
  try {
    const adGroupInput = await ask('  Ad Group Name (e.g., Agentforce-7-Lessons): ');
    adGroup = validateAdGroupName(adGroupInput);
    log('  ✅ Ad Group: ' + adGroup + '\n', 'green');
  } catch (error) {
    log('  ❌ ' + error.message + '\n', 'yellow');
    rl.close();
    return;
  }

  // Get landing page URL with validation
  let fullLpUrl;
  try {
    const urlInput = await ask('  Full Landing Page URL: ');
    fullLpUrl = validateUrl(urlInput);
  } catch (error) {
    log('  ❌ ' + error.message + '\n', 'yellow');
    rl.close();
    return;
  }

  // Generate mini LP URL using robust URL parsing
  let miniLpUrl;
  try {
    miniLpUrl = createMiniLpUrl(fullLpUrl);
    log('  ✅ Mini LP URL: ' + miniLpUrl + '\n', 'green');
  } catch (error) {
    log('  ⚠️  Could not generate mini LP URL: ' + error.message + '\n', 'yellow');
    log('  Using original URL for mini LP\n', 'yellow');
    miniLpUrl = fullLpUrl;
  }

  // Get subtheme (optional) with validation
  let subTheme = '';
  try {
    const subThemeInput = await ask('  Sub-theme (optional, press Enter): ') || '';
    if (subThemeInput) {
      subTheme = validateAdGroupName(subThemeInput); // Reuse same validation
    }
  } catch (error) {
    log('  ⚠️  Invalid sub-theme: ' + error.message + '. Using empty sub-theme.\n', 'yellow');
    subTheme = '';
  }
  const subThemeStr = subTheme ? ' | ' + subTheme : '';

  log('\n📁 Step 2: Google Drive Configuration\n', 'cyan');

  // Get Drive folder with path.join for safety
  const baseFolder = await ask('  Drive Folder (default: Bluprintx/Ads/Images): ') || 'Bluprintx/Ads/Images';
  const imageFolder = subTheme 
    ? path.join(baseFolder, adGroup, subTheme)
    : path.join(baseFolder, adGroup);

  log('  📂 Images folder: ' + imageFolder + '\n', 'blue');

  log('📊 Step 3: Google Sheets Configuration\n', 'cyan');

  // Get Sheet ID with validation
  let sheetId = '';
  const sheetIdInput = await ask('  Google Sheet ID: ');
  if (sheetIdInput) {
    try {
      sheetId = validateSheetId(sheetIdInput);
      log('  ✅ Sheet ID: ' + sheetId + '\n', 'green');
    } catch (error) {
      log('  ⚠️  Invalid sheet ID: ' + error.message + '. Using example data.\n', 'yellow');
      sheetId = '';
    }
  } else {
    log('  ⚠️  No sheet provided - using example data\n', 'yellow');
  }

  log('🔄 Step 4: Processing\n', 'cyan');
  rl.close();

  // Create output directory using path.join and async operations
  const outputDir = path.join('./output', adGroup);
  try {
    await fs.mkdir(outputDir, { recursive: true });
    await fs.mkdir(path.join(outputDir, 'ads'), { recursive: true });
    await fs.mkdir(path.join(outputDir, 'images'), { recursive: true });
  } catch (error) {
    log('\n❌ Failed to create output directory: ' + error.message + '\n', 'yellow');
    throw error;
  }

  // Step 1: Fetch images from Drive with error handling
  log('  📥 Fetching images from Drive...\n', 'blue');
  let images = [];
  if (sheetId) {
    try {
      images = await fetchImagesFromDrive(imageFolder);
    } catch (error) {
      log('  ⚠️  Error fetching images: ' + error.message + '\n', 'yellow');
      // Re-throw critical network errors
      if (error.code === 'ENOTFOUND' || error.code === 'ECONNREFUSED') {
        throw new Error('Network error: Unable to connect to Google Drive API. Please check your internet connection.');
      }
      // For other errors, continue with example images
      images = [];
    }
  }
  
  if (images.length === 0) {
    log('  ⚠️  No images found in Drive, using example images\n', 'yellow');
    // Example images if no Drive access
    const exampleImages = [
      { id: 'img_1', name: 'Img-V1', url: 'https://drive.google.com/.../v1.png' },
      { id: 'img_2', name: 'Img-V2', url: 'https://drive.google.com/.../v2.png' },
      { id: 'img_3', name: 'Img-V3', url: 'https://drive.google.com/.../v3.png' }
    ];
    images.push(...exampleImages);
  }

  log('  ✅ Found ' + images.length + ' images\n', 'green');

  // Step 2: Fetch text from Sheets or use example with error handling
  log('  📥 Fetching text variations...\n', 'blue');
  let textVariations;
  if (sheetId) {
    try {
      textVariations = await fetchTextFromSheet(sheetId);
      if (!textVariations || Object.keys(textVariations).length === 0) {
        throw new Error('No data found in sheet');
      }
    } catch (error) {
      log('  ⚠️  Error reading sheet: ' + error.message + '. Using example data.\n', 'yellow');
      textVariations = getExampleText();
    }
  } else {
    textVariations = getExampleText();
  }

  log('  ✅ Text loaded:\n', 'green');
  Object.keys(textVariations).forEach(key => {
    log('     - ' + key + ': ' + textVariations[key].length + ' items\n', 'blue');
  });

  // Step 3: Generate combinations with URL variants
  log('  🔄 Generating combinations...\n', 'blue');
  const combinations = generateCombinations(images, textVariations, {
    adGroup,
    subTheme: subThemeStr,
    fullLpUrl,
    miniLpUrl
  });

  log('  ✅ Generated ' + combinations.length + ' ad variations\n', 'green');

  // Step 4: Save everything with error handling
  log('  💾 Saving to ' + outputDir + '...\n', 'blue');
  try {
    await saveCombinations(combinations, outputDir, { adGroup, subThemeStr, fullLpUrl, miniLpUrl });
  } catch (error) {
    log('\n❌ Failed to save combinations: ' + error.message + '\n', 'yellow');
    console.error('Save error:', error);
    throw error;
  }

  // Final summary
  console.log('');
  console.log('════════════════════════════════════════════════════════════');
  log('          ✅ Generation Complete!', 'green');
  console.log('════════════════════════════════════════════════════════════');
  console.log('');
  console.log('  📁 Output Directory: ' + outputDir);
  console.log('  📝 Total Variations: ' + combinations.length);
  console.log('  🔗 Landing Pages: 2 (FULL_LP + Mini_LP)');
  console.log('');
  console.log('  Files created:');
  console.log('    ├── manifest.json     - All combinations');
  console.log('    ├── summary.txt       - Human-readable');
  console.log('    └── ads/              - Individual ad files');
  console.log('');
  console.log('  Ad Title Format:');
  console.log('    ' + adGroup + subThemeStr + ' | {Theme} | Img-V{1-3}_FULL_LP');
  console.log('    ' + adGroup + subThemeStr + ' | {Theme} | Img-V{1-3}_Mini_LP');
  console.log('');
}

/**
 * Create mini landing page URL from full URL
 * @param {string} fullUrl - Full landing page URL
 * @param {string} suffix - Suffix to add (default: '-min')
 * @returns {string} - Mini LP URL
 * @throws {Error} - If URL is invalid
 */
function createMiniLpUrl(fullUrl, suffix = '-min') {
  try {
    const url = new URL(fullUrl);
    const pathname = url.pathname;
    
    // Add suffix before the last segment or at the end
    if (pathname.endsWith('/')) {
      url.pathname = pathname.slice(0, -1) + suffix + '/';
    } else {
      const parts = pathname.split('/').filter(p => p);
      if (parts.length > 0) {
        const lastPart = parts[parts.length - 1];
        parts[parts.length - 1] = lastPart + suffix;
        url.pathname = '/' + parts.join('/');
      } else {
        url.pathname = suffix;
      }
    }
    
    return url.toString();
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(`Invalid URL format: ${fullUrl}`);
    }
    throw error;
  }
}

async function fetchImagesFromDrive(folderPath) {
  try {
    // Find folder
    const folder = await drive.files.list({
      q: "name='" + folderPath + "' and mimeType='application/vnd.google-apps.folder' and trashed=false",
      fields: 'files(id)'
    });

    if (!folder.data.files.length) {
      log('  ⚠️  Folder not found: ' + folderPath + '\n', 'yellow');
      return [];
    }

    const folderId = folder.data.files[0].id;

    // List images (including shortcuts)
    const images = await drive.files.list({
      q: "'" + folderId + "' in parents and trashed=false and (mimeType contains 'image/' or mimeType='application/vnd.google-apps.shortcut')",
      fields: 'files(id, name, mimeType, webViewLink, thumbnailLink)'
    });

    return images.data.files.map(file => ({
      id: file.id,
      name: file.name.replace(/\.[^/.]+$/, ''), // Remove extension
      type: file.mimeType,
      url: file.webViewLink,
      isShortcut: file.mimeType === 'application/vnd.google-apps.shortcut'
    }));
  } catch (error) {
    // Log error with context
    console.error('Error fetching images from Drive:', error);
    throw error; // Re-throw to let caller handle
  }
}

async function fetchTextFromSheet(sheetId) {
  try {
    const meta = await sheets.spreadsheets.get({ spreadsheetId: sheetId });
    const sheetsList = meta.data.sheets.map(s => s.properties.title);
    const variations = {};

    for (const sheetName of sheetsList) {
      // Sanitize sheet name to prevent injection
      const sanitizedName = sanitizeSheetName(sheetName);
      if (!sanitizedName) {
        continue; // Skip invalid sheet names
      }

      const result = await sheets.spreadsheets.values.get({
        spreadsheetId: sheetId,
        range: sanitizedName + '!A:A'
      });

      if (result.data.values && result.data.values.length > 1) {
        const values = result.data.values.slice(1).map(row => row[0]).filter(v => v);
        if (values.length > 0) {
          variations[sanitizedName.toLowerCase()] = values;
        }
      }
    }

    return variations;
  } catch (error) {
    console.error('Error reading Google Sheet:', error);
    throw error; // Re-throw to let caller handle
  }
}

function getExampleText() {
  return {
    themes: [
      'Salesforce-Communities',
      'Boss-Wants-AI',
      'Enterprise-Ready',
      'ROI-Driven'
    ],
    headlines: [
      '7 Lessons from Agentforce Pioneers',
      'Why Your Boss Wants AI Agents',
      'Enterprise AI That Actually Works',
      'Drive ROI with Agentforce'
    ],
    ctas: [
      'Download Guide',
      'Learn More',
      'Get Started'
    ]
  };
}

function generateCombinations(images, textVariations, options) {
  const { adGroup, subTheme, fullLpUrl, miniLpUrl } = options;
  const combinations = [];
  
  const themes = textVariations.themes || textVariations.theme || [];
  const headlines = textVariations.headlines || textVariations.headline || [];
  const ctas = textVariations.ctas || textVariations.cta || [];

  // Generate for each landing page variant
  const lpVariants = [
    { type: 'FULL_LP', url: fullLpUrl },
    { type: 'Mini_LP', url: miniLpUrl }
  ];

  let count = 0;

  for (const image of images) {
    for (const theme of themes) {
      const themeStr = theme ? ' | ' + theme : '';
      for (const headline of headlines) {
        for (const cta of ctas) {
          for (const lp of lpVariants) {
            // Format: AdGroup | SubTheme | Theme | Img-V1_LP-Type
            const adTitle = adGroup + subTheme + themeStr + ' | ' + image.name + '_' + lp.type;
            
            combinations.push({
              id: 'ad_' + uuidv4(),
              ad_title: adTitle,
              ad_group: adGroup,
              sub_theme: subTheme.replace(' | ', ''),
              theme: theme,
              image: image,
              headline: headline,
              cta: cta,
              landing_page: lp.url,
              lp_variant: lp.type,
              platform: 'reddit',
              created: new Date().toISOString()
            });
            count++;
          }
        }
      }
    }
  }

  return combinations;
}

async function saveCombinations(combinations, outputDir, options) {
  const { adGroup, subTheme, fullLpUrl, miniLpUrl } = options;

  // Save manifest
  const manifest = {
    config: {
      ad_group: adGroup,
      sub_theme: subTheme,
      landing_pages: {
        full: fullLpUrl,
        mini: miniLpUrl
      },
      generated: new Date().toISOString(),
      total_variations: combinations.length
    },
    combinations: combinations
  };

  const SUMMARY_PREVIEW_LIMIT = 20;

  // Save manifest using async file operations
  await fs.writeFile(
    path.join(outputDir, 'manifest.json'),
    JSON.stringify(manifest, null, 2)
  );

  // Save summary
  let summary = 'Ad Creative Summary\n';
  summary += '═══════════════════════════════════════\n\n';
  summary += 'Ad Group:        ' + adGroup + '\n';
  summary += 'Sub-theme:       ' + (subTheme || 'None') + '\n';
  summary += 'Landing Pages:\n';
  summary += '  FULL_LP: ' + fullLpUrl + '\n';
  summary += '  Mini_LP: ' + miniLpUrl + '\n';
  summary += 'Total Variations: ' + combinations.length + '\n\n';
  summary += '═══════════════════════════════════════\n';
  summary += 'Generated Ads\n';
  summary += '═══════════════════════════════════════\n\n';

  combinations.slice(0, SUMMARY_PREVIEW_LIMIT).forEach((ad, i) => {
    summary += (i + 1) + '. ' + ad.ad_title + '\n';
    summary += '   Headline: ' + ad.headline + '\n';
    summary += '   CTA: ' + ad.cta + '\n';
    summary += '   LP: ' + ad.lp_variant + '\n\n';
  });

  if (combinations.length > SUMMARY_PREVIEW_LIMIT) {
    summary += '... and ' + (combinations.length - SUMMARY_PREVIEW_LIMIT) + ' more variations\n';
  }

  await fs.writeFile(path.join(outputDir, 'summary.txt'), summary);

  // Save individual ad files using async operations with concurrency control
  const writePromises = combinations.map(ad =>
    fs.writeFile(
      path.join(outputDir, 'ads', ad.id + '.json'),
      JSON.stringify(ad, null, 2)
    )
  );

  await Promise.all(writePromises);
}

main().catch(error => {
  console.error('\n❌ Fatal error:', error.message);
  console.error(error);
  process.exit(1);
});
