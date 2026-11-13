with open("phase1_audit/phase2c_data_update/05_apply_data_update.py", "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect where r['pressure_bf'] and r['career_bf'] came from
for i, line in enumerate(text.split("\n")):
    if "pressure_bf" in line or "career_bf" in line or "pressure_b" in line or "career_b" in line:
        print(f"{i}: {line}")

