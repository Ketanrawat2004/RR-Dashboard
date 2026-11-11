with open('generate_calibrated_charts.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print(f'Total lines: {len(lines)}')
# print lines 150 to 310
for i in range(140, min(len(lines), 310)):
    print(f'{i+1}: {lines[i]}')

