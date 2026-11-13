with open("phase1_audit/step3_1_validation/STEP3_1_INDEPENDENT_VALIDATION_REPORT.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
m = re.findall(r'\|[^\n]*Umran Malik[^\n]*\|', text)
for line in m:
    print(line)

