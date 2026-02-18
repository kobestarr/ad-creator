# Research Framework - Building the Empire

**Created:** 2026-02-01  
**Purpose:** Systematic research capture → Ideas → Projects → Revenue

---

## The Problem

You watch YouTube tutorials and want to:
- Remember what you learned
- Extract actionable ideas
- Build projects from blueprints
- Iterate and improve

## The Solution: Research Pipeline

```
🎬 YouTube Video
       ↓
📝 Transcribe (UniScribe API)
       ↓
📊 Extract Insights (Auto + Manual)
       ↓
💡 Add to Ideas List (MEMORY.md)
       ↓
🚀 Build Project (From Blueprint)
       ↓
💰 Generate Revenue
```

---

## Nick Saraev Integration

### His Blueprints → Your Projects

| His Video | Your Use | Revenue |
|-----------|----------|---------|
| Cold Email Icebreaker | Local business outreach | £4-8K/mo |
| Upwork Proposals | Freelance services | £2-5K/mo |
| LinkedIn Automation | Bluprintx clients | £5-10K/mo |
| Job Scraping | OE strategy + service | £5-15K/mo |

### Research Capture Workflow

1. **Watch video → Send URL to Robyn**
2. **I transcribe → Extract key methods**
3. **Save to** `/root/clawd/research/transcriptions/`
4. **Add to** `/root/clawd/memory/COMPLETE_IDEAS_LIST.md`
5. **Build → Test → Scale**

---

## Research Categories

### 1. Automation (High Priority)
**Tags:** `automation`, `n8n`, `make`, `zapier`

Focus: Build once, use infinitely
- Nick Saraev workflows
- AI automation
- Content automation

### 2. Business Development
**Tags:** `outreach`, `sales`, `marketing`

Focus: Revenue generation
- Cold email
- LinkedIn outreach
- Local business

### 3. Personal Productivity
**Tags:** `productivity`, `oe`, `jobs`

Focus: Your personal income
- Job scraping
- OE strategy
- Time management

### 4. Client Services
**Tags:** `salesforce`, `consulting`, `bluprintx`

Focus: Billable hours
- Salesforce hiring tracker
- Content automation
- Process improvement

---

## Research Output Structure

```
/root/clawd/research/
├── transcriptions/          # Full video transcriptions
│   ├── _index.json         # Master index
│   └── {video_title}_{timestamp}/
│       ├── transcript.txt
│       ├── summary.txt
│       ├── outline.md
│       ├── insights.md
│       └── full.json
├── ideas/                   # Extracted ideas
│   └── YYYY-MM-DD-ideas.md
├── templates/               # Reusable templates
│   ├── email-templates/
│   ├── workflow-templates/
│   └── project-templates/
└── projects/                # Built projects
    └── {project-name}/
```

---

## Ideas Pipeline

### Automatic Capture
When research is transcribed, key insights are automatically:
1. Saved to `insights.md`
2. Indexed in `_index.json`
3. Added to daily notes

### Manual Processing
Weekly review of transcriptions to:
1. Extract actionable ideas
2. Prioritize by revenue potential
3. Add to COMPLETE_IDEAS_LIST.md
4. Assign to agents or build yourself

---

## Measurement

Track research effectiveness:

| Metric | Target | Actual |
|--------|--------|--------|
| Videos transcribed/week | 5-10 | - |
| Ideas extracted/video | 3-5 | - |
| Ideas implemented/week | 1-2 | - |
| Revenue from research | £5K+/mo | - |

---

## Next Steps

1. [ ] Test transcription with a Nick Saraev video
2. [ ] Add YouTube API for playlist monitoring
3. [ ] Set up automated weekly review
4. [ ] Connect ideas to agent tasks

---

*Research → Ideas → Empire*
