with open('rr_war_room_terminal.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<div class="doc-grid">')
print("=== CONTEXT AROUND .doc-grid ===")
print(text[idx-600:idx+400])

import re
for m in re.finditer(r'\.doc-grid\s*\{[^}]+\}', text):
    print("\n=== .doc-grid CSS ===")
    print(m.group(0))
for m in re.finditer(r'\.tactical-card\s*\{[^}]+\}', text):
    print("\n=== .tactical-card CSS ===")
    print(m.group(0))
for m in re.finditer(r'\.doc-box\s*\{[^}]+\}', text):
    print("\n=== .doc-box CSS ===")
    print(m.group(0))

