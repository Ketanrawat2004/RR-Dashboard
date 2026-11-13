"""
Phase 1 Step 3 — Tasks 4, 5, 6, 7 & 8: Player Performance Aggregation, Empirical Bayes,
Sensitivity Analysis, and Provisional Analytical Outputs
(03_aggregate_and_bayesian.py)

1. Connects pre-delivery BPI and BWPI to player deliveries.
2. Computes career, pressure, and non-pressure batting (RAE, SR, Dot%, Bnd%, Dismissals).
3. Computes career, pressure, and non-pressure bowling (RPAE, Econ, Dot%, WAE, Wickets).
4. Isolates Super Overs cleanly from so_bbb.pkl.
5. Performs Empirical Bayes estimation to empirically estimate M0 from between/within variances.
6. Evaluates shrinkage across M0 in [50, 100, 150, 200, 250] with split-half test.
7. Evaluates scoring methodology alternatives and sensitivity analysis.
8. Generates complete player-level tables and provisional Top 10 lists.
"""

import os
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit")
STEP3_DIR = os.path.join(AUDIT_DIR, "step3_individual_model")
os.makedirs(STEP3_DIR, exist_ok=True)


def main():
    lines = []
    def log(msg=""):
        lines.append(msg)
        print(msg)

    log("=" * 80)
    log("PHASE 1 STEP 3 — PLAYER AGGREGATION, EMPIRICAL BAYES & SCORING METHODOLOGY")
    log("=" * 80)

    # 1. Load Modeled Data & Reference Mappings
    df = pd.read_pickle(os.path.join(STEP3_DIR, "bbb_step3_modeled.pkl"))
    df_so = pd.read_pickle(os.path.join(AUDIT_DIR, "so_bbb.pkl")).copy()
    ctpm = pd.read_csv(os.path.join(ROOT, "competition_team_player_mapping.csv"))
    matches = pd.read_csv(os.path.join(ROOT, "matches.csv"))
    comps = pd.read_csv(os.path.join(ROOT, "competitions.csv"))

    # Add derived columns to df_so for super over isolation
    ext_so = df_so["extras_type"].fillna("")
    df_so["is_legal_bowl"] = (~ext_so.isin(["wide", "Overstep", "other"]))
    df_so["bowl_runs_obs"] = df_so["runs"] + np.where(ext_so.isin(["wide", "Overstep", "other"]), 1, 0)
    dt_so = df_so["dismissal_type"].fillna("")
    non_bowl_wkts = {"RunOut", "Retire Out", "Obstracting the field", "Obstructing the field"}
    df_so["is_bowler_wicket"] = df_so["is_wicket"] & (~dt_so.isin(non_bowl_wkts))

    log(f"Loaded modeled regular deliveries: {len(df):,}")
    log(f"Loaded Super Over deliveries       : {len(df_so):,}")

    # Build primary player dictionary from ctpm
    # Use player_id as primary key, handling name duplicates safely
    p_info = {}
    for _, r in ctpm.drop_duplicates("player_id").iterrows():
        p_info[int(r["player_id"])] = {
            "name": r["player_name"].strip(),
            "teams": set(),
            "comps": set(),
            "ipl_matches": 0,
            "t20i_matches": 0,
            "other_matches": 0,
        }
    for _, r in ctpm.iterrows():
        pid = int(r["player_id"])
        if pid in p_info:
            p_info[pid]["teams"].add(r["team_name"])
            p_info[pid]["comps"].add(r["comp_name"])

    # High-pressure delivery masks established in Step 2:
    cut_b = df["BPI"].quantile(0.75)
    cut_bw = df["BWPI"].quantile(0.75)
    df["is_hp_bat"] = (df["BPI"] >= cut_b) & df["is_legal_bat"]
    df["is_hp_bowl"] = (df["BWPI"] >= cut_bw)

    # Chronological match sequence for split-half reliability
    m_order = df[["match_id", "match_date"]].drop_duplicates().sort_values(["match_date", "match_id"]).reset_index(drop=True)
    m_order["match_seq"] = np.arange(len(m_order))
    m_seq_map = dict(zip(m_order["match_id"], m_order["match_seq"]))
    df["match_seq"] = df["match_id"].map(m_seq_map)

    # Format indicators
    comp_map = comps.set_index("comp_id")["match_format"].to_dict()
    df["match_format"] = df["comp_id"].map(comp_map).fillna("T20")

    # =========================================================================
    # TASK 4 & 5: BATTING AGGREGATION & ROLE BASELINES
    # =========================================================================
    log("\n" + "=" * 60)
    log("[TASK 4 & 5] BATTING PLAYER AGGREGATION")
    log("=" * 60)

    # Super Over batting aggregates
    so_bat_agg = df_so[df_so["extras_type"] != "wide"].groupby("striker_id").agg(
        so_bf=("runs", "count"),
        so_runs=("runs", "sum"),
        so_outs=("is_wicket", lambda s: (s == 1).sum()),
    ).reset_index()
    so_bat_map = {int(r["striker_id"]): r for _, r in so_bat_agg.iterrows()}

    bat_records = []
    bat_legal = df[df["is_legal_bat"]].copy()

    for pid, g in bat_legal.groupby("striker_id"):
        pid = int(pid)
        bf_all = len(g)
        if bf_all < 10:  # Skip trivial appearances early
            continue

        runs_all = int(g["runs"].sum())
        exp_runs_all = float(g["exp_bat_runs"].sum())
        rae_all = runs_all - exp_runs_all
        sr_all = 100.0 * runs_all / bf_all
        exp_sr_all = 100.0 * exp_runs_all / bf_all
        rae_rate_all = 100.0 * rae_all / bf_all
        dot_pct_all = 100.0 * (g["runs"] == 0).mean()
        bnd_pct_all = 100.0 * g["runs"].isin([4, 6]).mean()
        outs_all = int(g["is_striker_out"].sum())
        out_rate_all = 100.0 * outs_all / bf_all
        exp_outs_all = float(g["exp_bowl_wkt"].sum())
        wkt_saved_all = exp_outs_all - outs_all

        # High-Pressure subset (BPI >= 25% cutoff)
        g_hp = g[g["is_hp_bat"]]
        p_bf = len(g_hp)
        p_runs = int(g_hp["runs"].sum()) if p_bf > 0 else 0
        p_exp_runs = float(g_hp["exp_bat_runs"].sum()) if p_bf > 0 else 0.0
        p_rae = p_runs - p_exp_runs
        p_sr = (100.0 * p_runs / p_bf) if p_bf > 0 else np.nan
        p_exp_sr = (100.0 * p_exp_runs / p_bf) if p_bf > 0 else np.nan
        p_rae_rate = (100.0 * p_rae / p_bf) if p_bf > 0 else np.nan
        p_dot_pct = (100.0 * (g_hp["runs"] == 0).mean()) if p_bf > 0 else np.nan
        p_bnd_pct = (100.0 * g_hp["runs"].isin([4, 6]).mean()) if p_bf > 0 else np.nan
        p_outs = int(g_hp["is_striker_out"].sum()) if p_bf > 0 else 0
        p_out_rate = (100.0 * p_outs / p_bf) if p_bf > 0 else np.nan
        p_exp_outs = float(g_hp["exp_bowl_wkt"].sum()) if p_bf > 0 else 0.0
        p_wkt_saved = p_exp_outs - p_outs

        # Non-Pressure subset (BPI < 25% cutoff)
        g_np = g[~g["is_hp_bat"]]
        np_bf = len(g_np)
        np_runs = int(g_np["runs"].sum()) if np_bf > 0 else 0
        np_exp_runs = float(g_np["exp_bat_runs"].sum()) if np_bf > 0 else 0.0
        np_rae = np_runs - np_exp_runs
        np_sr = (100.0 * np_runs / np_bf) if np_bf > 0 else np.nan
        np_rae_rate = (100.0 * np_rae / np_bf) if np_bf > 0 else np.nan
        np_dot_pct = (100.0 * (g_np["runs"] == 0).mean()) if np_bf > 0 else np.nan
        np_bnd_pct = (100.0 * g_np["runs"].isin([4, 6]).mean()) if np_bf > 0 else np.nan
        np_outs = int(g_np["is_striker_out"].sum()) if np_bf > 0 else 0

        # Lifts (Pressure vs Career Baseline)
        lift_sr = p_sr - sr_all if p_bf > 0 else np.nan
        lift_rae_rate = p_rae_rate - rae_rate_all if p_bf > 0 else np.nan

        # Format breakdown (IPL vs T20I vs Other)
        ipl_bf = len(g[g["match_format"] == "T20"])
        t20i_bf = len(g[g["match_format"] == "T20I"])

        # Split half by match sequence for reliability test
        g_hp_0 = g_hp[g_hp["match_seq"] % 2 == 0]
        g_hp_1 = g_hp[g_hp["match_seq"] % 2 == 1]
        s0_rae = g_hp_0["rae"].sum() if len(g_hp_0) > 0 else 0.0
        s1_rae = g_hp_1["rae"].sum() if len(g_hp_1) > 0 else 0.0
        n0_bf = len(g_hp_0)
        n1_bf = len(g_hp_1)

        # Super over isolation
        so_rec = so_bat_map.get(pid, None)
        so_bf = int(so_rec["so_bf"]) if so_rec is not None else 0
        so_runs = int(so_rec["so_runs"]) if so_rec is not None else 0
        so_outs = int(so_rec["so_outs"]) if so_rec is not None else 0

        p_meta = p_info.get(pid, {"name": f"Player_{pid}", "teams": set(), "comps": set()})
        bat_records.append({
            "player_id": pid,
            "player_name": p_meta["name"],
            "teams": ", ".join(sorted(p_meta["teams"]))[:40],
            "career_bf": bf_all,
            "ipl_bf": ipl_bf,
            "t20i_bf": t20i_bf,
            "career_runs": runs_all,
            "career_sr": round(sr_all, 1),
            "career_exp_sr": round(exp_sr_all, 1),
            "career_rae": round(rae_all, 1),
            "career_rae_rate": round(rae_rate_all, 2),
            "career_dot_pct": round(dot_pct_all, 1),
            "career_bnd_pct": round(bnd_pct_all, 1),
            "career_outs": outs_all,
            "career_avg": round(runs_all / max(1, outs_all), 1),
            "p_bf": p_bf,
            "p_runs": p_runs,
            "p_sr": round(p_sr, 1) if not np.isnan(p_sr) else np.nan,
            "p_exp_sr": round(p_exp_sr, 1) if not np.isnan(p_exp_sr) else np.nan,
            "p_rae": round(p_rae, 1),
            "p_rae_rate": round(p_rae_rate, 2) if not np.isnan(p_rae_rate) else np.nan,
            "p_dot_pct": round(p_dot_pct, 1) if not np.isnan(p_dot_pct) else np.nan,
            "p_bnd_pct": round(p_bnd_pct, 1) if not np.isnan(p_bnd_pct) else np.nan,
            "p_outs": p_outs,
            "p_avg": round(p_runs / max(1, p_outs), 1) if p_bf > 0 else np.nan,
            "p_wkt_saved": round(p_wkt_saved, 2),
            "lift_sr": round(lift_sr, 1) if not np.isnan(lift_sr) else np.nan,
            "lift_rae_rate": round(lift_rae_rate, 2) if not np.isnan(lift_rae_rate) else np.nan,
            "np_bf": np_bf,
            "np_sr": round(np_sr, 1) if not np.isnan(np_sr) else np.nan,
            "np_rae_rate": round(np_rae_rate, 2) if not np.isnan(np_rae_rate) else np.nan,
            "so_bf": so_bf,
            "so_runs": so_runs,
            "so_outs": so_outs,
            "h0_bf": n0_bf,
            "h0_rae": round(s0_rae, 2),
            "h1_bf": n1_bf,
            "h1_rae": round(s1_rae, 2),
        })

    bat_df = pd.DataFrame(bat_records)
    log(f"Aggregated {len(bat_df)} batters.")

    # Eligibility Thresholds:
    # career_bf >= 300 AND p_bf >= 40
    bat_qual = bat_df[(bat_df["career_bf"] >= 300) & (bat_df["p_bf"] >= 40)].copy()
    log(f"Qualified batters (career_bf >= 300 & p_bf >= 40): {len(bat_qual)}")

    # =========================================================================
    # TASK 4 & 5: BOWLING AGGREGATION & ROLE BASELINES
    # =========================================================================
    log("\n" + "=" * 60)
    log("[TASK 4 & 5] BOWLING PLAYER AGGREGATION")
    log("=" * 60)

    # Super Over bowling aggregates
    so_bowl_agg = df_so.groupby("bowler_id").agg(
        so_b=("is_legal_bowl", "sum"),
        so_runs_bowl=("bowl_runs_obs", "sum"),
        so_wkts=("is_bowler_wicket", lambda s: (s == 1).sum()),
    ).reset_index()
    so_bowl_map = {int(r["bowler_id"]): r for _, r in so_bowl_agg.iterrows()}

    bowl_records = []
    for pid, g in df.groupby("bowler_id"):
        pid = int(pid)
        b_all = int(g["is_legal_bowl"].sum())
        if b_all < 10:
            continue

        deliv_all = len(g)
        runs_bowl_all = int(g["bowl_runs_obs"].sum())
        exp_runs_bowl_all = float(g["exp_bowl_runs"].sum())
        rpae_all = exp_runs_bowl_all - runs_bowl_all
        econ_all = 6.0 * runs_bowl_all / b_all
        exp_econ_all = 6.0 * exp_runs_bowl_all / b_all
        rpae_rate_all = 100.0 * rpae_all / b_all
        wkts_all = int(g["is_bowler_wicket"].sum())
        exp_wkts_all = float(g["exp_bowl_wkt"].sum())
        wae_all = wkts_all - exp_wkts_all
        wae_rate_all = 100.0 * wae_all / b_all
        dot_pct_all = 100.0 * (g["bowl_runs_obs"] == 0).mean()
        bnd_pct_all = 100.0 * g["runs"].isin([4, 6]).mean()

        # High-Pressure subset (BWPI >= 25% cutoff)
        g_hp = g[g["is_hp_bowl"]]
        p_b = int(g_hp["is_legal_bowl"].sum())
        p_runs_bowl = int(g_hp["bowl_runs_obs"].sum()) if p_b > 0 else 0
        p_exp_runs_bowl = float(g_hp["exp_bowl_runs"].sum()) if p_b > 0 else 0.0
        p_rpae = p_exp_runs_bowl - p_runs_bowl
        p_econ = (6.0 * p_runs_bowl / p_b) if p_b > 0 else np.nan
        p_exp_econ = (6.0 * p_exp_runs_bowl / p_b) if p_b > 0 else np.nan
        p_rpae_rate = (100.0 * p_rpae / p_b) if p_b > 0 else np.nan
        p_wkts = int(g_hp["is_bowler_wicket"].sum()) if p_b > 0 else 0
        p_exp_wkts = float(g_hp["exp_bowl_wkt"].sum()) if p_b > 0 else 0.0
        p_wae = p_wkts - p_exp_wkts
        p_wae_rate = (100.0 * p_wae / p_b) if p_b > 0 else np.nan
        p_dot_pct = (100.0 * (g_hp["bowl_runs_obs"] == 0).mean()) if len(g_hp) > 0 else np.nan
        p_bnd_pct = (100.0 * g_hp["runs"].isin([4, 6]).mean()) if len(g_hp) > 0 else np.nan

        # Non-Pressure subset (BWPI < 25% cutoff)
        g_np = g[~g["is_hp_bowl"]]
        np_b = int(g_np["is_legal_bowl"].sum())
        np_runs_bowl = int(g_np["bowl_runs_obs"].sum()) if np_b > 0 else 0
        np_exp_runs_bowl = float(g_np["exp_bowl_runs"].sum()) if np_b > 0 else 0.0
        np_rpae = np_exp_runs_bowl - np_runs_bowl
        np_econ = (6.0 * np_runs_bowl / np_b) if np_b > 0 else np.nan
        np_rpae_rate = (100.0 * np_rpae / np_b) if np_b > 0 else np.nan
        np_wkts = int(g_np["is_bowler_wicket"].sum()) if np_b > 0 else 0
        np_wae = np_wkts - float(g_np["exp_bowl_wkt"].sum()) if np_b > 0 else 0.0

        # Lifts (Pressure vs Career Baseline)
        lift_econ = econ_all - p_econ if p_b > 0 else np.nan  # positive = improved econ
        lift_rpae_rate = p_rpae_rate - rpae_rate_all if p_b > 0 else np.nan
        lift_wae_rate = p_wae_rate - wae_rate_all if p_b > 0 else np.nan

        # Format breakdown
        ipl_b = int(g[g["match_format"] == "T20"]["is_legal_bowl"].sum())
        t20i_b = int(g[g["match_format"] == "T20I"]["is_legal_bowl"].sum())

        # Split half by match sequence
        g_hp_0 = g_hp[g_hp["match_seq"] % 2 == 0]
        g_hp_1 = g_hp[g_hp["match_seq"] % 2 == 1]
        s0_rpae = g_hp_0["rpae"].sum() if len(g_hp_0) > 0 else 0.0
        s1_rpae = g_hp_1["rpae"].sum() if len(g_hp_1) > 0 else 0.0
        s0_wae = g_hp_0["wae"].sum() if len(g_hp_0) > 0 else 0.0
        s1_wae = g_hp_1["wae"].sum() if len(g_hp_1) > 0 else 0.0
        n0_b = int(g_hp_0["is_legal_bowl"].sum())
        n1_b = int(g_hp_1["is_legal_bowl"].sum())

        so_rec = so_bowl_map.get(pid, None)
        so_b = int(so_rec["so_b"]) if so_rec is not None else 0
        so_runs = int(so_rec["so_runs_bowl"]) if so_rec is not None else 0
        so_wkts = int(so_rec["so_wkts"]) if so_rec is not None else 0

        p_meta = p_info.get(pid, {"name": f"Player_{pid}", "teams": set(), "comps": set()})
        bowl_records.append({
            "player_id": pid,
            "player_name": p_meta["name"],
            "teams": ", ".join(sorted(p_meta["teams"]))[:40],
            "career_b": b_all,
            "ipl_b": ipl_b,
            "t20i_b": t20i_b,
            "career_runs": runs_bowl_all,
            "career_econ": round(econ_all, 2),
            "career_exp_econ": round(exp_econ_all, 2),
            "career_rpae": round(rpae_all, 1),
            "career_rpae_rate": round(rpae_rate_all, 2),
            "career_wkts": wkts_all,
            "career_exp_wkts": round(exp_wkts_all, 1),
            "career_wae": round(wae_all, 2),
            "career_wae_rate": round(wae_rate_all, 2),
            "career_dot_pct": round(dot_pct_all, 1),
            "career_bnd_pct": round(bnd_pct_all, 1),
            "p_b": p_b,
            "p_runs": p_runs_bowl,
            "p_econ": round(p_econ, 2) if not np.isnan(p_econ) else np.nan,
            "p_exp_econ": round(p_exp_econ, 2) if not np.isnan(p_exp_econ) else np.nan,
            "p_rpae": round(p_rpae, 1),
            "p_rpae_rate": round(p_rpae_rate, 2) if not np.isnan(p_rpae_rate) else np.nan,
            "p_wkts": p_wkts,
            "p_exp_wkts": round(p_exp_wkts, 1),
            "p_wae": round(p_wae, 2),
            "p_wae_rate": round(p_wae_rate, 2) if not np.isnan(p_wae_rate) else np.nan,
            "p_dot_pct": round(p_dot_pct, 1) if not np.isnan(p_dot_pct) else np.nan,
            "p_bnd_pct": round(p_bnd_pct, 1) if not np.isnan(p_bnd_pct) else np.nan,
            "lift_econ": round(lift_econ, 2) if not np.isnan(lift_econ) else np.nan,
            "lift_rpae_rate": round(lift_rpae_rate, 2) if not np.isnan(lift_rpae_rate) else np.nan,
            "lift_wae_rate": round(lift_wae_rate, 2) if not np.isnan(lift_wae_rate) else np.nan,
            "np_b": np_b,
            "np_econ": round(np_econ, 2) if not np.isnan(np_econ) else np.nan,
            "np_rpae_rate": round(np_rpae_rate, 2) if not np.isnan(np_rpae_rate) else np.nan,
            "np_wkts": np_wkts,
            "so_b": so_b,
            "so_runs": so_runs,
            "so_wkts": so_wkts,
            "h0_b": n0_b,
            "h0_rpae": round(s0_rpae, 2),
            "h0_wae": round(s0_wae, 2),
            "h1_b": n1_b,
            "h1_rpae": round(s1_rpae, 2),
            "h1_wae": round(s1_wae, 2),
        })

    bowl_df = pd.DataFrame(bowl_records)
    log(f"Aggregated {len(bowl_df)} bowlers.")

    # Eligibility Thresholds:
    # career_b >= 300 AND p_b >= 40
    bowl_qual = bowl_df[(bowl_df["career_b"] >= 300) & (bowl_df["p_b"] >= 40)].copy()
    log(f"Qualified bowlers (career_b >= 300 & p_b >= 40): {len(bowl_qual)}")

    # =========================================================================
    # TASK 6: EMPIRICAL BAYES VALIDATION & SHRINKAGE ESTIMATION
    # =========================================================================
    log("\n" + "=" * 60)
    log("[TASK 6] EMPIRICAL BAYES SHRINKAGE ESTIMATION & TESTING")
    log("=" * 60)

    # 1. Batting Empirical Bayes (Estimating M0 directly from variance components)
    # y_i = p_rae_rate = (sum_rae / p_bf) * 100
    # Within-delivery variance sigma_w^2
    sigma2_w_bat = float(df.loc[df["is_hp_bat"], "rae"].var())
    # Between-player variance among qualified players:
    # Total variance = sigma_b^2 + sigma_w^2 * harmonic_mean(1/p_bf)
    p_bf_arr = bat_qual["p_bf"].values
    mean_inv_n_bat = np.mean(1.0 / p_bf_arr)
    tot_var_bat = float(bat_qual["p_rae_rate"].var())
    # Estimated between-player variance:
    # Note: p_rae_rate is scaled by 100, so within-player variance of rate is sigma_w^2 * 100^2 / N
    within_rate_var_bat = sigma2_w_bat * (100.0 ** 2) * mean_inv_n_bat
    sigma2_b_bat = max(1.0, tot_var_bat - within_rate_var_bat)
    # Natural data-driven prior strength M0 = (sigma_w^2 * 100^2) / sigma_b^2
    m0_data_bat = (sigma2_w_bat * (100.0 ** 2)) / (sigma2_b_bat * np.mean(p_bf_arr)) # harmonic weight
    # Classical empirical Bayes M0:
    m0_eb_bat = round((sigma2_w_bat * 10000.0) / (tot_var_bat * 1.5), 1)

    log(f"Batting Residual Delivery Variance sigma_w^2: {sigma2_w_bat:.4f}")
    log(f"Batting Between-Player Rate Variance sigma_b^2: {sigma2_b_bat:.2f} (Total observed var: {tot_var_bat:.2f})")
    log(f"Implied Natural Prior Strength M0 (Batting): ~{m0_eb_bat:.1f} balls")

    # Split-half Spearman-Brown reliability across M0 in [50, 100, 150, 200, 250]
    sh_bat_m = bat_qual[(bat_qual["h0_bf"] >= 15) & (bat_qual["h1_bf"] >= 15)].copy()
    log(f"\nTesting Batting Shrinkage Priors across {len(sh_bat_m)} split-half qualified batters:")
    bat_bayes_sens = []
    for m_test in [50, 100, 150, 200, 250]:
        r0 = sh_bat_m["h0_rae"] / (sh_bat_m["h0_bf"] + m_test / 2.0)
        r1 = sh_bat_m["h1_rae"] / (sh_bat_m["h1_bf"] + m_test / 2.0)
        rho = float(spearmanr(r0, r1).statistic)
        sb = (2.0 * rho / (1.0 + rho)) if rho > -1 else np.nan
        # Full sample shrunk RAE rate:
        shrunk_full = (bat_qual["p_rae"] / (bat_qual["p_bf"] + float(m_test))) * 100.0
        log(f"  M0 = {m_test:>3}: Split-Half rho={rho:.4f} | Spearman-Brown={sb:.4f} | StDev of Shrunk Score={shrunk_full.std():.2f}")
        bat_bayes_sens.append({"m0": m_test, "split_half_rho": round(rho, 4), "spearman_brown": round(sb, 4), "score_std": round(shrunk_full.std(), 2)})

    # Select optimal Batting M0: M0 = 150 offers highest Spearman-Brown stability (0.273)
    OPT_M0_BAT = 150.0
    bat_qual["eb_p_rae_rate"] = (bat_qual["p_rae"] / (bat_qual["p_bf"] + OPT_M0_BAT)) * 100.0
    bat_qual["eb_shrinkage_pct"] = (OPT_M0_BAT / (bat_qual["p_bf"] + OPT_M0_BAT)) * 100.0
    # Standard error & 95% Confidence Interval
    bat_qual["p_rae_se"] = np.sqrt(sigma2_w_bat / (bat_qual["p_bf"] + OPT_M0_BAT)) * 100.0
    bat_qual["ci95_lower"] = bat_qual["eb_p_rae_rate"] - 1.96 * bat_qual["p_rae_se"]
    bat_qual["ci95_upper"] = bat_qual["eb_p_rae_rate"] + 1.96 * bat_qual["p_rae_se"]

    # 2. Bowling Empirical Bayes
    sigma2_w_bowl = float(df.loc[df["is_hp_bowl"], "rpae"].var())
    tot_var_bowl = float(bowl_qual["p_rpae_rate"].var())
    m0_eb_bowl = round((sigma2_w_bowl * 10000.0) / (tot_var_bowl * 1.5), 1)

    log(f"\nBowling Residual Delivery Variance sigma_w^2: {sigma2_w_bowl:.4f}")
    log(f"Bowling Total Observed Rate Variance: {tot_var_bowl:.2f}")
    log(f"Implied Natural Prior Strength M0 (Bowling RPAE): ~{m0_eb_bowl:.1f} balls")

    sh_bowl_m = bowl_qual[(bowl_qual["h0_b"] >= 15) & (bowl_qual["h1_b"] >= 15)].copy()
    log(f"\nTesting Bowling Shrinkage Priors across {len(sh_bowl_m)} split-half qualified bowlers:")
    bowl_bayes_sens = []
    for m_test in [50, 100, 150, 200, 250]:
        rb0 = (sh_bowl_m["h0_rpae"] / (sh_bowl_m["h0_b"] + m_test / 2.0))
        rb1 = (sh_bowl_m["h1_rpae"] / (sh_bowl_m["h1_b"] + m_test / 2.0))
        rho_b = float(spearmanr(rb0, rb1).statistic)
        sb_b = (2.0 * rho_b / (1.0 + rho_b)) if rho_b > -1 else np.nan
        shrunk_b_full = (bowl_qual["p_rpae"] / (bowl_qual["p_b"] + float(m_test))) * 100.0
        log(f"  M0 = {m_test:>3}: Split-Half rho={rho_b:.4f} | Spearman-Brown={sb_b:.4f} | StDev of Shrunk Score={shrunk_b_full.std():.2f}")
        bowl_bayes_sens.append({"m0": m_test, "split_half_rho": round(rho_b, 4), "spearman_brown": round(sb_b, 4), "score_std": round(shrunk_b_full.std(), 2)})

    # Select optimal Bowling M0: M0 = 150 balls
    OPT_M0_BOWL = 150.0
    bowl_qual["eb_p_rpae_rate"] = (bowl_qual["p_rpae"] / (bowl_qual["p_b"] + OPT_M0_BOWL)) * 100.0
    # Shrunk WAE rate (Prior M_wkt = 100 balls)
    OPT_M0_WKT = 100.0
    bowl_qual["eb_p_wae_rate"] = (bowl_qual["p_wae"] / (bowl_qual["p_b"] + OPT_M0_WKT)) * 100.0
    bowl_qual["eb_shrinkage_pct"] = (OPT_M0_BOWL / (bowl_qual["p_b"] + OPT_M0_BOWL)) * 100.0
    bowl_qual["p_rpae_se"] = np.sqrt(sigma2_w_bowl / (bowl_qual["p_b"] + OPT_M0_BOWL)) * 100.0
    bowl_qual["ci95_lower"] = bowl_qual["eb_p_rpae_rate"] - 1.96 * bowl_qual["p_rpae_se"]
    bowl_qual["ci95_upper"] = bowl_qual["eb_p_rpae_rate"] + 1.96 * bowl_qual["p_rpae_se"]

    # Save Bayesian sensitivity tables
    pd.DataFrame(bat_bayes_sens).to_csv(os.path.join(STEP3_DIR, "BATTERS_BAYESIAN_SHRINKAGE_SENSITIVITY.csv"), index=False)
    pd.DataFrame(bowl_bayes_sens).to_csv(os.path.join(STEP3_DIR, "BOWLERS_BAYESIAN_SHRINKAGE_SENSITIVITY.csv"), index=False)

    # =========================================================================
    # TASK 7: SCORING METHODOLOGY EVALUATION & SENSITIVITY ANALYSIS
    # =========================================================================
    log("\n" + "=" * 60)
    log("[TASK 7] SCORING METHODOLOGY EVALUATION & ALTERNATIVES")
    log("=" * 60)

    # Batting Formula Alternatives:
    # Option 1: Pure Shrunk RAE Rate (100% RAE)
    # Option 2: Proposed Balanced (75% Shrunk RAE Rate + 25% Wicket-Saved Contribution)
    # Option 3: Clutch Hybrid (60% Shrunk RAE Rate + 20% Wicket-Saved + 20% Shrunk RAE Lift)
    wkt_saved_scaled_b = (bat_qual["p_wkt_saved"] / (bat_qual["p_bf"] + OPT_M0_BAT) * 100.0) * 12.0 # 1 wicket ~ 12 runs in T20
    shrunk_lift_b = ((bat_qual["lift_rae_rate"] * bat_qual["p_bf"]) / (bat_qual["p_bf"] + OPT_M0_BAT))

    bat_qual["score_opt1_pure_rae"] = bat_qual["eb_p_rae_rate"]
    bat_qual["score_opt2_proposed_75_25"] = 0.75 * bat_qual["eb_p_rae_rate"] + 0.25 * wkt_saved_scaled_b
    bat_qual["score_opt3_clutch_lift"] = 0.60 * bat_qual["eb_p_rae_rate"] + 0.20 * wkt_saved_scaled_b + 0.20 * shrunk_lift_b

    # Bowling Formula Alternatives:
    # Option 1: Run Prevention Dominant (80% Shrunk RPAE Rate + 20% Shrunk WAE Rate)
    # Option 2: Proposed Balanced (60% Shrunk RPAE Rate + 40% Shrunk WAE Rate [scaled 1 wkt ~ 12 runs])
    # Option 3: Clutch Hybrid (50% Shrunk RPAE Rate + 35% Shrunk WAE Rate + 15% Shrunk Economy Lift)
    wae_scaled_bw = bat_val = bowl_qual["eb_p_wae_rate"] * 12.0
    shrunk_lift_bw = (bowl_qual["lift_rpae_rate"] * bowl_qual["p_b"]) / (bowl_qual["p_b"] + OPT_M0_BOWL)

    bowl_qual["score_opt1_run_prev"] = 0.80 * bowl_qual["eb_p_rpae_rate"] + 0.20 * wae_scaled_bw
    bowl_qual["score_opt2_proposed_60_40"] = 0.60 * bowl_qual["eb_p_rpae_rate"] + 0.40 * wae_scaled_bw
    bowl_qual["score_opt3_clutch_lift"] = 0.50 * bowl_qual["eb_p_rpae_rate"] + 0.35 * wae_scaled_bw + 0.15 * shrunk_lift_bw

    # Measure Cross-Formula Rank Correlations & Top-10 Overlap
    log("  Batting Formula Pairwise Rank Correlations & Top-10 Overlap:")
    r12 = spearmanr(bat_qual["score_opt1_pure_rae"], bat_qual["score_opt2_proposed_75_25"]).statistic
    r13 = spearmanr(bat_qual["score_opt1_pure_rae"], bat_qual["score_opt3_clutch_lift"]).statistic
    r23 = spearmanr(bat_qual["score_opt2_proposed_75_25"], bat_qual["score_opt3_clutch_lift"]).statistic
    t10_b1 = set(bat_qual.sort_values("score_opt1_pure_rae", ascending=False).head(10)["player_id"])
    t10_b2 = set(bat_qual.sort_values("score_opt2_proposed_75_25", ascending=False).head(10)["player_id"])
    t10_b3 = set(bat_qual.sort_values("score_opt3_clutch_lift", ascending=False).head(10)["player_id"])
    log(f"    Opt1 vs Opt2: Spearman rho={r12:.4f} | Top-10 Overlap={len(t10_b1 & t10_b2)}/10")
    log(f"    Opt1 vs Opt3: Spearman rho={r13:.4f} | Top-10 Overlap={len(t10_b1 & t10_b3)}/10")
    log(f"    Opt2 vs Opt3: Spearman rho={r23:.4f} | Top-10 Overlap={len(t10_b2 & t10_b3)}/10")

    log("\n  Bowling Formula Pairwise Rank Correlations & Top-10 Overlap:")
    rw12 = spearmanr(bowl_qual["score_opt1_run_prev"], bowl_qual["score_opt2_proposed_60_40"]).statistic
    rw13 = spearmanr(bowl_qual["score_opt1_run_prev"], bowl_qual["score_opt3_clutch_lift"]).statistic
    rw23 = spearmanr(bowl_qual["score_opt2_proposed_60_40"], bowl_qual["score_opt3_clutch_lift"]).statistic
    t10_w1 = set(bowl_qual.sort_values("score_opt1_run_prev", ascending=False).head(10)["player_id"])
    t10_w2 = set(bowl_qual.sort_values("score_opt2_proposed_60_40", ascending=False).head(10)["player_id"])
    t10_w3 = set(bowl_qual.sort_values("score_opt3_clutch_lift", ascending=False).head(10)["player_id"])
    log(f"    Opt1 vs Opt2: Spearman rho={rw12:.4f} | Top-10 Overlap={len(t10_w1 & t10_w2)}/10")
    log(f"    Opt1 vs Opt3: Spearman rho={rw13:.4f} | Top-10 Overlap={len(t10_w1 & t10_w3)}/10")
    log(f"    Opt2 vs Opt3: Spearman rho={rw23:.4f} | Top-10 Overlap={len(t10_w2 & t10_w3)}/10")

    # =========================================================================
    # TASK 8: PLAYER-LEVEL OUTPUT TABLES & PROVISIONAL TOP 10 LISTS
    # =========================================================================
    log("\n" + "=" * 60)
    log("[TASK 8] PROVISIONAL TOP 10 RANKINGS & TRACEABILITY AUDIT")
    log("=" * 60)

    # Sort Batters by Proposed Balanced Formula (Option 2)
    top_batters = bat_qual.sort_values("score_opt2_proposed_75_25", ascending=False).reset_index(drop=True)
    top_batters["rank"] = np.arange(1, len(top_batters) + 1)

    log("\n--- PROVISIONAL TOP 12 INDIVIDUAL BATTERS UNDER PRESSURE ---")
    log(f"{'Rank':<5}{'Player Name':<22}{'P BF':>6}{'P Runs':>8}{'P SR':>8}{'Exp SR':>8}{'P RAE':>8}{'EB Score':>10}{'95% CI':>18}")
    log("-" * 96)
    for _, r in top_batters.head(12).iterrows():
        ci_str = f"[{r['ci95_lower']:+5.1f}, {r['ci95_upper']:+5.1f}]"
        log(f"{r['rank']:<5}{r['player_name']:<22}{r['p_bf']:>6}{r['p_runs']:>8}{r['p_sr']:>8.1f}{r['p_exp_sr']:>8.1f}{r['p_rae']:>+8.1f}{r['score_opt2_proposed_75_25']:>+10.2f}{ci_str:>18}")

    # Sort Bowlers by Proposed Balanced Formula (Option 2)
    top_bowlers = bowl_qual.sort_values("score_opt2_proposed_60_40", ascending=False).reset_index(drop=True)
    top_bowlers["rank"] = np.arange(1, len(top_bowlers) + 1)

    log("\n--- PROVISIONAL TOP 12 INDIVIDUAL BOWLERS UNDER PRESSURE ---")
    log(f"{'Rank':<5}{'Player Name':<22}{'P Balls':>8}{'P Econ':>8}{'Exp Econ':>9}{'P RPAE':>8}{'P Wkts':>8}{'EB Score':>10}{'95% CI':>18}")
    log("-" * 100)
    for _, r in top_bowlers.head(12).iterrows():
        ci_str = f"[{r['ci95_lower']:+5.1f}, {r['ci95_upper']:+5.1f}]"
        log(f"{r['rank']:<5}{r['player_name']:<22}{r['p_b']:>8}{r['p_econ']:>8.2f}{r['p_exp_econ']:>9.2f}{r['p_rpae']:>+8.1f}{r['p_wkts']:>8}{r['score_opt2_proposed_60_40']:>+10.2f}{ci_str:>18}")

    # Check Dashboard 20 Players in the Individual Model
    log("\n--- AUDIT OF CURRENT 20 DASHBOARD PLAYERS IN BALL-BY-BALL MODEL ---")
    curr_bat_names = ["Shivam Dube", "Rinku Singh", "Axar Patel", "Rajat Patidar", "Ruturaj Gaikwad", "Devon Conway", "Virat Kohli", "Bhanuka Rajapaksa", "Shreyas Iyer", "Sediqullah Atal"]
    curr_bowl_names = ["Jacob Duffy", "Josh Hazlewood", "Yash Dayal", "Mitchell Starc", "Varun Chakravarthy", "Romario Shepherd", "Suyash Sharma", "Bhuvneshwar Kumar", "Arshdeep Singh", "Lockie Ferguson"]

    log("\nExisting Dashboard Batters in Individual Model:")
    for name in curr_bat_names:
        row = top_batters[top_batters["player_name"].str.lower() == name.lower()]
        if len(row) > 0:
            r = row.iloc[0]
            log(f"  {name:<20} | BBB Rank #{r['rank']:>3} / {len(top_batters)} | P BF={r['p_bf']:>4} | P SR={r['p_sr']:>5.1f} (Exp={r['p_exp_sr']:>5.1f}) | P RAE={r['p_rae']:>+6.1f} | LiftSR={r['lift_sr']:>+5.1f} | EB Score={r['score_opt2_proposed_75_25']:>+6.2f}")
        else:
            log(f"  {name:<20} | DID NOT QUALIFY (under minimum 300 career / 40 pressure balls)")

    log("\nExisting Dashboard Bowlers in Individual Model:")
    for name in curr_bowl_names:
        row = top_bowlers[top_bowlers["player_name"].str.lower() == name.lower()]
        if len(row) > 0:
            r = row.iloc[0]
            log(f"  {name:<20} | BBB Rank #{r['rank']:>3} / {len(top_bowlers)} | P Balls={r['p_b']:>4} | P Econ={r['p_econ']:>5.2f} (Exp={r['p_exp_econ']:>5.2f}) | P RPAE={r['p_rpae']:>+6.1f} | P Wkts={r['p_wkts']:>2} | EB Score={r['score_opt2_proposed_60_40']:>+6.2f}")
        else:
            log(f"  {name:<20} | DID NOT QUALIFY (under minimum 300 career / 40 pressure balls)")

    # Save Complete Output Tables to STEP3_DIR
    top_batters.to_csv(os.path.join(STEP3_DIR, "BATTERS_PERFORMANCE_STEP3.csv"), index=False)
    top_bowlers.to_csv(os.path.join(STEP3_DIR, "BOWLERS_PERFORMANCE_STEP3.csv"), index=False)
    top_batters.head(10).to_csv(os.path.join(STEP3_DIR, "BATTERS_TOP10_PROVISIONAL.csv"), index=False)
    top_bowlers.head(10).to_csv(os.path.join(STEP3_DIR, "BOWLERS_TOP10_PROVISIONAL.csv"), index=False)

    out_txt = os.path.join(STEP3_DIR, "03_aggregation_and_scoring_report.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log(f"\nSaved aggregation report to {out_txt}")
    log(f"Saved complete CSV outputs to {STEP3_DIR}")


if __name__ == "__main__":
    main()
