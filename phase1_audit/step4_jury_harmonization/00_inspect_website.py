import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print(f"Total HTML length: {len(html):,} chars")

# Find views / tab buttons / nav items
tabs = re.findall(r'data-tab=[\'"](.*?)[\'"]', html)
print("Tabs/Views found:", set(tabs))

sections = re.findall(r'<div[^>]*class=[\'"][^\'"]*view[^\'"]*[\'"][^>]*id=[\'"](.*?)[\'"]', html)
print("View IDs found:", sections)

# Modal / Player profile components
modals = re.findall(r'id=[\'"](.*?(?:modal|profile|drawer|popup).*?)[\'"]', html, re.I)
print("Modals/Drawers found:", set(modals))

# Chart elements / Canvas
canvases = re.findall(r'<canvas[^>]*id=[\'"](.*?)[\'"]', html)
print("Canvas chart IDs:", canvases)

# Script tags / libraries
scripts = re.findall(r'<script[^>]*src=[\'"](.*?)[\'"]', html)
print("External scripts:", scripts)

