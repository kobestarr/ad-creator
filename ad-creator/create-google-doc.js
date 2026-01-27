/**
 * Create Google Doc with ad permutations
 * 
 * Requires Google Service Account credentials
 * 
 * Setup:
 * 1. Create Google Cloud project
 * 2. Enable Google Docs API and Google Drive API
 * 3. Create service account, download JSON credentials
 * 4. Share a Google Doc folder with the service account email
 * 5. Set GOOGLE_SERVICE_ACCOUNT_EMAIL and GOOGLE_PRIVATE_KEY env vars
 */

const { google } = require('googleapis');
const fs = require('fs');

// Load credentials from environment
const SERVICE_ACCOUNT_EMAIL = process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
const PRIVATE_KEY = process.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, '\n');
const DOC_FOLDER_ID = process.env.GOOGLE_DOC_FOLDER_ID;

async function createPermutationsDoc(permutations, docTitle = 'Reddit Ad Permutations') {
  
  if (!SERVICE_ACCOUNT_EMAIL || !PRIVATE_KEY) {
    throw new Error('Missing Google credentials. Set GOOGLE_SERVICE_ACCOUNT_EMAIL and GOOGLE_PRIVATE_KEY');
  }

  // Authenticate
  const auth = new google.auth.JWT(
    SERVICE_ACCOUNT_EMAIL,
    null,
    PRIVATE_KEY,
    ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
  );

  const docs = google.docs({ version: 'v1', auth });
  const drive = google.drive({ version: 'v3', auth });

  console.log('📄 Creating Google Doc...');

  // Create the document
  const createResponse = await docs.documents.create({
    requestBody: { title: docTitle }
  });

  const documentId = createResponse.data.documentId;
  console.log(`   Document ID: ${documentId}`);

  // Build table content
  const tableRows = [];
  
  // Header row
  tableRows.push([
    'Image', 'Headline', 'Body', 'CTA', 'URL'
  ]);

  // Data rows (limit to 50 per doc - Google Docs has limits)
  const maxRows = Math.min(permutations.length, 50);
  for (let i = 0; i < maxRows; i++) {
    const p = permutations[i];
    tableRows.push([
      p.image,
      p.headline,
      p.body,
      p.cta,
      p.url
    ]);
  }

  // Build the document content
  const requests = [];

  // Add title
  requests.push({
    insertText: {
      location: { index: 1 },
      text: `Reddit Ad Permutations\n\nGenerated: ${new Date().toLocaleString()}\n\n`
    }
  });

  // Add table
  requests.push({
    insertTable: {
      rows: tableRows.length,
      columns: 5,
      location: { index: 1 }
    }
  });

  // Fill table cells
  for (let row = 0; row < tableRows.length; row++) {
    for (let col = 0; col < tableRows[row].length; col++) {
      const cellContent = tableRows[row][col];
      // Calculate cell index (approximate - table starts at index after title)
      const tableStartIndex = 1 + docTitle.length + 40 + (row * 5 * 100) + (col * 20);
      
      if (cellContent) {
        requests.push({
          insertText: {
            location: { index: 1 },
            text: cellContent
          }
        });
      }
    }
  }

  // Execute batch update
  await docs.documents.batchUpdate({
    documentId: documentId,
    requestBody: { requests }
  });

  console.log(`   Table created with ${tableRows.length} rows`);

  // Move to folder if specified
  if (DOC_FOLDER_ID) {
    await drive.files.update({
      fileId: documentId,
      addParents: DOC_FOLDER_ID,
      fields: 'id, name, webViewLink'
    });
  }

  // Make it publicly accessible (or share with specific email)
  await drive.permissions.create({
    fileId: documentId,
    requestBody: {
      role: 'reader',
      type: 'anyone'
    }
  });

  // Get the shareable link
  const file = await drive.files.get({
    fileId: documentId,
    fields: 'name, webViewLink'
  });

  console.log('');
  console.log('═'.repeat(60));
  console.log('✅ GOOGLE DOC CREATED!');
  console.log('═'.repeat(60));
  console.log('');
  console.log(`📄 Document: ${file.data.name}`);
  console.log(`🔗 Link: ${file.data.webViewLink}`);
  console.log('');
  console.log('Open this link to see all your ad permutations!');
  console.log('');

  return {
    documentId,
    url: file.data.webViewLink,
    name: file.data.name
  };
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  
  // Simple demo if no args
  const permutations = [
    { image: 'v1.jpg', headline: 'Headline 1', body: 'Body 1', cta: 'DOWNLOAD', url: 'https://example.com/1' },
    { image: 'v1.jpg', headline: 'Headline 1', body: 'Body 1', cta: 'LEARN_MORE', url: 'https://example.com/1' },
    { image: 'v2.jpg', headline: 'Headline 2', body: 'Body 2', cta: 'DOWNLOAD', url: 'https://example.com/2' },
  ];

  if (args.includes('--demo') || args.length === 0) {
    console.log('');
    console.log('Reddit Ad Permutations - Google Doc Creator');
    console.log('');
    console.log('Usage:');
    console.log('  node create-google-doc.js --demo          # Run demo');
    console.log('  node create-google-doc.js --help          # Show this help');
    console.log('');
    console.log('Setup required:');
    console.log('  export GOOGLE_SERVICE_ACCOUNT_EMAIL=xxx@project.iam.gserviceaccount.com');
    console.log('  export GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----..."');
    console.log('  export GOOGLE_DOC_FOLDER_ID=folder_id     # Optional');
    console.log('');
    
    if (!SERVICE_ACCOUNT_EMAIL) {
      console.log('⚠️  Google credentials not configured');
      console.log('   Set the environment variables above to create Google Docs');
    } else {
      console.log('✅ Google credentials configured');
      try {
        await createPermutationsDoc(permutations, 'Demo - Reddit Ad Permutations');
      } catch (error) {
        console.log('Error:', error.message);
      }
    }
    return;
  }

  if (args.includes('--help')) {
    console.log('Reddit Ad Permutations - Google Doc Creator');
    console.log('');
    console.log('This tool creates a Google Doc with all ad permutations.');
    console.log('');
    console.log('Required environment variables:');
    console.log('  GOOGLE_SERVICE_ACCOUNT_EMAIL');
    console.log('  GOOGLE_PRIVATE_KEY');
    console.log('');
    console.log('Optional:');
    console.log('  GOOGLE_DOC_FOLDER_ID - Folder to save doc in');
    return;
  }
}

main().catch(console.error);
