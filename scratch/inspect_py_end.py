with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

print("=== CSS END IN fix_dashboard_and_wagon.py ===")
idx_style = text.find('</style>')
print(text[idx_style-400:idx_style+100])

print("\n=== HTML END IN fix_dashboard_and_wagon.py ===")
idx_script = text.find('<!-- Interactive Power BI Slicer')
print(text[idx_script-400:idx_script+200])

