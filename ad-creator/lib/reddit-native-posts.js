/**
 * Reddit Native API - Post Creation
 * 
 * Creates posts on subreddits with custom headline, body, image, CTA
 */

const https = require('https');

const NATIVE_CONFIG = {
  userAgent: 'ad-creator/2.0'
};

/**
 * Create a text post
 */
async function createTextPost(accessToken, subreddit, title, body) {
  return new Promise((resolve, reject) => {
    const params = new URLSearchParams({
      sr: subreddit,
      title: title,
      text: body,
      kind: 'self',
      send_replies: 'false'
    });

    const req = https.request({
      hostname: 'oauth.reddit.com',
      path: '/api/submit',
      method: 'POST',
      headers: {
        'User-Agent': NATIVE_CONFIG.userAgent,
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': params.toString().length
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode !== 200) {
          reject(new Error(`Post creation failed: ${res.statusCode} - ${data}`));
          return;
        }

        try {
          const response = JSON.parse(data);
          if (response.json?.errors?.length > 0) {
            reject(new Error(`Post errors: ${response.json.errors.join(', ')}`));
          } else {
            resolve({
              postId: response.json?.data?.id,
              url: response.json?.data?.url,
              fullName: response.json?.data?.name
            });
          }
        } catch (error) {
          reject(new Error(`Failed to parse response: ${error.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(params.toString());
    req.end();
  });
}

/**
 * Create a link post (with URL destination)
 */
async function createLinkPost(accessToken, subreddit, title, url) {
  return new Promise((resolve, reject) => {
    const params = new URLSearchParams({
      sr: subreddit,
      title: title,
      url: url,
      kind: 'link',
      send_replies: 'false'
    });

    const req = https.request({
      hostname: 'oauth.reddit.com',
      path: '/api/submit',
      method: 'POST',
      headers: {
        'User-Agent': NATIVE_CONFIG.userAgent,
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': params.toString().length
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          resolve({
            postId: response.json?.data?.id,
            url: response.json?.data?.url,
            fullName: response.json?.data?.name
          });
        } catch (error) {
          reject(new Error(`Failed to parse response: ${error.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(params.toString());
    req.end();
  });
}

/**
 * Upload image and get media URL
 */
async function uploadImage(accessToken, imagePath) {
  // Note: Reddit's native image upload requires multipart form-data
  // This is a placeholder - actual implementation would use form-data library
  throw new Error('Image upload requires additional implementation with form-data library');
}

/**
 * Create post with image (media post)
 */
async function createMediaPost(accessToken, subreddit, title, imageUrl, flairId = null) {
  return new Promise((resolve, reject) => {
    const params = new URLSearchParams({
      sr: subreddit,
      title: title,
      url: imageUrl,
      kind: 'link',
      send_replies: 'false'
    });

    if (flairId) {
      params.append('flair_id', flairId);
    }

    const req = https.request({
      hostname: 'oauth.reddit.com',
      path: '/api/submit',
      method: 'POST',
      headers: {
        'User-Agent': NATIVE_CONFIG.userAgent,
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': params.toString().length
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          resolve({
            postId: response.json?.data?.id,
            url: response.json?.data?.url,
            fullName: response.json?.data?.name
          });
        } catch (error) {
          reject(new Error(`Failed to parse response: ${error.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(params.toString());
    req.end();
  });
}

/**
 * Get user's subreddits
 */
async function getUserSubreddits(accessToken) {
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'oauth.reddit.com',
      path: '/api/v1/mine/subreddits?limit=100',
      method: 'GET',
      headers: {
        'User-Agent': NATIVE_CONFIG.userAgent,
        'Authorization': `Bearer ${accessToken}`
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          resolve(response.data?.children?.map(s => ({
            name: s.data.display_name,
            id: s.data.id,
            url: s.data.url
          })) || []);
        } catch (error) {
          reject(new Error(`Failed to parse subreddits: ${error.message}`));
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

module.exports = {
  createTextPost,
  createLinkPost,
  createMediaPost,
  uploadImage,
  getUserSubreddits
};
