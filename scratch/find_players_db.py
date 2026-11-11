with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "players_db" in l and ("=" in l or "load" in l):
        print(f"{i+1}: {l.strip()[:100]}")

