with open("phase1_audit/phase2_backup_pre_implementation/players_db.json", "r", encoding="utf-8") as f:
    text = f.read()

import json
db_orig = json.loads(text)
print("Keys in db_orig[0]:", list(db_orig[0].keys()))
for p in db_orig[:5]:
    print(p["name"], p["category"], "hp_m:", p.get("hp_m"), "total_m:", p.get("total_m"))

