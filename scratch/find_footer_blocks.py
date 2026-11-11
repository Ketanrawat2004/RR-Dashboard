with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<!-- Executive Analyst Footer', text)]
print(f"Found {len(matches)} footer blocks in fix_dashboard_and_wagon.py")
for idx in matches:
    print(f"At {idx}: {text[idx-40:idx+120].replace(chr(10), ' ')}")

