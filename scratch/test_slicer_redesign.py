with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
slicer_card = re.search(r'<!-- Power BI Interactive Slicer Bar -->.*?<!-- Table 1: Batters -->', text, re.DOTALL)
if slicer_card:
    print("Found slicer card! Length:", len(slicer_card.group(0)))
    print(slicer_card.group(0)[:500])
else:
    print("Not found!")

