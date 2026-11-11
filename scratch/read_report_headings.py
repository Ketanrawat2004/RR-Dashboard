with open('pressure_output/methodology_report.md', 'r', encoding='utf-8') as f:
    text = f.read()

print('Length of methodology_report.md:', len(text))
for line in text.split('\n'):
    if line.startswith('## '):
        print(line)

