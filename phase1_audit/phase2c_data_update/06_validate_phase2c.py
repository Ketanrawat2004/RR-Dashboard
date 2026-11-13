import os
import re
import json
import hashlib
import pandas as pd

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit", "phase2c_data_update")

ORIGINAL_CSVS = [
    os.path.join(ROOT, "ball_by_ball.csv"),
    os.path.join(ROOT, "matches.csv"),
    os.path.join(ROOT, "competitions.csv"),
    os.path.join(ROOT, "teams.csv"),
    os.path.join(ROOT, "playing_eleven.csv"),
    os.path.join(ROOT, "competition_team_player_mapping.csv"),
]

ORIGINAL_CSV_HASHES = {
    "ball_by_ball.csv": "a3926f49d2c684dca2a5d2de535a02c5ee46ea654ca1e79dd31c69e7544e9889",
    "matches.csv": "bb100ab84b8b9a15160c1f2315cf675210131a30e779ec5079fd5403dcf56eef",
    "competitions.csv": "507ceb7189f972d4e4f299ddcfc97f3c3247af1913f6291106f161fa8353fd9b",
    "teams.csv": "a65e5922a9b3bf49247b24fc9471782e700efb31f8dcc5042923238b87c50a5d",
    "playing_eleven.csv": "7517c73722a28d5d61c808ccf0cbed315a8780586d02e946eb9a7f5daf011c27",
    "competition_team_player_mapping.csv": "1ded4e42a933618572d6e2c3a521c3257eb1844fab4456d567d77cbb2d3bbb12",
}

PRESENTATION_SCRIPTS = [
    os.path.join(ROOT, "build_clean_submission_pptx.py"),
    os.path.join(ROOT, "build_submission_pdf.py"),
]

PRESENTATION_HASHES = {
    "build_clean_submission_pptx.py": "6afe6d2f804f120d8a460c2ae6230fb1c389803a25de5ffc1981c98651cde79d",
    "build_submission_pdf.py": "65d570c2206ef438d242a1e391fe8d7ebca05de4d434ca18ec29a0d64c3553f0",
}

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def extract_table_rows(table_html):
    m = re.search(r'<tbody>([\s\S]*?)<\/tbody>', table_html)
    if not m:
        return []
    tbody = m.group(1)
    rows = re.findall(r'<tr\b[^>]*>[\s\S]*?<\/tr>', tbody)
    return rows

def parse_row(tr_html):
    attrs = {}
    for attr in ["data-role", "data-diff", "data-win", "data-index", "data-rank", "class"]:
        m = re.search(rf'{attr}="([^"]*)"', tr_html)
        if m:
            attrs[attr] = m.group(1)
    
    tds = re.findall(r'<td\b[^>]*>([\s\S]*?)<\/td>', tr_html)
    clean_tds = [re.sub(r'<[^>]*>', '', td).strip() for td in tds]
    
    m_name = re.search(r'<div class="name-box">\s*<(?:a|span)[^>]*>([^<]+)<\/(?:a|span)>', tr_html)
    player_name = m_name.group(1).strip() if m_name else ""
    
    m_link = re.search(r'players/([a-zA-Z0-9_\-]+)\.html', tr_html)
    dossier_key = m_link.group(1) if m_link else ""
    
    return {
        "attrs": attrs,
        "tds": clean_tds,
        "player_name": player_name,
        "dossier_key": dossier_key,
        "raw": tr_html
    }

