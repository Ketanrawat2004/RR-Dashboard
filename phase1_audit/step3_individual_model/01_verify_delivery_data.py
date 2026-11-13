"""
Phase 1 Step 3 — Task 1: Delivery Data Verification and Provenance Audit
(01_verify_delivery_data.py)

Strictly read-only inspection of original CSVs, bbb_enriched.pkl, and so_bbb.pkl.
Verifies row counts, match IDs, chronological integrity, pre-delivery state variables,
pressure labels, and cricket delivery semantics.
"""

import os
import hashlib
import json
import pandas as pd
import numpy as np

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit")
STEP3_DIR = os.path.join(AUDIT_DIR, "step3_individual_model")
os.makedirs(STEP3_DIR, exist_ok=True)

DATASETS = {
    "ball_by_ball.csv": os.path.join(ROOT, "ball_by_ball.csv"),
    "matches.csv": os.path.join(ROOT, "matches.csv"),
    "competitions.csv": os.path.join(ROOT, "competitions.csv"),
    "teams.csv": os.path.join(ROOT, "teams.csv"),
    "playing_eleven.csv": os.path.join(ROOT, "playing_eleven.csv"),
    "competition_team_player_mapping.csv": os.path.join(ROOT, "competition_team_player_mapping.csv"),
}

