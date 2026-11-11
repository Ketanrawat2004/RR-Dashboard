with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
idx = text.find('Jasprit Bumrah')
if idx != -1:
    print(text[idx-200:idx+600])

