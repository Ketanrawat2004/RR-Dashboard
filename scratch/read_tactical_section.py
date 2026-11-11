with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

s = html.find('id="section-tactical-xi"')
e = html.find('id="section-methodology"', s)
if e == -1:
    e = html.find('</main>', s)

print("Length of section-tactical-xi:", e - s)
section = html[s:e]

# Let's count cards and headings
import re
titles = re.findall(r'<div class="tactical-card-title">([\s\S]*?)</div>', section)
for t in titles:
    print("CARD TITLE:", t.strip().replace('\n', ' '))
