import json

with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

b = next(p for p in db if p["category"] == "Batter")
print("Batter fields with exp or sr:")
for k, v in b.items():
    if "exp" in k or "sr" in k or "econ" in k:
        print(f"  {k}: {v}")

bw = next(p for p in db if p["category"] == "Bowler")
print("\nBowler fields with exp or sr or econ:")
for k, v in bw.items():
    if "exp" in k or "sr" in k or "econ" in k:
        print(f"  {k}: {v}")

