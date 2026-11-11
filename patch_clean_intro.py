import base64
import re
from pathlib import Path

# 1. Read the current fix_dashboard_and_wagon.py
with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines currently: {len(lines)}")

# Let's clean the accidental injection in player template (between line 1400 and 1510)
# Look for line with '<!-- Cinematic War Room Intro Controller -->'
cleaned_lines = []
skip = False
for idx, line in enumerate(lines):
    if "<!-- Cinematic War Room Intro Controller -->" in line:
        skip = True
        continue
    if skip and "</body>" in line:
        skip = False
        cleaned_lines.append("</body>\n")
        continue
    if not skip:
        cleaned_lines.append(line)

content = "".join(cleaned_lines)

# Also remove any trailing duplicate intro controller before the final </body>
# Let's inspect if there is any other intro controller in content
parts = content.split("<!-- Cinematic War Room Intro Controller -->")
if len(parts) > 1:
    # Keep before the intro controller and take after </html>
    before = parts[0]
    after = parts[-1].split("</html>\n\"\"\"")[-1]
    content = before + "</body>\n</html>\n\"\"\"" + after

# Also remove .rr-entry-overlay from inside the CSS if it's there
# We will inject it via clean replace outside f-string
content = re.sub(r'/\* =+\s*CINEMATIC WAR ROOM ENTRY ANIMATION OVERLAY[\s\S]*?@media \(max-width: 600px\) \{\{[\s\S]*?\}\}\s*', '', content)

# Also remove the entry overlay html from inside the template if it's there
content = re.sub(r'<!-- CINEMATIC WAR ROOM STARTING ENTRY OVERLAY -->[\s\S]*?<!-- Header Section -->', '<!-- Header Section -->', content)

# Check rr_official_logo.png
with open("rr_official_logo.png", "rb") as f:
    rr_official_logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

# Let's write out this clean base
with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✓ Base fix_dashboard_and_wagon.py cleaned.")

