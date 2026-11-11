with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class="doc-grid"')
print(text[idx:idx+900])

