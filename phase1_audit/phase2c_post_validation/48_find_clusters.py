import os
import re

targets = {
    "Andre Russell": 192,
    "Glenn Maxwell": 120,
    "Tim David": 188,
    "Abhishek Sharma": 113,
    "Matheesha Pathirana": 137,
    "Jasprit Bumrah": 378,
    "Maheesh Theekshana": 117,
    "Umran Malik": 147,
    "Mayank Yadav": 62
}

for root, dirs, files in os.walk("phase1_audit"):
    for f in files:
        if f.endswith((".txt", ".md", ".csv", ".json", ".py")):
            p = os.path.join(root, f)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as fl:
                    text = fl.read()
                    matches = []
                    for name, num in targets.items():
                        if name in text and str(num) in text:
                            matches.append(f"{name}:{num}")
                    if len(matches) >= 3:
                        print(f"High match in {p}: {matches}")
            except:
                pass

