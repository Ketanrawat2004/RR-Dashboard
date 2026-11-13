with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
sections = re.findall(r'<div id="(section-[^"]*)"', text)
print("Sections in index.html in order:", sections)

