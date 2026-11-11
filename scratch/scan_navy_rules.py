with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'([^{]+)\{([^}]+)\}', text)
print("CSS rules using --rr-navy:")
for sel, body in matches:
    if '--rr-navy' in body:
        print(f"  {sel.strip()[:50]} -> {[line.strip() for line in body.split(';') if '--rr-navy' in line]}")

