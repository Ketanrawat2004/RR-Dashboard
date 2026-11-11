with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

retained_keys = ['yashasvi_jaiswal', 'sanju_samson', 'riyan_parag', 'dhruv_jurel', 'shimron_hetmyer', 'sandeep_sharma']

for k in retained_keys:
    pattern = f"onclick=\"window.location.href='players/{k}.html'\""
    replacement = "title=\"Retained Franchise Core &bull; Not in Auction Pool\" style=\"cursor:default;\""
    text = text.replace(pattern, replacement)

with open('fix_dashboard_and_wagon.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated retained players click behavior in fix_dashboard_and_wagon.py")

