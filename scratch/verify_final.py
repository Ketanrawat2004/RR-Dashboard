with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# check tier-badge in table
tier_matches = re.findall(r'<span class="tier-badge[^"]*"[^>]*>[^<]+</span>', text)
print('Tier badges in index.html:', len(tier_matches))
for tm in tier_matches[:4]:
    print(' ', tm)

# check prices
price_matches = re.findall(r'&#8377;[\d\.]+\s*Cr', text)
print('Prices in index.html:', len(price_matches))
for pm in price_matches[:4]:
    print(' ', pm)

# check SVG scatter plot
svg_match = '<svg viewBox="0 0 860 480"' in text
print('Light-mode SVG scatter plot present:', svg_match)

# check CSS for tier-badge
tb_css = re.search(r'\.tier-badge\s*\{([^}]+)\}', text)
if tb_css:
    print('.tier-badge CSS:', tb_css.group(1).replace('\n', ' '))

