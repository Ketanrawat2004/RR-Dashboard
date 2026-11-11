with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('id="section-tactical-xi"')
e = text.find('<!-- Bottom Card:', s)
print(text[s:s+2500])
print("\n... [MIDDLE] ...\n")
print(text[e-1500:e+300])

