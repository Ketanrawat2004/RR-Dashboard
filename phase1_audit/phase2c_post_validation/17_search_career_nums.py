import os

nums = ["2143", "2,143", "1777", "1,777", "1288", "1,288", "3205", "3,205", "1414", "1,414"]

for root, dirs, files in os.walk("."):
    if ".git" in root or "venv" in root:
        continue
    for f in files:
        if f.endswith((".py", ".csv", ".json", ".txt", ".md", ".html")):
            p = os.path.join(root, f)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as fl:
                    c = fl.read()
                    for n in nums:
                        if n in c:
                            print(f"Found {n} in {p}")
                            break
            except:
                pass

