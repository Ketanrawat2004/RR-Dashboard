with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
match = re.search(r'<div id="section-superstars".*?</table>', html, re.DOTALL)
if match:
    table = match.group(0)
    rows = re.findall(r'<tr>(.*?)</tr>', table, re.DOTALL)
    for r in rows[1:]: # skip header
        cells = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
        if len(cells) >= 6:
            name_m = re.search(r'<strong>(.*?)</strong>', cells[0])
            name = name_m.group(1) if name_m else "Unknown"
            dataset_matches = cells[1].strip()
            overall_wr = cells[2].strip()
            hp_matches = cells[3].strip()
            hp_wr = cells[4].strip()
            diff = re.search(r'>([^<]+)</span>', cells[5]).group(1) if re.search(r'>([^<]+)</span>', cells[5]) else cells[5]
            print(f"{name:20}: Dataset Matches={dataset_matches}, Overall WR={overall_wr}, HP Matches={hp_matches}, HP WR={hp_wr}, Diff={diff}")

