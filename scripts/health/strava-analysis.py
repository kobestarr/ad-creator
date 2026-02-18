#!/usr/bin/env python3
# Strava analysis script
import requests
import json
from collections import defaultdict

TOKEN = "948a09b5cd6076701d4ddd761dc04e8e40290892"

# Fetch all pages
all_activities = []
page = 1

print("Fetching Strava data...")
while True:
    r = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers={"Authorization": f"Bearer {TOKEN}"},
        params={"per_page": 200, "page": page}
    )
    data = r.json()
    if not data:
        break
    all_activities.extend(data)
    print(f"Page {page}: {len(data)} activities (Total: {len(all_activities)})")
    page += 1
    if page > 15:  # Safety limit
        break

print(f"\nTotal activities: {len(all_activities)}")

# Year by year stats
years = defaultdict(lambda: {'runs': 0, 'rides': 0, 'distance': 0, 'time': 0, 'suffer': 0})

for a in all_activities:
    year = a['start_date'][:4]
    activity_type = a.get('type')
    
    if activity_type == 'Run':
        years[year]['runs'] += 1
    elif activity_type == 'Ride':
        years[year]['rides'] += 1
    
    years[year]['distance'] += a.get('distance', 0) / 1000  # km
    years[year]['time'] += a.get('moving_time', 0) / 3600  # hours
    if a.get('suffer_score'):
        years[year]['suffer'] += a['suffer_score']

print("\n" + "=" * 70)
print("📊 TRAINING HISTORY BY YEAR")
print("=" * 70)
print(f"\n{'Year':<8} {'Runs':<8} {'Rides':<8} {'Distance (km)':<15} {'Time (hrs)':<12} {'Suffer Score'}")
print("-" * 70)

for year in sorted(years.keys()):
    d = years[year]
    print(f"{year:<8} {d['runs']:<8} {d['rides']:<8} {d['distance']:<15.1f} {d['time']:<12.1f} {d['suffer']}")

# Recent running pace analysis
print("\n" + "=" * 70)
print("🏃 RECENT RUNNING PACE ANALYSIS")
print("=" * 70)

runs = [a for a in all_activities if a.get('type') == 'Run']
fast_runs = [r for r in runs if r.get('distance', 0) > 0 and (r['moving_time']/60)/(r['distance']/1000) < 7]

if fast_runs:
    avg_pace = sum((r['moving_time']/60)/(r['distance']/1000) for r in fast_runs) / len(fast_runs)
    print(f"\nAverage training pace (last {len(fast_runs)} fast runs): {avg_pace:.2f} min/km")
    
    # Race predictions
    pace_sec = avg_pace * 60
    print("\n🏆 RACE TIME PREDICTIONS")
    print("-" * 40)
    for dist, name in [(5, '5K'), (10, '10K'), (21.0975, 'Half'), (42.195, 'Marathon')]:
        seconds = pace_sec * (dist ** 1.06)  # Riegel formula
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        print(f"{name:12} {h:02}:{m:02}:{s:02}")
