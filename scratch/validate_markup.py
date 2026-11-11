import re

with open('scratch/preview_chart.html', 'r', encoding='utf-8') as f:
    html = f.read()

circles = []
for m in re.finditer(r'<circle cx="([\d\.]+)" cy="([\d\.]+)" r="([\d\.]+)"', html):
    cy = float(m.group(2))
    if cy > 40:
        circles.append((float(m.group(1)), cy, float(m.group(3))))

texts = []
for m in re.finditer(r'<text x="([\d\.]+)" y="([\d\.]+)"(?: text-anchor="(start|middle|end)")?[^>]*>(.*?)</text>', html):
    x = float(m.group(1))
    y = float(m.group(2))
    anchor = m.group(3) or 'start'
    content = m.group(4)
    if any(tag in content for tag in ['Batters', 'Bowlers', 'sample volume', 'Close Finishes', 'Pressure Lift', '%']):
        continue
    texts.append((x, y, anchor, content))

print(f'Total player dots: {len(circles)}')
print(f'Total player/quadrant texts: {len(texts)}')

char_w = 6.2
line_h = 12
boxes = []
for x, y, anchor, content in texts:
    tw = len(content.replace('&bull;', '•')) * char_w
    if anchor == 'middle':
        bx1 = x - tw/2
        bx2 = x + tw/2
    elif anchor == 'end':
        bx1 = x - tw
        bx2 = x
    else:
        bx1 = x
        bx2 = x + tw
    by1 = y - line_h
    by2 = y + 2
    boxes.append((content, (bx1, by1, bx2, by2)))

collisions = []
for i in range(len(boxes)):
    for j in range(i+1, len(boxes)):
        n1, b1 = boxes[i]
        n2, b2 = boxes[j]
        pad = 2
        if not (b1[2] + pad < b2[0] or b2[2] + pad < b1[0] or b1[3] + pad < b2[1] or b2[3] + pad < b1[1]):
            collisions.append((n1, n2))

print(f'Text-to-text collisions: {len(collisions)}')
for c in collisions:
    print('  COLLISION:', c[0], '<--->', c[1])

dot_collisions = []
for content, b in boxes:
    for cx, cy, r in circles:
        if (b[0] - 6 <= cx <= b[2] + 6) and (b[1] - 6 <= cy <= b[3] + 6):
            dot_collisions.append((content, (cx, cy)))

print(f'Text-to-dot collisions: {len(dot_collisions)}')
for dc in dot_collisions:
    print('  DOT OVERLAP:', dc[0], 'covers dot at', dc[1])

