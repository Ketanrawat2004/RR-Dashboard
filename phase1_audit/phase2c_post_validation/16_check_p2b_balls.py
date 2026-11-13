with open("phase1_audit/phase2b_integration/06_build_expanded_players_db.py", "r", encoding="utf-8") as f:
    text = f.read()

for i, line in enumerate(text.split("\n")):
    if "pressure_balls" in line or "career_balls" in line:
        print(f"{i}: {line}")

