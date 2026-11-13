import os
import re

print("Searching for '192' in phase1_audit files...")
for root, dirs, files in os.walk("phase1_audit"):
    for f in files:
        if f.endswith((".txt", ".md", ".csv", ".py")):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fl:
                for line_no, line in enumerate(fl):
                    if "192" in line and any(w in line for w in ["Russell", "bf", "pressure", "balls"]):
                        print(f"{p}:{line_no}: {line.strip()[:100]}")

