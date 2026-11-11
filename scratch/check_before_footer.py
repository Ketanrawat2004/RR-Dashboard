with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<footer class="analyst-footer"')
print(text[idx-2000:idx+100])

