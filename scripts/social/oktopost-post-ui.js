/**
 * Oktopost UI Automation via Playwright
 * Posts content to Oktopost through the browser UI (alternative to API method)
 * Note: API confirmed working as of Feb 2026 - prefer post-to-oktopost.py for API-based posting
 * 
 * Usage: node oktopost-post-ui.js "LinkedIn" "CampaignID" "Post content here"
 */

const { chromium } = require('playwright');

const OKTOPOST_URL = 'https://app.oktopost.com/login';
const EMAIL = 'kobi.omenaka@bluprintx.com';
// Note: Password must be set in environment variable
const PASSWORD = process.env.OKTOPOST_PASSWORD;

async function login(page) {
  console.log('Logging into Oktopost...');
  await page.goto(OKTOPOST_URL);
  await page.fill('input[type="email"]', EMAIL);
  await page.fill('input[type="password"]', PASSWORD);
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard**', { timeout: 30000 });
  console.log('✅ Logged in successfully');
}

async function navigateToCampaign(page, campaignId) {
  console.log(`Navigating to campaign ${campaignId}...`);
  await page.goto(`https://app.oktopost.com/campaign/${campaignId}/message`);
  await page.waitForLoadState('networkidle');
  console.log('✅ On campaign page');
}

async function createPost(page, network, content) {
  console.log(`Creating ${network} post...`);
  
  // Click "New Message" button
  await page.click('button:has-text("New Message"), a:has-text("New Message")');
  
  // Select network
  const networkSelect = await page.$('select, div[role="combobox"]');
  if (networkSelect) {
    await networkSelect.click();
    await page.click(`div[role="option"]:has-text("${network}")`);
  }
  
  // Fill content
  const contentEditor = await page.$('div[contenteditable="true"], textarea');
  if (contentEditor) {
    await contentEditor.fill(content);
  }
  
  // Click Save as Draft
  await page.click('button:has-text("Save as Draft"), button:has-text("Save Draft")');
  
  // Wait for success
  await page.waitForTimeout(2000);
  console.log(`✅ ${network} draft saved`);
}

async function main() {
  const network = process.argv[2] || 'LinkedIn';
  const campaignId = process.argv[3] || '002g5m4amrtu2xs';
  const content = process.argv[4] || 'Test post from Playwright';
  
  if (!PASSWORD) {
    console.log('❌ Error: Set OKTOPOST_PASSWORD environment variable');
    console.log('Usage: OKTOPOST_PASSWORD=yourpass node oktopost-post-ui.js LinkedIn 002g5m4amrtu2xs "Post content"');
    process.exit(1);
  }
  
  console.log(`\n🚀 Creating ${network} post in campaign ${campaignId}`);
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    await login(page);
    await navigateToCampaign(page, campaignId);
    await createPost(page, network, content);
    console.log('\n✅ Post created successfully via UI!');
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await browser.close();
  }
}

main();
