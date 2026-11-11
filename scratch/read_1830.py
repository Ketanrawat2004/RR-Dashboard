with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1830, 1910):
    print(f"{i+1}: {lines[i].rstrip()}")

