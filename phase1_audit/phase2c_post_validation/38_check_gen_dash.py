with open("generate_powerbi_wagon_dashboard.py", "r", encoding="utf-8") as f:
    text = f.read()

for i, line in enumerate(text.split("\n")):
    if any(k in line for k in ["Russell", "Maxwell", "Bumrah", "Pathirana", "192", "378"]):
        print(f"Line {i}: {line.strip()[:100]}")

