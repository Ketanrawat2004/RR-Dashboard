with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find all inline styles or css with color: var(--rr-navy) or blue hexes in text
blue_text_patterns = [
    r'color:\s*var\(--rr-navy\)',
    r'color:\s*#001D48',
    r'color:\s*#0284C7',
    r'color:\s*#00122e',
    r'color:\s*#0A2540',
]

for pat in blue_text_patterns:
    matches = list(re.finditer(pat, text, re.IGNORECASE))
    print(f"Pattern {pat}: {len(matches)} occurrences")

# Find occurrences in index.html as well
with open('index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

for pat in blue_text_patterns:
    matches = list(re.finditer(pat, html_text, re.IGNORECASE))
    print(f"HTML Pattern {pat}: {len(matches)} occurrences")

