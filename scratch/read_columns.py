with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(2530, 2560):
    print(f"{i+1}: {lines[i]}", end="")
print("...")
for i in range(2750, 2780):
    print(f"{i+1}: {lines[i]}", end="")

