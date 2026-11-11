with open('rr_war_room_terminal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("File length:", len(text))
# Check body background
bg_match = re.search(r'body\s*\{([^}]+)\}', text)
if bg_match:
    print("Body style:", bg_match.group(1).replace('\n', ' '))

# Check header style
header_match = re.search(r'\.header-container\s*\{([^}]+)\}', text)
if header_match:
    print("Header style:", header_match.group(1).replace('\n', ' '))

# Check nav tabs
tab_match = re.search(r'\.nav-tab-btn\s*\{([^}]+)\}', text)
if tab_match:
    print("Tab style:", tab_match.group(1).replace('\n', ' '))

