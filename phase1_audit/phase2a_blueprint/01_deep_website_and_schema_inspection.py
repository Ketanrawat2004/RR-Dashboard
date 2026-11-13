import os
import re
import json
import hashlib
import glob
import pandas as pd
from pathlib import Path

ROOT = r"C:\RR NEW"
BLUEPRINT_DIR = os.path.join(ROOT, "phase1_audit", "phase2a_blueprint")
STEP4_DIR = os.path.join(ROOT, "phase1_audit", "step4_jury_harmonization")

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("=" * 80)
    print("PHASE 2A: DEEP WEBSITE, DATA & SCRIPT DEPENDENCY INSPECTION")
    print("=" * 80)

    # 1. Compare the 3 HTML files
    html_files = ["index.html", "rr_pressure_dashboard.html", "rr_war_room_terminal.html"]
    html_contents = {}
    html_hashes = {}
    for hf in html_files:
        p = os.path.join(ROOT, hf)
        with open(p, "rb") as f:
            b = f.read()
        html_contents[hf] = b
        html_hashes[hf] = hashlib.sha256(b).hexdigest()
        print(f"File: {hf:<28} Size: {len(b):>10,} bytes  SHA256: {html_hashes[hf]}")

    print("\nPairwise equality check:")
    print(f"  index.html == rr_pressure_dashboard.html : {html_contents['index.html'] == html_contents['rr_pressure_dashboard.html']}")
    print(f"  index.html == rr_war_room_terminal.html   : {html_contents['index.html'] == html_contents['rr_war_room_terminal.html']}")

    # 2. Parse index.html structure
    index_text = html_contents["index.html"].decode("utf-8", errors="ignore")
    print(f"\nindex.html text length: {len(index_text):,} characters")

    # Tables in index.html
    table_pattern = re.compile(r'<table\b[^>]*id=["\']([^"\']+)["\'][^>]*>([\s\S]*?)<\/table>', re.IGNORECASE)
    tables = table_pattern.findall(index_text)
    print(f"\nTables found ({len(tables)}):")
    for tid, tbody in tables:
        # count thead th
        headers = re.findall(r'<th\b[^>]*>([\s\S]*?)<\/th>', tbody, re.IGNORECASE)
        # clean headers
        headers_clean = [re.sub(r'<[^>]+>', '', h).strip() for h in headers]
        row_count = len(re.findall(r'<tr\b', tbody, re.IGNORECASE)) - 1 # minus header row
        print(f"  Table ID: #{tid:<20} Rows: {row_count:>3}  Headers ({len(headers_clean)}): {headers_clean}")

    # Inspect all interactive controls, inputs, selects, buttons
    inputs = re.findall(r'<input\b[^>]*id=["\']([^"\']+)["\'][^>]*>', index_text, re.IGNORECASE)
    selects = re.findall(r'<select\b[^>]*id=["\']([^"\']+)["\'][^>]*>', index_text, re.IGNORECASE)
    buttons = re.findall(r'<button\b[^>]*id=["\']([^"\']+)["\'][^>]*>', index_text, re.IGNORECASE)
    print(f"\nInteractive controls found:")
    print(f"  Inputs:  {inputs}")
    print(f"  Selects: {selects}")
    print(f"  Buttons: {buttons}")

    # Inspect Modals
    modals = re.findall(r'id=["\']([^"\']*(?:modal|popup)[^"\']*)["\']', index_text, re.IGNORECASE)
    print(f"  Modal-related IDs: {set(modals)}")

    # Extract all inline JavaScript code
    scripts = re.findall(r'<script\b[^>]*>([\s\S]*?)<\/script>', index_text, re.IGNORECASE)
    print(f"\nInline scripts count: {len(scripts)}")
    for idx, sc in enumerate(scripts):
        print(f"  Script {idx+1} length: {len(sc):,} chars")
        # List function names declared
        funcs = re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', sc)
        vars_decl = re.findall(r'(?:var|let|const)\s+([a-zA-Z0-9_$]+)\s*=', sc)
        print(f"    Functions: {funcs}")
        print(f"    Variables: {vars_decl[:15]}")

    # 3. Inspect players_db.json
    pdb_path = os.path.join(ROOT, "players_db.json")
    with open(pdb_path, "r", encoding="utf-8") as f:
        pdb = json.load(f)
    print(f"\nplayers_db.json records count: {len(pdb)}")
    # Collect all keys and check consistency
    all_keys = set()
    for r in pdb:
        all_keys.update(r.keys())
    print(f"Total unique keys across all records in players_db.json: {len(all_keys)}")
    print(f"Keys: {sorted(list(all_keys))}")

    # Check key types and presence across all records
    key_presence = {k: 0 for k in all_keys}
    key_types = {k: set() for k in all_keys}
    for r in pdb:
        for k in all_keys:
            if k in r:
                key_presence[k] += 1
                key_types[k].add(type(r[k]).__name__)
    print("\nField presence and types in players_db.json:")
    for k in sorted(all_keys):
        print(f"  {k:<25} Count: {key_presence[k]:>2}/{len(pdb)}  Types: {list(key_types[k])}")

    # 4. Compare with Step 4 CSVs
    bat_csv = pd.read_csv(os.path.join(STEP4_DIR, "FINAL_BATTER_RANKINGS.csv"))
    bowl_rae_csv = pd.read_csv(os.path.join(STEP4_DIR, "FINAL_BOWLER_RANKINGS_RAE.csv"))
    bowl_comp_csv = pd.read_csv(os.path.join(STEP4_DIR, "FINAL_BOWLER_RANKINGS_COMPOSITE.csv"))

    print(f"\nStep 4 Columns:")
    print(f"  Batters ({len(bat_csv.columns)}): {bat_csv.columns.tolist()}")
    print(f"  Bowlers RAE ({len(bowl_rae_csv.columns)}): {bowl_rae_csv.columns.tolist()}")
    print(f"  Bowlers Comp ({len(bowl_comp_csv.columns)}): {bowl_comp_csv.columns.tolist()}")

    # 5. Check players in players_db.json vs Step 4 Top players
    pdb_names = set(r["name"] for r in pdb)
    pdb_keys = set(r["key"] for r in pdb)
    print(f"\nExisting players in players_db.json ({len(pdb_names)}):")
    for r in pdb:
        print(f"  [{r.get('category')}] #{r.get('rank')} {r.get('name')} (key: {r.get('key')}) - {r.get('teams')}")

    # Check Top 25 Batters vs players_db.json
    top25_bat = bat_csv.head(25)
    print(f"\nTop 10 Batters overlap with players_db.json:")
    for _, r in bat_csv.head(10).iterrows():
        in_db = r["player_name"] in pdb_names
        print(f"  #{r['rank']:>2} {r['player_name']:<24} (Score: {r['shrunk_rae_score']:>+6.2f}) In DB: {in_db}")

    print(f"\nTop 10 Bowlers (Pure RPAE) overlap with players_db.json:")
    for _, r in bowl_rae_csv.head(10).iterrows():
        in_db = r["player_name"] in pdb_names
        print(f"  #{r['rank_rpae']:>2} {r['player_name']:<24} (Score: {r['shrunk_rpae_score']:>+6.2f}) In DB: {in_db}")

    print(f"\nTop 10 Bowlers (Composite) overlap with players_db.json:")
    for _, r in bowl_comp_csv.head(10).iterrows():
        in_db = r["player_name"] in pdb_names
        print(f"  #{r['rank_composite']:>2} {r['player_name']:<24} (Score: {r['composite_score']:>+6.2f}) In DB: {in_db}")

    # 6. Dossier files in players/
    players_dir = os.path.join(ROOT, "players")
    dossier_files = glob.glob(os.path.join(players_dir, "*.html"))
    dossier_keys = [os.path.splitext(os.path.basename(f))[0] for f in dossier_files]
    print(f"\nExisting dossier files in players/ ({len(dossier_files)}):")
    for dk in sorted(dossier_keys):
        print(f"  - {dk}.html")

    # Check if all 20 players_db keys have dossiers
    missing_dossiers = [k for k in pdb_keys if k not in dossier_keys]
    print(f"Missing dossiers for existing players_db.json: {missing_dossiers}")

    # 7. Images in player_images/
    img_dir = os.path.join(ROOT, "player_images")
    img_files = glob.glob(os.path.join(img_dir, "*.*"))
    img_keys = [os.path.splitext(os.path.basename(f))[0] for f in img_files]
    print(f"\nPlayer images in player_images/ ({len(img_files)}):")
    for ik in sorted(img_keys):
        print(f"  - {ik}")

    # Check how many Step 4 top players have images
    def to_key(name):
        return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')

    print(f"\nImage check for Top 10 Batters:")
    for _, r in bat_csv.head(10).iterrows():
        k = to_key(r["player_name"])
        has_img = k in img_keys
        print(f"  {r['player_name']:<24} -> key: {k:<22} image exists: {has_img}")

    print(f"\nImage check for Top 10 Bowlers (Composite):")
    for _, r in bowl_comp_csv.head(10).iterrows():
        k = to_key(r["player_name"])
        has_img = k in img_keys
        print(f"  {r['player_name']:<24} -> key: {k:<22} image exists: {has_img}")

    # 8. Inspect build_submission_pdf.py and build_submission_pptx.py
    print("\n" + "=" * 80)
    print("INSPECTING PRESENTATION SCRIPTS")
    print("=" * 80)
    pdf_script = os.path.join(ROOT, "build_submission_pdf.py")
    with open(pdf_script, "r", encoding="utf-8", errors="ignore") as f:
        pdf_code = f.read()
    print(f"build_submission_pdf.py length: {len(pdf_code):,} chars, {len(pdf_code.splitlines())} lines")
    pdf_inputs = [l.strip() for l in pdf_code.splitlines() if "open(" in l or ".read(" in l or ".load(" in l or ".csv" in l or ".json" in l or ".html" in l]
    print(f"File accesses in build_submission_pdf.py:")
    for pi in pdf_inputs[:15]:
        print(f"  {pi}")

    pptx_script = os.path.join(ROOT, "build_submission_pptx.py")
    with open(pptx_script, "r", encoding="utf-8", errors="ignore") as f:
        pptx_code = f.read()
    print(f"\nbuild_submission_pptx.py length: {len(pptx_code):,} chars, {len(pptx_code.splitlines())} lines")
    pptx_inputs = [l.strip() for l in pptx_code.splitlines() if "open(" in l or ".read(" in l or ".load(" in l or ".csv" in l or ".json" in l or ".html" in l]
    print(f"File accesses in build_submission_pptx.py:")
    for pi in pptx_inputs[:15]:
        print(f"  {pi}")

    # Also clean_submission_pptx
    clean_pptx = os.path.join(ROOT, "build_clean_submission_pptx.py")
    if os.path.exists(clean_pptx):
        with open(clean_pptx, "r", encoding="utf-8", errors="ignore") as f:
            clean_code = f.read()
        print(f"\nbuild_clean_submission_pptx.py length: {len(clean_code):,} chars, {len(clean_code.splitlines())} lines")

if __name__ == "__main__":
    main()

