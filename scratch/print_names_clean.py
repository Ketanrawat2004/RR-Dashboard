with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
match = re.search(r'<div id="section-superstars".*?</table>', html, re.DOTALL)
if match:
    rows = re.findall(r'<tr>(.*?)</tr>', match.group(0), re.DOTALL)
    for r in rows[1:]:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
        name_clean = re.sub(r'<[^>]+>', '', cells[0]).strip()
        print(f"{name_clean:20}: Dataset Matches={cells[1].strip()}, HP Matches={cells[3].strip()}, HP WR={cells[4].strip()}, Lift={cells[5].strip()}")

