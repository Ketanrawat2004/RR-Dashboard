import json

with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

for p in db[:5]:
    print(f"[{p['category']}] {p['name']}: rank_ci_90={p.get('rank_ci_90')}")

for p in db:
    if p["name"] in ["Matheesha Pathirana", "Jasprit Bumrah", "Umran Malik"]:
        print(f"[{p['category']}] {p['name']}: rank_ci_90={p.get('rank_ci_90')}")

