with open("phase1_audit/phase2c_data_update/07_generate_completion_report.py", "r", encoding="utf-8") as f:
    text = f.read()

for i, line in enumerate(text.split("\n")):
    if "Andre Russell" in line or "192" in line or "378" in line:
        print(f"{i}: {line}")

