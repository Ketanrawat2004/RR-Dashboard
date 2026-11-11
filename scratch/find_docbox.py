with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'\.doc-box', text)]
print("Total occurrences of .doc-box in fix_dashboard_and_wagon.py:", len(matches))
for idx in matches:
    print("---")
    print(text[idx-20:idx+250].replace('\n', ' '))

