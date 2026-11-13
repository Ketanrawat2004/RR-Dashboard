import json

with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

# check keys of a sample batter and bowler
print("Keys in batter:", list(db[0].keys()))
for p in db[:5]:
    print(p["category"], p["name"], "| role_desc:", p.get("role_desc"), "| role:", p.get("role"))

