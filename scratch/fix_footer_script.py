with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix line 1310: replace 8-space indent and 'html =' with 4-space indent and 'player_html ='
old_player_inject = """        html = html.replace('</div>\\n\\n</body>', '''"""
new_player_inject = """    player_html = player_html.replace('</div>\\n\\n</body>', '''"""
assert old_player_inject in text, "old_player_inject not found!"
text = text.replace(old_player_inject, new_player_inject, 1)

# Check player_html replace string: let's also verify what follows '</div>\n\n</body>' in player template
# earlier:
# 1304:     </div>
# 1305: </div>
# 1306: 
# 1307: </body>
# So '</div>\n\n</body>' matches line 1305-1307! That puts the footer right inside the player's .container!

# 2. Fix dashboard footer injection to put it INSIDE .dashboard-container (right before '</div>\n\n<!-- Interactive Power BI Slicer')
old_dash_target = "target_pos = master_dashboard_html.find('<!-- Interactive Power BI Slicer')"
new_dash_target = "target_pos = master_dashboard_html.find('</div>\\n\\n<!-- Interactive Power BI Slicer')"
assert old_dash_target in text, "old_dash_target not found!"
text = text.replace(old_dash_target, new_dash_target, 1)

with open('fix_dashboard_and_wagon.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("✓ Fixed indentation and footer injection placement in fix_dashboard_and_wagon.py")

