with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2825, min(2870, len(lines))):
    print(f"{i+1}: {lines[i].rstrip()}")

