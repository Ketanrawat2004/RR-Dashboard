with open("phase1_audit/03_delivery_state_and_pressure_report.txt", "r", encoding="utf-8") as f:
    text = f.read()

for line in text.split("\n"):
    if any(k in line for k in ["Russell", "Bumrah", "Pathirana", "192", "323", "469", "378"]):
        print(line[:120])

