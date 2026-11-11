with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "superstars_audit" in l or "jasprit_bumrah" in l:
        print(f"{i+1}: {l.strip()[:100]}")

