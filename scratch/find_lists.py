with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:100]):
    if '=' in l and any(k in l for k in ['top_', 'players', 'audit', 'data', 'batters', 'bowlers']):
        print(f"Line {i+1}: {l.strip()[:80]}")

