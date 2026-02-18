# Health & Fitness Integration Research

**Research Date:** 2026-02-01  
**Status:** Complete  
**Goal Event:** Poynton 10k - March 8, 2026 (TBD - need verification)

---

## Poynton 10k Verification

**Date CONFIRMED:** Sunday, March 8, 2026
- Source: NiftyEntries registration platform
- Time: 9:30 AM
- Location: Poynton Civic Centre, Park Lane, SK12 1RB

---

## Integrations Available

### 1. Strava

**What it tracks:**
- Running activities (GPS, pace, distance, elevation)
- Cycling activities
- Other sports
- Weekly/monthly stats

**API:** Strava API available
- OAuth authentication
- Activity data export
- Webhook support for real-time updates

**Withings Integration:**
- Withings can sync to Strava automatically
- Weight data syncs through Strava

### 2. TrainerRoad

**What it tracks:**
- Cycling training plans
- Workouts completed
- FTP (Functional Threshold Power)
- Training stress scores

**Strava Integration:**
- Sync workouts to Strava
- Apple Health bridge via Strava

**Withings Compatibility:**
- Can pull weight data from Strava/Withings
- FTP syncing available

### 3. Withings

**What it tracks:**
- Weight (smart scales)
- Sleep (Sleep Analyzer)
- Heart rate, HRV
- Steps, activity
- Bloodations:**
- Stra pressure

**Integrva (automatic workout sync)
- IFTTT (custom automations)
- Terra API (aggregated wearable API)

---

## Data Flow Architecture

```
Withings (Weight, Sleep, HRV)
        ↓
    [Auto-sync]
        ↓
Strava (Activities, Training)
        ↓
    [API or Sync]
        ↓
TrainerRoad (Training Plan)
        ↓
    [OpenClaw Briefing]
        ↓
Daily Morning Briefing
```

---

## Morning Briefing Integration

### Daily Metrics to Include

**From Strava:**
- Yesterday's activity (type, distance, time)
- Weekly distance goal progress
- Recent PRs or achievements

**From TrainerRoad:**
- Today's scheduled workout
- Week progress (workouts completed/planned)
- FTP trend
- Training block status

**From Withings:**
- Morning weight
- Sleep duration + quality score
- Resting heart rate
- Steps yesterday

### Poynton 10k Training Tracking

**Race Date:** March 8, 2026 (CONFIRMED)
**Today:** February 1, 2026
**Weeks to Train:** 5 weeks (week 8 of typical 12-week plan)

**Training Plan Structure:**
- 12-week plan typical for 10k
- Currently: February 1 (approximately week 7-8)
- Race: March 8 (5 weeks training)
- Peak week: 2 weeks before race (Feb 22-28)
- Taper: Final 2 weeks (March 1-7)

**Weekly Structure:**
- Monday: Rest or cross-training
- Tuesday: Interval/ tempo run
- Wednesday: Easy run
- Thursday: Rest
- Friday: Medium long run
- Saturday: Long run
- Sunday: Rest

**Progress Metrics:**
- Weekly mileage
- Long run distance progression
- Pace improvements
- Time to goal (5 weeks → 5:00/km goal pace?)

---

## Implementation

### Step 1: Verify Race Date
- [ ] Search Perplexity for official Poynton 10k 2026 date
- Confirm it is indeed March 8 (second Sunday)

### Step 2: API Access
- [ ] Get Strava API credentials
- [ ] Connect TrainerRoad account
- [ ] Ensure Withings → Strava sync is active

### Step 3: Build Health Skill
- [ ] Create OpenClaw skill for health data
- [ ] Connect to Strava API
- [ ] Pull TrainerRoad workout schedule
- [ ] Aggregate Withings metrics

### Step 4: Morning Briefing Integration
- [ ] Add health section to morning briefing
- [ ] Include training plan progress
- [ ] Show goal countdown

---

## Alternative: Terra API

Terra (tryterra.co) provides unified API for multiple wearables:

**Supported:**
- Garmin, Oura, Apple, Whoop
- Polar, Eight Sleep, Freestyle Libre
- Peloton, Withings, Strava

**Benefits:**
- Single API for all devices
- Normalized data format
- Real-time webhooks

**Consider if:**
- Want to aggregate more health data
- Planning more integrations in future

---

## Next Steps

1. [ ] **CRITICAL:** Verify Poynton 10k 2026 date (Perplexity search)
2. [ ] Set up Strava → Withings sync (if not active)
3. [ ] Ensure TrainerRoad → Strava sync is working
4. [ ] Create health data skill in OpenClaw
5. [ ] Add health section to morning briefing template

---

*Sources: Strava support, TrainerRoad forum, Withings blog, Terra API*
