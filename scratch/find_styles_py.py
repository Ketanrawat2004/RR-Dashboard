with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for i, m in enumerate(re.finditer(r'</style>', text)):
    idx = m.start()
    print(f"Occurrence {i} at {idx}:")
    print(text[idx-120:idx+120])
    print("---")

