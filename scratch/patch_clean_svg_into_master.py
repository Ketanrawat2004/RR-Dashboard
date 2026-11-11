import os
import sys
import re

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("scratch"))

from generate_clean_svg import generate_zero_collision_svg

with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    content = f.read()

# Target pattern: <svg viewBox="0 0 860 480" ... </svg>
pattern = r'<svg viewBox="0 0 860 480".*?</svg>'
match = re.search(pattern, content, re.DOTALL)
if not match:
    print("ERROR: Target old SVG not found in fix_dashboard_and_wagon.py!")
else:
    print(f"Found old SVG at {match.start()} to {match.end()} (length: {len(match.group(0))})")
    new_svg = generate_zero_collision_svg()
    updated_content = content[:match.start()] + new_svg + content[match.end():]
    
    with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("Successfully replaced SVG in fix_dashboard_and_wagon.py!")
