with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'players_db = \[(.*?)\]\n\n#', text, re.DOTALL)
if matches:
    print("players_db length:", len(matches[0]))
    # parse ranks and names
    names = re.findall(r'"rank":\s*(\d+).*?"name":\s*"([^"]+)".*?"category":\s*"([^"]+)"', matches[0], re.DOTALL)
    print("Batters in players_db:")
    for r, n, c in names:
        if c == 'Batter':
            print(f"  Rank {r}: {n}")
    print("\nBowlers in players_db:")
    for r, n, c in names:
        if c == 'Bowler':
            print(f"  Rank {r}: {n}")

