with open("phase1_audit/final_independent_verification/FINAL_VERIFICATION_REPORT.md", "r", encoding="utf-8") as f:
    text = f.read()

for line in text.split("\n"):
    if any(k in line for k in ["Russell", "Bumrah", "Pathirana", "192", "378", "137"]):
        print(line[:120])

