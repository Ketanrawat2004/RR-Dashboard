with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
style_content = re.search(r'<style>(.*?)</style>', text, re.DOTALL).group(1)

# Find where brace count goes negative
count = 0
for line_no, line in enumerate(style_content.splitlines(), start=1):
    for ch in line:
        if ch == '{':
            count += 1
        elif ch == '}':
            count -= 1
            if count < 0:
                print(f"Stray closing brace at style line {line_no}: {line.strip()}")
                break
    if count < 0:
        break

print("Final balance count:", count)

