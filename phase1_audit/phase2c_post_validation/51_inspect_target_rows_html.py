import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

rows = re.findall(r'<tr[^>]*>.*?</tr>', html, re.DOTALL)
print(f'Total rows in index.html: {len(rows)}')

targets = [
    'Andre Russell', 'Glenn Maxwell', 'Tim David', 'Abhishek Sharma',
    'Matheesha Pathirana', 'Jasprit Bumrah', 'Maheesh Theekshana', 'Umran Malik', 'Mayank Yadav'
]

for name in targets:
    found = [r for r in rows if name in r]
    print(f'=== {name} ({len(found)} rows) ===')
    for r in found:
        # extract td content
        tds = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
        clean = [' '.join(re.sub(r'<[^>]+>', ' ', td).split()) for td in tds]
        classes = re.findall(r'class="([^"]*)"', r)
        print(f'  Classes: {classes}')
        print(f'  Cells: {clean[:9]}')

