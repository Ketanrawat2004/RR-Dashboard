import json

with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

for p in db:
    if p["name"] in ["Jasprit Bumrah", "Matheesha Pathirana", "Andre Russell", "Vaibhav Sooryavanshi"]:
        print(f"[{p['category']}] {p['name']}: rank={p['rank']}, hp_wr={p['hp_wr']}, base_wr={p['base_wr']}, lift={p['lift']}, shrunk_score={p['shrunk_score']}, comp={p.get('composite_score')}, rpae={p.get('shrunk_rpae_score')}")

