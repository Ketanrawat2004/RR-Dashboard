with open('index.html', encoding='utf-8') as f:
    html = f.read()

idx = html.find('class="simple-footer"')
print(html[idx:idx+2500])
