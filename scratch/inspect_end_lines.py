with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)-80, len(lines)):
    print(f"{i+1}: {lines[i].rstrip()}")

