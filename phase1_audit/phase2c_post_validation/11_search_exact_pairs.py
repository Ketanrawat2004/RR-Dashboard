import os
import re

patterns = ["192", "120", "188", "113", "137", "378", "117", "147", "62"]

for root, dirs, files in os.walk("."):
    if ".git" in root or "venv" in root:
        continue
    for f in files:
        if f.endswith((".py", ".csv", ".json", ".txt", ".md", ".html")):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as fl:
                    content = fl.read()
                    # Check if Russell and 192 are near each other or Maxwell and 120
                    if "Russell" in content and "192" in content:
                        print(f"[Russell & 192] in {path}")
                    if "Maxwell" in content and "120" in content:
                        print(f"[Maxwell & 120] in {path}")
                    if "Pathirana" in content and "137" in content:
                        print(f"[Pathirana & 137] in {path}")
                    if "Bumrah" in content and "378" in content:
                        print(f"[Bumrah & 378] in {path}")
                    if "Umran" in content and "147" in content:
                        print(f"[Umran & 147] in {path}")
            except:
                pass

