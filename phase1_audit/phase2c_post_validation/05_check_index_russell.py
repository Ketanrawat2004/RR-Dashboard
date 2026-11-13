with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
m = re.findall(r'<tr[^>]*>[\s\S]*?Andre Russell[\s\S]*?<\/tr>', text)
for r in m:
    print(r)
    print("="*60)

