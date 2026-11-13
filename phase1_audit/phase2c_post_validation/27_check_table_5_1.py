with open("phase1_audit/step3_1_validation/STEP3_1_INDEPENDENT_VALIDATION_REPORT.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(215, 240):
    print(f"{i}: {lines[i]}", end="")

