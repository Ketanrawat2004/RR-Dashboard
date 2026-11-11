with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find where .doc-box starts around line 1830
idx1 = text.find('.doc-box {{')
if idx1 == -1:
    idx1 = text.find('.doc-box {')

# Find where this block ends (right after .code-snippet)
idx2 = text.find('.footer', idx1)
if idx2 == -1:
    idx2 = text.find('.pill-header', idx1)

print("Found doc-box block between:", idx1, idx2)
print("Snippet to replace:")
print(text[idx1:idx1+800])

