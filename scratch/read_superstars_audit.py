with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "superstars_audit =" in l:
        for j in range(max(0, i-2), min(len(lines), i+60)):
            print(f"{j+1}: {lines[j]}", end="")
        break

