# Morning Briefing & Daily Stand-up System Research

**Research Date:** 2026-02-01  
**Status:** IN PROGRESS - Deep dive needed with user  
**Priority:** HIGH (user requested)

---

## Goal

Reduce cognitive load by creating a comprehensive morning briefing that covers:
- School management (dropoff, pickup, emails, messages)
- Meal prep & planning
- Financial tracking
- Health & fitness (Strava, TrainerRoad, Withings)
- Media tracking (IMDb, Letterboxd)
- Daily priorities
- Work focus areas

---

## Current State (Needs Brain Dump)

### School Management
- [ ] Dropoff time/location
- [ ] Pickup time/location
- [ ] School emails/messages to check
- [ ] Event reminders
- [ ] Permission slips/actions needed

### Meal Planning
- [ ] Weekly meal plan overview
- [ ] What's for dinner tonight
- [ ] Ingredients needed
- [ ] Prep time required
- [ ] Leftover usage

### Financial
- [ ] Today's cash position
- [ ] Upcoming payments due
- [ ] Invoices sent/expected
- [ ] Debt payoff progress

### Health & Fitness
- [ ] Yesterday's activity
- [ ] Today's planned workout (Poynton 10k training)
- [ ] Weekly training schedule
- [ ] Nutrition goals
- [ ] Sleep data (Withings)

### Media/Entertainment
- [ ] Currently watching (TV/films)
- [ ] Progress tracking
- [ ] Watchlist updates
- [ ] What to watch tonight

### Work
- [ ] Top 3 priorities
- [ ] Meetings scheduled
- [ ] Deadlines today/this week
- [ ] Agent task updates

---

## Proposed Briefing Structure

### Morning Briefing Format

```
═══════════════════════════════════════════════════════
                    MORNING BRIEFING
                  Sunday, February 1, 2026
═══════════════════════════════════════════════════════

📅 TODAY AT A GLANCE
├── School: Dropoff 8:30 AM, Pickup 3:30 PM
├── Meals: Dinner - Pasta, Prep at 5:00 PM
├── Money: Balance £X,XXX, Invoice due from Y
├── Health: 5km run scheduled, 7h sleep last night
├── Media: "The Bear" S3E4 (2/8 watched)
└── Work: Top 3 priorities + meetings

═══════════════════════════════════════════════════════

🏫 SCHOOL
├── 📧 Emails to check: [school@email.com]
├── 📅 Events: Book fair Friday, return forms by Wed
├── 🎒 Supplies needed: [none]
└── 🚗 Schedule: Dropoff 8:30 AM, Pickup 3:30 PM

═══════════════════════════════════════════════════════

🍽️ MEAL PREP
├── Tonight: Pasta Primavera
├── Prep time: 5:00 PM (30 mins)
├── Ingredients: [pasta, vegetables, garlic]
├── Needs shopping: [none - have everything]
└── Leftover plan: Lunch tomorrow

═══════════════════════════════════════════════════════

💰 FINANCES
├── KSD Balance: £X,XXX.XX
├── Stripped Media: £X,XXX.XX
├── Personal: -£X,XXX.XX (overdraft)
├── Debt Payoff: £X,XXX paid / £100,045 total
├── This week target: £4,624
└── Due this week: [HMRC £X,XXX on Friday]

═══════════════════════════════════════════════════════

🏃 HEALTH & FITNESS (Poynton 10k: March 8, 2026 - CONFIRMED)
├── Yesterday: 5km run (28:45), 7h 12m sleep
├── Today: Rest day (recovery week)
├── This week: Mon-rest, Tue-5km, Wed-intervals, Thu-rest, Fri-6km, Sat-long run, Sun-rest
├── Weight: [from Withings]
├── Training plan: TrainerRoad [Week 7-8 of 12]
└── Progress: [5 weeks to race day!]

═══════════════════════════════════════════════════════

🎬 MEDIA TRACKING
├── Currently Watching:
│   ├── TV: The Bear S3 (2/8 eps) ████████░░░░░░ 25%
│   ├── Film: [current watch] 
│   └── Shows: [list with progress]
│
├── To Watch:
│   ├── [Priority 1]
│   ├── [Priority 2]
│   └── [Priority 3]
│
└── Watched This Week: [3 episodes, 0 films]

═══════════════════════════════════════════════════════

💼 WORK PRIORITIES
├── High Priority:
│   1. [ ] Task 1
│   2. [ ] Task 2
│   3. [ ] Task 3
│
├── Meetings:
│   ├── 10:00 AM - Bluprintx sync
│   └── 2:00 PM - Client call
│
├── Deadlines:
│   ├── Today: [something due]
│   ├── This week: [big deliverable]
│   └── Next week: [project milestone]
│
├── Agent Updates:
│   ├── KSD Outreach: Agent 1 researching Apify
│   └── Content Automation: 12 drafts created
│
└── Focus Time Blocked: 9:00 AM - 12:00 PM

═══════════════════════════════════════════════════════

🎯 DAILY FOCUS
[Based on priorities, what should you focus on TODAY?]

Example:
"Today, focus on the local outreach agent research review.
Everything else can wait until that's done."

═══════════════════════════════════════════════════════

🤖 ACTION ITEMS
├── [ ] Review agent research from overnight
├── [ ] Send Oktopost support email
├── [ ] Start financial tracking expansion
└── [ ] [Your custom action]

═══════════════════════════════════════════════════════
```

---

## Integration Points

### APIs to Connect
| Data | Source | Method |
|------|--------|--------|
| School | Manual input or email scrape | User input |
| Meals | Meal planning app or manual | User input |
| Finances | Freeagent + Starling APIs | Auto-sync |
| Health | Strava, TrainerRoad, Withings | API integrations |
| Media | IMDb, Letterboxd | API or manual |
| Work | Calendar, task list | API + manual |

### OpenClaw Skills Needed
- Financial tracking skill (exists, expand)
- Health/fitness skill (needs build)
- Media tracking skill (needs build)
- Task management skill (needs build)
- Calendar integration (existing or new)

---

## Brain Dump Questions (Need User Input)

### School Management
1. Which school? What system do they use (email, app, portal)?
2. How do you currently track pickups/dropoffs?
3. What's the biggest friction in school communication?

### Meal Planning
1. Current system (app, spreadsheet, nothing)?
2. How far ahead do you plan (weekly, daily)?
3. Who cooks? Any dietary restrictions?
4. Budget for groceries?

### Daily Routine
1. What time do you want the briefing?
2. Morning or evening (or both)?
3. Preferred format (WhatsApp, voice, text)?

### Priorities
1. What's the biggest cognitive load today?
2. What decisions do you make repeatedly that could be automated?
3. What information do you always wish you had at your fingertips?

---

## Next Steps

1. [ ] **DEEP DIVE BRAIN DUMP** - Walk through each area with user
2. [ ] Map current manual processes
3. [ ] Prioritize integrations by pain point
4. [ ] Build briefing skill incrementally
5. [ ] Start with MVP (finance + health), add others

---

*This document is a placeholder for the brain dump session.*
