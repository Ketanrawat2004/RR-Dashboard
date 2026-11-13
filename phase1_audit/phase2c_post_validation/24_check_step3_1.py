import os

for f in os.listdir("phase1_audit/step3_1_validation"):
    p = os.path.join("phase1_audit/step3_1_validation", f)
    if os.path.isfile(p):
        with open(p, "r", encoding="utf-8", errors="ignore") as fl:
            text = fl.read()
            for name in ["Russell", "Maxwell", "David", "Pathirana", "Bumrah", "Theekshana", "Umran", "Mayank"]:
                for n in [192, 120, 188, 113, 137, 378, 117, 147, 62]:
                    if f"{name}" in text and f"{n}" in text:
                        # find lines
                        lines = [l.strip() for l in text.split("\n") if name in l and str(n) in l]
                        if lines:
                            print(f"{f}: {lines[0][:120]}")
                            break

