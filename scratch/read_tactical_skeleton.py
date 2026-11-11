with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

s = html.find('id="section-tactical-xi"')
e = html.find('<!-- Interactive Power BI Slicer', s)
section = html[s:e]
print("Length:", len(section))
# print skeleton of div tags / headings inside section-tactical-xi
import re
for line in section.split('\n'):
    stripped = line.strip()
    if any(k in stripped for k in ['class="tactical-', '<h', 'Contingency', 'Phase-by-Phase', 'War Room', 'Auction Bidding', '<table', 'Impact Subs']):
        print(stripped[:110])

