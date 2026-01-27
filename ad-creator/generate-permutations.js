#!/usr/bin/env node

/**
 * Reddit Ad Permutation Generator
 * 
 * Reads input CSV with headlines/body and generates all permutations
 * with different images, CTAs, and URL variants.
 * 
 * Usage: node generate-permutations.js [input.csv] [output.csv]
 * 
 * Input CSV format:
 *   Image,Headline,Body,CTA,URL
 * 
 * Output CSV format (ready for copy/paste):
 *   Image,Headline,Body,CTA,URL,Notes
 */

const fs = require('fs');
const readline = require('readline');

// Configuration
const DEFAULT_INPUT = 'permutations-input.csv';
const DEFAULT_OUTPUT = 'permutations-output.csv';

// URL variants to generate
const URL_VARIANTS = [
  { name: 'full', suffix: '' },
  { name: 'mini', suffix: '-min' }
];

// CTA variants to generate
const CTA_VARIANTS = ['DOWNLOAD', 'LEARN_MORE'];

// Images to use (appended to base images from CSV)
const IMAGE_VARIANTS = ['v1', 'v2', 'v3'];

/**
 * Generate URL with variant suffix
 */
function generateUrl(baseUrl, suffix) {
  if (!suffix) return baseUrl;
  
  // Handle different URL formats
  if (baseUrl.includes('/agentforce-360')) {
    return baseUrl.replace('/agentforce-360', `/agentforce-360${suffix}`);
  }
  
  // Add suffix before query params
  const [path, query] = baseUrl.split('?');
  if (suffix && path.endsWith('/')) {
    return path.slice(0, -1) + suffix + (query ? `?${query}` : '');
  }
  
  return baseUrl + suffix;
}

/**
 * Generate notes for easy identification
 */
function generateNotes(headline, image, cta, urlVariant) {
  const shortHeadline = headline.substring(0, 25).replace(/,/g, '') + '...';
  return `${shortHeadline} | img:${image} | ${cta} | ${urlVariant}`;
}

/**
 * Process the permutation logic
 */
async function processPermutations(inputPath, outputPath) {
  console.log('');
  console.log('═'.repeat(60));
  console.log('  REDDIT AD PERMUTATION GENERATOR');
  console.log('═'.repeat(60));
  console.log('');
  
  // Check if input file exists
  if (!fs.existsSync(inputPath)) {
    console.log(`❌ Input file not found: ${inputPath}`);
    console.log('');
    console.log('Create a CSV with this format:');
    console.log('  Image,Headline,Body,CTA,URL');
    console.log('');
    console.log('Example:');
    console.log('  v1.jpg,Your headline here,Body text here,DOWNLOAD,https://example.com');
    console.log('');
    return;
  }
  
  console.log(`📄 Reading: ${inputPath}`);
  console.log('');
  
  // Read input file
  const inputContent = fs.readFileSync(inputPath, 'utf8');
  const inputLines = inputContent.trim().split('\n');
  const headers = inputLines[0].split(',').map(h => h.trim().toLowerCase());
  
  console.log(`📊 Found headers: ${headers.join(', ')}`);
  console.log('');
  
  // Parse input rows
  const inputRows = [];
  for (let i = 1; i < inputLines.length; i++) {
    const values = parseCsvLine(inputLines[i]);
    if (values.length >= 5) {
      inputRows.push({
        image: values[0]?.trim() || '',
        headline: values[1]?.trim() || '',
        body: values[2]?.trim() || '',
        cta: values[3]?.trim() || '',
        url: values[4]?.trim() || ''
      });
    }
  }
  
  console.log(`📝 Loaded ${inputRows.length} input rows`);
  console.log('');
  
  // Generate permutations
  const outputRows = [];
  let permutationCount = 0;
  
  console.log('🔄 Generating permutations...');
  console.log('');
  
  for (const row of inputRows) {
    // Skip empty rows
    if (!row.headline || !row.body || !row.url) continue;
    
    for (const image of IMAGE_VARIANTS) {
      for (const urlVar of URL_VARIANTS) {
        for (const cta of CTA_VARIANTS) {
          const finalUrl = generateUrl(row.url, urlVar.suffix);
          const notes = generateNotes(row.headline, image, cta, urlVar.name);
          
          outputRows.push({
            image: `${image}.jpg`,
            headline: row.headline,
            body: row.body,
            cta: cta,
            url: finalUrl,
            notes: notes
          });
          
          permutationCount++;
        }
      }
    }
  }
  
  console.log(`✅ Generated ${permutationCount} permutations`);
  console.log('');
  
  // Generate output CSV
  let csv = 'Image,Headline,Body,CTA,URL,Notes\n';
  
  for (const row of outputRows) {
    csv += `"${row.image}","${escapeCsv(row.headline)}","${escapeCsv(row.body)}","${row.cta}","${row.url}","${row.notes}"\n`;
  }
  
  // Write output
  fs.writeFileSync(outputPath, csv);
  
  console.log('═'.repeat(60));
  console.log('  OUTPUT READY');
  console.log('═'.repeat(60));
  console.log('');
  console.log(`📁 Output file: ${outputPath}`);
  console.log(`📊 Total permutations: ${permutationCount}`);
  console.log('');
  console.log('Copy each row to Reddit Ads Manager:');
  console.log('  1. Go to ads.reddit.com');
  console.log('  2. Create Ad → Freeform');
  console.log('  3. Copy from this sheet');
  console.log('');
  
  // Print first few rows as preview
  console.log('Preview (first 5 rows):');
  console.log('-'.repeat(60));
  for (let i = 0; i < Math.min(5, outputRows.length); i++) {
    const r = outputRows[i];
    console.log(`${i + 1}. [${r.image}] ${r.headline.substring(0, 40)}...`);
    console.log(`   CTA: ${r.cta} | URL: ${r.url.substring(0, 50)}...`);
  }
  console.log('');
}

/**
 * Parse CSV line handling quoted values
 */
function parseCsvLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    
    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      result.push(current);
      current = '';
    } else {
      current += char;
    }
  }
  
  result.push(current);
  return result;
}

/**
 * Escape CSV value
 */
function escapeCsv(value) {
  if (value.includes(',') || value.includes('"') || value.includes('\n')) {
    return `"${value.replace(/"/g, '""')}"`;
  }
  return value;
}

// CLI
const inputPath = process.argv[2] || DEFAULT_INPUT;
const outputPath = process.argv[3] || DEFAULT_OUTPUT;

processPermutations(inputPath, outputPath).catch(console.error);
