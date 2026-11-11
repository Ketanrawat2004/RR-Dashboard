with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.tactical-grid {')
print(text[idx:idx+400])

print("=== SECTION TACTICAL XI STRUCTURE ===")
s = text.find('<div class="tactical-grid">')
e = text.find('<!-- Bottom Card:', s)
print("Length of tactical-grid block:", e - s)
# let's print the contingency / phase-by-phase / war room blocks
c_idx = text.find('<!-- 1. Contingency', s)
print(text[c_idx:e])

