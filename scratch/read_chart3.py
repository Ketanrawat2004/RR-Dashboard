with open('generate_calibrated_charts.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('chart3_path')
if idx != -1:
    print(text[max(0, idx-2000):idx+200])

