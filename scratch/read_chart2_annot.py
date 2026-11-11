with open('generate_calibrated_charts.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i in range(105, 145):
    print(f'{i+1}: {lines[i]}')

