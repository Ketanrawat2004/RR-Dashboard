with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'function applySlicers\(.*?\n\}', text, re.DOTALL)
for m in matches:
    print("applySlicers implementation:\n", m)

matches2 = re.findall(r'function showSection\(.*?\n\}', text, re.DOTALL)
for m in matches2:
    print("showSection implementation:\n", m)

