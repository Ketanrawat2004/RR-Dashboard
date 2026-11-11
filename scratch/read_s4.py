with open('pressure_output/methodology_report.md', 'r', encoding='utf-8') as f:
    text = f.read()

s4 = text.find('## 4. Final Ordered Player Rankings')
s6 = text.find('## 6. Addressing Tournament Evaluation Criteria')
print(text[s4:s4+2000])

