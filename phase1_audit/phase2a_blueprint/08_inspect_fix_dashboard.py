import os

ROOT = r"C:\RR NEW"

def main():
    path = os.path.join(ROOT, "fix_dashboard_and_wagon.py")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        
    print(f"Total lines in fix_dashboard_and_wagon.py: {len(lines)}")
    for i, line in enumerate(lines):
        if any(term in line for term in ["open('index.html'", 'open("index.html"', "table-batters", "players_db"]):
            print(f"Line {i+1}: {line.strip()[:100]}")

if __name__ == "__main__":
    main()

