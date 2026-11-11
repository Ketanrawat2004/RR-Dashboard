import json

with open("players_db.json", "r", encoding="utf-8") as f:
    players = json.load(f)

sorted_by_lift = sorted(players, key=lambda x: x["lift"], reverse=True)
print("Top 10 Differentials in DB:")
for p in sorted_by_lift[:10]:
    print(f"{p['name']:20} ({p['category']}) | Lift: {p['lift']:+.1f}% | HP: {p['hp_wr']:.1f}% | Base: {p['base_wr']:.1f}%")

