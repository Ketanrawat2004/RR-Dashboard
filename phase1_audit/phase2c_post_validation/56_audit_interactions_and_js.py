import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inspect switchBowlingFramework function
m_switch = re.search(r'function switchBowlingFramework\([^)]*\)\s*\{[\s\S]*?\n\}', html)
print("=== switchBowlingFramework ===")
if m_switch:
    print(m_switch.group(0)[:500])
else:
    print("switchBowlingFramework NOT FOUND!")

# 2. Inspect applySlicers function
m_slicers = re.search(r'function applySlicers\([^)]*\)\s*\{[\s\S]*?\n\}', html)
print("\n=== applySlicers ===")
if m_slicers:
    print(m_slicers.group(0)[:500])
else:
    print("applySlicers NOT FOUND!")

# 3. Check dossier links
links = re.findall(r'href=[\'"]players/([^\'"]+)\.html[\'"]', html)
unique_links = sorted(list(set(links)))
print(f"\nTotal player links in index.html: {len(links)}, Unique slugs: {len(unique_links)}")

missing_files = []
existing_files = []
for slug in unique_links:
    fpath = os.path.join('players', f'{slug}.html')
    if os.path.exists(fpath):
        existing_files.append(slug)
    else:
        missing_files.append(slug)

print(f"Existing player dossier files: {len(existing_files)}")
print(f"Missing player dossier files: {len(missing_files)}")
if missing_files:
    print("Sample missing:", missing_files[:10])

# 4. Check CSS and Responsive classes
classes_to_check = [
    'bowler-row-composite', 'bowler-row-rpae', 'col-bowler-comp', 'col-bowler-rpae',
    'tab-group', 'nav-tab-btn', 'framework-toggle-btn', 'active', 'data-section'
]
css_check = {}
for c in classes_to_check:
    css_check[c] = c in html

print("\n=== CSS Class Check in index.html ===")
for c, found in css_check.items():
    print(f"  {c}: {'FOUND' if found else 'MISSING'}")

