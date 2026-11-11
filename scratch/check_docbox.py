with open('rr_war_room_terminal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
doc_match = re.search(r'\.doc-box\s*\{([^}]+)\}', text)
if doc_match:
    print(".doc-box style:", doc_match.group(1).replace('\n', ' '))
else:
    print(".doc-box not found in CSS")

