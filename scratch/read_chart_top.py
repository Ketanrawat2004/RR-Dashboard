with open('generate_calibrated_charts.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i in range(0, min(105, len(lines))):
    print(f'{i+1}: {lines[i]}')

