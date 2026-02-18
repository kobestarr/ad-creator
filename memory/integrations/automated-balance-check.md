# Automated Daily Balance Check

## Setup
- **Script:** `/root/clawd/scripts/daily-balance-check.sh`
- **Schedule:** Daily at 9:00 AM (London time)
- **Cron ID:** `3bf3e403-f050-42bd-a693-40b27d045ff6`

## Output Format
```
=== DAILY BALANCE CHECK ===

🐆 KOBESTARR ENGINEERING
   Main Account:    £280.99
   Savings (Spaces): £755.05
   TOTAL:           £1036.04

🐆 STRIPPED MEDIA
   TOTAL:           £2457.06

========================================
💰 GRAND TOTAL:      £3493.10
========================================
```

## Manual Run
```bash
/root/clawd/scripts/daily-balance-check.sh
```

## Notes
- Uses `totalEffectiveBalance` for grand totals
- Breaks out main vs savings for transparency
- All data pulled via Starling API in real-time

---

*Created: 2026-02-01*
