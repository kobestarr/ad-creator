#!/usr/bin/env node

/**
 * Token Usage Tracker
 * 
 * Usage:
 *   node token-tracker.js add <count>
 *   node token-tracker.js status
 *   node token-tracker.js reset
 */

const fs = require('fs');
const path = require('path');

const TRACKER_FILE = path.join(__dirname, 'token-tracker.json');

// Read tracker state
function readTracker() {
  try {
    return JSON.parse(fs.readFileSync(TRACKER_FILE, 'utf8'));
  } catch (e) {
    return {
      session_start: null,
      session_tokens: 0,
      total_tokens: 0,
      last_reset: null,
      thresh_crossed: []
    };
  }
}

// Write tracker state
function writeTracker(data) {
  fs.writeFileSync(TRACKER_FILE, JSON.stringify(data, null, 2));
}

// Format for display
function formatDisplay(data) {
  const now = new Date().toISOString();
  const started = data.session_start || now;
  const resetAgo = data.last_reset ? 
    Math.floor((Date.now() - new Date(data.last_reset).getTime()) / 1000) : 0;
  
  return `┌─────────────────────────────────────────┐
│         TOKEN USAGE TRACKER               │
├─────────────────────────────────────────┤
│ Session Start:  ${new Date(started).toLocaleTimeString()}          │
│ Session Total:  ${data.session_tokens.toString().padStart(8)} tokens      │
│ Lifetime Total: ${data.total_tokens.toString().padStart(8)} tokens      │
│ Last Reset:     ${resetAgo}s ago                  │
│ Crossed:        ${data.thresh_crossed.join(', ') || 'None'}         │
└─────────────────────────────────────────┘`;
}

const args = process.argv.slice(2);
const command = args[0];

const tracker = readTracker();

if (command === 'add') {
  const tokens = parseInt(args[1]) || 0;
  tracker.session_tokens += tokens;
  tracker.total_tokens += tokens;
  
  if (tracker.session_start === null) {
    tracker.session_start = new Date().toISOString();
  }
  
  // Check thresholds (1000, 2000, 3000, 5000, 8000, 10000...)
  const thresholds = [1000, 2000, 3000, 5000, 8000, 10000, 15000, 20000, 30000, 50000, 100000];
  
  thresholds.forEach(t => {
    if (tracker.session_tokens >= t && !tracker.thresh_crossed.includes(t)) {
      tracker.thresh_crossed.push(t);
      console.log(`\n🚨 THRESHOLD CROSSED: ${t.toLocaleString()} tokens!\n`);
    }
  });
  
  writeTracker(tracker);
  console.log(`Added ${tokens} tokens`);
  console.log(formatDisplay(tracker));
  
} else if (command === 'status') {
  console.log(formatDisplay(tracker));
  
  // Warning if approaching 80% of typical limit (assuming 100k context)
  const contextLimit = 200000;
  const percent = (tracker.session_tokens / contextLimit) * 100;
  
  if (percent >= 80) {
    console.log(`\n⚠️  WARNING: ${percent.toFixed(1)}% of context limit reached!`);
  }
  
} else if (command === 'reset') {
  tracker.session_tokens = 0;
  tracker.session_start = new Date().toISOString();
  tracker.last_reset = new Date().toISOString();
  tracker.thresh_crossed = [];
  writeTracker(tracker);
  console.log('Token counter reset');
  console.log(formatDisplay(tracker));
  
} else {
  console.log('Token Usage Tracker');
  console.log('');
  console.log('Commands:');
  console.log('  add <count>    Add tokens to counter');
  console.log('  status         Show current usage');
  console.log('  reset          Reset session counter');
  console.log('');
  console.log(formatDisplay(tracker));
}
