with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
style_content = re.search(r'<style>(.*?)</style>', text, re.DOTALL).group(1)
lines = style_content.splitlines()

for i in range(max(0, 1115), min(len(lines), 1130)):
    print(f"{i+1}: {lines[i]}")

