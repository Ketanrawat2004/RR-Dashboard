with open('players/jasprit_bumrah.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'KEY CAPABILITY', text)]
print('KEY CAPABILITY matches in jasprit_bumrah.html:', len(matches))
for m in matches:
    print(text[m-50:m+400])

