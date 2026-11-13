with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

for i, line in enumerate(text.split("\n")):
    if "378" in line or "192" in line or "137" in line:
        print(f"Line {i}: {line.strip()[:100]}")

