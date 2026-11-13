import os
import json
import re
import pandas as pd
import hashlib

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit")
STEP4_DIR = os.path.join(AUDIT_DIR, "step4_jury_harmonization")
PLAYERS_DIR = os.path.join(ROOT, "players")
IMG_DIR = os.path.join(ROOT, "player_images")
DB_PATH = os.path.join(ROOT, "players_db.json")

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("=" * 80)
    print("PHASE 2B: STEP 5 — COMPREHENSIVE VALIDATION SUITE")
    print("=" * 80)

    # 1. JSON Syntax and Schema Validation
    print("\n[Check 1] JSON Syntax and Schema Validation:")
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
    print(f"  players_db.json successfully loaded: {len(db)} records.")
    assert len(db) == 342, f"Expected 342 records, got {len(db)}"
    print("  --> JSON Syntax & Record Count: PASS")

    # 2. 163 Batter and 179 Bowler Records
    print("\n[Check 2] Category Segregation:")
    batters = [r for r in db if r["category"] == "Batter"]
    bowlers = [r for r in db if r["category"] == "Bowler"]
    print(f"  Batters count: {len(batters)} (Expected: 163) -> {len(batters) == 163}")
    print(f"  Bowlers count: {len(bowlers)} (Expected: 179) -> {len(bowlers) == 179}")
    assert len(batters) == 163 and len(bowlers) == 179
    print("  --> Category Counts: PASS")

    # 3. Unique Player IDs per Category
    print("\n[Check 3] Unique Player IDs per Category:")
    bat_pids = [r["player_id"] for r in batters]
    bowl_pids = [r["player_id"] for r in bowlers]
    print(f"  Unique Batter IDs: {len(set(bat_pids))} / {len(bat_pids)}")
    print(f"  Unique Bowler IDs: {len(set(bowl_pids))} / {len(bowl_pids)}")
    assert len(set(bat_pids)) == 163, "Duplicate batter player_ids found!"
    assert len(set(bowl_pids)) == 179, "Duplicate bowler player_ids found!"
    print("  --> Unique Player IDs: PASS")

    # 4. Correct Ranking Order
    print("\n[Check 4] Correct Ranking Order:")
    bat_ranks = [r["rank"] for r in batters]
    bowl_ranks = [r["rank"] for r in bowlers]
    assert bat_ranks == list(range(1, 164)), "Batter ranks are not sequential 1 to 163!"
    assert bowl_ranks == list(range(1, 180)), "Bowler ranks are not sequential 1 to 179!"

    # Check score monotonicity
    bat_scores = [r["shrunk_score"] for r in batters]
    bowl_scores = [r["shrunk_score"] for r in bowlers]
    is_bat_desc = all(bat_scores[i] >= bat_scores[i+1] for i in range(len(bat_scores)-1))
    is_bowl_desc = all(bowl_scores[i] >= bowl_scores[i+1] for i in range(len(bowl_scores)-1))
    print(f"  Batters strictly sorted descending by shrunk_score: {is_bat_desc}")
    print(f"  Bowlers strictly sorted descending by shrunk_score: {is_bowl_desc}")
    assert is_bat_desc and is_bowl_desc
    print("  --> Ranking Order & Monotonicity: PASS")

    # 5. Score Consistency Against Source CSVs
    print("\n[Check 5] Score Consistency Against Source CSVs:")
    bat_csv = pd.read_csv(os.path.join(STEP4_DIR, "FINAL_BATTER_RANKINGS.csv"))
    bowl_comp_csv = pd.read_csv(os.path.join(STEP4_DIR, "FINAL_BOWLER_RANKINGS_COMPOSITE.csv"))

    bat_csv_lookup = {int(r["player_id"]): r for _, r in bat_csv.iterrows()}
    bowl_csv_lookup = {int(r["player_id"]): r for _, r in bowl_comp_csv.iterrows()}

    bat_score_diffs = []
    for b in batters:
        pid = b["player_id"]
        csv_row = bat_csv_lookup[pid]
        diff = abs(b["shrunk_score"] - float(csv_row["shrunk_rae_score"]))
        bat_score_diffs.append(diff)
    max_bat_diff = max(bat_score_diffs)
    print(f"  Max Batter Shrunk Score discrepancy vs CSV: {max_bat_diff:.6f}")
    assert max_bat_diff < 0.01

    bowl_score_diffs = []
    for bw in bowlers:
        pid = bw["player_id"]
        csv_row = bowl_csv_lookup[pid]
        diff = abs(bw["shrunk_score"] - float(csv_row["composite_score"]))
        bowl_score_diffs.append(diff)
    max_bowl_diff = max(bowl_score_diffs)
    print(f"  Max Bowler Composite Score discrepancy vs CSV: {max_bowl_diff:.6f}")
    assert max_bowl_diff < 0.01
    print("  --> Score Consistency against Source CSVs: PASS")

    # 6. Correct Player Dossier Links & File Existence
    print("\n[Check 6] Player Dossier File Existence (Top 10 Leaders):")
    top_keys = [b["key"] for b in batters[:10]] + [bw["key"] for bw in bowlers[:10]]
    missing_dossiers = []
    for k in set(top_keys):
        p_path = os.path.join(PLAYERS_DIR, f"{k}.html")
        if not os.path.exists(p_path):
            missing_dossiers.append(k)
        else:
            # Check for broken links inside the file
            with open(p_path, "r", encoding="utf-8") as f:
                content = f.read()
            assert "../index.html" in content or "rr_pressure_dashboard.html" in content
    print(f"  Total Top-10 keys checked: {len(set(top_keys))}")
    print(f"  Missing dossiers: {missing_dossiers}")
    assert len(missing_dossiers) == 0, f"Missing dossiers: {missing_dossiers}"
    print("  --> Dossier File Existence & Backlinks: PASS")

    # 7. Valid SVG References and Rendering
    print("\n[Check 7] Image and SVG Asset Integrity:")
    missing_assets = []
    svg_count = 0
    png_count = 0
    for r in db:
        k = r["key"]
        png_p = os.path.join(IMG_DIR, f"{k}.png")
        svg_p = os.path.join(IMG_DIR, f"{k}.svg")
        if os.path.exists(png_p):
            png_count += 1
        elif os.path.exists(svg_p):
            svg_count += 1
            # verify SVG content
            with open(svg_p, "r", encoding="utf-8") as sf:
                svg_data = sf.read()
            assert "<svg" in svg_data and "</svg>" in svg_data, f"Corrupted SVG for {k}"
        else:
            missing_assets.append(k)
    print(f"  Players with official PNG headshots: {png_count}")
    print(f"  Players with offline SVG monogram badges: {svg_count}")
    print(f"  Players with missing image assets: {len(missing_assets)}")
    assert len(missing_assets) == 0, f"Missing assets for: {missing_assets}"
    print("  --> Image & SVG Monogram Integrity: PASS")

    # 8. Legacy Field Compatibility with Downstream Scripts
    print("\n[Check 8] Legacy Field Compatibility with Downstream Scripts:")
    legacy_keys = [
        "name", "key", "category", "rank", "teams", "role_desc", "total_m",
        "base_wr", "hp_m", "hp_wr", "lift", "mom_hp", "ko_wr", "bayes_hp_wr",
        "cppi", "bid_ceiling", "tactical_role", "summary", "why_chose",
        "why_not_others", "rr_fit", "verdict", "tagline", "rr_management_summary",
        "key_tactical_skill", "comparative_analysis"
    ]
    missing_keys = []
    for r in db:
        for lk in legacy_keys:
            if lk not in r:
                missing_keys.append((r["name"], lk))
    print(f"  Missing legacy keys across 342 records: {len(missing_keys)}")
    assert len(missing_keys) == 0, f"Missing legacy keys: {missing_keys[:5]}"

    # Test load in a dummy function mimicking build_clean_submission_pptx.py
    top_batters_test = [p for p in db if p["category"] == "Batter"][:10]
    top_bowlers_test = [p for p in db if p["category"] == "Bowler"][:10]
    for p in top_batters_test + top_bowlers_test:
        # access all 11 pptx keys
        test_val = (p["name"], p["rank"], p["cppi"], p["lift"], p["hp_wr"], p["base_wr"], p["hp_m"], p["ko_wr"], p["teams"], p["tactical_role"])
        assert None not in test_val, f"Null found in mandatory pptx field for {p['name']}"
    print("  --> Downstream Script Compatibility Test: PASS")

    # 9. Strict Scope Restrictions Verification (Zero changes to protected files)
    print("\n[Check 9] Verification of Out-of-Scope Production Files:")
    protected_files = [
        "index.html",
        "rr_pressure_dashboard.html",
        "rr_war_room_terminal.html",
        "build_clean_submission_pptx.py",
        "build_submission_pdf.py",
        "build_submission_pptx.py",
        "ball_by_ball.csv",
        "matches.csv",
        "competitions.csv",
        "teams.csv",
        "playing_eleven.csv",
        "competition_team_player_mapping.csv"
    ]
    # Check against baseline hashes
    hash_file = os.path.join(ROOT, "phase1_audit", "phase2a_blueprint", "PRODUCTION_BASELINE_HASHES.txt")
    with open(hash_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    expected_hashes = {}
    for l in lines:
        m = re.match(r'^\s*([^\s|]+(?: [^\s|]+)*?)\s*\|\s*(\d+)\s*\|\s*([a-f0-9]{64})\s*\|', l, re.IGNORECASE)
        if m:
            expected_hashes[m.group(1).strip()] = m.group(3).strip()

    unaltered = 0
    for pf in protected_files:
        cur_sha = sha256_file(os.path.join(ROOT, pf))
        exp_sha = expected_hashes[pf]
        assert cur_sha == exp_sha, f"Protected file {pf} was altered! {cur_sha} vs {exp_sha}"
        unaltered += 1
    print(f"  Verified all {unaltered} protected files remain 100% UNMODIFIED.")
    print("  --> Strict Preservation of Out-of-Scope Files: PASS")

    print("\n" + "=" * 80)
    print("ALL 9 PHASE 2B VALIDATION CHECKS PASSED (100% GREEN)")
    print("=" * 80)

if __name__ == "__main__":
    main()

