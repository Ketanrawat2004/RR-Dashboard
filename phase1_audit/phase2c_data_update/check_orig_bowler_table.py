with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
m = re.search(r'<table id="table-bowlers">[\s\S]*?</table>', text)
if m:
    lines = m.group(0).split("\n")
    print("\n".join(lines[:40]))

