/**
 * LinkedIn URL Cleaner
 * Removes tracking parameters from LinkedIn URLs
 * 
 * Examples:
 * - https://www.linkedin.com/jobs/view/java-developer-at-mango-analytics-4368116790?trk=public_jobs_topcard-title
 *   → https://www.linkedin.com/jobs/view/java-developer-at-mango-analytics-4368116790
 * - https://www.linkedin.com/company/mango-analytics-ai?trk=public_jobs_topcard-org-name
 *   → https://www.linkedin.com/company/mango-analytics-ai
 */

class LinkedInUrlCleaner {
  constructor() {
    // Common LinkedIn tracking parameters to remove
    this.trackingParams = [
      'trk',
      'utm_source',
      'utm_medium',
      'utm_campaign',
      'utm_term',
      'utm_content',
      'utm_id',
      'src',
      'ref',
      'trackingId',
      'trackingid',
      'li_fat_id',
      'li_member_id',
      'li_source',
      'li_campaign',
      'li_medium',
      'li_content',
      'li_term',
      'originalSubdomain',
      'goback',
      'sessionToken',
      'csrfToken',
      'trkInfo',
      'lipi',
      'licu',
      'liam',
      'fts',
      'trk_contact',
      'trk_msg',
      'trk_module',
      'trk_public_profile',
      'trk_profile_view'
    ];
  }

  /**
   * Clean a LinkedIn URL by removing all tracking parameters
   * @param {string} url - The URL to clean
   * @returns {string} - The cleaned URL
   */
  cleanUrl(url) {
    if (!url || typeof url !== 'string') {
      return url;
    }

    try {
      // Parse the URL
      const urlObj = new URL(url);
      
      // Only process LinkedIn URLs
      if (!this.isLinkedInUrl(urlObj)) {
        return url;
      }

      // Remove tracking parameters
      this.trackingParams.forEach(param => {
        urlObj.searchParams.delete(param);
      });

      // Remove any other parameters that might be tracking-related
      // (parameters that are very short or contain common tracking patterns)
      const paramsToDelete = [];
      for (const [key, value] of urlObj.searchParams) {
        if (this.isLikelyTrackingParam(key, value)) {
          paramsToDelete.push(key);
        }
      }
      
      paramsToDelete.forEach(param => {
        urlObj.searchParams.delete(param);
      });

      // Return the cleaned URL
      return urlObj.toString();
    } catch (error) {
      console.warn('Error cleaning URL:', error.message);
      return url;
    }
  }

  /**
   * Check if a URL is a LinkedIn URL
   * @param {URL} urlObj - The URL object to check
   * @returns {boolean} - True if it's a LinkedIn URL
   */
  isLinkedInUrl(urlObj) {
    const hostname = urlObj.hostname.toLowerCase();
    return hostname === 'www.linkedin.com' || 
           hostname === 'linkedin.com' ||
           hostname.endsWith('.linkedin.com');
  }

  /**
   * Check if a parameter is likely a tracking parameter
   * @param {string} key - The parameter key
   * @param {string} value - The parameter value
   * @returns {boolean} - True if it's likely a tracking parameter
   */
  isLikelyTrackingParam(key, value) {
    const keyLower = key.toLowerCase();
    const valueLower = value.toLowerCase();
    
    // Check for common tracking patterns
    const trackingPatterns = [
      'track', 'trk', 'utm_', 'ref', 'src', 'session', 'token',
      'campaign', 'medium', 'source', 'content', 'term', 'id'
    ];
    
    // Check if key contains tracking patterns
    if (trackingPatterns.some(pattern => keyLower.includes(pattern))) {
      return true;
    }
    
    // Check if value looks like a tracking ID (long random strings)
    if (value.length > 20 && /^[a-zA-Z0-9_-]+$/.test(value)) {
      return true;
    }
    
    // Check if value is a common tracking value
    const commonTrackingValues = ['email', 'social', 'paid', 'organic', 'referral'];
    if (commonTrackingValues.includes(valueLower)) {
      return true;
    }
    
    return false;
  }

  /**
   * Clean multiple URLs at once
   * @param {string[]} urls - Array of URLs to clean
   * @returns {string[]} - Array of cleaned URLs
   */
  cleanUrls(urls) {
    if (!Array.isArray(urls)) {
      return [];
    }
    
    return urls.map(url => this.cleanUrl(url));
  }

  /**
   * Extract the base URL without any parameters
   * @param {string} url - The URL to process
   * @returns {string} - The base URL
   */
  getBaseUrl(url) {
    if (!url || typeof url !== 'string') {
      return url;
    }

    try {
      const urlObj = new URL(url);
      urlObj.search = '';
      return urlObj.toString();
    } catch (error) {
      console.warn('Error extracting base URL:', error.message);
      return url;
    }
  }

  /**
   * Check if a URL contains tracking parameters
   * @param {string} url - The URL to check
   * @returns {boolean} - True if the URL contains tracking parameters
   */
  hasTrackingParams(url) {
    if (!url || typeof url !== 'string') {
      return false;
    }

    try {
      const urlObj = new URL(url);
      
      // Check for known tracking parameters
      const hasKnownTracking = this.trackingParams.some(param => 
        urlObj.searchParams.has(param)
      );
      
      if (hasKnownTracking) {
        return true;
      }
      
      // Check for other potential tracking parameters
      for (const [key, value] of urlObj.searchParams) {
        if (this.isLikelyTrackingParam(key, value)) {
          return true;
        }
      }
      
      return false;
    } catch (error) {
      return false;
    }
  }
}

// Export for use in Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = LinkedInUrlCleaner;
}

// Export for use in browsers
if (typeof window !== 'undefined') {
  window.LinkedInUrlCleaner = LinkedInUrlCleaner;
}