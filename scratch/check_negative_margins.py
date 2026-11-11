with open('rr_war_room_terminal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Negative margins found:")
for m in re.finditer(r'margin[^:]*:\s*-[0-9]+', text):
    idx = m.start()
    print(text[max(0, idx-40):min(len(text), idx+60)].replace('\n', ' '))

print("\nChecking all elements with position:absolute or relative or z-index:")
for m in re.finditer(r'position:\s*(absolute|fixed|sticky)', text):
    idx = m.start()
    print(text[max(0, idx-50):min(len(text), idx+80)].replace('\n', ' '))

