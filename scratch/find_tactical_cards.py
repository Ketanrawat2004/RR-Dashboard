with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'tactical-card', text)]
print(f'tactical-card matches: {len(matches)}')
for i, m in enumerate(matches):
    print(f'Match {i}:')
    print(text[m:m+250].replace('\n', ' '))

