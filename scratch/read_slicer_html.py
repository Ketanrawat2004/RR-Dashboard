with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(2330, 2370):
    print(f"{i+1}: {lines[i]}", end="")

