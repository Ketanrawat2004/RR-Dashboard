with open('rr_war_room_terminal.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Pressure Win Rate vs Normal Win Rate')
print(text[idx-150:idx+3000])

