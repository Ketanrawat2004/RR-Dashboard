import os

ROOT = r"C:\RR NEW"

def main():
    p = os.path.join(ROOT, "fix_dashboard_and_wagon.py")
    with open(p, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"Total lines: {len(lines)}")
    for i, line in enumerate(lines[:120]):
        print(f"{i+1}: {line.rstrip()[:100]}")

if __name__ == "__main__":
    main()

