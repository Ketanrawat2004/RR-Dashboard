with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
m = re.search(r'<table id="table-batters">[\s\S]*?<\/tbody>', text)
if m:
    rows = re.findall(r'<tr[^>]*>[\s\S]*?<\/tr>', m.group(0))
    for r in rows[1:6]:
        print(r)
        print("-" * 50)

