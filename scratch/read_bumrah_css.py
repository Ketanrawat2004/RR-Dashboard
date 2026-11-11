with open('players/jasprit_bumrah.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m1 = re.search(r'\.section-card\s*\{[^}]+\}', text)
if m1: print(m1.group(0))
m2 = re.search(r'\.section-header\s*\{[^}]+\}', text)
if m2: print(m2.group(0))
m3 = re.search(r'\.section-content\s*\{[^}]+\}', text)
if m3: print(m3.group(0))

