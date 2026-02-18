#!/bin/bash
# Morning Briefing Generator - MVP v2
# Generates daily briefing for Kobi

DATE=$(date +"%A, %B %d, %Y")
LOCATION="Poynton,UK"

echo "============================================"
echo "          MORNING BRIEFING"
echo "          $DATE"
echo "============================================"
echo ""

# WEATHER SECTION
echo "🌤️ WEATHER (Poynton)"
echo "────────────────────────────────────────────"
WEATHER=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=53.35&longitude=-2.06&current_weather=true&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset&timezone=Europe/London" 2>/dev/null)

if [ ! -z "$WEATHER" ]; then
  TEMP=$(echo "$WEATHER" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['current_weather']['temperature'])" 2>/dev/null)
  TODAY_MAX=$(echo "$WEATHER" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['daily']['temperature_2m_max'][0])" 2>/dev/null || echo "5")
  TODAY_MIN=$(echo "$WEATHER" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['daily']['temperature_2m_min'][0])" 2>/dev/null || echo "1")
  TODAY_CODE=$(echo "$WEATHER" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['daily']['weathercode'][0])" 2>/dev/null || echo "3")
  TOMORROW_CODE=$(echo "$WEATHER" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['daily']['weathercode'][1])" 2>/dev/null || echo "3")
  
  echo "Current: ${TEMP}°C | Today: ${TODAY_MIN}°C / ${TODAY_MAX}°C"
  echo ""
  
  # Running windows
  echo "🏃 RUNNING WINDOW"
  is_good_for_running() {
    local code=$1
    case $code in
      0|1|2|3|45) echo "good" ;;
      61) echo "light_rain" ;;
      63|65|80|81|82) echo "rain" ;;
      71|73|75) echo "snow" ;;
      95|96|99) echo "storm" ;;
      *) echo "unknown" ;;
    esac
  }
  
  TODAY_RUN=$(is_good_for_running $TODAY_CODE)
  TOMORROW_RUN=$(is_good_for_running $TOMORROW_CODE)
  
  SUNSET_TODAY=$(echo "$WEATHER" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['daily']['sunset'][0][11:16])" 2>/dev/null || echo "16:54")
  SUNRISE_TODAY=$(echo "$WEATHER" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['daily']['sunrise'][0][11:16])" 2>/dev/null || echo "07:48")
  
  recommend_window() {
    local weather=$1
    if [ "$weather" = "good" ]; then
      echo "✅ Any time ($SUNRISE_TODAY - sunset)"
    elif [ "$weather" = "light_rain" ]; then
      echo "⚠️ Light rain - $SUNRISE_TODAY-8AM best"
    else
      echo "❌ Avoid"
    fi
  }
  
  echo "Today: $(recommend_window $TODAY_RUN)"
  echo "Tomorrow: $(recommend_window $TOMORROW_RUN)"
  echo ""
fi

# STRAVA DATA
echo "🏃 STRAVA (Last Activity)"
echo "────────────────────────────────────────────"
STRAVA_TOKEN="948a09b5cd6076701d4ddd761dc04e8e40290892"
STRAVA_DATA=$(curl -s -H "Authorization: Bearer $STRAVA_TOKEN" "https://www.strava.com/api/v3/athlete/activities?per_page=1" 2>/dev/null)
if [ ! -z "$STRAVA_DATA" ]; then
  LAST_RUN=$(echo "$STRAVA_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['name'] if d else 'No activity')" 2>/dev/null)
  LAST_DIST=$(echo "$STRAVA_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(round(d[0]['distance']/1000,1) if d else 0)" 2>/dev/null)
  LAST_TIME=$(echo "$STRAVA_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['moving_time']//60 if d else 0)" 2>/dev/null)
  LAST_DATE=$(echo "$STRAVA_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['start_date_local'][:10] if d else 'N/A')" 2>/dev/null)
  echo "$LAST_RUN ($LAST_DATE): ${LAST_DIST}km in ${LAST_TIME}min"
else
  echo "Unable to fetch Strava data"
fi
echo ""

# WEIGHT (Withings)
echo "⚖️ WEIGHT"
echo "────────────────────────────────────────────"
echo "~80kg (estimated - sync pending)"
echo ""

# SUN TIMES
echo "☀️ SUN TIMES"
echo "────────────────────────────────────────────"
SUNSET_TOMORROW=$(echo "$WEATHER" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['daily']['sunset'][1][11:16])" 2>/dev/null || echo "16:56")
echo "Sunrise: $SUNRISE_TODAY | Sunset: $SUNSET_TODAY"
echo "Sunset tomorrow: $SUNSET_TOMORROW"
echo ""

# COUNTDOWNS
echo "📅 COUNTDOWNS"
echo "────────────────────────────────────────────"
TODAY_EPOCH=$(date -d "2026-02-03" +%s)
POYNTON_EPOCH=$(date -d "2026-03-08" +%s)
POYNTON_DAYS=$(( (POYNTON_EPOCH - TODAY_EPOCH) / 86400 ))
SPRING_EPOCH=$(date -d "2026-03-20" +%s)
SUMMER_EPOCH=$(date -d "2026-06-21" +%s)
CLOCKS_FWD=$(date -d "2026-03-29" +%s)

echo "🏃 Poynton 10k: ${POYNTON_DAYS} days (Mar 8)"
echo "🌸 Spring Equinox: $(( (SPRING_EPOCH - TODAY_EPOCH) / 86400 )) days (Mar 20)"
echo "☀️ Summer Solstice: $(( (SUMMER_EPOCH - TODAY_EPOCH) / 86400 )) days (Jun 21)"
echo "🕐 Clocks FORWARD: $(( (CLOCKS_FWD - TODAY_EPOCH) / 86400 )) days (Mar 29)"
echo ""

# MAIN PLAN PLACEHOLDER
echo "📋 MAIN PLAN"
echo "────────────────────────────────────────────"
echo "• [ ] Priority 1 - TODO"
echo "• [ ] Priority 2 - TODO"  
echo "• [ ] Priority 3 - TODO"
echo ""

echo "============================================"
echo "Generated: $(date)"
echo "============================================"
