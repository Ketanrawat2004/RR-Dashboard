with open("phase1_audit/step3_individual_model/BOWLERS_PERFORMANCE_STEP3.csv", "r", encoding="utf-8") as f:
    header = f.readline()
    print("Header:", header.strip())
    for line in f:
        for name in ["Russell", "Maxwell", "Abhishek", "Pathirana", "Bumrah", "Theekshana", "Umran", "Mayank"]:
            if name in line:
                print(f"{name}: {line.strip()[:140]}")

