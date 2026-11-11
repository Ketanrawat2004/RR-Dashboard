with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.rfind("master_dashboard_html = master_dashboard_html.replace")
print(text[idx:])

