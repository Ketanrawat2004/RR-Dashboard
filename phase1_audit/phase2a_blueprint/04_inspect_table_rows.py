import os
import re

ROOT = r"C:\RR NEW"

def main():
    with open(os.path.join(ROOT, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()

    # Match row 1 of table-batters
    tb_match = re.search(r'<table\b[^>]*id=["\']table-batters["\'][^>]*>([\s\S]*?)<\/table>', html, re.IGNORECASE)
    if tb_match:
        rows = re.findall(r'<tr\b[^>]*>[\s\S]*?<\/tr>', tb_match.group(1), re.IGNORECASE)
        print("=== ROW 1 OF TABLE-BATTERS ===")
        row_clean = re.sub(r'src=["\']data:image/[^;]+;base64,[^"\']+["\']', 'src="[BASE64_IMAGE]"', rows[1])
        print(row_clean)

    # Match row 1 of table-bowlers
    bw_match = re.search(r'<table\b[^>]*id=["\']table-bowlers["\'][^>]*>([\s\S]*?)<\/table>', html, re.IGNORECASE)
    if bw_match:
        rows = re.findall(r'<tr\b[^>]*>[\s\S]*?<\/tr>', bw_match.group(1), re.IGNORECASE)
        print("\n=== ROW 1 OF TABLE-BOWLERS ===")
        row_clean = re.sub(r'src=["\']data:image/[^;]+;base64,[^"\']+["\']', 'src="[BASE64_IMAGE]"', rows[1])
        print(row_clean)

    # Also inspect nav tabs and section IDs in index.html
    nav_tabs = re.findall(r'<button\b[^>]*class=["\'][^"\']*nav-tab-btn[^"\']*["\'][^>]*>([\s\S]*?)<\/button>', html, re.IGNORECASE)
    print(f"\nNav Tab Buttons ({len(nav_tabs)}):")
    for nt in nav_tabs:
        print(f"  - {re.sub(r'<[^>]+>', '', nt).strip()}")

    # Inspect data-sections
    secs = re.findall(r'<div\b[^>]*class=["\'][^"\']*data-section[^"\']*["\'][^>]*>', html, re.IGNORECASE)
    print(f"\nData section divs ({len(secs)}):")
    for s in secs:
        print(f"  {s}")

    # Inspect all links to players/
    player_links = re.findall(r'href=["\']players/([^"\']+)["\']', html)
    print(f"\nUnique player dossier links in index.html ({len(set(player_links))}):")
    for pl in sorted(set(player_links)):
        print(f"  players/{pl}")

if __name__ == "__main__":
    main()
