with open("phase1_audit/step3_1_validation/STEP3_1_INDEPENDENT_VALIDATION_REPORT.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "Umran Malik" in l and "61" in l:
        for j in range(max(0, i-5), min(len(lines), i+15)):
            print(f"{j}: {lines[j]}", end="")
        break

