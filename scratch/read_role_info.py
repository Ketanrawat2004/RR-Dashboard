with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "technical_strength" in l:
        for j in range(max(0, i-40), min(len(lines), i+30)):
            print(f"{j+1}: {lines[j]}", end="")
        break

