with open('players/jasprit_bumrah.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<div class="section-card">([\s\S]*?)</div>', text)
print('section-card count:', len(matches))
for i, m in enumerate(matches):
    print(f'Card {i}:', m[:200].replace('\n', ' '))
