with open("pressure_output/methodology_report.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
print("Checking methodology_report.md for Rank 1 Batters and Bowlers:")
for line in text.splitlines():
    if "Rank 1" in line or "#1" in line or "Dube" in line or "Duffy" in line or "Patidar" in line:
        print(" ", line.strip()[:100])

