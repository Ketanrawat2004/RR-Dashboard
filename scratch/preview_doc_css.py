with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\.doc-[^{]+)\{([^}]+)\}', text)
for sel, body in matches:
    print(sel.strip(), '->', body.strip().replace('\n', ' '))

