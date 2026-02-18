# LinkedIn URL Cleaner

A robust JavaScript utility for removing tracking parameters from LinkedIn URLs while preserving the base URL structure.

## Features

- ✅ Removes all LinkedIn tracking parameters (`?trk=`, `?utm_source=`, etc.)
- ✅ Preserves base URL structure and legitimate parameters
- ✅ Handles various LinkedIn URL types (jobs, companies, profiles, feeds, schools, groups)
- ✅ Safe handling of invalid URLs and edge cases
- ✅ Batch processing support
- ✅ Browser and Node.js compatible
- ✅ Comprehensive tracking parameter detection

## Installation

```javascript
// Copy the linkedin-url-cleaner.js file to your project
const LinkedInUrlCleaner = require('./linkedin-url-cleaner.js');
```

## Usage

### Basic Usage

```javascript
const LinkedInUrlCleaner = require('./linkedin-url-cleaner.js');
const cleaner = new LinkedInUrlCleaner();

// Clean a single URL
const dirtyUrl = 'https://www.linkedin.com/jobs/view/java-developer-at-mango-analytics-4368116790?trk=public_jobs_topcard-title';
const cleanUrl = cleaner.cleanUrl(dirtyUrl);
console.log(cleanUrl); // https://www.linkedin.com/jobs/view/java-developer-at-mango-analytics-4368116790

// Clean company URLs
const companyUrl = 'https://www.linkedin.com/company/mango-analytics-ai?trk=public_jobs_topcard-org-name';
const cleanCompanyUrl = cleaner.cleanUrl(companyUrl);
console.log(cleanCompanyUrl); // https://www.linkedin.com/company/mango-analytics-ai
```

### Batch Processing

```javascript
// Clean multiple URLs at once
const dirtyUrls = [
  'https://www.linkedin.com/jobs/view/123?trk=test1',
  'https://www.linkedin.com/company/abc?utm_source=linkedin',
  'https://www.linkedin.com/in/profile?trk=profile'
];

const cleanUrls = cleaner.cleanUrls(dirtyUrls);
console.log(cleanUrls);
// [
//   'https://www.linkedin.com/jobs/view/123',
//   'https://www.linkedin.com/company/abc',
//   'https://www.linkedin.com/in/profile'
// ]
```

### Check for Tracking Parameters

```javascript
// Check if a URL contains tracking parameters
const hasTracking = cleaner.hasTrackingParams('https://www.linkedin.com/jobs/view/123?trk=test');
console.log(hasTracking); // true
```

### Extract Base URL

```javascript
// Get the base URL without any parameters
const baseUrl = cleaner.getBaseUrl('https://www.linkedin.com/jobs/view/123456?trk=test&param=value');
console.log(baseUrl); // https://www.linkedin.com/jobs/view/123456
```

## Examples

### Job URLs
```javascript
// Input:  https://www.linkedin.com/jobs/view/java-developer-at-mango-analytics-4368116790?trk=public_jobs_topcard-title
// Output: https://www.linkedin.com/jobs/view/java-developer-at-mango-analytics-4368116790

// Input:  https://www.linkedin.com/jobs/view/senior-software-engineer-at-tech-corp-1234567890?trk=public_jobs_topcard-title&utm_source=linkedin&utm_medium=paid-social&utm_campaign=hiring
// Output: https://www.linkedin.com/jobs/view/senior-software-engineer-at-tech-corp-1234567890
```

### Company URLs
```javascript
// Input:  https://www.linkedin.com/company/mango-analytics-ai?trk=public_jobs_topcard-org-name
// Output: https://www.linkedin.com/company/mango-analytics-ai

// Input:  https://www.linkedin.com/company/google?trk=companies_directory&originalSubdomain=www
// Output: https://www.linkedin.com/company/google
```

### Profile URLs
```javascript
// Input:  https://www.linkedin.com/in/john-doe-123456?trk=public_profile_browsemap&lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3B1234567890%3D
// Output: https://www.linkedin.com/in/john-doe-123456
```

## Tracking Parameters Removed

The cleaner removes these known LinkedIn tracking parameters:

- `trk` and all `trk_*` variants
- All UTM parameters (`utm_source`, `utm_medium`, `utm_campaign`, etc.)
- Session tokens and CSRF tokens
- LinkedIn-specific tracking (`lipi`, `licu`, `liam`, etc.)
- Referral and source parameters
- Any other parameters that match tracking patterns

## API Reference

### `cleanUrl(url)`
Cleans a single URL by removing tracking parameters.
- **Parameters:** `url` (string) - The URL to clean
- **Returns:** `string` - The cleaned URL

### `cleanUrls(urls)`
Cleans multiple URLs at once.
- **Parameters:** `urls` (array) - Array of URLs to clean
- **Returns:** `array` - Array of cleaned URLs

### `hasTrackingParams(url)`
Checks if a URL contains tracking parameters.
- **Parameters:** `url` (string) - The URL to check
- **Returns:** `boolean` - True if tracking parameters are found

### `getBaseUrl(url)`
Extracts the base URL without any parameters.
- **Parameters:** `url` (string) - The URL to process
- **Returns:** `string` - The base URL

## Browser Usage

Include the script in your HTML:

```html
<script src="linkedin-url-cleaner.js"></script>
<script>
  const cleaner = new LinkedInUrlCleaner();
  const cleanUrl = cleaner.cleanUrl('https://www.linkedin.com/jobs/view/123?trk=test');
  console.log(cleanUrl);
</script>
```

## Error Handling

The cleaner safely handles:
- Invalid URLs (returns original input)
- Empty strings
- Non-LinkedIn URLs (returns unchanged)
- Malformed URLs

## Testing

Run the comprehensive test suite:

```bash
node test-linkedin-url-cleaner.js
```

## License

This utility is provided as-is for cleaning LinkedIn URLs. Use responsibly and in accordance with LinkedIn's terms of service.