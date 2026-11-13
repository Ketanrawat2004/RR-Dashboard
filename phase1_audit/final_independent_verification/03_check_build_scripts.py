import os
import re

ROOT = r"C:\RR NEW"

def main():
    script_path = os.path.join(ROOT, "build_player_pages_and_dashboard.py")
    with open(script_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"Total lines in build_player_pages_and_dashboard.py: {len(lines)}")
    for i, line in enumerate(lines):
        if any(target in line for target in ["index.html", "players_db.json", "rr_pressure_dashboard.html", "rr_war_room_terminal.html", "players/"]):
            print(f"Line {i+1}: {line.strip()}")

    # Also check other scripts in ROOT that reference players_db.json or index.html
    print("\nOther scripts writing or reading index.html or players_db.json:")
    for fname in os.listdir(ROOT):
        if fname.endswith(".py") and fname != "build_player_pages_and_dashboard.py":
            fpath = os.path.join(ROOT, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                matches = []
                if "players_db.json" in content:
                    matches.append("players_db.json")
                if "index.html" in content:
                    matches.append("index.html")
                if matches:
                    print(f"  {fname}: {matches}")
            except Exception as e:
                pass

if __name__ == "__main__":
    main()

