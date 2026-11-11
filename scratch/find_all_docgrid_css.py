with open('rr_war_room_terminal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'\.doc-grid\s*\{[^}]+\}', text):
    start = m.start()
    print(f"At {start}: {text[max(0, start-60):start+150]}")