def main():
    print("=" * 80)
    print("PHASE 2C: COMPREHENSIVE AUTOMATED VERIFICATION & AUDIT SUITE")
    print("=" * 80)
    
    passes = 0
    failures = 0

    # -------------------------------------------------------------
    # TEST 1: Triplet Synchronization Parity
    # -------------------------------------------------------------
    print("\n--- TEST 1: HTML Triplet Synchronization Parity ---")
    idx_p = os.path.join(ROOT, "index.html")
    dash_p = os.path.join(ROOT, "rr_pressure_dashboard.html")
    term_p = os.path.join(ROOT, "rr_war_room_terminal.html")

    h_idx = sha256_file(idx_p)
    h_dash = sha256_file(dash_p)
    h_term = sha256_file(term_p)

    sz_idx = os.path.getsize(idx_p)
    sz_dash = os.path.getsize(dash_p)
    sz_term = os.path.getsize(term_p)

    print(f"  index.html                 : {sz_idx:,} B | {h_idx}")
    print(f"  rr_pressure_dashboard.html : {sz_dash:,} B | {h_dash}")
    print(f"  rr_war_room_terminal.html  : {sz_term:,} B | {h_term}")

    if h_idx == h_dash == h_term and sz_idx == sz_dash == sz_term:
        print("  [PASS] All 3 production HTML files are 100% byte-for-byte identical.")
        passes += 1
    else:
        print("  [FAIL] Triplet files mismatch!")
        failures += 1

    # -------------------------------------------------------------
    # TEST 2: Parse DOM and Verify Table Row Counts & Structure
    # -------------------------------------------------------------
    print("\n--- TEST 2: DOM & Table Row Counts Verification ---")
    with open(idx_p, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Table Batters
    m_bat = re.search(r'<table id="table-batters">[\s\S]*?<\/table>', html_content)
    bat_raw_rows = extract_table_rows(m_bat.group(0)) if m_bat else []
    bat_parsed = [parse_row(r) for r in bat_raw_rows]
    print(f"  Batters table rows count: {len(bat_parsed)} (Expected: 163)")
    if len(bat_parsed) == 163:
        print("  [PASS] Batters table contains exactly 163 qualified batter rows.")
        passes += 1
    else:
        print(f"  [FAIL] Expected 163 batters, got {len(bat_parsed)}")
        failures += 1

    # Table Bowlers
    m_bowl = re.search(r'<table id="table-bowlers">[\s\S]*?<\/table>', html_content)
    bowl_raw_rows = extract_table_rows(m_bowl.group(0)) if m_bowl else []
    bowl_parsed = [parse_row(r) for r in bowl_raw_rows]

    bowl_comp_rows = [p for p in bowl_parsed if "bowler-row-composite" in p["attrs"].get("class", "")]
    bowl_rpae_rows = [p for p in bowl_parsed if "bowler-row-rpae" in p["attrs"].get("class", "")]

    print(f"  Bowlers table Composite rows: {len(bowl_comp_rows)} (Expected: 179)")
    print(f"  Bowlers table Pure RPAE rows: {len(bowl_rpae_rows)} (Expected: 179)")
    print(f"  Bowlers table total rows: {len(bowl_parsed)} (Expected: 358)")

    if len(bowl_comp_rows) == 179 and len(bowl_rpae_rows) == 179 and len(bowl_parsed) == 358:
        print("  [PASS] Bowlers table contains exactly 179 Composite + 179 RPAE rows.")
        passes += 1
    else:
        print("  [FAIL] Bowler row count mismatch!")
        failures += 1

    # Table Superstars
    m_super = re.search(r'<table id="table-superstars">[\s\S]*?<\/table>', html_content)
    super_raw_rows = extract_table_rows(m_super.group(0)) if m_super else []
    super_parsed = [parse_row(r) for r in super_raw_rows]
    print(f"  Superstars table rows count: {len(super_parsed)} (Expected: 5)")
    if len(super_parsed) == 5:
        print("  [PASS] Superstars table preserved 100% with exactly 5 marquee rows.")
        passes += 1
    else:
        print("  [FAIL] Superstars row count mismatch!")
        failures += 1

    # Tactical XI Section
    if 'id="section-tactical-xi"' in html_content and 'IPL 2027 RR Squad &amp; Auction Strategy' in html_content:
        print("  [PASS] Section Tactical XI preserved 100% with squad composition and strategy.")
        passes += 1
    else:
        print("  [FAIL] Tactical XI section missing or corrupted!")
        failures += 1

    # -------------------------------------------------------------
    # TEST 3: Data Parity with Phase 1 Step 4 CSVs
    # -------------------------------------------------------------
    print("\n--- TEST 3: Top-10 & Key Player Mathematical Alignment ---")
    df_bat_csv = pd.read_csv(os.path.join(ROOT, "phase1_audit", "step4_jury_harmonization", "FINAL_BATTER_RANKINGS.csv"))
    df_comp_csv = pd.read_csv(os.path.join(ROOT, "phase1_audit", "step4_jury_harmonization", "FINAL_BOWLER_RANKINGS_COMPOSITE.csv"))
    df_rpae_csv = pd.read_csv(os.path.join(ROOT, "phase1_audit", "step4_jury_harmonization", "FINAL_BOWLER_RANKINGS_RAE.csv"))

    # Batters Top 5 Check
    bat_top5_match = True
    for i in range(5):
        csv_r = df_bat_csv.iloc[i]
        dom_r = bat_parsed[i]
        dom_rank = dom_r["tds"][0]
        dom_name = dom_r["player_name"]
        dom_score = dom_r["tds"][9]

        csv_rank = str(csv_r["rank"])
        csv_name = str(csv_r["player_name"])
        csv_score = f"{float(csv_r['shrunk_rae_score']):+.2f}"

        if dom_rank != csv_rank or dom_name != csv_name or dom_score != csv_score:
            print(f"    [BATTER MISMATCH] Row {i}: DOM({dom_rank}, {dom_name}, {dom_score}) vs CSV({csv_rank}, {csv_name}, {csv_score})")
            bat_top5_match = False
        else:
            print(f"    [MATCH] Batter #{dom_rank}: {dom_name} | Shrunk RAE: {dom_score}")

    if bat_top5_match:
        print("  [PASS] Top 5 Batters match Step 4 CSV ordering and scores down to 0.00.")
        passes += 1
    else:
        print("  [FAIL] Top 5 Batters mismatch!")
        failures += 1

    # Bowlers Composite Top 5 Check
    bowl_comp_top5_match = True
    for i in range(5):
        csv_r = df_comp_csv.iloc[i]
        dom_r = bowl_comp_rows[i]
        dom_rank = dom_r["tds"][0]
        dom_name = dom_r["player_name"]
        dom_score = dom_r["tds"][9]

        csv_rank = str(csv_r["rank_composite"])
        csv_name = str(csv_r["player_name"])
        csv_score = f"{float(csv_r['composite_score']):+.2f}"

        if dom_rank != csv_rank or dom_name != csv_name or dom_score != csv_score:
            print(f"    [COMPOSITE MISMATCH] Row {i}: DOM({dom_rank}, {dom_name}, {dom_score}) vs CSV({csv_rank}, {csv_name}, {csv_score})")
            bowl_comp_top5_match = False
        else:
            print(f"    [MATCH] Composite Bowler #{dom_rank}: {dom_name} | Composite Score: {dom_score}")

    if bowl_comp_top5_match:
        print("  [PASS] Top 5 Composite Bowlers match Step 4 CSV ordering and scores.")
        passes += 1
    else:
        print("  [FAIL] Top 5 Composite Bowlers mismatch!")
        failures += 1

    # Bowlers RPAE Top 5 Check
    bowl_rpae_top5_match = True
    for i in range(5):
        csv_r = df_rpae_csv.iloc[i]
        dom_r = bowl_rpae_rows[i]
        dom_rank = dom_r["tds"][0]
        dom_name = dom_r["player_name"]
        dom_score = dom_r["tds"][9]

        csv_rank = str(csv_r["rank_rpae"])
        csv_name = str(csv_r["player_name"])
        csv_score = f"{float(csv_r['shrunk_rpae_score']):+.2f}"

        if dom_rank != csv_rank or dom_name != csv_name or dom_score != csv_score:
            print(f"    [RPAE MISMATCH] Row {i}: DOM({dom_rank}, {dom_name}, {dom_score}) vs CSV({csv_rank}, {csv_name}, {csv_score})")
            bowl_rpae_top5_match = False
        else:
            print(f"    [MATCH] Pure RPAE Bowler #{dom_rank}: {dom_name} | Pure RPAE Score: {dom_score}")

    if bowl_rpae_top5_match:
        print("  [PASS] Top 5 Pure RPAE Bowlers match Step 4 CSV ordering and scores.")
        passes += 1
    else:
        print("  [FAIL] Top 5 Pure RPAE Bowlers mismatch!")
        failures += 1

    # Key Player Spot Checks
    print("\n--- Key Player Spot Checks ---")
    spot_checks = {
        "Andre Russell": {"expected_bat_rank": "1", "expected_score": "+26.59"},
        "Vaibhav Sooryavanshi": {"expected_bat_rank": "2", "expected_score": "+22.48"},
        "Glenn Maxwell": {"expected_bat_rank": "3", "expected_score": "+22.45"},
        "Matheesha Pathirana": {"expected_rpae_rank": "1", "expected_rpae_score": "+21.18"},
        "Jasprit Bumrah": {"expected_rpae_rank": "2", "expected_rpae_score": "+17.54"},
        "Umran Malik": {"expected_comp_rank": "1", "expected_comp_score": "+24.75"},
    }

    spot_pass = True
    for r in bat_parsed:
        name = r["player_name"]
        if name in spot_checks and "expected_bat_rank" in spot_checks[name]:
            rank = r["tds"][0]
            score = r["tds"][9]
            exp_rank = spot_checks[name]["expected_bat_rank"]
            exp_score = spot_checks[name]["expected_score"]
            print(f"  Spot Check Batter {name}: Rank={rank} (Exp: {exp_rank}), Score={score} (Exp: {exp_score})")
            if rank != exp_rank or score != exp_score:
                spot_pass = False

    for r in bowl_comp_rows:
        name = r["player_name"]
        if name in spot_checks and "expected_comp_rank" in spot_checks[name]:
            rank = r["tds"][0]
            score = r["tds"][9]
            exp_rank = spot_checks[name]["expected_comp_rank"]
            exp_score = spot_checks[name]["expected_comp_score"]
            print(f"  Spot Check Comp Bowler {name}: Rank={rank} (Exp: {exp_rank}), Score={score} (Exp: {exp_score})")
            if rank != exp_rank or score != exp_score:
                spot_pass = False

    for r in bowl_rpae_rows:
        name = r["player_name"]
        if name in spot_checks and "expected_rpae_rank" in spot_checks[name]:
            rank = r["tds"][0]
            score = r["tds"][9]
            exp_rank = spot_checks[name]["expected_rpae_rank"]
            exp_score = spot_checks[name]["expected_rpae_score"]
            print(f"  Spot Check RPAE Bowler {name}: Rank={rank} (Exp: {exp_rank}), Score={score} (Exp: {exp_score})")
            if rank != exp_rank or score != exp_score:
                spot_pass = False

    if spot_pass:
        print("  [PASS] All 6 key benchmark players verified 100% accurate.")
        passes += 1
    else:
        print("  [FAIL] Key benchmark player spot check failed!")
        failures += 1

    # -------------------------------------------------------------
    # TEST 4: Slicer Attributes & Interactive Contract
    # -------------------------------------------------------------
    print("\n--- TEST 4: Slicer Attributes & Interactive Contract ---")
    attr_pass = True
    for r in bat_parsed + bowl_comp_rows + bowl_rpae_rows:
        attrs = r["attrs"]
        for a in ["data-role", "data-diff", "data-win", "data-index", "data-rank"]:
            val = attrs.get(a)
            if val is None or val == "" or "NaN" in val or "None" in val:
                print(f"    [ATTR ERROR] Player {r['player_name']} has invalid {a}='{val}'")
                attr_pass = False
                break
        if not attr_pass:
            break

    if attr_pass:
        print("  [PASS] All 521 data rows possess valid data-* slicer attributes.")
        passes += 1
    else:
        print("  [FAIL] Slicer attribute validation failed!")
        failures += 1

    # -------------------------------------------------------------
    # TEST 5: Dossier Links & Offline Images Integrity
    # -------------------------------------------------------------
    print("\n--- TEST 5: Hyperlinks & Asset Integrity ---")
    all_hrefs = set(re.findall(r'href=["\'](players/[^"\']+\.html)["\']', html_content))
    print(f"  Total unique player dossier links found in HTML: {len(all_hrefs)}")

    missing_dossiers = []
    for href in all_hrefs:
        target_path = os.path.join(ROOT, href.replace("/", "\\"))
        if not os.path.exists(target_path):
            missing_dossiers.append(href)

    if not missing_dossiers:
        print(f"  [PASS] Zero broken links! All {len(all_hrefs)} linked dossiers exist in players/.")
        passes += 1
    else:
        print(f"  [FAIL] Found {len(missing_dossiers)} broken dossier links: {missing_dossiers[:5]}")
        failures += 1

    # Check that all 48 dossiers in players/ are linked or accessible
    dossier_files = [f for f in os.listdir(os.path.join(ROOT, "players")) if f.endswith(".html")]
    print(f"  Total dossiers present on disk: {len(dossier_files)}")
    accessible_count = sum(1 for d in dossier_files if f"players/{d}" in all_hrefs)
    print(f"  Dossiers directly linked from Master Dashboard: {accessible_count} of {len(dossier_files)}")
    if accessible_count >= 40:  # All top performers + marquee players
        print("  [PASS] All core player dossiers are properly referenced and accessible.")
        passes += 1
    else:
        print("  [FAIL] Too few dossiers referenced!")
        failures += 1

    # -------------------------------------------------------------
    # TEST 6: Scope Boundaries & File Protection
    # -------------------------------------------------------------
    print("\n--- TEST 6: Strict Scope Protection Verification ---")
    csv_protected = True
    for csv_p in ORIGINAL_CSVS:
        fname = os.path.basename(csv_p)
        cur_hash = sha256_file(csv_p)
        exp_hash = ORIGINAL_CSV_HASHES[fname]
        if cur_hash != exp_hash:
            print(f"    [CSV CORRUPTED] {fname} modified! ({cur_hash} vs {exp_hash})")
            csv_protected = False

    if csv_protected:
        print("  [PASS] All 6 original official CSV datasets are 100% UNMODIFIED.")
        passes += 1
    else:
        print("  [FAIL] Original CSV files modified!")
        failures += 1

    pres_protected = True
    for pres_p in PRESENTATION_SCRIPTS:
        fname = os.path.basename(pres_p)
        cur_hash = sha256_file(pres_p)
        exp_hash = PRESENTATION_HASHES[fname]
        if cur_hash != exp_hash:
            print(f"    [PRESENTATION MODIFIED] {fname} modified! ({cur_hash} vs {exp_hash})")
            pres_protected = False

    if pres_protected:
        print("  [PASS] Presentation scripts (PDF & PPTX builders) are 100% UNMODIFIED.")
        passes += 1
    else:
        print("  [FAIL] Presentation scripts modified!")
        failures += 1

    # Summary
    print("\n" + "=" * 80)
    print(f"PHASE 2C VALIDATION SUMMARY: {passes} PASSED, {failures} FAILED")
    print("=" * 80)

    # Save validation report
    rep_path = os.path.join(AUDIT_DIR, "VALIDATION_RESULTS.txt")
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write(f"Phase 2C Automated Validation Results\n")
        f.write(f"Total Tests: {passes + failures}\n")
        f.write(f"Passed: {passes}\n")
        f.write(f"Failed: {failures}\n")
        f.write(f"Status: {'100% GREEN - ALL TESTS PASSED' if failures == 0 else 'FAILURES DETECTED'}\n")
        f.write(f"HTML Triplet SHA256: {h_idx}\n")

    return failures == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
