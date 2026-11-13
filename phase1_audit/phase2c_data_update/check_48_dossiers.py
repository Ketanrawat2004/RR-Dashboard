import os
import json

dossiers = os.listdir("players")
print(f"Total dossiers in players/: {len(dossiers)}")

with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db_keys = {p["key"]: p for p in db}

matched = 0
for d in dossiers:
    key = d.replace(".html", "")
    if key in db_keys:
        matched += 1
    else:
        print(f"  Dossier not in db: {d}")

print(f"Matched {matched} of {len(dossiers)} dossiers to players_db.json.")

