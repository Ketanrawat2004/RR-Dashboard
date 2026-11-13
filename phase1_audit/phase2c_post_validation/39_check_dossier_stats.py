import os
import re

for name in ["andre_russell", "jasprit_bumrah", "glenn_maxwell", "matheesha_pathirana", "umran_malik", "tim_david", "abhishek_sharma"]:
    path = f"players/{name}.html"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
            # find stats grid
            m = re.findall(r'<div class="stat-card">[\s\S]*?<\/div>', c)
            print(f"=== {name} ===")
            for sc in m[:4]:
                print(" ", re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', ' ', sc)).strip())
