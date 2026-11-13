"""
Phase 1 Read-Only Dataset Audit Script (01_six_dataset_audit.py)
Audits all six official Rajasthan Royals SupeRR Selector Season 2 datasets without
modifying any original files. Outputs DATASET_AUDIT.csv and 01_dataset_audit_report.txt
inside phase1_audit/.
"""

import hashlib
import os
import json
import pandas as pd
import numpy as np

ROOT = r"c:\Rajasthan Royals"
OUT_DIR = os.path.join(ROOT, "phase1_audit")
os.makedirs(OUT_DIR, exist_ok=True)

DATASETS = [
    ("ball_by_ball.csv", [os.path.join(ROOT, "ball_by_ball.csv")]),
    ("matches.csv", [os.path.join(ROOT, "matches.csv"), os.path.join(ROOT, "season2_data", "matches.csv")]),
    ("competitions.csv", [os.path.join(ROOT, "competitions.csv"), os.path.join(ROOT, "season2_data", "competitions.csv")]),
    ("teams.csv", [os.path.join(ROOT, "teams.csv"), os.path.join(ROOT, "season2_data", "teams.csv")]),
    ("playing_eleven.csv", [os.path.join(ROOT, "playing_eleven.csv"), os.path.join(ROOT, "season2_data", "playing_eleven.csv")]),
    ("competition_team_player_mapping.csv", [
        os.path.join(ROOT, "competition_team_player_mapping.csv"),
        os.path.join(ROOT, "season2_data", "competition_team_player_mapping.csv"),
    ]),
]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    lines = []
    def log(msg=""):
        lines.append(msg)
        print(msg)

    log("=" * 80)
    log("PHASE 1 — SIX OFFICIAL DATASETS AUDIT REPORT")
    log("=" * 80)

    # 1. File discovery, sizes, SHA-256 verification
    log("\n[1] FILE INVENTORY & SHA-256 INTEGRITY")
    file_records = []
    dfs = {}
    for name, paths in DATASETS:
        hashes = {}
        for p in paths:
            exists = os.path.exists(p)
            if not exists:
                log(f"MISSING: {p}")
                continue
            size = os.path.getsize(p)
            h = sha256_file(p)
            hashes[p] = (size, h)
            log(f"  {name:<40} | {p:<65} | {size:>10,} B | {h}")
        unique_hashes = set(v[1] for v in hashes.values())
        log(f"  -> Distinct hashes for {name}: {len(unique_hashes)} (identical across copies: {len(unique_hashes) == 1})")
        primary_path = paths[0]
        df = pd.read_csv(primary_path, low_memory=False)
        dfs[name] = df
        file_records.append({
            "dataset": name,
            "primary_path": primary_path,
            "copy_paths": "; ".join(paths),
            "size_bytes": os.path.getsize(primary_path),
            "sha256": list(unique_hashes)[0] if unique_hashes else "",
            "copies_identical": len(unique_hashes) == 1,
            "rows": len(df),
            "cols": df.shape[1],
            "exact_duplicate_rows": int(df.duplicated().sum()),
        })

    # 2. Column-level audit -> DATASET_AUDIT.csv
    log("\n[2] COLUMN-LEVEL SCHEMA, MISSINGNESS & UNIQUE COUNTS")
    col_audit_rows = []
    for name, df in dfs.items():
        log(f"\n--- {name}: {len(df):,} rows x {df.shape[1]} cols | exact duplicates: {df.duplicated().sum()} ---")
        for col in df.columns:
            s = df[col]
            n_miss = int(s.isna().sum())
            pct_miss = round(100.0 * n_miss / max(1, len(df)), 3)
            n_uniq = int(s.nunique(dropna=True))
            dtype_str = str(s.dtype)
            non_null = s.dropna()
            if pd.api.types.is_numeric_dtype(s) and len(non_null) > 0:
                min_val = str(non_null.min())
                max_val = str(non_null.max())
                sample_vals = ", ".join(map(str, non_null.head(3).tolist()))
            else:
                vc = non_null.astype(str).value_counts().head(4)
                min_val = ""
                max_val = ""
                sample_vals = "; ".join(f"{k} ({v})" for k, v in vc.items())
            col_audit_rows.append({
                "dataset": name,
                "column": col,
                "dtype": dtype_str,
                "total_rows": len(df),
                "non_null_count": int(len(df) - n_miss),
                "missing_count": n_miss,
                "missing_pct": pct_miss,
                "nunique": n_uniq,
                "min_val": min_val,
                "max_val": max_val,
                "top_or_sample_values": sample_vals,
            })
            log(f"  {col:<28} | {dtype_str:<8} | miss={n_miss:>7} ({pct_miss:>6.2f}%) | uniq={n_uniq:>7} | {sample_vals[:60]}")

    audit_df = pd.DataFrame(col_audit_rows)
    # Also write dataset summary CSV alongside DATASET_AUDIT.csv
    audit_df.to_csv(os.path.join(OUT_DIR, "DATASET_AUDIT.csv"), index=False)
    pd.DataFrame(file_records).to_csv(os.path.join(OUT_DIR, "DATASET_FILES_SUMMARY.csv"), index=False)

    bbb = dfs["ball_by_ball.csv"]
    matches = dfs["matches.csv"]
    comps = dfs["competitions.csv"]
    teams = dfs["teams.csv"]
    p11 = dfs["playing_eleven.csv"]
    ctpm = dfs["competition_team_player_mapping.csv"]

    # 3. Primary Keys & Duplicate Checks
    log("\n[3] PRIMARY KEYS, COMPOSITE KEYS & DUPLICATES")
    log(f"  matches.match_id unique: {matches['match_id'].nunique()} / {len(matches)} (dups={matches['match_id'].duplicated().sum()})")
    log(f"  competitions.comp_id unique: {comps['comp_id'].nunique()} / {len(comps)} (dups={comps['comp_id'].duplicated().sum()})")
    log(f"  teams (comp_id, team_id) unique rows: {len(teams.drop_duplicates(['comp_id','team_id']))} / {len(teams)}")
    log(f"  teams team_id distinct: {teams['team_id'].nunique()}")
    log(f"  playing_eleven (match_id, team_id, player_id) unique: {len(p11.drop_duplicates(['match_id','team_id','player_id']))} / {len(p11)}")
    log(f"  playing_eleven (match_id, player_id) unique: {len(p11.drop_duplicates(['match_id','player_id']))} / {len(p11)}")
    log(f"  ctpm (comp_id, team_id, player_id) unique: {len(ctpm.drop_duplicates(['comp_id','team_id','player_id']))} / {len(ctpm)}")
    bbb_key_cols = ["match_id", "innings", "overid", "over_ball_num", "innings_ball_num"]
    log(f"  bbb (match_id, innings, overid, over_ball_num, innings_ball_num) unique: {len(bbb.drop_duplicates(bbb_key_cols))} / {len(bbb)}")
    bbb_dup_mask = bbb.duplicated(subset=bbb_key_cols, keep=False)
    if bbb_dup_mask.sum() > 0:
        log(f"  WARNING: {bbb_dup_mask.sum()} rows share {bbb_key_cols}! Sample:")
        log(bbb[bbb_dup_mask][bbb_key_cols + ["striker_name", "bowler_name", "runs", "extras_type", "extras1_runs"]].head(20).to_string())

    # 4. Foreign-Key Integrity
    log("\n[4] FOREIGN-KEY RELATIONSHIPS")
    m_in_bbb = set(bbb["match_id"].unique())
    m_in_matches = set(matches["match_id"].unique())
    m_in_p11 = set(p11["match_id"].unique())
    log(f"  matches -> competitions (comp_id missing in comps): {len(set(matches['comp_id']) - set(comps['comp_id']))}")
    log(f"  bbb match_ids not in matches: {len(m_in_bbb - m_in_matches)}")
    log(f"  matches match_ids missing from bbb: {len(m_in_matches - m_in_bbb)} -> IDs: {sorted(m_in_matches - m_in_bbb)}")
    missing_bbb_matches = matches[matches["match_id"].isin(m_in_matches - m_in_bbb)]
    log("  Missing-from-bbb matches results:")
    log(missing_bbb_matches[["match_id", "comp_id", "match_date", "home_team", "away_team", "result"]].to_string())
    log(f"  p11 match_ids not in matches: {len(m_in_p11 - m_in_matches)}")
    log(f"  matches match_ids missing from p11: {len(m_in_matches - m_in_p11)} -> IDs: {sorted(m_in_matches - m_in_p11)}")
    missing_p11_matches = matches[matches["match_id"].isin(m_in_matches - m_in_p11)]
    log(missing_p11_matches[["match_id", "comp_id", "match_date", "result"]].to_string())

    # Player FK checks
    bbb_pids = set(bbb["striker_id"].dropna().astype(int)) | set(bbb["non_striker_id"].dropna().astype(int)) | set(bbb["bowler_id"].dropna().astype(int))
    bbb_dismissed_pids = set(bbb["dismissed_player_id"].dropna().astype(int))
    p11_pids = set(p11["player_id"].dropna().astype(int))
    ctpm_pids = set(ctpm["player_id"].dropna().astype(int))
    log(f"  Distinct striker+non_striker+bowler player_ids in bbb: {len(bbb_pids)}")
    log(f"  Distinct dismissed_player_ids in bbb: {len(bbb_dismissed_pids)} (not in striker/ns/bowler: {len(bbb_dismissed_pids - bbb_pids)})")
    log(f"  bbb players not in p11: {len(bbb_pids - p11_pids)}")
    log(f"  bbb players not in ctpm: {len(bbb_pids - ctpm_pids)}")
    log(f"  p11 players not in ctpm: {len(p11_pids - ctpm_pids)}")
    log(f"  ctpm players not in p11: {len(ctpm_pids - p11_pids)}")

    # Check player_id -> player_name uniqueness across bbb & ctpm
    s_names = bbb[["striker_id", "striker_name"]].dropna().drop_duplicates()
    multi_names_s = s_names.groupby("striker_id")["striker_name"].nunique()
    b_names = bbb[["bowler_id", "bowler_name"]].dropna().drop_duplicates()
    multi_names_b = b_names.groupby("bowler_id")["bowler_name"].nunique()
    ctpm_names = ctpm[["player_id", "player_name"]].dropna().drop_duplicates()
    multi_names_c = ctpm_names.groupby("player_id")["player_name"].nunique()
    log(f"  player_ids with >1 striker_name: {(multi_names_s > 1).sum()}")
    if (multi_names_s > 1).sum() > 0:
        log(f"    -> {s_names[s_names['striker_id'].isin(multi_names_s[multi_names_s > 1].index)].to_dict('records')}")
    log(f"  player_ids with >1 bowler_name: {(multi_names_b > 1).sum()}")
    log(f"  player_ids with >1 ctpm player_name: {(multi_names_c > 1).sum()}")
    # Also check same striker_name -> multiple striker_ids!
    multi_ids_s = s_names.groupby("striker_name")["striker_id"].nunique()
    multi_ids_b = b_names.groupby("bowler_name")["bowler_id"].nunique()
    log(f"  striker_names shared by >1 striker_id: {(multi_ids_s > 1).sum()}")
    if (multi_ids_s > 1).sum() > 0:
        log(s_names[s_names["striker_name"].isin(multi_ids_s[multi_ids_s > 1].index)].sort_values("striker_name").to_string())
    log(f"  bowler_names shared by >1 bowler_id: {(multi_ids_b > 1).sum()}")
    if (multi_ids_b > 1).sum() > 0:
        log(b_names[b_names["bowler_name"].isin(multi_ids_b[multi_ids_b > 1].index)].sort_values("bowler_name").to_string())

    # 5. Competitions & Matches Breakdown
    log("\n[5] COMPETITION & MATCH COVERAGE")
    m_comp = matches.merge(comps, on="comp_id", how="left")
    log("  Matches by match_format:")
    log(m_comp["match_format"].value_counts(dropna=False).to_string())
    log("  Matches by season:")
    log(m_comp["season"].value_counts(dropna=False).sort_index().to_string())
    log("  Matches by competition format & name (non-T20I or Emerging):")
    log(comps[comps["match_format"] != "T20I"].to_string())
    emerging_comps = comps[comps["comp_name"].str.contains("Emerging|Rising|A Team|Qualifier|Asia Cup", case=False, na=False)]
    log("  Emerging / Asia Cup / Rising competitions in comps:")
    log(emerging_comps.to_string())
    log("  Matches by stage (top 20):")
    log(matches["stage"].value_counts(dropna=False).head(20).to_string())
    log(f"  knock_out value_counts: {matches['knock_out'].value_counts(dropna=False).to_dict()}")
    log(f"  win_team_id isna count: {matches['win_team_id'].isna().sum()}")
    log("  Matches with win_team_id NaN categorized by result pattern:")
    no_win = matches[matches["win_team_id"].isna()]
    log(no_win[["match_id", "comp_id", "stage", "knock_out", "result"]].to_string())

    # 6. Revised Overs & DLS Units Inspection
    log("\n[6] REVISED OVERS, REVISED TARGET & DLS AUDIT")
    rev = matches[matches["first_inn_revised_overs"].notna() | matches["second_inn_revised_overs"].notna() | matches["revised_target"].notna()]
    log(f"  Total matches with any revised column populated: {len(rev)}")
    log(rev[["match_id", "first_inn_revised_overs", "second_inn_revised_overs", "revised_target", "result"]].to_string())
    # Check actual legal balls bowled in those revised matches!
    bbb_rev = bbb[bbb["match_id"].isin(rev["match_id"])]
    is_legal = ~bbb_rev["extras_type"].isin(["wide", "Overstep", "other"])
    rev_balls = bbb_rev.assign(legal=is_legal).groupby(["match_id", "innings"])["legal"].sum().unstack(fill_value=0)
    rev_check = rev[["match_id", "first_inn_revised_overs", "second_inn_revised_overs", "revised_target", "result"]].merge(
        rev_balls, on="match_id", how="left"
    )
    log("  Actual legal balls bowled in revised matches:")
    log(rev_check.to_string())

    # 7. Ball-by-Ball Delivery Semantics: Overid, Ball Numbering, Extras, Wickets
    log("\n[7] BALL-BY-BALL DELIVERY SEMANTICS")
    log(f"  innings values: {bbb['innings'].value_counts(dropna=False).sort_index().to_dict()}")
    log(f"  overid range per innings:")
    log(bbb.groupby("innings")["overid"].agg(["min", "max", "nunique"]).to_string())
    log(f"  runs value_counts: {bbb['runs'].value_counts(dropna=False).sort_index().to_dict()}")
    log(f"  is_four vs runs crosstab:\n{pd.crosstab(bbb['runs'], bbb['is_four'], dropna=False)}")
    log(f"  is_six vs runs crosstab:\n{pd.crosstab(bbb['runs'], bbb['is_six'], dropna=False)}")
    log(f"  extras_type x extras1_runs crosstab:\n{pd.crosstab(bbb['extras_type'].fillna('<NaN>'), bbb['extras1_runs'], dropna=False)}")
    log(f"  extras_type x extras_2_runs crosstab:\n{pd.crosstab(bbb['extras_type'].fillna('<NaN>'), bbb['extras_2_runs'].fillna(-1), dropna=False)}")
    log(f"  extras_type x runs crosstab:\n{pd.crosstab(bbb['extras_type'].fillna('<NaN>'), bbb['runs'], dropna=False)}")

    # Check the 36 rows where extras_2_runs > 0 and anomalous rows
    log("\n  Rows with extras_2_runs > 0 (grouped):")
    e2 = bbb[bbb["extras_2_runs"].fillna(0) > 0]
    log(e2[["match_id", "innings", "overid", "over_ball_num", "innings_ball_num", "runs", "extras_type", "extras1_runs", "extras_2_runs", "is_four", "is_six"]].to_string())

    log("\n  Anomalous legbyes with runs > 0:")
    log(bbb[(bbb["extras_type"] == "legbyes") & (bbb["runs"] > 0)][["match_id", "innings", "overid", "over_ball_num", "innings_ball_num", "striker_name", "bowler_name", "runs", "extras_type", "extras1_runs", "extras_2_runs", "is_wicket", "dismissal_type"]].to_string())

    # Check wickets
    log("\n  Wicket & Dismissal Semantics:")
    log(f"  is_wicket value_counts: {bbb['is_wicket'].value_counts(dropna=False).to_dict()}")
    log("  is_wicket==1 vs dismissal_type:")
    log(bbb[bbb["is_wicket"] == 1]["dismissal_type"].fillna("<NaN>").value_counts().to_string())
    log("  is_wicket==0 but dismissal_type notna:")
    w0_dt = bbb[(bbb["is_wicket"] == 0) & (bbb["dismissal_type"].notna())]
    log(f"  Count: {len(w0_dt)}")
    if len(w0_dt) > 0:
        log(w0_dt[["match_id", "innings", "overid", "over_ball_num", "runs", "extras_type", "is_wicket", "dismissal_type", "dismissed_player_id"]].head(10).to_string())
    log("  is_wicket==1 but dismissed_player_id isna:")
    na_dp = bbb[(bbb["is_wicket"] == 1) & bbb["dismissed_player_id"].isna()]
    log(f"  Count: {len(na_dp)}")
    if len(na_dp) > 0:
        log(na_dp[["match_id", "innings", "overid", "over_ball_num", "striker_name", "non_striker_name", "bowler_name", "is_wicket", "dismissal_type"]].to_string())
    log(f"  batting_order values > 11 count: {(bbb['batting_order'] > 11).sum()} (max={bbb['batting_order'].max()}); over_ball_num max={bbb['over_ball_num'].max()}, innings_ball_num max={bbb['innings_ball_num'].max()}")
    log("  is_wicket==1 & dismissed_player_id != striker_id (e.g. non-striker runout/retired):")
    non_str_w = bbb[(bbb["is_wicket"] == 1) & (bbb["dismissed_player_id"] != bbb["striker_id"])]
    log(f"  Count: {len(non_str_w)} | breakdown by dismissal_type: {non_str_w['dismissal_type'].value_counts(dropna=False).to_dict()}")
    log("  is_wicket==1 on wide / Overstep / other:")
    w_ext = bbb[(bbb["is_wicket"] == 1) & (bbb["extras_type"].notna())]
    log(pd.crosstab(w_ext["extras_type"], w_ext["dismissal_type"].fillna("<NaN>")).to_string())

    # 8. Innings Margin Reconciliation Check (Proves extras ambiguity quantitatively!)
    log("\n[8] INNINGS TOTAL & MATCH MARGIN RECONCILIATION")
    # Compute lower bound observable delivery runs: runs + (1 if wide/Overstep/other/legbyes/byes else 0) + (5 if Penalty else 0) + extras_2_runs.fillna(0)
    ext = bbb["extras_type"].fillna("")
    e2v = bbb["extras_2_runs"].fillna(0)
    min_ext = np.where(ext.isin(["wide", "Overstep", "other", "legbyes", "byes"]), 1,
              np.where(ext == "Penalty", 5, 0))
    # Rule A (literal broken formula): runs + extras1_runs + extras_2_runs
    # Rule B (minimal legal+observable): runs + min_ext + extras_2_runs (note on Penalty might be 5, on byes/legbyes/wide >=1)
    # Wait: what if extras_2_runs IS the extra run count on wides/byes/legbyes when >1? No, only 36 rows have extras_2_runs > 0! Let's check!
    bbb_calc = bbb[["match_id", "innings", "runs", "is_wicket", "extras_type", "extras1_runs", "extras_2_runs"]].copy()
    bbb_calc["min_obs_runs"] = bbb_calc["runs"] + min_ext + np.where((ext == "Overstep") & (e2v > 0), e2v, 0)
    # Wait: check Overstep + extras_2_runs=1 vs e2v on NaN/other: let's just sum min_ext + e2v directly as minimal observable
    bbb_calc["min_runs_v2"] = bbb_calc["runs"] + min_ext + e2v
    inn_sums = bbb_calc[bbb_calc["innings"].isin([1, 2])].groupby(["match_id", "innings"]).agg(
        bat_runs=("runs", "sum"),
        min_obs=("min_runs_v2", "sum"),
        wkts=("is_wicket", "sum"),
        n_wide=("extras_type", lambda s: (s == "wide").sum()),
        n_byes=("extras_type", lambda s: (s == "byes").sum()),
        n_legbyes=("extras_type", lambda s: (s == "legbyes").sum()),
        n_nb=("extras_type", lambda s: s.isin(["Overstep", "other"]).sum()),
        n_balls=("runs", "count"),
    ).unstack(level=1)

    # Flatten columns
    inn_flat = pd.DataFrame(index=inn_sums.index)
    for col, inn in inn_sums.columns:
        inn_flat[f"i{inn}_{col}"] = inn_sums[(col, inn)]
    inn_flat = inn_flat.reset_index().merge(
        matches[["match_id", "home_team_id", "away_team_id", "win_team_id", "result", "revised_target"]],
        on="match_id", how="left"
    )
    # Extract numeric run margin for matches won by runs ("won by X runs" case-insensitive)
    run_margin_matches = inn_flat[inn_flat["result"].str.contains(r"won by \d+ run", case=False, na=False)].copy()
    run_margin_matches["reported_margin"] = run_margin_matches["result"].str.extract(r"(?i)won by (\d+) run", expand=False).astype(float)
    run_margin_matches = run_margin_matches[run_margin_matches["reported_margin"].notna()].copy()
    run_margin_matches["reported_margin"] = run_margin_matches["reported_margin"].astype(int)
    # Exclude revised_target / DLS matches first for clean comparison
    clean_rm = run_margin_matches[run_margin_matches["revised_target"].isna() & ~run_margin_matches["result"].str.contains("DLS|D/L", case=False, na=False)].copy()
    clean_rm["calc_margin_min_obs"] = clean_rm["i1_min_obs"] - clean_rm["i2_min_obs"]
    clean_rm["diff_runs"] = clean_rm["reported_margin"] - clean_rm["calc_margin_min_obs"]
    log(f"  Non-DLS 'won by X runs' matches: {len(clean_rm)}")
    log(f"  Exact margin match (diff == 0) using min_obs (1 per extra + extras_2_runs): {(clean_rm['diff_runs'] == 0).sum()} / {len(clean_rm)} ({100*(clean_rm['diff_runs']==0).mean():.1f}%)")
    log(f"  Within +/- 2 runs: {(clean_rm['diff_runs'].abs() <= 2).sum()} / {len(clean_rm)}")
    log(f"  Diff quantiles: {clean_rm['diff_runs'].quantile([0, 0.05, 0.25, 0.5, 0.75, 0.95, 1.0]).to_dict()}")
    log("  Sample non-DLS run-margin mismatches (showing i1_min_obs, i2_min_obs, reported_margin, extras counts):")
    log(clean_rm[clean_rm["diff_runs"] != 0][["match_id", "i1_min_obs", "i2_min_obs", "reported_margin", "calc_margin_min_obs", "diff_runs", "i1_n_wide", "i1_n_byes", "i1_n_legbyes", "i2_n_wide", "i2_n_byes", "i2_n_legbyes"]].head(15).to_string())

    # Check if wide / bye / legbye total unrecorded multi-runs correlate with diff!
    # Also check matches where i1 had ZERO byes/legbyes/wides vs non-zero:
    zero_ambig = clean_rm[(clean_rm["i1_n_wide"] + clean_rm["i1_n_byes"] + clean_rm["i1_n_legbyes"] + clean_rm["i2_n_wide"] + clean_rm["i2_n_byes"] + clean_rm["i2_n_legbyes"]) == 0]
    log(f"  Non-DLS run-margin matches with ZERO wides/byes/legbyes: {len(zero_ambig)}, exact diff==0: {(zero_ambig['diff_runs']==0).sum()}")

    # Check non-DLS wicket-margin matches where team2 chasing appears NOT to pass i1_min_obs!
    wkt_matches = inn_flat[inn_flat["result"].str.contains(r"won by \d+ wkt|won by \d+ wicket", case=False, na=False)].copy()
    clean_wm = wkt_matches[wkt_matches["revised_target"].isna() & ~wkt_matches["result"].str.contains("DLS|D/L", case=False, na=False)].copy()
    clean_wm["chase_shortfall"] = clean_wm["i1_min_obs"] + 1 - clean_wm["i2_min_obs"]
    log(f"  Non-DLS 'won by X wkts' matches: {len(clean_wm)}")
    log(f"  Cases where i2_min_obs < i1_min_obs + 1 (proving unrecorded multi-run wides/byes/legbyes/penalties happened): {(clean_wm['chase_shortfall'] > 0).sum()} / {len(clean_wm)} ({100*(clean_wm['chase_shortfall']>0).mean():.1f}%)")
    log(f"  Chase shortfall quantiles (runs 'missing' from i2 due to unrecorded multi-run extras minus i1 unrecorded extras): {clean_wm['chase_shortfall'].quantile([0, 0.25, 0.5, 0.75, 0.95, 1.0]).to_dict()}")
    log("  Sample wicket-win matches where i2_min_obs <= i1_min_obs:")
    log(clean_wm[clean_wm["chase_shortfall"] > 0][["match_id", "i1_min_obs", "i2_min_obs", "chase_shortfall", "i2_n_wide", "i2_n_byes", "i2_n_legbyes", "result"]].head(12).to_string())

    # Also test strike-rotation tracking to see if multi-run byes/legbyes/wides are detectable from striker changes!
    log("\n[9] STRIKE-ROTATION FORENSICS FOR UNRECORDED EXTRA RUNS")
    # Sort bbb sequentially within each innings and check odd-run strike rotation on extras!
    # Look at byes & legbyes rows followed by another ball in the SAME over (so over-end doesn't swap strike).
    bbb_sorted = bbb.sort_values(["match_id", "innings", "innings_ball_num", "overid", "over_ball_num"]).reset_index(drop=True)
    same_inn_over = (
        (bbb_sorted["match_id"] == bbb_sorted["match_id"].shift(-1))
        & (bbb_sorted["innings"] == bbb_sorted["innings"].shift(-1))
        & (bbb_sorted["overid"] == bbb_sorted["overid"].shift(-1))
        & (bbb_sorted["is_wicket"] == 0)
    )
    bbb_sorted["next_striker_id"] = bbb_sorted["striker_id"].shift(-1)
    bbb_sorted["strike_rotated"] = bbb_sorted["striker_id"] != bbb_sorted["next_striker_id"]
    for et in ["wide", "legbyes", "byes", "Overstep", "other"]:
        sub = bbb_sorted[same_inn_over & (bbb_sorted["extras_type"] == et)]
        rot_pct = 100.0 * sub["strike_rotated"].mean() if len(sub) > 0 else np.nan
        log(f"  extras_type={et:<10} mid-over non-wicket balls={len(sub):>5} | strike rotated on next ball: {int(sub['strike_rotated'].sum()):>5} ({rot_pct:.1f}%) [note: if always 1 extra run, strike rotates ~100% on byes/legbyes and 0% on 1-wide!]")

    # 10. Scouting Feature Coverage (Hawk-Eye / Speed / Stroke / Pitch)
    log("\n[10] SCOUTING & TRACKING METADATA COVERAGE IN ball_by_ball.csv")
    scout_cols = ["batting_type", "bowling_type", "batting_order", "pace_or_spin", "bowl_speed", "stroke", "delivery_style", "over_or_around", "on_or_off", "delivery_ist_time"]
    for c in scout_cols:
        s = bbb[c]
        nn = int(s.notna().sum())
        pct = 100.0 * nn / len(bbb)
        if c == "bowl_speed":
            gt0 = int((s.fillna(-1) > 0).sum())
            eq0 = int((s == 0).sum())
            log(f"  {c:<18}: non-null={nn:>7} ({pct:>5.1f}%), >0={gt0:>7} ({100*gt0/len(bbb):>5.1f}%), ==0={eq0:>7}")
        else:
            top3 = "; ".join(f"{k}:{v}" for k, v in s.dropna().astype(str).value_counts().head(4).items())
            log(f"  {c:<18}: non-null={nn:>7} ({pct:>5.1f}%), uniq={s.nunique():>5} | top: {top3}")
    # Check bowl_speed coverage by competition format
    bbb_m = bbb[["match_id", "bowl_speed", "stroke", "delivery_style", "on_or_off"]].merge(
        matches[["match_id", "comp_id"]].merge(comps[["comp_id", "comp_name", "match_format", "season"]], on="comp_id"),
        on="match_id", how="left"
    )
    fmt_cov = bbb_m.groupby("match_format").agg(
        deliveries=("match_id", "count"),
        speed_gt0_pct=("bowl_speed", lambda s: 100.0 * (s.fillna(-1) > 0).mean()),
        stroke_pct=("stroke", lambda s: 100.0 * s.notna().mean()),
        delivery_style_pct=("delivery_style", lambda s: 100.0 * s.notna().mean()),
        on_or_off_pct=("on_or_off", lambda s: 100.0 * s.notna().mean()),
    )
    log("\n  Tracking metadata coverage by match_format:")
    log(fmt_cov.to_string())

    # 11. Additional Forensic Edge Cases
    log("\n[11] FORENSIC EDGE CASES")
    p11_dups = p11[p11.duplicated(["match_id", "player_id"], keep=False)]
    log(f"  playing_eleven duplicate (match_id, player_id) rows: {len(p11_dups)}")
    if len(p11_dups) > 0:
        log(p11_dups.head(12).to_string())
    missing_p11_pids = bbb_pids - p11_pids
    log(f"  bbb player_ids missing from playing_eleven: {missing_p11_pids}")
    if missing_p11_pids:
        log(ctpm[ctpm["player_id"].isin(missing_p11_pids)].drop_duplicates("player_id").to_string())
    log("  bowling_team_id == win_team_id? Any match_id anomalies in Super Overs (innings 3,4):")
    so = bbb[bbb["innings"].isin([3, 4])]
    so_summary = so.groupby("match_id").agg(innings=("innings", "unique"), rows=("runs", "count")).reset_index().merge(
        matches[["match_id", "comp_id", "result", "knock_out", "stage"]], on="match_id"
    )
    log(so_summary.to_string())
    # Check duplicate player IDs same name details
    dup_names = ["Abdul Samad", "Basil Hameed", "Haider Ali"]
    log("  Duplicate-name player records in ctpm:")
    log(ctpm[ctpm["player_name"].isin(dup_names)][["player_id", "player_name", "team_name", "comp_name"]].drop_duplicates().to_string())
    # Check bowl_speed == 0 vs > 0 distribution and unreal speeds
    bs_pos = bbb.loc[bbb["bowl_speed"] > 0, "bowl_speed"]
    log(f"  bowl_speed > 0 count={len(bs_pos)}, min={bs_pos.min()}, p01={bs_pos.quantile(0.01):.1f}, median={bs_pos.median():.1f}, p99={bs_pos.quantile(0.99):.1f}, max={bs_pos.max()}")
    log(f"  bowl_speed < 0 count={(bbb['bowl_speed'] < 0).sum()}")
    # Check runs=4 & is_four=False, runs=6 & is_six=False, runs=5
    log(f"  runs==4 & is_four==False count: {((bbb['runs']==4) & (~bbb['is_four'])).sum()} | runs==6 & is_six==False count: {((bbb['runs']==6) & (~bbb['is_six'])).sum()} | runs==5 count: {(bbb['runs']==5).sum()}")
    # Check batting_order > 11 rows
    log("  batting_order > 11 sample:")
    log(bbb[bbb["batting_order"] > 11][["match_id", "innings", "overid", "striker_id", "striker_name", "batting_order"]].drop_duplicates(["match_id", "striker_id"]).head(10).to_string())

    # Write full text report
    report_path = os.path.join(OUT_DIR, "01_dataset_audit_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log(f"\nSaved: {report_path}")
    log(f"Saved: {os.path.join(OUT_DIR, 'DATASET_AUDIT.csv')}")
    log(f"Saved: {os.path.join(OUT_DIR, 'DATASET_FILES_SUMMARY.csv')}")


if __name__ == "__main__":
    main()
