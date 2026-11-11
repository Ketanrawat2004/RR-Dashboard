with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<!-- Interactive Power BI Slicer')
print(repr(text[idx-120:idx+60]))

idx2 = text.rfind('# Inject Executive Footer')
print("FOOTER BLOCK AT:", idx2)
print(repr(text[idx2:idx2+300]))

