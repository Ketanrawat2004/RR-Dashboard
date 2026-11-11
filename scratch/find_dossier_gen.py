with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'players_db\[.*?\]|players_db\.json|def generate_player_dossier|player_html\s*=', text)
print("Matches in fix_dashboard_and_wagon.py:", matches[:10])

for line in text.splitlines():
    if "section-content" in line:
        print("section-content line:", line.strip())

