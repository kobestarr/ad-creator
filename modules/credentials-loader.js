/**
 * Centralized Credentials Loader
 * 
 * Provides secure access to API credentials stored in /root/.credentials/
 * Usage: const { getCredential, checkReoonLimit } = require('./credentials-loader');
 */

const fs = require('fs');
const path = require('path');

const CREDENTIALS_PATH = '/root/.credentials/api-keys.json';
const USAGE_TRACKER_PATH = '/root/.credentials/usage-tracker.json';

/**
 * Load credentials from JSON file
 */
function loadCredentials() {
  try {
    const data = fs.readFileSync(CREDENTIALS_PATH, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    throw new Error(`Failed to load credentials: ${error.message}`);
  }
}

/**
 * Get a specific credential value
 * @param {string} service - Service name (e.g., 'reoon', 'apify')
 * @param {string} key - Key name (e.g., 'apiKey', 'apiToken')
 * @returns {string|null} Credential value or null if not found
 */
function getCredential(service, key) {
  const credentials = loadCredentials();
  
  if (!credentials[service]) {
    console.warn(`Service '${service}' not found in credentials`);
    return null;
  }
  
  if (credentials[service][key] === 'PENDING') {
    console.warn(`Credential '${service}.${key}' is pending - not yet configured`);
    return null;
  }
  
  return credentials[service][key] || null;
}

/**
 * Get all credentials for a service
 * @param {string} service - Service name
 * @returns {object|null} Service credentials or null
 */
function getServiceCredentials(service) {
  const credentials = loadCredentials();
  return credentials[service] || null;
}

/**
 * Check Reoon daily limit and remaining quota
 * @returns {object} { remaining: number, used: number, limit: number, canUse: boolean }
 */
function checkReoonLimit() {
  try {
    const tracker = JSON.parse(fs.readFileSync(USAGE_TRACKER_PATH, 'utf8'));
    const today = new Date().toISOString().split('T')[0];
    
    // Reset if new day
    if (tracker.reoon.date !== today) {
      tracker.reoon.date = today;
      tracker.reoon.used = 0;
      tracker.reoon.remaining = tracker.reoon.limit;
      tracker.reoon.lastReset = new Date().toISOString();
      fs.writeFileSync(USAGE_TRACKER_PATH, JSON.stringify(tracker, null, 2));
    }
    
    return {
      remaining: tracker.reoon.remaining,
      used: tracker.reoon.used,
      limit: tracker.reoon.limit,
      canUse: tracker.reoon.remaining > 0
    };
  } catch (error) {
    console.error(`Failed to check Reoon limit: ${error.message}`);
    return { remaining: 0, used: 0, limit: 500, canUse: false };
  }
}

/**
 * Record Reoon usage (increment counter)
 * @param {number} count - Number of verifications used (default: 1)
 * @returns {boolean} Success status
 */
function recordReoonUsage(count = 1) {
  try {
    const tracker = JSON.parse(fs.readFileSync(USAGE_TRACKER_PATH, 'utf8'));
    const today = new Date().toISOString().split('T')[0];
    
    // Reset if new day
    if (tracker.reoon.date !== today) {
      tracker.reoon.date = today;
      tracker.reoon.used = 0;
      tracker.reoon.remaining = tracker.reoon.limit;
    }
    
    tracker.reoon.used += count;
    tracker.reoon.remaining = Math.max(0, tracker.reoon.limit - tracker.reoon.used);
    
    fs.writeFileSync(USAGE_TRACKER_PATH, JSON.stringify(tracker, null, 2));
    
    // Warn if approaching limit
    if (tracker.reoon.remaining < 50) {
      console.warn(`⚠️  Reoon daily limit warning: ${tracker.reoon.remaining} remaining (used: ${tracker.reoon.used}/${tracker.reoon.limit})`);
    }
    
    return true;
  } catch (error) {
    console.error(`Failed to record Reoon usage: ${error.message}`);
    return false;
  }
}

/**
 * Load environment variables from .env file
 * @returns {object} Environment variables as object
 */
function loadEnv() {
  try {
    const envPath = '/root/.credentials/.env';
    const envContent = fs.readFileSync(envPath, 'utf8');
    const env = {};
    
    envContent.split('\n').forEach(line => {
      line = line.trim();
      if (line && !line.startsWith('#')) {
        const [key, ...valueParts] = line.split('=');
        if (key && valueParts.length > 0) {
          env[key.trim()] = valueParts.join('=').trim();
        }
      }
    });
    
    return env;
  } catch (error) {
    console.error(`Failed to load .env: ${error.message}`);
    return {};
  }
}

module.exports = {
  getCredential,
  getServiceCredentials,
  checkReoonLimit,
  recordReoonUsage,
  loadEnv,
  loadCredentials
};
