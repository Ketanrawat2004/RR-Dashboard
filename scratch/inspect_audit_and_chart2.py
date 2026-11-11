import csv, json
from collections import Counter

with open("pressure_output/audit_match_pressure_scores.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

hp = [r for r in rows if r["is_high_pressure"] == "True"]
print(f"Total matches: {len(rows)}, HP matches: {len(hp)} ({len(hp)/len(rows)*100:.1f}%)")
print("Stage label counts inside HP:", Counter(r["stage_label"] for r in hp))
print("Close label counts inside HP:", Counter(r["close_label"] for r in hp))

with open("players_db.json", encoding="utf-8") as f:
    db = json.load(f)

batters = sorted([p for p in db if p["category"] == "Batter"], key=lambda x: x["rank"])
bowlers = sorted([p for p in db if p["category"] == "Bowler"], key=lambda x: x["rank"])
print("\nAll 20 players sorted by hp_wr:")
for p in sorted(batters + bowlers, key=lambda x: (x["hp_wr"], x["lift"])):
    print(f"{p['category']:<7} #{p['rank']:<2} {p['name']:<20} hp_wr={p['hp_wr']:>5.1f} lift={p['lift']:>+6.1f} hp_m={p['hp_m']}")
