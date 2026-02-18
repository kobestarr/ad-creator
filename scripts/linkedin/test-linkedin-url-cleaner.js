/**
 * Test file for LinkedIn URL Cleaner
 * Demonstrates the functionality with various LinkedIn URLs
 */

const LinkedInUrlCleaner = require('./linkedin-url-cleaner.js');

function testUrlCleaner() {
  const cleaner = new LinkedInUrlCleaner();
  
  console.log('🧹 LinkedIn URL Cleaner - Test Suite\n');
  
  // Test cases with different types of LinkedIn URLs and tracking parameters
  const testCases = [
    // Job URLs
    {
      name: 'Job URL with trk parameter',
      input: 'https://www.linkedin.com/jobs/view/java-developer-at-mango-analytics-4368116790?trk=public_jobs_topcard-title',
      expected: 'https://www.linkedin.com/jobs/view/java-developer-at-mango-analytics-4368116790'
    },
    {
      name: 'Job URL with multiple tracking parameters',
      input: 'https://www.linkedin.com/jobs/view/senior-software-engineer-at-tech-corp-1234567890?trk=public_jobs_topcard-title&utm_source=linkedin&utm_medium=paid-social&utm_campaign=hiring',
      expected: 'https://www.linkedin.com/jobs/view/senior-software-engineer-at-tech-corp-1234567890'
    },
    
    // Company URLs
    {
      name: 'Company URL with trk parameter',
      input: 'https://www.linkedin.com/company/mango-analytics-ai?trk=public_jobs_topcard-org-name',
      expected: 'https://www.linkedin.com/company/mango-analytics-ai'
    },
    {
      name: 'Company URL with multiple parameters',
      input: 'https://www.linkedin.com/company/google?trk=companies_directory&originalSubdomain=www',
      expected: 'https://www.linkedin.com/company/google'
    },
    
    // Profile URLs
    {
      name: 'Profile URL with tracking',
      input: 'https://www.linkedin.com/in/john-doe-123456?trk=public_profile_browsemap&lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3B1234567890%3D',
      expected: 'https://www.linkedin.com/in/john-doe-123456'
    },
    {
      name: 'Profile URL with session tracking',
      input: 'https://www.linkedin.com/in/jane-smith?sessionToken=abc123&trk=nav_response',
      expected: 'https://www.linkedin.com/in/jane-smith'
    },
    
    // Feed URLs
    {
      name: 'Feed URL with tracking',
      input: 'https://www.linkedin.com/feed/update/urn:li:share:1234567890?trk=homepage-basic_sign-in-submit',
      expected: 'https://www.linkedin.com/feed/update/urn:li:share:1234567890'
    },
    
    // School URLs
    {
      name: 'School URL with tracking',
      input: 'https://www.linkedin.com/school/stanford-university?trk=public_profile_school_profile',
      expected: 'https://www.linkedin.com/school/stanford-university'
    },
    
    // Group URLs
    {
      name: 'Group URL with tracking',
      input: 'https://www.linkedin.com/groups/1234567?trk=groups_guest_browse',
      expected: 'https://www.linkedin.com/groups/1234567'
    },
    
    // Non-LinkedIn URLs (should remain unchanged)
    {
      name: 'Non-LinkedIn URL',
      input: 'https://www.google.com/search?q=linkedin&utm_source=browser',
      expected: 'https://www.google.com/search?q=linkedin&utm_source=browser'
    },
    
    // Edge cases
    {
      name: 'URL with no parameters',
      input: 'https://www.linkedin.com/jobs/view/software-engineer-123456',
      expected: 'https://www.linkedin.com/jobs/view/software-engineer-123456'
    },
    {
      name: 'Invalid URL',
      input: 'not-a-valid-url',
      expected: 'not-a-valid-url'
    },
    {
      name: 'Empty string',
      input: '',
      expected: ''
    }
  ];
  
  let passed = 0;
  let failed = 0;
  
  testCases.forEach((testCase, index) => {
    console.log(`Test ${index + 1}: ${testCase.name}`);
    console.log(`Input:    ${testCase.input}`);
    
    const result = cleaner.cleanUrl(testCase.input);
    console.log(`Output:   ${result}`);
    console.log(`Expected: ${testCase.expected}`);
    
    if (result === testCase.expected) {
      console.log('✅ PASSED\n');
      passed++;
    } else {
      console.log('❌ FAILED\n');
      failed++;
    }
  });
  
  console.log(`\n📊 Test Results: ${passed} passed, ${failed} failed`);
  
  // Test additional functionality
  console.log('\n🔍 Additional Functionality Tests:');
  
  // Test hasTrackingParams method
  const urlsWithTracking = [
    'https://www.linkedin.com/jobs/view/123?trk=test',
    'https://www.linkedin.com/company/test?utm_source=linkedin',
    'https://www.linkedin.com/in/profile?sessionToken=abc123'
  ];
  
  urlsWithTracking.forEach(url => {
    console.log(`Has tracking params: ${url} → ${cleaner.hasTrackingParams(url)}`);
  });
  
  // Test getBaseUrl method
  console.log(`\nBase URL extraction:`);
  const testUrl = 'https://www.linkedin.com/jobs/view/123456?trk=test&param=value';
  console.log(`Original: ${testUrl}`);
  console.log(`Base:     ${cleaner.getBaseUrl(testUrl)}`);
  
  // Test batch cleaning
  console.log(`\nBatch cleaning:`);
  const dirtyUrls = [
    'https://www.linkedin.com/jobs/view/123?trk=test1',
    'https://www.linkedin.com/company/abc?utm_source=linkedin',
    'https://www.linkedin.com/in/profile?trk=profile'
  ];
  
  const cleanUrls = cleaner.cleanUrls(dirtyUrls);
  console.log('Original URLs:', dirtyUrls);
  console.log('Cleaned URLs: ', cleanUrls);
}

// Run the tests
if (require.main === module) {
  testUrlCleaner();
}