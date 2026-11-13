import os
import re

ROOT = r"C:\RR NEW"

def main():
    with open(os.path.join(ROOT, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()

    # Look for table-batters tbody
    tb_match = re.search(r'<table\b[^>]*id=["\']table-batters["\'][^>]*>([\s\S]*?)<\/table>', html, re.IGNORECASE)
    if tb_match:
        table_html = tb_match.group(1)
        rows = re.findall(r'<tr\b[^>]*>([\s\S]*?)<\/tr>', table_html, re.IGNORECASE)
        print(f"table-batters: Total rows = {len(rows)}")
        # print first 2 rows
        for i, r in enumerate(rows[:3]):
            # clean tags or print raw
            print(f"\n--- Row {i} ---")
            print(r.strip()[:500])

    # Check the script in index.html
    scripts = re.findall(r'<script\b[^>]*>([\s\S]*?)<\/script>', html, re.IGNORECASE)
    print(f"\nInline scripts count: {len(scripts)}")
    for idx, sc in enumerate(scripts):
        print(f"\n--- SCRIPT {idx+1} ({len(sc)} chars) ---")
        print(sc.strip()[:1500])
        print("...\n" + sc.strip()[-1000:])

if __name__ == "__main__":
    main()

