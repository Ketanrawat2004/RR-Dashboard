with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(3280, len(lines)):
    if 'slicer' in lines[i].lower() or 'search' in lines[i].lower() or 'tab' in lines[i].lower():
        print(f"{i+1}: {lines[i].strip()}")

