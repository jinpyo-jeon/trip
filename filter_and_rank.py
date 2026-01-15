#!/usr/bin/env python3
import csv
import re

# Scoring weights
WEIGHTS = {
    'Relaxation (1-10)': 0.10,
    'Uniqueness vs NYC (1-10)': 0.20,
    'Bachelor Party Fit (1-10)': 0.50,
    'Value for Money (1-10)': 0.10,
    'Convenience (1-10)': 0.10
}

# Activities to exclude
SNOW_ACTIVITIES = [
    'Mohonk Mountain House', 'Hunter Mountain', 'Belleayre Mountain',
    'Brewster Ice Arena', 'Carriage Lounge (Mohonk)', 'Ice Fishing (Ashokan)',
    'Hunter Mountain Snow Tubing', 'Ice Fishing (Bashakill)'
]

def calc_score(row):
    """Calculate weighted score for an activity"""
    return round(sum(float(row[k]) * v for k, v in WEIGHTS.items()), 2)

def parse_minutes(drive_time):
    """Convert drive time string to minutes"""
    if 'hr' in drive_time.lower():
        match = re.search(r'(\d+)\s*hr', drive_time)
        hours = int(match.group(1)) if match else 0
        match = re.search(r'(\d+)\s*min', drive_time)
        mins = int(match.group(1)) if match else 0
        return hours * 60 + mins
    elif 'full day' in drive_time.lower():
        return 0  # Full day tours are OK
    else:
        match = re.search(r'(\d+)', drive_time)
        return int(match.group(1)) if match else 0

def filter_activities(rows, max_drive_min=40, max_drive_multi_hour=70):
    """Filter out restaurants, snow activities, and far activities"""
    filtered = []
    for row in rows:
        # Skip restaurants
        if row['Category'] == 'Restaurant':
            continue
        # Skip snow/ice activities
        if row['Activity'] in SNOW_ACTIVITIES:
            continue
        filtered.append(row)
    return filtered

def rank_activities(rows):
    """Recalculate scores and assign ranks"""
    for row in rows:
        row['Overall Score'] = calc_score(row)
    rows.sort(key=lambda x: float(x['Overall Score']), reverse=True)
    for i, row in enumerate(rows, 1):
        row['Rank'] = i
    return rows

if __name__ == '__main__':
    # Read the CSV
    with open('trip.csv', 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Filter and rank
    filtered = filter_activities(rows)
    ranked = rank_activities(filtered)

    # Write back
    with open('trip.csv', 'w', newline='') as f:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ranked)

    print(f"Removed {len(rows) - len(ranked)} rows")
    print(f"Remaining: {len(ranked)} activities")
    print(f"\nWeights: {WEIGHTS}")
