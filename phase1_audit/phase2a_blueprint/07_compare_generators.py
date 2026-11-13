import os

ROOT = r"C:\RR NEW"

def main():
    for fname in ["clean_powerbi_dashboard.py", "fix_dashboard_and_wagon.py", "generate_powerbi_wagon_dashboard.py"]:
        path = os.path.join(ROOT, fname)
        size = os.path.getsize(path)
        mtime = os.path.getmtime(path)
        print(f"{fname:<38} Size: {size:>10,} bytes  Modified: {mtime}")

if __name__ == "__main__":
    main()

