with open("players/andre_russell.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
# find all numbers with labels
cards = re.findall(r'<div[^>]*class="[^"]*card[^"]*"[^>]*>[\s\S]*?<\/div>', text)
print(f"Total cards: {len(cards)}")
for c in cards[:10]:
    clean = re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', ' ', c)).strip()
    if clean:
        print(" ", clean[:100])

