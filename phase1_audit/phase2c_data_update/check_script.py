import re
from collections import Counter

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

roles = re.findall(r'data-role="([^"]*)"', text)
c = Counter(roles)
for k, v in c.items():
    print(f"{k}: {v}")

