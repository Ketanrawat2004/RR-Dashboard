with open('rr_war_room_terminal.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<div class="doc-grid">')
print(text[idx-1500:idx])

