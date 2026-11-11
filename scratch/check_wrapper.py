with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<!-- Interactive Power BI Slicer')
print("=== BEFORE SCRIPT TAG ===")
print(text[idx-250:idx])

