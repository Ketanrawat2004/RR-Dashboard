with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '.doc-box' in l or '.doc-heading' in l:
        print(f"Line {i+1}: {l.strip()[:100]}")

