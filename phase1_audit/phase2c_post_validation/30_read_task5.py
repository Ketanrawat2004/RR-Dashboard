with open("phase1_audit/step3_2_reconciliation/STEP3_2_FINAL_RECONCILIATION_REPORT.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
m = re.search(r'## TASK 5 — PLAYER AGGREGATION & SAMPLE-SIZE RECONCILIATION[\s\S]*?(?=## TASK 6|\Z)', text)
if m:
    print(m.group(0))

