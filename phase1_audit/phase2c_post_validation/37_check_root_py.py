import os

for f in os.listdir("."):
    if f.endswith(".py"):
        with open(f, "r", encoding="utf-8", errors="ignore") as fl:
            c = fl.read()
            if "378" in c:
                print(f"378 found in {f}")
            if "192" in c:
                print(f"192 found in {f}")

