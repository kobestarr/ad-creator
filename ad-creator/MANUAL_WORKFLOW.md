# Reddit Ad Creator - Manual Workflow

## The Problem
- Ads API doesn't accept custom headlines (requires existing post_id)
- Commercial approval pending
- Need manual posting in the meantime

## The Solution: Permutation Generator

Generate all combinations in a spreadsheet, then copy/paste into Reddit Ads Manager.

---

## Step 1: Prepare Your Inputs

Create a simple spreadsheet with these columns:

| Image | Headline | Body | CTA | URL |
|-------|----------|------|-----|-----|
| v1.jpg | Your boss wants AI in Salesforce | Here are 7 Agentforce lessons... | Download | bluprintx.com/agentforce-360 |
| v1.jpg | Your execs want AI in Salesforce | Enterprise AI that actually works | Learn More | bluprintx.com/agentforce-360 |
| v1.jpg | Your board wants AI in Salesforce | Lessons from 15+ orgs | Get Started | bluprintx.com/agentforce-360 |

---

## Step 2: Generate Permutations

Run this tool to generate all combinations:

```bash
node generate-permutations.js --input permutations.csv --output permutations-output.csv
```

---

## Step 3: Copy Each Row to Reddit Ads Manager

For each row in the output:

1. Go to: https://ads.reddit.com/accounts/a2_i5qw2u3t9aca
2. Click **Create Ad** → **Freeform**
3. Fill in:
   - **Headline**: Copy from row
   - **Body**: Copy from row
   - **CTA**: Select from dropdown
   - **Destination**: Copy URL from row
   - **Upload Image**: Select the image (v1.jpg, v2.jpg, etc.)
4. Click **Create Ad**
5. Repeat for next row

---

## Workflow Template

### Image 1 (v1.jpg)

| # | Headline | Body | CTA | URL |
|---|----------|------|-----|-----|
| 1 | Headline A1 | Body A1 | CTA 1 | URL 1 |
| 2 | Headline A2 | Body A2 | CTA 1 | URL 1 |
| 3 | Headline A3 | Body A3 | CTA 1 | URL 1 |
| 4 | Headline A1 | Body A1 | CTA 2 | URL 1 |
| ... | ... | ... | ... | ... |

### Image 2 (v2.jpg)

| # | Headline | Body | CTA | URL |
|---|----------|------|-----|-----|
| 1 | Headline B1 | Body B1 | CTA 1 | URL 1 |
| ... | ... | ... | ... | ... |

---

## Permutation Generator Tool

Create `generate-permutations.js`:

```javascript
#!/usr/bin/env node

const fs = require('fs');
const csv = require('csv-parser');
const { v4: uuidv4 } = require('uuid');

// Configuration
const IMAGES = ['v1.jpg', 'v2.jpg', 'v3.jpg'];
const URL_VARIANTS = ['full', 'mini'];
const CTA_VARIANTS = ['DOWNLOAD', 'LEARN_MORE'];

// Read input CSV
function generatePermutations(inputFile, outputFile) {
  const results = [];
  
  fs.createReadStream(inputFile)
    .pipe(csv())
    .on('data', (row) => {
      // Generate permutations
      IMAGES.forEach(image => {
        URL_VARIANTS.forEach(urlType => {
          CTA_VARIANTS.forEach(cta => {
            results.push({
              id: uuidv4().substring(0, 8),
              image: image,
              headline: row.headline,
              body: row.body,
              cta: cta,
              url: urlType === 'mini' 
                ? row.url.replace('.com/', '.com/agentforce-360-min/')
                : row.url,
              notes: `${row.headline.substring(0, 30)}... | ${image} | ${cta}`
            });
          });
        });
      });
    })
    .on('end', () => {
      // Write output
      let csv = 'Image,Headline,Body,CTA,URL,Notes\n';
      results.forEach(r => {
        csv += `"${r.image}","${r.headline}","${r.body}","${r.cta}","${r.url}","${r.notes}"\n`;
      });
      
      fs.writeFileSync(outputFile, csv);
      console.log(`Generated ${results.length} permutations`);
      console.log(`Output: ${outputFile}`);
    });
}

// CLI
const input = process.argv[2] || 'permutations-input.csv';
const output = process.argv[3] || 'permutations-output.csv';
generatePermutations(input, output);
```

---

## Quick Checklist (Print This)

### Before Starting
- [ ] Images ready in folder (v1.jpg, v2.jpg, v3.jpg)
- [ ] Headlines written (3-5 options)
- [ ] Body copy written (2-3 options)
- [ ] URLs ready (full + mini variants)
- [ ] This sheet printed

### For Each Image
- [ ] Note image name (v1.jpg)
- [ ] Upload image to Reddit once
- [ ] Create all ad permutations with that image
- [ ] Move to next image

### Ad Creation
- [ ] Headline: _______________
- [ ] Body: _______________
- [ ] CTA: _______________
- [ ] URL: _______________
- [ ] Image: v__.jpg
- [ ] Ad Name: _______________

---

## Example Workflow Session

```
=== REDDIT AD CREATION SESSION ===
Date: 2026-01-27
Account: Bluprintx

IMAGE 1: v1.jpg
[Upload v1.jpg to Reddit once]

Row 1: "Your boss wants AI" | "7 lessons..." | DOWNLOAD | URL-full
Row 2: "Your boss wants AI" | "7 lessons..." | LEARN_MORE | URL-full
Row 3: "Your boss wants AI" | "Enterprise..." | DOWNLOAD | URL-full
... (continue all permutations for v1.jpg)

IMAGE 2: v2.jpg  
[Upload v2.jpg to Reddit once]

Row 1: "Your execs want AI" | "7 lessons..." | DOWNLOAD | URL-full
... (continue all permutations for v2.jpg)

IMAGE 3: v3.jpg
[Upload v3.jpg to Reddit once]

... (finish remaining permutations)

TOTAL ADS CREATED: ___
```

---

## Pro Tips

1. **Upload image once** per image, then reuse it for all permutations
2. **Group by image** - finish all v1.jpg permutations before v2.jpg
3. **Use consistent naming**: `{Headline-Summary}_{Image}_{CTA}`
4. **Take breaks** - creating 50+ ads is tiring
5. **Check preview** before each ad creation

---

## Need Help?

- Reddit Ads Manager: https://ads.reddit.com/accounts/a2_i5qw2u3t9aca
- Upload images: Dashboard → Creatives → Upload Media
- Create ads: Dashboard → Ads → Create Ad → Freeform

---

*Last Updated: 2026-01-27*
