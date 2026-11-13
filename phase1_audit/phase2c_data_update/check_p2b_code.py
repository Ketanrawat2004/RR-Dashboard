with open("phase1_audit/phase2b_integration/06_build_expanded_players_db.py", "r", encoding="utf-8") as f:
    text = f.read()

for line in text.split("\n"):
    if "base_wr" in line or "hp_wr" in line or "lift" in line or "shrunk_score" in line:
        print(line)

