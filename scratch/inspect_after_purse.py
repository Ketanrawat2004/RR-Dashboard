with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
target = 'class="purse-table"'
idx = text.find(target)
if idx != -1:
    idx2 = text.find(target, idx + 100)
    sub = text[idx2:]
    end_tag = '<!-- Analytics Audit Tab Script'
    end_idx = sub.find(end_tag)
    if end_idx != -1:
        sub = sub[:end_idx]
    sub = re.sub(r'data:image/png;base64,[A-Za-z0-9+/=]+', '[BASE64_IMAGE]', sub)
    print("AFTER PURSE TABLE:")
    print(sub[:4000])
else:
    print("Not found")

