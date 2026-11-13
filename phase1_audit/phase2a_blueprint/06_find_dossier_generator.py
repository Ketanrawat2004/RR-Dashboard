import os
import re

ROOT = r"C:\RR NEW"

def main():
    with open(os.path.join(ROOT, "players", "shivam_dube.html"), "r", encoding="utf-8") as f:
        dube_html = f.read()

    # Look for unique phrases in shivam_dube.html
    phrase1 = "Quantitative Scouting Dossier | Rajasthan Royals Analytics"
    phrase2 = "IPL 2027 RR Squad & Auction Strategy"
    
    scripts = [f for f in os.listdir(ROOT) if f.endswith(".py")]
    print(f"Checking {len(scripts)} scripts for dossier generation code...")
    
    for s in scripts:
        spath = os.path.join(ROOT, s)
        try:
            with open(spath, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            if "players/{p['key']}.html" in code or 'players/{' in code or 'players/" + ' in code:
                has_p1 = phrase1 in code
                print(f"Generator candidate: {s:<35} Match Phrase1: {has_p1}")
        except Exception:
            pass

if __name__ == "__main__":
    main()

