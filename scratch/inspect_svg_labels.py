with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
svg_match = re.search(r'<svg viewBox="0 0 920 540"[^>]*>([\s\S]*?)</svg>', text)
if svg_match:
    svg_content = svg_match.group(1)
    texts = re.findall(r'<text([^>]*)>(.*?)</text>', svg_content)
    print(f'Total text elements in scatter SVG: {len(texts)}')
    for attrs, content in texts:
        if '#' in content or 'Kohli' in content or 'Iyer' in content or 'Atal' in content or 'QUADRANT' in content:
            x_m = re.search(r'x="([^"]+)"', attrs)
            y_m = re.search(r'y="([^"]+)"', attrs)
            anchor_m = re.search(r'text-anchor="([^"]+)"', attrs)
            x = x_m.group(1) if x_m else '?'
            y = y_m.group(1) if y_m else '?'
            anchor = anchor_m.group(1) if anchor_m else 'start'
            print(f'x={x:>6}, y={y:>6}, anchor={anchor:>6} | {content}')

