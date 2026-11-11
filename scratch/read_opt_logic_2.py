with open("optimize_rankings.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(80, 150):
    print(f"{i+1}: {lines[i]}", end="")

