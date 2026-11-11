with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'section-tactical-xi' in l:
        print(f"Tactical section starts at line {i+1}")
    if '<!-- Analytics Audit Tab Script' in l:
        print(f"Analytics Audit Tab Script at line {i+1}")

