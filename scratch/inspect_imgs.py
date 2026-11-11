import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

imgs = list(re.finditer(r'<img[^>]+>', text))
print(f'Total img tags: {len(imgs)}')
for i, m in enumerate(imgs):
    tag = m.group(0)
    tag_clean = re.sub(r'src="data:[^"]+"', 'src="[BASE64]"', tag)
    idx = m.start()
    before = text[max(0, idx-100):idx].replace('\n', ' ')
    print(f'IMG {i}: {tag_clean} | context: {before[-80:]}')

