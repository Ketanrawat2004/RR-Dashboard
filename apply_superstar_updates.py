with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add "key" to superstars_audit items
replacements = [
    ('"name": "Jasprit Bumrah",', '"name": "Jasprit Bumrah",\n        "key": "jasprit_bumrah",'),
    ('"name": "Mohammed Siraj",', '"name": "Mohammed Siraj",\n        "key": "mohammed_siraj",'),
    ('"name": "Rashid Khan",', '"name": "Rashid Khan",\n        "key": "rashid_khan",'),
    ('"name": "Heinrich Klaasen",', '"name": "Heinrich Klaasen",\n        "key": "heinrich_klaasen",'),
    ('"name": "Rohit Sharma",', '"name": "Rohit Sharma",\n        "key": "rohit_sharma",')
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f"Added key for {old}")

# 2. Update superstars table loop to include thumbnail photo
old_loop = '''for s in superstars_audit:
    diff_sign = f"{s['lift']:.1f}%"
    master_dashboard_html += f"""
                <tr>
                    <td><strong style="color:var(--rr-navy);font-size:13px;">{s['name']}</strong></td>'''

new_loop = '''for s in superstars_audit:
    s_img = player_images.get(s.get("key", ""), "")
    diff_sign = f"{s['lift']:.1f}%"
    master_dashboard_html += f"""
                <tr>
                    <td>
                        <div class="player-flex">
                            <div class="thumb-img"><img src="{s_img}" alt="{s['name']}"></div>
                            <div>
                                <strong style="color:var(--rr-navy);font-size:13px;">{s['name']}</strong>
                            </div>
                        </div>
                    </td>'''

if old_loop in content:
    content = content.replace(old_loop, new_loop, 1)
    print("Updated superstars table loop with photo thumbnails.")
else:
    print("Warning: old_loop not found directly, checking variations...")

with open('fix_dashboard_and_wagon.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved fix_dashboard_and_wagon.py.")

