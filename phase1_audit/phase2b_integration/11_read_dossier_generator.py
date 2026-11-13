import os

ROOT = r"C:\RR NEW"

def main():
    p = os.path.join(ROOT, "fix_dashboard_and_wagon.py")
    with open(p, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print("".join(lines[480:600]))

if __name__ == "__main__":
    main()

