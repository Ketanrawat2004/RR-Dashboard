with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<!-- Interactive Power BI Slicer')
print(text[idx-500:idx+200])

