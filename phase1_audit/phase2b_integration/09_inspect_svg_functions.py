import os

ROOT = r"C:\RR NEW"

def main():
    p = os.path.join(ROOT, "fix_dashboard_and_wagon.py")
    with open(p, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines[300:450]):
        if "def " in line or "<svg" in line or "wagon" in line.lower() or "pitch" in line.lower():
            print(f"{i+301}: {line.rstrip()[:100]}")

if __name__ == "__main__":
    main()

