with open("phase1_audit/step3_2_reconciliation/STEP3_2_FINAL_RECONCILIATION_REPORT.md", "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("#"):
            print(line.strip())