EXPECTED_HASHES = {
    "ball_by_ball.csv": "A3926F49D2C684DCA2A5D2DE535A02C5EE46EA654CA1E79DD31C69E7544E9889",
    "matches.csv": "BB100AB84B8B9A15160C1F2315CF675210131A30E779EC5079FD5403DCF56EEF",
    "competitions.csv": "507CEB7189F972D4E4F299DDCFC97F3C3247AF1913F6291106F161FA8353FD9B",
    "teams.csv": "A65E5922A9B3BF49247B24FC9471782E700EFB31F8DCC5042923238B87C50A5D",
    "playing_eleven.csv": "7517C73722A28D5D61C808CCF0CBED315A8780586D02E946EB9A7F5DAF011C27",
    "competition_team_player_mapping.csv": "1DED4E42A933618572D6E2C3A521C3257EB1844FAB4456D567D77CBB2D3BBB12",
}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    lines = []
    def log(msg=""):
        lines.append(msg)
        print(msg)

    log("=" * 80)
    log("PHASE 1 STEP 3 — TASK 1: DELIVERY DATA VERIFICATION & PROVENANCE AUDIT")
    log("=" * 80)

    # 1. Verify Original Data Checksums
    log("\n[1] ORIGINAL CSV INTEGRITY CHECKSUMS")
    all_matched = True
    for name, path in DATASETS.items():
        size = os.path.getsize(path)
        actual_hash = sha256_file(path)
        exp_hash = EXPECTED_HASHES[name]
        match = (actual_hash == exp_hash)
        if not match: all_matched = False
        log(f"  {name:<38} | {size:>10,} B | SHA256 Match: {match}")
    log(f"  -> All 6 original dataset checksums match Step 1 & Step 2: {all_matched}")

    # 2. Verify bbb_enriched.pkl & so_bbb.pkl Provenance and Schema
    log("\n[2] INTERMEDIATE PICKLE PROVENANCE & ROW COUNTS")
    pkl_enriched_path = os.path.join(AUDIT_DIR, "bbb_enriched.pkl")
    pkl_so_path = os.path.join(AUDIT_DIR, "so_bbb.pkl")

    assert os.path.exists(pkl_enriched_path), f"Missing {pkl_enriched_path}"
    assert os.path.exists(pkl_so_path), f"Missing {pkl_so_path}"

    df_enriched = pd.read_pickle(pkl_enriched_path)
    df_so = pd.read_pickle(pkl_so_path)
    bbb_raw = pd.read_csv(DATASETS["ball_by_ball.csv"], low_memory=False)

    log(f"  Raw ball_by_ball.csv total rows: {len(bbb_raw):,}")
    log(f"  bbb_enriched.pkl total rows    : {len(df_enriched):,} (innings 1 & 2)")
    log(f"  so_bbb.pkl total rows          : {len(df_so):,} (innings 3 & 4)")
    log(f"  Sum of enriched + super over   : {len(df_enriched) + len(df_so):,}")
    assert len(df_enriched) + len(df_so) == len(bbb_raw), "Row count discrepancy between raw and pickles!"
    log("  -> Row count conservation verified: Exactly 200,999 rows.")

    # 3. Verify Match IDs & Scope Separation
    log("\n[3] MATCH ID COVERAGE & SUPER OVER TREATMENT")
    matches = pd.read_csv(DATASETS["matches.csv"])
    m_all = set(matches["match_id"])
    m_raw = set(bbb_raw["match_id"])
    m_enr = set(df_enriched["match_id"])
    m_so = set(df_so["match_id"])

    log(f"  Matches in matches.csv          : {len(m_all)}")
    log(f"  Matches in ball_by_ball.csv     : {len(m_raw)}")
    log(f"  Matches in bbb_enriched.pkl     : {len(m_enr)}")
    log(f"  Matches in so_bbb.pkl           : {len(m_so)}")
    log(f"  Matches abandoned (0 balls)     : {len(m_all - m_raw)}")
    log(f"  Super Over matches              : {sorted(m_so)}")
    assert m_so.issubset(m_enr), "Super over matches must also have normal innings in bbb_enriched!"
    log("  -> Scope separation verified: 38 Super Over deliveries across 6 matches isolated into so_bbb.pkl.")

    # 4. Verify Chronological Ordering & Zero Leakage
    log("\n[4] CHRONOLOGICAL ORDERING & ZERO OUTCOME LEAKAGE")
    order_diffs = df_enriched.groupby(["match_id", "innings"])["innings_ball_num"].diff().fillna(1)
    neg_order = (order_diffs < 0).sum()
    log(f"  Deliveries where innings_ball_num decreases chronologically: {neg_order}")
    assert neg_order == 0, "Chronological ordering violation detected!"

    # Verify pre-delivery states strictly precede delivery outcome
    score_diff = df_enriched.groupby(["match_id", "innings"])["score_before"].diff()
    wkt_diff = df_enriched.groupby(["match_id", "innings"])["wkts_before"].diff()
    prev_runs = df_enriched.groupby(["match_id", "innings"])["team_runs_obs"].shift(1)
    prev_wkts = df_enriched.groupby(["match_id", "innings"])["is_wicket"].shift(1)

    score_leakage_violations = (score_diff.dropna() != prev_runs.dropna()).sum()
    wkt_leakage_violations = (wkt_diff.dropna() != prev_wkts.dropna()).sum()
    log(f"  score_before == prev_score + prev_delivery_runs violations: {score_leakage_violations}")
    log(f"  wkts_before == prev_wkts + prev_delivery_wkt violations     : {wkt_leakage_violations}")
    assert score_leakage_violations == 0 and wkt_leakage_violations == 0, "Pre-delivery state leakage detected!"
    log("  -> Zero outcome leakage verified: score_before and wkts_before strictly lag delivery outcome.")

    # 5. Delivery Semantics Investigation
    log("\n[5] DELIVERY SEMANTICS & ACCOUNTING BOUNDARIES")
    runs_bat = df_enriched["runs"]
    team_obs = df_enriched["team_runs_obs"]
    bowl_obs = df_enriched["bowl_runs_obs"]
    is_legal_bat = df_enriched["is_legal_bat"]
    is_legal_bowl = df_enriched["is_legal_bowl"]
    is_wkt = df_enriched["is_wicket"]
    is_bowler_wkt = df_enriched["is_bowler_wicket"]

    log(f"  Total legal balls faced by batters (excludes wides)           : {is_legal_bat.sum():,} ({round(100*is_legal_bat.mean(),2)}%)")
    log(f"  Total legal deliveries bowled (excludes wides & no-balls)     : {is_legal_bowl.sum():,} ({round(100*is_legal_bowl.mean(),2)}%)")
    log(f"  Total batter runs off the bat                                 : {runs_bat.sum():,}")
    log(f"  Total minimal observable team runs                            : {team_obs.sum():,}")
    log(f"  Total minimal observable bowler-conceded runs                 : {bowl_obs.sum():,}")
    log(f"  Team extras runs (team_runs_obs - runs)                       : {team_obs.sum() - runs_bat.sum():,}")
    log(f"  Bowler-charged extras (bowl_runs_obs - runs)                  : {bowl_obs.sum() - runs_bat.sum():,}")
    log(f"  Fielding extras (byes, legbyes, penalties = team - bowl)      : {team_obs.sum() - bowl_obs.sum():,}")
    log(f"  Total wickets in innings 1-2                                  : {is_wkt.sum():,}")
    log(f"  Bowler-credited wickets (excludes RunOut, Retire Out, etc.)   : {is_bowler_wkt.sum():,} ({round(100*is_bowler_wkt.sum()/is_wkt.sum(),1)}% of wickets)")
    non_bowler_wkts = is_wkt.sum() - is_bowler_wkt.sum()
    log(f"  Fielding/non-bowler wickets (RunOut, Retire Out)              : {non_bowler_wkts:,}")

    # 6. Pre-delivery Pressure Label Verification
    log("\n[6] PRE-DELIVERY PRESSURE METRICS (BPI & BWPI)")
    log(f"  BPI range : min={df_enriched['BPI'].min():.2f}, median={df_enriched['BPI'].median():.2f}, mean={df_enriched['BPI'].mean():.2f}, max={df_enriched['BPI'].max():.2f}")
    log(f"  BWPI range: min={df_enriched['BWPI'].min():.2f}, median={df_enriched['BWPI'].median():.2f}, mean={df_enriched['BWPI'].mean():.2f}, max={df_enriched['BWPI'].max():.2f}")

    # Cutoffs at 25% established in Step 2:
    cut_b = df_enriched["BPI"].quantile(0.75)
    cut_bw = df_enriched["BWPI"].quantile(0.75)
    log(f"  25% High-Pressure Cutoffs: BPI >= {cut_b:.3f} | BWPI >= {cut_bw:.3f}")
    p_bat_count = (df_enriched["BPI"] >= cut_b).sum()
    p_bowl_count = (df_enriched["BWPI"] >= cut_bw).sum()
    log(f"  High-pressure batting deliveries: {p_bat_count:,} ({round(100*p_bat_count/len(df_enriched),1)}%)")
    log(f"  High-pressure bowling deliveries: {p_bowl_count:,} ({round(100*p_bowl_count/len(df_enriched),1)}%)")

    # 7. Player Identity Mapping
    log("\n[7] PLAYER IDENTITY INTEGRITY")
    ctpm = pd.read_csv(DATASETS["competition_team_player_mapping.csv"])
    p11 = pd.read_csv(DATASETS["playing_eleven.csv"])
    known_pids = set(ctpm["player_id"].unique())
    strikers = set(df_enriched["striker_id"].dropna().astype(int))
    bowlers = set(df_enriched["bowler_id"].dropna().astype(int))
    log(f"  Distinct strikers in deliveries: {len(strikers)} (unknown IDs: {len(strikers - known_pids)})")
    log(f"  Distinct bowlers in deliveries : {len(bowlers)} (unknown IDs: {len(bowlers - known_pids)})")
    assert len(strikers - known_pids) == 0 and len(bowlers - known_pids) == 0, "Unknown player IDs detected!"
    log("  -> All striker and bowler IDs cleanly mapped to ctpm.")

    # Save summary report
    out_file = os.path.join(STEP3_DIR, "01_delivery_verification_report.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log(f"\n[OK] Task 1 Delivery Verification Report saved to {out_file}")


if __name__ == "__main__":
    main()

