with open("phase1_audit/final_independent_verification/FINAL_VERIFICATION_REPORT.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
lines = text.split("\n")
for i, l in enumerate(lines):
    if any(k in l for k in ["192", "378", "120", "137", "188", "113", "147"]):
        print(f"Line {i}: {l[:120]}")

