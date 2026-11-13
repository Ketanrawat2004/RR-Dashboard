import json

with open("phase1_audit/phase2_backup_pre_implementation/players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

for p in db[:10]:
    print(f"[{p['category']}] {p['name']}: hp_wr={p['hp_wr']}, base_wr={p['base_wr']}, lift={p['lift']}")

