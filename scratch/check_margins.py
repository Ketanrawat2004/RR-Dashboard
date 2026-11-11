with open('rr_war_room_terminal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for cls in ['.doc-grid', '.table-card', '.section-card', '.data-section', '.dashboard-container']:
    matches = re.findall(re.escape(cls) + r'\s*\{[^}]+\}', text)
    print(f"=== {cls} ===")
    for m in matches:
        print(m)

