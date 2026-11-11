with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
target = 'romario_shepherd'
idx = text.find(target)
if idx != -1:
    sub = text[idx:idx+5000]
    sub = re.sub(r'data:image/png;base64,[A-Za-z0-9+/=]+', '[BASE64_IMAGE]', sub)
    print("AFTER ROMARIO:")
    print(sub)
else:
    print("Not found")

