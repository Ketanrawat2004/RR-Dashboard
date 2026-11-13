import json

with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

missing_id = [p for p in db if "player_id" not in p or p["player_id"] is None]
print(f"Missing player_id count: {len(missing_id)}")

