import json

with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

for p in db:
    if p["name"] in ["Jasprit Bumrah", "Matheesha Pathirana", "Rashid Khan", "Sunil Narine", "Mohit Sharma"]:
        if p["category"] == "Bowler":
            print(f"Bowler {p['name']}: rank={p['rank']}, rank_composite={p.get('rank_composite')}, rank_pure_rpae={p.get('rank_pure_rpae')}, comp_score={p.get('composite_score')}, rpae_score={p.get('shrunk_rpae_score')}")

