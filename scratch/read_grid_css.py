with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
matches = re.findall(r'\.tactical-grid\s*\{[^}]+\}', html)
for m in matches:
    print(m)
matches2 = re.findall(r'\.tactical-card\s*\{[^}]+\}', html)
for m in matches2:
    print(m)

