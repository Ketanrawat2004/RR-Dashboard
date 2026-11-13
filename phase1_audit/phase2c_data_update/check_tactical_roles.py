import json

with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

from collections import Counter
c = Counter(p.get('tactical_role', '') for p in db if p['category'] == 'Batter')
print("Batters tactical_role:")
for k, v in c.items():
    print(f"  {k}: {v}")

c_bowl = Counter(p.get('tactical_role', '') for p in db if p['category'] == 'Bowler')
print("\nBowlers tactical_role:")
for k, v in c_bowl.items():
    print(f"  {k}: {v}")

