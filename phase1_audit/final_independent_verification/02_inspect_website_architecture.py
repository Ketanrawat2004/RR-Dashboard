import os
import re
import json

ROOT = r"C:\RR NEW"

def main():
    print("=" * 80)
    print("WEBSITE ARCHITECTURE AND DEPENDENCY AUDIT")
    print("=" * 80)

    index_path = os.path.join(ROOT, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    print(f"index.html size: {len(html):,} characters")

    # Check href and src
    href_matches = set(re.findall(r'href=["\']([^"\']+)["\']', html))
    src_matches = set(re.findall(r'src=["\']([^"\']+)["\']', html))

    print(f"\nTotal unique hrefs found: {len(href_matches)}")
    player_hrefs = [h for h in href_matches if "players/" in h or ".html" in h]
    print(f"Hrefs pointing to html/players ({len(player_hrefs)}):")
    for ph in sorted(player_hrefs):
        print(f"  - {ph}")

    print(f"\nTotal unique srcs found: {len(src_matches)}")
    for sm in sorted(src_matches):
        print(f"  - {sm}")

    # Check script tags
    scripts = re.findall(r'<script\b[^>]*>([\s\S]*?)<\/script>', html, re.IGNORECASE)
    print(f"\nTotal inline script blocks: {len(scripts)}")
    for i, sc in enumerate(scripts):
        print(f"  Script block {i+1}: length = {len(sc):,} chars")
        # Check for fetch, XMLHttpRequest, JSON.parse, etc.
        calls = []
        if "fetch(" in sc:
            calls.append("fetch")
        if "XMLHttpRequest" in sc:
            calls.append("XHR")
        if "players_db" in sc:
            calls.append("players_db reference")
        if "openModal" in sc:
            calls.append("openModal")
        if "filter" in sc or "slicer" in sc.lower():
            calls.append("filter/slicer")
        print(f"    Features detected: {calls}")

    # Inspect tables and IDs
    tables = re.findall(r'<table\b[^>]*id=["\']([^"\']+)["\']', html)
    print(f"\nTables with IDs: {tables}")

    tbodies = re.findall(r'<tbody\b[^>]*id=["\']([^"\']+)["\']', html)
    print(f"Tbody elements with IDs: {tbodies}")

    # Inspect players_db.json
    db_path = os.path.join(ROOT, "players_db.json")
    with open(db_path, "r", encoding="utf-8") as f:
        pdb = json.load(f)
    print(f"\nplayers_db.json records: {len(pdb)}")
    print(f"First record keys: {list(pdb[0].keys())}")
    names = [r.get("name") for r in pdb]
    print(f"Players in players_db.json: {names}")

    # Check identical dashboard files
    dash_path = os.path.join(ROOT, "rr_pressure_dashboard.html")
    war_path = os.path.join(ROOT, "rr_war_room_terminal.html")
    with open(dash_path, "r", encoding="utf-8") as f:
        dash_html = f.read()
    with open(war_path, "r", encoding="utf-8") as f:
        war_html = f.read()

    print(f"\nIdentical check:")
    print(f"  index.html == rr_pressure_dashboard.html: {html == dash_html}")
    print(f"  index.html == rr_war_room_terminal.html: {html == war_html}")

if __name__ == "__main__":
    main()

