with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'matches', text, re.IGNORECASE):
    idx = m.start()
    print(text[max(0, idx-40):min(len(text), idx+60)].replace('\n', ' '))

