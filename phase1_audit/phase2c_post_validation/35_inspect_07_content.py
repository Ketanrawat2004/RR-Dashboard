import json

with open(r"C:\RR NEW\phase1_audit\phase2c_data_update\07_generate_completion_report.py", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split("\n")
for i in range(90, 140):
    print(f"{i}: {lines[i]}")

