with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="section-tactical-xi"')
print("TACTICAL SECTION PREVIEW:")
print(text[idx:idx+1500])

