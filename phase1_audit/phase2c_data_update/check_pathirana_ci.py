import json

with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

for p in db:
    if p["name"] == "Matheesha Pathirana":
        for k, v in p.items():
            if "ci" in k or "rank" in k:
                print(f"  {k}: {v}")

