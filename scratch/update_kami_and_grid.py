import re

# 1. Read fix_dashboard_and_wagon.py
with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any occurrence of Kami
print("Occurrences of 'kami' in fix_dashboard_and_wagon.py before:", len(re.findall(r'kami', text, re.IGNORECASE)))
text = re.sub(r'\(Kami\s*/\s*Shortcoming\)', '(Strategic Assessment)', text, flags=re.IGNORECASE)
text = re.sub(r'Kami\s*/\s*Shortcoming', 'Strategic Assessment', text, flags=re.IGNORECASE)
text = re.sub(r'\bKami\b', 'Shortcoming', text, flags=re.IGNORECASE)
print("Occurrences of 'kami' in fix_dashboard_and_wagon.py after:", len(re.findall(r'kami', text, re.IGNORECASE)))

# Check tactical-grid CSS
css_old = """.tactical-grid {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 24px;
            margin-bottom: 24px;
        }"""

css_new = """.tactical-grid {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 24px;
            margin-bottom: 24px;
            align-items: start;
        }"""

if css_old in text:
    text = text.replace(css_old, css_new)
    print("✓ Replaced .tactical-grid CSS with align-items: start")
else:
    print("tactical-grid CSS pattern not directly matched, searching with regex")
    text = re.sub(r'\.tactical-grid\s*\{\s*display:\s*grid;\s*grid-template-columns:\s*1\.15fr 0\.85fr;\s*gap:\s*24px;\s*margin-bottom:\s*24px;\s*\}',
                  css_new, text)

# Now let's reorganize the right column inside section-tactical-xi in fix_dashboard_and_wagon.py
# In the right column, we have:
# - Target table
# - Auction Bidding Rule
# - Contingency Bidding Matrix
# - Phase-by-Phase Purse Distribution
# - War Room Strategic Principles
# Let's inspect where they are in fix_dashboard_and_wagon.py
with open('fix_dashboard_and_wagon.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved updated fix_dashboard_and_wagon.py")

