with open("players/jasprit_bumrah.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
sections = re.findall(r'<div class="section-card">\s*<div class="section-header">(.*?)</div>\s*<div class="section-content">(.*?)</div>\s*</div>', text, re.DOTALL)
for header, content in sections:
    print(f"HEADER: {header}")
    print(f"CONTENT:\n{content.strip()}\n" + "-"*40)

