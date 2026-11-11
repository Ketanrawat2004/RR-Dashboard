import os, re

files = ['jasprit_bumrah.html', 'mohammed_siraj.html', 'rashid_khan.html', 'heinrich_klaasen.html', 'rohit_sharma.html']

for f in files:
    path = os.path.join('players', f)
    with open(path, 'r', encoding='utf-8') as fh:
        text = fh.read()
    matches = re.findall(r'<div class="section-header">([0-9]\.[^<]+)</div>\s*<div class="section-content">(.*?)</div>', text, re.DOTALL)
    print(f"=== {f} ===")
    for title, content in matches:
        content_clean = content.strip().replace('<strong></strong>', '')
        print(f"  {title}: len={len(content_clean)}")

