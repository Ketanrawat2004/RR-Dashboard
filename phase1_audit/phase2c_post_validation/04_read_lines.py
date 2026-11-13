with open("phase1_audit/phase2c_data_update/05_apply_data_update.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(50, 115):
    print(f"{i}: {lines[i]}", end="")

