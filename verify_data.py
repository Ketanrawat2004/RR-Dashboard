import json

with open("players_db.json", "r", encoding="utf-8") as f:
    players = json.load(f)

print("=== BATTERS ===")
for p in players:
    if p["category"] == "Batter":
        print(f"Rank {p['rank']:2}: {p['name']:20} | HP: {p['hp_wr']:5.1f}% | Base: {p['base_wr']:5.1f}% | Diff: {p['lift']:+5.1f}% | CPPI: {p['cppi']:5.2f}")

print("\n=== BOWLERS ===")
for p in players:
    if p["category"] == "Bowler":
        print(f"Rank {p['rank']:2}: {p['name']:20} | HP: {p['hp_wr']:5.1f}% | Base: {p['base_wr']:5.1f}% | Diff: {p['lift']:+5.1f}% | CPPI: {p['cppi']:5.2f}")

