with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class="quadrant-light-grid"')
if idx != -1:
    print("QUADRANTS AND TAKEAWAYS HTML PREVIEW:")
    print(text[idx:idx+2500])

