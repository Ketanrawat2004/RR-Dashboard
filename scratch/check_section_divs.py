with open('rr_war_room_terminal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Check all data-section ids and their div balance
sections = list(re.finditer(r'<div id="(section-[^"]+)"', text))
for i, m in enumerate(sections):
    start = m.start()
    end = sections[i+1].start() if i+1 < len(sections) else text.find('<div class="doc-grid">')
    block = text[start:end]
    opens = len(re.findall(r'<div\b', block))
    closes = len(re.findall(r'</div>', block))
    print(f"Section {m.group(1):22s} | opens: {opens:3d} | closes: {closes:3d} | diff: {opens - closes}")

