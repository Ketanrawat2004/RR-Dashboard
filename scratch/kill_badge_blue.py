with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace #1E40AF with #0F172A
text = text.replace('color: #1E40AF;', 'color: #0F172A;')
text = text.replace('background: #EFF6FF;', 'background: #F1F5F9;')
text = text.replace('border: 1px solid #BFDBFE;', 'border: 1px solid #CBD5E1;')

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Replaced retained badge blue colors with neutral slate!")

