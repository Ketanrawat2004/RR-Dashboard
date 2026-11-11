import json

with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

print("Total players in players_db.json:", len(db))
batters = [p for p in db if p["category"] == "Batter"]
bowlers = [p for p in db if p["category"] == "Bowler"]

print("\n--- BATTERS in players_db.json (Rank order) ---")
for p in sorted(batters, key=lambda x: x["rank"]):
    print(f"Rank {p['rank']:2d}: {p['name']:20} | CPPI: {p['cppi']:.2f} | HP WR: {p['hp_wr']:.1f}% | Lift: {p['lift']:+.1f}%")

print("\n--- BOWLERS in players_db.json (Rank order) ---")
for p in sorted(bowlers, key=lambda x: x["rank"]):
    print(f"Rank {p['rank']:2d}: {p['name']:20} | CPPI: {p['cppi']:.2f} | HP WR: {p['hp_wr']:.1f}% | Lift: {p['lift']:+.1f}%")

