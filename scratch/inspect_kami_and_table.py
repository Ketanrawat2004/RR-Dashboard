import re

with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

print("=== KAMI IN fix_dashboard_and_wagon.py ===")
for m in re.finditer(r'kami', text, re.IGNORECASE):
    idx = m.start()
    print(text[max(0, idx-80):min(len(text), idx+100)].replace('\n', ' '))
    print("---")

with open('rr_war_room_terminal.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("\n=== AROUND LINE 2945 OF rr_war_room_terminal.html ===")
for i in range(max(0, 2930), min(len(lines), 2965)):
    print(f"{i+1}: {lines[i].rstrip()}")

print("\n=== KAMI IN rr_war_room_terminal.html ===")
html_text = "".join(lines)
for m in re.finditer(r'kami', html_text, re.IGNORECASE):
    idx = m.start()
    print(html_text[max(0, idx-80):min(len(html_text), idx+100)].replace('\n', ' '))
    print("---")

