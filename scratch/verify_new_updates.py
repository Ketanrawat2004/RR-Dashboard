import re

for filename in ['index.html', 'rr_war_room_terminal.html', 'rr_pressure_dashboard.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    print(f"=== Checking {filename} ===")
    
    # 1. CSS & Script Braces
    style_matches = re.findall(r'<style>(.*?)</style>', html, re.DOTALL)
    for i, s in enumerate(style_matches):
        opens = s.count('{')
        closes = s.count('}')
        print(f"  Style {i+1}: {opens} opens, {closes} closes (diff: {opens - closes})")
        if opens != closes:
            print("  ERROR: CSS brace mismatch!")

    script_matches = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
    for i, sc in enumerate(script_matches):
        opens = sc.count('{')
        closes = sc.count('}')
        print(f"  Script {i+1}: {opens} opens, {closes} closes (diff: {opens - closes})")
        if opens != closes:
            print("  ERROR: Script brace mismatch!")

    # 2. Donut Rolling Animation
    has_animate = '<animateTransform attributeName="transform" type="rotate" from="0 80 80" to="360 80 80"' in html
    has_rolling_class = 'class="rolling-donut-ring"' in html
    has_rolling_keyframes = '@keyframes rollingDonut' in html
    print(f"  Donut animateTransform: {has_animate}")
    print(f"  Donut rolling class: {has_rolling_class}")
    print(f"  Donut @keyframes: {has_rolling_keyframes}")

    # 3. Slicer Layout
    has_tabs_row = 'class="slicer-tabs-row"' in html
    has_controls_row = 'class="slicer-controls-row"' in html
    has_search_wrapper = 'class="search-wrapper"' in html
    has_status_badge = 'class="slicer-status-badge"' in html
    has_reset_btn = 'class="slicer-reset-btn"' in html
    has_reset_fn = 'function resetSlicers()' in html
    print(f"  Slicer tabs row: {has_tabs_row}")
    print(f"  Slicer controls row: {has_controls_row}")
    print(f"  Slicer search wrapper: {has_search_wrapper}")
    print(f"  Slicer status badge: {has_status_badge}")
    print(f"  Slicer reset button: {has_reset_btn}")
    print(f"  Slicer reset JS: {has_reset_fn}")

print("\nRunning scatter plot collision verification...")
import subprocess
res = subprocess.run(["python", "scratch/validate_all_html.py"], capture_output=True, text=True)
print(res.stdout)

