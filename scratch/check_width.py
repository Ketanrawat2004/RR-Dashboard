with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
idx = text.find('master_dashboard_html = f"""')
for m in re.finditer(r'max-width:\s*\d+px', text[idx:idx+4000]):
    print(m.group(0), '|', text[idx+m.start()-60:idx+m.end()+20].replace('\n', ' '))

