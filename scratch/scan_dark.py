with open('rr_war_room_terminal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# find background colors in css
styles = re.findall(r'([^{]+)\{([^}]+)\}', text[:text.find('</style>')])
print("Styles with dark backgrounds (#0... or #1... or rgb(0...):")
for sel, body in styles:
    if any(k in body.lower() for k in ['#001', '#0b1', '#0a2', '#00122e', '#001026', '#020', '#111']):
        print(f"Selector: {sel.strip()[:60]} -> {body.strip()[:100]}...")

