with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class="executive-header"')
# find where executive-header div closes
idx2 = text.find('<div', idx + 100)
# search for next major class
import re
classes = re.findall(r'<div class="([^"]+)"', text[idx:idx+15000])
print("Classes after executive-header:")
print(classes[:15])

