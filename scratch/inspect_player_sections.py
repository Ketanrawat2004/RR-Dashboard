with open('players/rinku_singh.html', 'r', encoding='utf-8') as f:
    text_rinku = f.read()

with open('players/jasprit_bumrah.html', 'r', encoding='utf-8') as f:
    text_bumrah = f.read()

import re

print("--- Rinku Sections containing numbers 1, 2, 3, 4 ---")
for line in text_rinku.splitlines():
    if any(k in line for k in ['KEY CAPABILITY', 'COMPARATIVE PERFORMANCE', 'TACTICAL DEPLOYMENT', 'VALUATION & AUCTION', '1.', '2.', '3.', '4.']):
        if len(line.strip()) < 120:
            print("Rinku:", line.strip())

print("\n--- Bumrah Sections containing numbers 1, 2, 3, 4 ---")
for line in text_bumrah.splitlines():
    if any(k in line for k in ['KEY CAPABILITY', 'COMPARATIVE PERFORMANCE', 'TACTICAL DEPLOYMENT', 'VALUATION & AUCTION', '1.', '2.', '3.', '4.']):
        if len(line.strip()) < 120:
            print("Bumrah:", line.strip())

