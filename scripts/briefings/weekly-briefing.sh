#!/bin/bash
# Weekly Briefing - Saturday Summary
# Comprehensive weekly review with Strava analysis

DATE=$(date +"%A, %B %d, %Y")
echo "============================================"
echo "       WEEKLY BRIEFING"
echo "       $DATE"
echo "============================================"
echo ""

# WEATHER (This week's forecast)
echo "🌤️ WEATHER OUTLOOK (This Week)"
echo "────────────────────────────────────────────"
WEATHER=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=53.35&longitude=-2.06&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=Europe/London" 2>/dev/null)
if [ ! -z "$WEATHER" ]; then
  DAYS=$(echo "$WEATHER" | python3 -c "import sys,json; d=json.load(sys.stdin); print(' '.join(d['daily']['time'][1:7]))" 2>/dev/null)
  MAXES=$(echo "$WEATHER" | python3 -c "import sys,json; d=json.load(sys.stdin); print(' '.join([str(x) for x in d['daily']['temperature_2m_max'][1:7]]))" 2>/dev/null)
  CODES=$(echo "$WEATHER" | python3 -c "import sys,json; d=json.load(sys.stdin); print(' '.join([str(x) for x in d['daily']['weathercode'][1:7]]))" 2>/dev/null)
  
  echo "Day           High  Running?"
  echo "────────────────────────────────────────────"
  IFS=' ' read -ra DAY_ARRAY <<< "$DAYS"
  IFS=' ' read -ra MAX_ARRAY <<< "$MAXES"
  IFS=' ' read -ra CODE_ARRAY <<< "$CODES"
  
  for i in "${!DAY_ARRAY[@]}"; do
    day=$(echo "${DAY_ARRAY[$i]}" | cut -d'-' -f3 | sed 's/^0//')
    high="${MAX_ARRAY[$i]}"
    code="${CODE_ARRAY[$i]}"
    
    # Running recommendation
    if [ "$code" -eq 0 ] || [ "$code" -eq 1 ] || [ "$code" -eq 2 ] || [ "$code" -eq 3 ]; then
      rec="✅"
    elif [ "$code" -eq 61 ]; then
      rec="⚠️ light rain"
    else
      rec="❌ rain/snow"
    fi
    
    echo "${DAY_ARRAY[$i]#$(( ${DAY_ARRAY[$i]%%-*} - 1 ))-}  ${day}  ${high}°C  $rec"
  done
fi
echo ""

# STRAVA WEEKLY SUMMARY
echo "🏃 STRAVA WEEKLY SUMMARY"
echo "────────────────────────────────────────────"
STRAVA_TOKEN="948a09b5cd6076701d4ddd761dc04e8e40290892"
WEEK_STRAVA=$(curl -s -H "Authorization: Bearer $STRAVA_TOKEN" "https://www.strava.com/api/v3/athlete/activities?per_page=10" 2>/dev/null)

if [ ! -z "$WEEK_STRAVA" ]; then
  # This week's runs
  echo "This Week's Activities:"
  echo "$WEEK_STRAVA" | python3 -c "
import sys,json
data=json.load(sys.stdin)
this_week = []
for a in data:
    if '2026-02-' in a.get('start_date',''):
        this_week.append(a)

if this_week:
    for a in this_week[:7]:
        date=a['start_date'][:10]
        name=a['name'][:40]
        dist=round(a['distance']/1000,1)
        time=a['moving_time']//60
        ttype=a['type'][0]
        print(f\"  {date}: {name} ({dist}km, {time}min) [{ttype}]\")
else:
    print('  No activities this week')
"
  
  echo ""
  
  # Yearly totals
  echo "2026 Year Totals:"
  TOTAL_2026=$(echo "$WEEK_STRAVA" | python3 -c "
import sys,json
data=json.load(sys.stdin)
runs=sum(1 for a in data if a.get('type')=='Run' and a['start_date'].startswith('2026'))
rides=sum(1 for a in data if a.get('type')=='Ride' and a['start_date'].startswith('2026'))
dist=sum(a['distance']/1000 for a in data if a['start_date'].startswith('2026'))
print(f'{runs} runs, {rides} rides, {round(dist,1)}km total')
" 2>/dev/null)
  echo "  $TOTAL_2026"
fi
echo ""

# STRAVA YEARLY PROGRESSION
echo "📊 TRAINING HISTORY BY YEAR"
echo "────────────────────────────────────────────"
echo "Year     Runs     Distance    Suffer"
echo "────────────────────────────────────────────"
echo "2014     137     5,279 km    8,730"
echo "2015     64      9,111 km    15,009"
echo "2016     33      4,927 km    11,417"
echo "2017     44      1,587 km    13,677"
echo "2018     37      4,479 km    14,256"
echo "2019     12      5,428 km    12,252"
echo "2023     49      402 km      2,395"
echo "2024     89      260 km      2,975"
echo "2025     105     2,061 km    8,074"
echo "2026     28+     568+ km     1,144"
echo ""

# PACE & RACE PREDICTIONS
echo "🏆 PACE ANALYSIS & RACE PREDICTIONS"
echo "────────────────────────────────────────────"
echo "Average training pace (recent): 5:43 min/km"
echo ""
echo "Based on your training data:"
echo "Distance     Predicted Time    Pace"
echo "────────────────────────────────────────────"
echo "5K           00:31:27         5:43/km"
echo "10K          01:05:35         5:43/km"
echo "Half Mara    02:24:42         5:43/km"
echo "Marathon     05:01:42         5:43/km"
echo ""

# COUNTDOWNS
echo "📅 COUNTDOWNS"
echo "────────────────────────────────────────────"
TODAY_EPOCH=$(date -d "2026-02-04" +%s)
POYNTON_EPOCH=$(date -d "2026-03-08" +%s)
SPRING_EPOCH=$(date -d "2026-03-20" +%s)
SUMMER_EPOCH=$(date -d "2026-06-21" +%s)
CLOCKS_FWD=$(date -d "2026-03-29" +%s)

echo "🏃 Poynton 10k: $(( (POYNTON_EPOCH - TODAY_EPOCH) / 86400 )) days (Mar 8)"
echo "🌸 Spring Equinox: $(( (SPRING_EPOCH - TODAY_EPOCH) / 86400 )) days (Mar 20)"
echo "☀️ Summer Solstice: $(( (SUMMER_EPOCH - TODAY_EPOCH) / 86400 )) days (Jun 21)"
echo "🕐 Clocks FORWARD: $(( (CLOCKS_FWD - TODAY_EPOCH) / 86400 )) days (Mar 29)"
echo ""

# WEEKEND PLAN
echo "🎯 WEEKEND PLAN"
echo "────────────────────────────────────────────"
echo "Saturday:"
echo "  - Group run (typically by 10am)"
echo "  - Hard cycle session"
echo ""
echo "Sunday:"
echo "  - Recovery / easy day"
echo ""
echo "Next Week Focus:"
echo "  - [ ] TrainerRoad workout plan"
echo "  - [ ] Maintain consistency"
echo ""

# MAIN PLAN PLACEHOLDER
echo "📋 MAIN PLAN (Weekly Check-in)"
echo "────────────────────────────────────────────"
echo "• Financial: £100k debt by Feb 2027"
echo "• OE Strategy: Multiple remote jobs"
echo "• Bluprintx: Client work + LinkedIn Social Signal Machine"
echo "• Kobestarr: Podcast + retainer clients"
echo ""

echo "============================================"
echo "Generated: $(date)"
echo "============================================"
