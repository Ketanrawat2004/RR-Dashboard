with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# Check Superstars table rows
superstar_rows = re.findall(r'<td style="text-align:center;font-weight:600;">(\d+)</td>', html)
print("Superstars table matches counts:", superstar_rows[:10])

# Check Right Column additions
has_contingency = "Contingency Bidding Matrix" in html
has_purse_dist = "Phase-by-Phase Purse Distribution" in html
has_war_room = "War Room Principles &bull; IPL 2027 Auction" in html

print("Right Column additions in index.html:")
print("  has_contingency:", has_contingency)
print("  has_purse_dist:", has_purse_dist)
print("  has_war_room:", has_war_room)

