import os
import json
import glob

# Search in players_db.json
with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

print("--- Searching in players_db.json ---")
for p in db:
    if p["name"] in ["Andre Russell", "Glenn Maxwell", "Tim David", "Abhishek Sharma",
                     "Matheesha Pathirana", "Jasprit Bumrah", "Maheesh Theekshana", "Umran Malik", "Mayank Yadav"]:
        print(f"[{p['category']}] {p['name']}: pressure_balls={p.get('pressure_balls')}, career_balls={p.get('career_balls')}")

# Search where 192, 120, 188, 137, 378, 147 come from in all files
target_nums = [192, 120, 188, 113, 137, 378, 117, 147, 62]
print("\n--- Searching for target numbers in python/csv/json files ---")
for root, dirs, files in os.walk("phase1_audit"):
    for f in files:
        if f.endswith((".py", ".csv", ".json", ".txt")):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as fl:
                    content = fl.read()
                    for num in [192, 378, 137]:
                        if str(num) in content:
                            print(f"Found {num} in {path}")
                            break
            except Exception as e:
                pass

