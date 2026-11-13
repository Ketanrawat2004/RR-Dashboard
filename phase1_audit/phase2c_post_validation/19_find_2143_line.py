with open("phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if "2143" in line:
            print(f"Line {i}: {line.strip()}")

