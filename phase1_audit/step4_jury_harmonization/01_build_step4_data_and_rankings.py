"""
Phase 1 Step 4 — Final Data Harmonization & Ranking Engine
(01_build_step4_data_and_rankings.py)

Generates authoritative Step 4 ranking CSVs:
1. FINAL_BATTER_RANKINGS.csv (All 163 qualified batters, Pure Shrunk RAE, 500-replicate cluster bootstrap)
2. FINAL_BOWLER_RANKINGS_RAE.csv (All 179 qualified bowlers, Pure Shrunk RPAE run prevention)
3. FINAL_BOWLER_RANKINGS_COMPOSITE.csv (All 179 qualified bowlers, 60/40 Composite RPAE + WAE)
"""

import os
import numpy as np
import pandas as pd

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit")
STEP4_DIR = os.path.join(AUDIT_DIR, "step4_jury_harmonization")
os.makedirs(STEP4_DIR, exist_ok=True)


def main():
    print("=" * 80)
    print("PHASE 1 STEP 4 — DATA HARMONIZATION & FINAL RANKINGS GENERATION")
    print("=" * 80)

    # Load modeled regular deliveries and Super Over deliveries
    df = pd.read_pickle(os.path.join(AUDIT_DIR, "step3_individual_model", "bbb_step3_modeled.pkl"))
    ctpm = pd.read_csv(os.path.join(ROOT, "competition_team_player_mapping.csv"))
    matches = pd.read_csv(os.path.join(ROOT, "matches.csv"))
    comps = pd.read_csv(os.path.join(ROOT, "competitions.csv"))

    # Player metadata
    p_names = dict(zip(ctpm["player_id"], ctpm["player_name"]))
    p_teams = ctpm.groupby("player_id")["team_name"].apply(lambda s: ", ".join(sorted(set(s)))).to_dict()

    # Formats mapping
    comp_map = comps.set_index("comp_id")["match_format"].to_dict()
    df["match_format"] = df["comp_id"].map(comp_map).fillna("T20")

    # Authoritative High-Pressure definitions (Top 25% BPI / BWPI)
    cut_b = df["BPI"].quantile(0.75)
    cut_bw = df["BWPI"].quantile(0.75)
    df["is_hp_bat"] = (df["BPI"] >= cut_b) & df["is_legal_bat"]
    df["is_hp_bowl"] = (df["BWPI"] >= cut_bw)

    # =========================================================================
    # 1. BATTING AGGREGATION & FINAL RANKINGS
    # =========================================================================
    print("\n[1] Aggregating Batting Data & Running Match-Clustered Bootstrap...")

    # Career metrics
    bat_career = df[df["is_legal_bat"]].groupby("striker_id").agg(
        career_bf=("runs", "count"),
        career_runs=("runs", "sum"),
        career_exp_runs=("exp_bat_runs", "sum"),
        career_rae=("rae", "sum"),
        career_outs=("is_striker_out", "sum")
    ).reset_index()

    # Pressure metrics
    bat_pressure = df[df["is_hp_bat"]].groupby("striker_id").agg(
        pressure_bf=("runs", "count"),
        pressure_runs=("runs", "sum"),
        pressure_exp_runs=("exp_bat_runs", "sum"),
        pressure_rae=("rae", "sum"),
        pressure_outs=("is_striker_out", "sum")
    ).reset_index()

    # Non-pressure metrics
    bat_np = df[df["is_legal_bat"] & (~df["is_hp_bat"])].groupby("striker_id").agg(
        np_bf=("runs", "count"),
        np_runs=("runs", "sum"),
        np_exp_runs=("exp_bat_runs", "sum"),
        np_rae=("rae", "sum")
    ).reset_index()

    # Merge
    bat_all = bat_career.merge(bat_pressure, on="striker_id", how="left").fillna(0)
    bat_all = bat_all.merge(bat_np, on="striker_id", how="left").fillna(0)

    # Eligibility filter: career_bf >= 300 and pressure_bf >= 40
    bat_qual = bat_all[(bat_all["career_bf"] >= 300) & (bat_all["pressure_bf"] >= 40)].copy()
    print(f"  Qualified Batters (career >= 300 & pressure >= 40): {len(bat_qual)}")

    M0_BAT = 150.0
    bat_qual["career_sr"] = (100.0 * bat_qual["career_runs"] / bat_qual["career_bf"]).round(2)
    bat_qual["career_exp_sr"] = (100.0 * bat_qual["career_exp_runs"] / bat_qual["career_bf"]).round(2)
    bat_qual["career_rae_rate"] = (100.0 * bat_qual["career_rae"] / bat_qual["career_bf"]).round(2)

    bat_qual["pressure_sr"] = (100.0 * bat_qual["pressure_runs"] / bat_qual["pressure_bf"]).round(2)
    bat_qual["pressure_exp_sr"] = (100.0 * bat_qual["pressure_exp_runs"] / bat_qual["pressure_bf"]).round(2)
    bat_qual["raw_pressure_rae_rate"] = (100.0 * bat_qual["pressure_rae"] / bat_qual["pressure_bf"]).round(2)

    bat_qual["non_pressure_sr"] = np.where(bat_qual["np_bf"] > 0, (100.0 * bat_qual["np_runs"] / bat_qual["np_bf"]).round(2), np.nan)
    bat_qual["non_pressure_rae_rate"] = np.where(bat_qual["np_bf"] > 0, (100.0 * bat_qual["np_rae"] / bat_qual["np_bf"]).round(2), np.nan)
    bat_qual["clutch_rae_lift"] = (bat_qual["raw_pressure_rae_rate"] - bat_qual["non_pressure_rae_rate"]).round(2)

    # Shrunk Pure RAE Score
    bat_qual["shrunk_rae_score"] = ((bat_qual["pressure_rae"] / (bat_qual["pressure_bf"] + M0_BAT)) * 100.0).round(2)

    # Match-clustered bootstrap for all qualified batters (500 replicates)
    unique_matches = df["match_id"].unique()
    n_matches = len(unique_matches)
    rng = np.random.default_rng(42)

    bat_p_df = df[df["is_hp_bat"]].groupby(["match_id", "striker_id"]).agg(
        n_bf=("runs", "count"),
        sum_rae=("rae", "sum")
    ).reset_index()

    m_to_bat = {m: g for m, g in bat_p_df.groupby("match_id")}
    match_list = np.array(unique_matches)
    qual_bat_pids = bat_qual["striker_id"].tolist()
    pid_to_i_b = {p: i for i, p in enumerate(qual_bat_pids)}
    n_p_b = len(qual_bat_pids)

    cnt_mat_b = np.zeros((n_matches, n_p_b))
    sum_mat_b = np.zeros((n_matches, n_p_b))
    for mi, m in enumerate(match_list):
        if m in m_to_bat:
            for _, r in m_to_bat[m].iterrows():
                pid = r["striker_id"]
                if pid in pid_to_i_b:
                    pi = pid_to_i_b[pid]
                    cnt_mat_b[mi, pi] = r["n_bf"]
                    sum_mat_b[mi, pi] = r["sum_rae"]

    n_boot = 500
    boot_scores_bat = np.zeros((n_boot, n_p_b))
    boot_ranks_bat = np.zeros((n_boot, n_p_b))

    for b in range(n_boot):
        sample_indices = rng.integers(0, n_matches, size=n_matches)
        boot_cnt = cnt_mat_b[sample_indices].sum(axis=0)
        boot_sum = sum_mat_b[sample_indices].sum(axis=0)
        sc = (boot_sum / (boot_cnt + M0_BAT)) * 100.0
        boot_scores_bat[b] = sc
        boot_ranks_bat[b] = np.argsort(np.argsort(-sc)) + 1

    boot_means_b = np.mean(boot_scores_bat, axis=0).round(2)
    boot_ses_b = np.std(boot_scores_bat, axis=0).round(2)
    ci_lows_b = np.percentile(boot_scores_bat, 2.5, axis=0).round(2)
    ci_highs_b = np.percentile(boot_scores_bat, 97.5, axis=0).round(2)
    rk_lows_b = np.percentile(boot_ranks_bat, 5, axis=0).astype(int)
    rk_highs_b = np.percentile(boot_ranks_bat, 95, axis=0).astype(int)
    top10_probs_b = (100.0 * (boot_ranks_bat <= 10).mean(axis=0)).round(1)

    bat_qual["bootstrap_mean"] = [boot_means_b[pid_to_i_b[p]] for p in bat_qual["striker_id"]]
    bat_qual["bootstrap_se"] = [boot_ses_b[pid_to_i_b[p]] for p in bat_qual["striker_id"]]
    bat_qual["ci95_lower"] = [ci_lows_b[pid_to_i_b[p]] for p in bat_qual["striker_id"]]
    bat_qual["ci95_upper"] = [ci_highs_b[pid_to_i_b[p]] for p in bat_qual["striker_id"]]
    bat_qual["rank_ci_90"] = [f"#{rk_lows_b[pid_to_i_b[p]]} to #{rk_highs_b[pid_to_i_b[p]]}" for p in bat_qual["striker_id"]]
    bat_qual["top10_prob_pct"] = [top10_probs_b[pid_to_i_b[p]] for p in bat_qual["striker_id"]]

    # Sample size badges
    def get_badge(n):
        if n >= 150:
            return "High Volume (N >= 150)"
        elif n >= 75:
            return "Moderate Volume (75 <= N < 150)"
        else:
            return "Small Sample Caution (40 <= N < 75)"

    bat_qual["sample_size_badge"] = bat_qual["pressure_bf"].apply(get_badge)
    bat_qual["player_name"] = bat_qual["striker_id"].map(p_names).fillna("Unknown")
    bat_qual["franchises"] = bat_qual["striker_id"].map(p_teams).fillna("Unknown")

    # Sort by shrunk Pure RAE score
    bat_qual = bat_qual.sort_values("shrunk_rae_score", ascending=False).reset_index(drop=True)
    bat_qual.index += 1
    bat_qual["rank"] = bat_qual.index

    cols_bat_final = [
        "rank", "player_id", "player_name", "franchises",
        "career_bf", "career_runs", "career_sr", "career_exp_sr", "career_rae_rate",
        "pressure_bf", "pressure_runs", "pressure_exp_runs", "pressure_sr", "pressure_exp_sr",
        "pressure_rae", "raw_pressure_rae_rate", "non_pressure_sr", "non_pressure_rae_rate",
        "clutch_rae_lift", "shrunk_rae_score", "bootstrap_mean", "bootstrap_se",
        "ci95_lower", "ci95_upper", "rank_ci_90", "top10_prob_pct", "sample_size_badge"
    ]
    bat_final = bat_qual.rename(columns={"striker_id": "player_id"})[cols_bat_final]
    bat_final.to_csv(os.path.join(STEP4_DIR, "FINAL_BATTER_RANKINGS.csv"), index=False)
    print(f"  Saved FINAL_BATTER_RANKINGS.csv ({len(bat_final)} qualified batters).")

    # =========================================================================
    # 2. BOWLING AGGREGATION & FINAL RANKINGS (PURE RPAE & COMPOSITE)
    # =========================================================================
    print("\n[2] Aggregating Bowling Data & Running Match-Clustered Bootstrap...")

    bowl_career = df[df["is_legal_bowl"]].groupby("bowler_id").agg(
        career_b=("is_legal_bowl", "sum"),
        career_runs=("bowl_runs_obs", "sum"),
        career_exp_runs=("exp_bowl_runs", "sum"),
        career_rpae=("rpae", "sum"),
        career_wkts=("is_bowler_wicket", "sum"),
        career_exp_wkts=("exp_bowl_wkt", "sum"),
        career_wae=("wae", "sum")
    ).reset_index()

    bowl_pressure = df[df["is_hp_bowl"]].groupby("bowler_id").agg(
        pressure_b=("is_legal_bowl", "sum"),
        pressure_runs=("bowl_runs_obs", "sum"),
        pressure_exp_runs=("exp_bowl_runs", "sum"),
        pressure_rpae=("rpae", "sum"),
        pressure_wkts=("is_bowler_wicket", "sum"),
        pressure_exp_wkts=("exp_bowl_wkt", "sum"),
        pressure_wae=("wae", "sum")
    ).reset_index()

    bowl_np = df[df["is_legal_bowl"] & (~df["is_hp_bowl"])].groupby("bowler_id").agg(
        np_b=("is_legal_bowl", "sum"),
        np_runs=("bowl_runs_obs", "sum"),
        np_rpae=("rpae", "sum")
    ).reset_index()

    bowl_all = bowl_career.merge(bowl_pressure, on="bowler_id", how="left").fillna(0)
    bowl_all = bowl_all.merge(bowl_np, on="bowler_id", how="left").fillna(0)

    # Eligibility filter: career_b >= 300 and pressure_b >= 40
    bowl_qual = bowl_all[(bowl_all["career_b"] >= 300) & (bowl_all["pressure_b"] >= 40)].copy()
    print(f"  Qualified Bowlers (career >= 300 & pressure >= 40): {len(bowl_qual)}")

    M0_BOWL = 150.0
    M0_WKT = 100.0
    W_EQUIV = 12.0

    bowl_qual["career_econ"] = ((bowl_qual["career_runs"] / bowl_qual["career_b"]) * 6.0).round(2)
    bowl_qual["career_exp_econ"] = ((bowl_qual["career_exp_runs"] / bowl_qual["career_b"]) * 6.0).round(2)
    bowl_qual["career_rpae_rate"] = ((bowl_qual["career_rpae"] / bowl_qual["career_b"]) * 100.0).round(2)

    bowl_qual["pressure_econ"] = ((bowl_qual["pressure_runs"] / bowl_qual["pressure_b"]) * 6.0).round(2)
    bowl_qual["pressure_exp_econ"] = ((bowl_qual["pressure_exp_runs"] / bowl_qual["pressure_b"]) * 6.0).round(2)
    bowl_qual["raw_pressure_rpae_rate"] = ((bowl_qual["pressure_rpae"] / bowl_qual["pressure_b"]) * 100.0).round(2)

    bowl_qual["non_pressure_econ"] = np.where(bowl_qual["np_b"] > 0, ((bowl_qual["np_runs"] / bowl_qual["np_b"]) * 6.0).round(2), np.nan)
    bowl_qual["non_pressure_rpae_rate"] = np.where(bowl_qual["np_b"] > 0, ((bowl_qual["np_rpae"] / bowl_qual["np_b"]) * 100.0).round(2), np.nan)
    bowl_qual["clutch_rpae_lift"] = (bowl_qual["raw_pressure_rpae_rate"] - bowl_qual["non_pressure_rpae_rate"]).round(2)

    # Scoring components
    bowl_qual["shrunk_rpae_score"] = ((bowl_qual["pressure_rpae"] / (bowl_qual["pressure_b"] + M0_BOWL)) * 100.0).round(2)
    bowl_qual["shrunk_wae_rate"] = ((bowl_qual["pressure_wae"] / (bowl_qual["pressure_b"] + M0_WKT)) * 100.0).round(3)
    bowl_qual["wae_run_equivalent"] = (bowl_qual["shrunk_wae_rate"] * W_EQUIV).round(2)
    bowl_qual["composite_score"] = (0.60 * bowl_qual["shrunk_rpae_score"] + 0.40 * bowl_qual["wae_run_equivalent"]).round(2)
    bowl_qual["sample_size_badge"] = bowl_qual["pressure_b"].apply(get_badge)
    bowl_qual["player_name"] = bowl_qual["bowler_id"].map(p_names).fillna("Unknown")
    bowl_qual["franchises"] = bowl_qual["bowler_id"].map(p_teams).fillna("Unknown")

    # Match-clustered bootstrap for bowlers (500 replicates)
    bowl_p_df = df[df["is_hp_bowl"]].groupby(["match_id", "bowler_id"]).agg(
        n_b=("is_legal_bowl", "sum"),
        sum_rpae=("rpae", "sum"),
        sum_wae=("wae", "sum")
    ).reset_index()

    m_to_bowl = {m: g for m, g in bowl_p_df.groupby("match_id")}
    qual_bowl_pids = bowl_qual["bowler_id"].tolist()
    pid_to_i_w = {p: i for i, p in enumerate(qual_bowl_pids)}
    n_p_w = len(qual_bowl_pids)

    cnt_mat_w = np.zeros((n_matches, n_p_w))
    sum_rpae_mat_w = np.zeros((n_matches, n_p_w))
    sum_wae_mat_w = np.zeros((n_matches, n_p_w))
    for mi, m in enumerate(match_list):
        if m in m_to_bowl:
            for _, r in m_to_bowl[m].iterrows():
                pid = r["bowler_id"]
                if pid in pid_to_i_w:
                    pi = pid_to_i_w[pid]
                    cnt_mat_w[mi, pi] = r["n_b"]
                    sum_rpae_mat_w[mi, pi] = r["sum_rpae"]
                    sum_wae_mat_w[mi, pi] = r["sum_wae"]

    boot_scores_pure_bowl = np.zeros((n_boot, n_p_w))
    boot_ranks_pure_bowl = np.zeros((n_boot, n_p_w))

    boot_scores_comp_bowl = np.zeros((n_boot, n_p_w))
    boot_ranks_comp_bowl = np.zeros((n_boot, n_p_w))

    for b in range(n_boot):
        sample_indices = rng.integers(0, n_matches, size=n_matches)
        b_cnt = cnt_mat_w[sample_indices].sum(axis=0)
        b_rpae = sum_rpae_mat_w[sample_indices].sum(axis=0)
        b_wae = sum_wae_mat_w[sample_indices].sum(axis=0)

        sc_rpae = (b_rpae / (b_cnt + M0_BOWL)) * 100.0
        sc_comp = 0.60 * sc_rpae + 0.40 * (b_wae / (b_cnt + M0_WKT) * 100.0) * W_EQUIV

        boot_scores_pure_bowl[b] = sc_rpae
        boot_ranks_pure_bowl[b] = np.argsort(np.argsort(-sc_rpae)) + 1

        boot_scores_comp_bowl[b] = sc_comp
        boot_ranks_comp_bowl[b] = np.argsort(np.argsort(-sc_comp)) + 1

    # Populate Pure RPAE table
    bowl_pure = bowl_qual.copy()
    b_means_pure = np.mean(boot_scores_pure_bowl, axis=0).round(2)
    b_ses_pure = np.std(boot_scores_pure_bowl, axis=0).round(2)
    ci_lows_pure = np.percentile(boot_scores_pure_bowl, 2.5, axis=0).round(2)
    ci_highs_pure = np.percentile(boot_scores_pure_bowl, 97.5, axis=0).round(2)
    rk_lows_pure = np.percentile(boot_ranks_pure_bowl, 5, axis=0).astype(int)
    rk_highs_pure = np.percentile(boot_ranks_pure_bowl, 95, axis=0).astype(int)
    top10_probs_pure = (100.0 * (boot_ranks_pure_bowl <= 10).mean(axis=0)).round(1)

    bowl_pure["bootstrap_mean"] = [b_means_pure[pid_to_i_w[p]] for p in bowl_pure["bowler_id"]]
    bowl_pure["bootstrap_se"] = [b_ses_pure[pid_to_i_w[p]] for p in bowl_pure["bowler_id"]]
    bowl_pure["ci95_lower"] = [ci_lows_pure[pid_to_i_w[p]] for p in bowl_pure["bowler_id"]]
    bowl_pure["ci95_upper"] = [ci_highs_pure[pid_to_i_w[p]] for p in bowl_pure["bowler_id"]]
    bowl_pure["rank_ci_90"] = [f"#{rk_lows_pure[pid_to_i_w[p]]} to #{rk_highs_pure[pid_to_i_w[p]]}" for p in bowl_pure["bowler_id"]]
    bowl_pure["top10_prob_pct"] = [top10_probs_pure[pid_to_i_w[p]] for p in bowl_pure["bowler_id"]]

    bowl_pure = bowl_pure.sort_values("shrunk_rpae_score", ascending=False).reset_index(drop=True)
    bowl_pure.index += 1
    bowl_pure["rank_rpae"] = bowl_pure.index

    cols_bowl_pure = [
        "rank_rpae", "player_id", "player_name", "franchises",
        "career_b", "career_econ", "career_exp_econ", "career_rpae_rate",
        "pressure_b", "pressure_runs", "pressure_exp_runs", "pressure_econ", "pressure_exp_econ",
        "pressure_rpae", "raw_pressure_rpae_rate", "non_pressure_econ", "non_pressure_rpae_rate",
        "clutch_rpae_lift", "shrunk_rpae_score", "bootstrap_mean", "bootstrap_se",
        "ci95_lower", "ci95_upper", "rank_ci_90", "top10_prob_pct", "sample_size_badge"
    ]
    bowl_pure_final = bowl_pure.rename(columns={"bowler_id": "player_id"})[cols_bowl_pure]
    bowl_pure_final.to_csv(os.path.join(STEP4_DIR, "FINAL_BOWLER_RANKINGS_RAE.csv"), index=False)
    print(f"  Saved FINAL_BOWLER_RANKINGS_RAE.csv ({len(bowl_pure_final)} qualified bowlers).")

    # Populate Composite table
    bowl_comp = bowl_qual.copy()
    b_means_comp = np.mean(boot_scores_comp_bowl, axis=0).round(2)
    b_ses_comp = np.std(boot_scores_comp_bowl, axis=0).round(2)
    ci_lows_comp = np.percentile(boot_scores_comp_bowl, 2.5, axis=0).round(2)
    ci_highs_comp = np.percentile(boot_scores_comp_bowl, 97.5, axis=0).round(2)
    rk_lows_comp = np.percentile(boot_ranks_comp_bowl, 5, axis=0).astype(int)
    rk_highs_comp = np.percentile(boot_ranks_comp_bowl, 95, axis=0).astype(int)
    top10_probs_comp = (100.0 * (boot_ranks_comp_bowl <= 10).mean(axis=0)).round(1)

    bowl_comp["bootstrap_mean"] = [b_means_comp[pid_to_i_w[p]] for p in bowl_comp["bowler_id"]]
    bowl_comp["bootstrap_se"] = [b_ses_comp[pid_to_i_w[p]] for p in bowl_comp["bowler_id"]]
    bowl_comp["ci95_lower"] = [ci_lows_comp[pid_to_i_w[p]] for p in bowl_comp["bowler_id"]]
    bowl_comp["ci95_upper"] = [ci_highs_comp[pid_to_i_w[p]] for p in bowl_comp["bowler_id"]]
    bowl_comp["rank_ci_90"] = [f"#{rk_lows_comp[pid_to_i_w[p]]} to #{rk_highs_comp[pid_to_i_w[p]]}" for p in bowl_comp["bowler_id"]]
    bowl_comp["top10_prob_pct"] = [top10_probs_comp[pid_to_i_w[p]] for p in bowl_comp["bowler_id"]]

    # Map rank_pure_rpae to composite table
    pure_rank_map = dict(zip(bowl_pure["bowler_id"], bowl_pure["rank_rpae"]))
    bowl_comp["rank_pure_rpae"] = bowl_comp["bowler_id"].map(pure_rank_map)

    bowl_comp = bowl_comp.sort_values("composite_score", ascending=False).reset_index(drop=True)
    bowl_comp.index += 1
    bowl_comp["rank_composite"] = bowl_comp.index
    bowl_comp["rank_shift_vs_rpae"] = bowl_comp["rank_pure_rpae"] - bowl_comp["rank_composite"]

    cols_bowl_comp = [
        "rank_composite", "rank_pure_rpae", "rank_shift_vs_rpae", "player_id", "player_name", "franchises",
        "career_b", "pressure_b", "pressure_rpae", "shrunk_rpae_score",
        "pressure_wkts", "pressure_exp_wkts", "pressure_wae", "shrunk_wae_rate",
        "wae_run_equivalent", "composite_score", "bootstrap_mean", "bootstrap_se",
        "ci95_lower", "ci95_upper", "rank_ci_90", "top10_prob_pct", "sample_size_badge"
    ]
    bowl_comp_final = bowl_comp.rename(columns={"bowler_id": "player_id"})[cols_bowl_comp]
    bowl_comp_final.to_csv(os.path.join(STEP4_DIR, "FINAL_BOWLER_RANKINGS_COMPOSITE.csv"), index=False)
    print(f"  Saved FINAL_BOWLER_RANKINGS_COMPOSITE.csv ({len(bowl_comp_final)} qualified bowlers).")

    print("\nAll 3 ranking CSV files successfully generated and reconciled!")


if __name__ == "__main__":
    main()
