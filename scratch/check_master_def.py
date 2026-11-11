with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'master_dashboard_html\s*=', text)]
for m in matches:
    print(text[m:m+120])
    print('---')
