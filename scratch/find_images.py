with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<img\s+src="data:image', text)]
print(f"Total base64 images in fix_dashboard_and_wagon.py: {len(matches)}")
for idx in matches:
    print(text[idx-200:idx+100].replace('\n', ' '))

