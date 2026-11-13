import os
import re

for root, dirs, files in os.walk(r"C:\RR NEW"):
    if ".git" in root:
        continue
    for f in files:
        if f.endswith((".py", ".csv", ".json", ".txt", ".md", ".html")):
            p = os.path.join(root, f)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as fl:
                    content = fl.read()
                    # Look for Tim David and 188
                    if "Tim David" in content and "188" in content:
                        print(f"[Tim David & 188] in {p}")
                    # Look for Abhishek Sharma and 113
                    if "Abhishek Sharma" in content and "113" in content:
                        print(f"[Abhishek Sharma & 113] in {p}")
                    # Look for Theekshana and 117
                    if "Theekshana" in content and "117" in content:
                        print(f"[Theekshana & 117] in {p}")
                    # Look for Mayank Yadav and 62
                    if "Mayank Yadav" in content and "62" in content:
                        print(f"[Mayank Yadav & 62] in {p}")
            except:
                pass

