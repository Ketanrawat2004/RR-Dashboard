with open('players/jasprit_bumrah.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<div class="section-card">([\s\S]*?)</div>\s*</div>', text)
for i, m in enumerate(matches):
    if 'Key Capability' in m:
        print(f'Match {i}:')
        print(m)

