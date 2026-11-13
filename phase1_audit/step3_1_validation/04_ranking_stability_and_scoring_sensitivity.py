"""
Phase 1 Step 3.1 — Sections 7 & 8: Ranking Stability Across Thresholds & Scoring Weight Sensitivity
(04_ranking_stability_and_scoring_sensitivity.py)

1. Threshold Sensitivity: Evaluates stability across Top 15%, 20%, 25% (baseline), 30% of BPI/BWPI.
   - Measures delivery volume, qualified player count, Spearman rho, Kendall tau, Top-10 & Top-20 overlap.
2. Scoring Formula & Weight Sensitivity:
   - Batting: Pure RAE vs Step 3 Provisional (75/25) vs Hybrid Lift vs Wicket Equivalence (8, 10, 12, 15, 20 runs).
   - Bowling: Pure RPAE vs RPAE/WAE splits (80/20, 70/30, 60/40, 50/50, 40/60, 30/70) vs Wicket Equivalence (8, 10, 12, 15, 20 runs).
   - Prior weight variations M0 in [50, 75, 100, 150, 200, 250].

Outputs:
- RANKING_STABILITY_VALIDATION.csv
- SCORING_WEIGHT_SENSITIVITY.csv
- 04_ranking_stability_and_scoring_sensitivity_report.txt
"""

import os
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, kendalltau

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit")
VAL_DIR = os.path.join(AUDIT_DIR, "step3_1_validation")
os.makedirs(VAL_DIR, exist_ok=True)


def main():
    lines = []
    def log(msg=""):
        lines.append(msg)
        print(msg)

    log("=" * 80)
    log("PHASE 1 STEP 3.1 — SECTIONS 7 & 8: RANKING STABILITY & WEIGHT SENSITIVITY")
    log("=" * 80)

    # Load modeled deliveries from Step 3
    df = pd.read_pickle(os.path.join(AUDIT_DIR, "step3_individual_model", "bbb_step3_modeled.pkl"))
    ctpm = pd.read_csv(os.path.join(ROOT, "competition_team_player_mapping.csv"))
    p_names = dict(zip(ctpm["player_id"], ctpm["player_name"]))

    # =========================================================================
    # PART 1: PRESSURE THRESHOLD SENSITIVITY (15%, 20%, 25%, 30%)
    # =========================================================================
    log("\n[1] RANKING STABILITY ACROSS PRESSURE THRESHOLDS (15%, 20%, 25%, 30%)")

    threshold_pcts = [15, 20, 25, 30]
    thresh_records = []

    # Pre-calculate player total career balls faced / bowled for eligibility
    career_bf = df[df["is_legal_bat"]].groupby("striker_id")["runs"].count()
    career_bowl_b = df[df["is_legal_bowl"]].groupby("bowler_id")["is_legal_bowl"].count()

    # Pre-compute player scores across the 4 thresholds
    bat_thresh_scores = {}
    bowl_thresh_scores = {}
    bat_thresh_quals = {}
    bowl_thresh_quals = {}

    M0 = 150.0

    for pct in threshold_pcts:
        q_val = 1.0 - (pct / 100.0)
        cut_b = df.loc[df["is_legal_bat"], "BPI"].quantile(q_val)
        cut_bw = df.loc[df["is_legal_bowl"], "BWPI"].quantile(q_val)

        mask_bat = (df["BPI"] >= cut_b) & df["is_legal_bat"]
        mask_bowl = (df["BWPI"] >= cut_bw) & df["is_legal_bowl"]

        n_deliv_bat = int(mask_bat.sum())
        n_deliv_bowl = int(mask_bowl.sum())

        # Batting player aggregates under this threshold
        p_bat = df[mask_bat].groupby("striker_id").agg(
            n_bf=("runs", "count"),
            sum_rae=("rae", "sum"),
            sum_exp_wkt=("exp_bowl_wkt", "sum"),
            sum_outs=("is_striker_out", "sum")
        )
        p_bat["career_bf"] = career_bf
        p_bat["career_bf"] = p_bat["career_bf"].fillna(0)
        # Eligibility: career_bf >= 300 & p_bf >= 40
        qual_bat = p_bat[(p_bat["career_bf"] >= 300) & (p_bat["n_bf"] >= 40)].copy()
        qual_bat["pure_rae_score"] = (qual_bat["sum_rae"] / (qual_bat["n_bf"] + M0)) * 100.0
        # Step 3 provisional 75/25 formula
        qual_bat["wkt_saved"] = qual_bat["sum_exp_wkt"] - qual_bat["sum_outs"]
        qual_bat["wkt_saved_scaled"] = (qual_bat["wkt_saved"] / (qual_bat["n_bf"] + M0) * 100.0) * 12.0
        qual_bat["composite_score"] = 0.75 * qual_bat["pure_rae_score"] + 0.25 * qual_bat["wkt_saved_scaled"]
        
        bat_thresh_scores[pct] = qual_bat
        bat_thresh_quals[pct] = set(qual_bat.index)

        # Bowling player aggregates under this threshold
        p_bowl = df[mask_bowl].groupby("bowler_id").agg(
            n_b=("is_legal_bowl", "sum"),
            sum_rpae=("rpae", "sum"),
            sum_wae=("wae", "sum")
        )
        p_bowl["career_b"] = career_bowl_b
        p_bowl["career_b"] = p_bowl["career_b"].fillna(0)
        qual_bowl = p_bowl[(p_bowl["career_b"] >= 300) & (p_bowl["n_b"] >= 40)].copy()
        qual_bowl["pure_rpae_score"] = (qual_bowl["sum_rpae"] / (qual_bowl["n_b"] + M0)) * 100.0
        qual_bowl["wae_scaled"] = (qual_bowl["sum_wae"] / (qual_bowl["n_b"] + 100.0) * 100.0) * 12.0
        qual_bowl["composite_score"] = 0.60 * qual_bowl["pure_rpae_score"] + 0.40 * qual_bowl["wae_scaled"]

        bowl_thresh_scores[pct] = qual_bowl
        bowl_thresh_quals[pct] = set(qual_bowl.index)

    # Reference is 25% baseline
    ref_bat_pure = bat_thresh_scores[25]["pure_rae_score"]
    ref_bat_comp = bat_thresh_scores[25]["composite_score"]
    ref_bowl_comp = bowl_thresh_scores[25]["composite_score"]
    ref_bowl_pure = bowl_thresh_scores[25]["pure_rpae_score"]

    ref_bat_top10 = set(ref_bat_pure.sort_values(ascending=False).head(10).index)
    ref_bat_top20 = set(ref_bat_pure.sort_values(ascending=False).head(20).index)
    ref_bowl_top10 = set(ref_bowl_comp.sort_values(ascending=False).head(10).index)
    ref_bowl_top20 = set(ref_bowl_comp.sort_values(ascending=False).head(20).index)

    log("\n  Threshold Stability Summary (Compared with 25% Baseline):")
    log(f"  {'Discipline':<10}{'Threshold':<12}{'Delivs':>9}{'Qual N':>8}{'Spearman rho':>14}{'Kendall tau':>13}{'Top-10 In':>11}{'Top-20 In':>11}{'Status':>12}")
    log("  " + "-" * 95)

    for pct in threshold_pcts:
        # Batting (Pure RAE)
        q_b = bat_thresh_scores[pct]
        common_b = q_b.index.intersection(ref_bat_pure.index)
        s_rho_b = float(spearmanr(ref_bat_pure.loc[common_b], q_b.loc[common_b, "pure_rae_score"]).statistic)
        k_tau_b = float(kendalltau(ref_bat_pure.loc[common_b], q_b.loc[common_b, "pure_rae_score"]).statistic)
        t10_b = len(ref_bat_top10.intersection(set(q_b["pure_rae_score"].sort_values(ascending=False).head(10).index)))
        t20_b = len(ref_bat_top20.intersection(set(q_b["pure_rae_score"].sort_values(ascending=False).head(20).index)))

        status_b = "BASELINE" if pct == 25 else ("HIGH STABILITY" if s_rho_b >= 0.85 else "MODERATE")
        log(f"  {'Batting':<10}{f'Top {pct}%':<12}{len(df[(df['BPI'] >= df.loc[df['is_legal_bat'],'BPI'].quantile(1-pct/100.0)) & df['is_legal_bat']]):>9,}{len(q_b):>8}{s_rho_b:>14.4f}{k_tau_b:>13.4f}{f'{t10_b}/10':>11}{f'{t20_b}/20':>11}{status_b:>12}")

        thresh_records.append({
            "discipline": "Batting",
            "metric": "Pure_RAE",
            "threshold_pct": f"Top {pct}%",
            "deliveries": len(df[(df['BPI'] >= df.loc[df['is_legal_bat'],'BPI'].quantile(1-pct/100.0)) & df['is_legal_bat']]),
            "qualified_players": len(q_b),
            "spearman_rho_vs_25pct": round(s_rho_b, 4),
            "kendall_tau_vs_25pct": round(k_tau_b, 4),
            "top10_overlap": f"{t10_b}/10",
            "top20_overlap": f"{t20_b}/20",
            "stability_status": status_b
        })

        # Bowling (Composite)
        q_bw = bowl_thresh_scores[pct]
        common_bw = q_bw.index.intersection(ref_bowl_comp.index)
        s_rho_bw = float(spearmanr(ref_bowl_comp.loc[common_bw], q_bw.loc[common_bw, "composite_score"]).statistic)
        k_tau_bw = float(kendalltau(ref_bowl_comp.loc[common_bw], q_bw.loc[common_bw, "composite_score"]).statistic)
        t10_bw = len(ref_bowl_top10.intersection(set(q_bw["composite_score"].sort_values(ascending=False).head(10).index)))
        t20_bw = len(ref_bowl_top20.intersection(set(q_bw["composite_score"].sort_values(ascending=False).head(20).index)))

        status_bw = "BASELINE" if pct == 25 else ("HIGH STABILITY" if s_rho_bw >= 0.85 else "MODERATE")
        log(f"  {'Bowling':<10}{f'Top {pct}%':<12}{len(df[(df['BWPI'] >= df.loc[df['is_legal_bowl'],'BWPI'].quantile(1-pct/100.0)) & df['is_legal_bowl']]):>9,}{len(q_bw):>8}{s_rho_bw:>14.4f}{k_tau_bw:>13.4f}{f'{t10_bw}/10':>11}{f'{t20_bw}/20':>11}{status_bw:>12}")

        thresh_records.append({
            "discipline": "Bowling",
            "metric": "Composite_60_40",
            "threshold_pct": f"Top {pct}%",
            "deliveries": len(df[(df['BWPI'] >= df.loc[df['is_legal_bowl'],'BWPI'].quantile(1-pct/100.0)) & df['is_legal_bowl']]),
            "qualified_players": len(q_bw),
            "spearman_rho_vs_25pct": round(s_rho_bw, 4),
            "kendall_tau_vs_25pct": round(k_tau_bw, 4),
            "top10_overlap": f"{t10_bw}/10",
            "top20_overlap": f"{t20_bw}/20",
            "stability_status": status_bw
        })

    pd.DataFrame(thresh_records).to_csv(os.path.join(VAL_DIR, "RANKING_STABILITY_VALIDATION.csv"), index=False)
    log(f"\nSaved threshold stability table to {os.path.join(VAL_DIR, 'RANKING_STABILITY_VALIDATION.csv')}")

    # =========================================================================
    # PART 2: SCORING METHODOLOGY & WEIGHT SENSITIVITY
    # =========================================================================
    log("\n" + "=" * 80)
    log("[2] SCORING FORMULA & WEIGHT SENSITIVITY ANALYSIS")
    log("=" * 80)

    # Use 25% baseline qualified player data
    bat_base = bat_thresh_scores[25].copy()
    bowl_base = bowl_thresh_scores[25].copy()

    # Pre-compute lifts from Step 3
    # Career RAE rates
    all_bat = df[df["is_legal_bat"]].groupby("striker_id").agg(n_all=("runs", "count"), s_all=("rae", "sum"))
    bat_base = bat_base.join(all_bat)
    bat_base["career_rae_rate"] = (bat_base["s_all"] / bat_base["n_all"]) * 100.0
    bat_base["lift_rae_rate"] = ((bat_base["sum_rae"] / bat_base["n_bf"]) * 100.0) - bat_base["career_rae_rate"]

    all_bowl = df[df["is_legal_bowl"]].groupby("bowler_id").agg(n_all=("is_legal_bowl", "sum"), s_all=("rpae", "sum"))
    bowl_base = bowl_base.join(all_bowl)
    bowl_base["career_rpae_rate"] = (bowl_base["s_all"] / bowl_base["n_all"]) * 100.0
    bowl_base["lift_rpae_rate"] = ((bowl_base["sum_rpae"] / bowl_base["n_b"]) * 100.0) - bowl_base["career_rpae_rate"]

    weight_records = []

    # -------------------------------------------------------------
    # 2.1 BATTING FORMULA SENSITIVITY
    # -------------------------------------------------------------
    log("\n  [2.1] BATTING FORMULA SENSITIVITY:")
    log(f"  {'Formula Scheme':<36}{'Spearman rho':>14}{'Top-10 Overlap':>16}{'Top Player':<22}{'Top Player Score':>18}")
    log("  " + "-" * 110)

    # Baseline Batting: Pure RAE (M0=150)
    bat_ref = (bat_base["sum_rae"] / (bat_base["n_bf"] + 150.0)) * 100.0
    ref_top10_bat = set(bat_ref.sort_values(ascending=False).head(10).index)

    bat_schemes = {}
    # Option 1: Pure RAE (M0=150)
    bat_schemes["Pure RAE (M0=150) [Recommended]"] = bat_ref
    # Option 2: Step 3 Provisional (75% RAE + 25% WktSaved * 12)
    bat_schemes["Step 3 Provisional (75% RAE + 25% WktSaved)"] = (
        0.75 * ((bat_base["sum_rae"] / (bat_base["n_bf"] + 150.0)) * 100.0) +
        0.25 * ((bat_base["wkt_saved"] / (bat_base["n_bf"] + 150.0) * 100.0) * 12.0)
    )
    # Option 3: Clutch Hybrid (60% RAE + 20% WktSaved + 20% Lift)
    shrunk_lift_b = (bat_base["lift_rae_rate"] * bat_base["n_bf"]) / (bat_base["n_bf"] + 150.0)
    bat_schemes["Clutch Hybrid (60% RAE + 20% Wkt + 20% Lift)"] = (
        0.60 * ((bat_base["sum_rae"] / (bat_base["n_bf"] + 150.0)) * 100.0) +
        0.20 * ((bat_base["wkt_saved"] / (bat_base["n_bf"] + 150.0) * 100.0) * 12.0) +
        0.20 * shrunk_lift_b
    )
    # Option 4: Pure RAE with alternative M0: 75, 100, 200
    for m in [75, 100, 200]:
        bat_schemes[f"Pure RAE (M0={m})"] = (bat_base["sum_rae"] / (bat_base["n_bf"] + float(m))) * 100.0

    # Option 5: Wicket Equivalence Factor Sensitivity in Step 3 Provisional (W_equiv in 8, 10, 15, 20)
    for w in [8, 10, 15, 20]:
        bat_schemes[f"Provisional 75/25 (WktEquiv={w} runs)"] = (
            0.75 * ((bat_base["sum_rae"] / (bat_base["n_bf"] + 150.0)) * 100.0) +
            0.25 * ((bat_base["wkt_saved"] / (bat_base["n_bf"] + 150.0) * 100.0) * float(w))
        )

    for name, s_series in bat_schemes.items():
        s_rho = float(spearmanr(bat_ref, s_series).statistic)
        t10_cnt = len(ref_top10_bat.intersection(set(s_series.sort_values(ascending=False).head(10).index)))
        top_pid = s_series.sort_values(ascending=False).index[0]
        top_name = p_names.get(top_pid, f"Player {top_pid}")
        top_score = s_series.loc[top_pid]

        log(f"  {name:<36}{s_rho:>14.4f}{f'{t10_cnt}/10':>16}{top_name:<22}{top_score:>18.2f}")

        weight_records.append({
            "discipline": "Batting",
            "scheme_name": name,
            "spearman_rho_vs_ref": round(s_rho, 4),
            "top10_overlap": f"{t10_cnt}/10",
            "top_player": top_name,
            "top_player_score": round(top_score, 2)
        })

    # -------------------------------------------------------------
    # 2.2 BOWLING FORMULA SENSITIVITY
    # -------------------------------------------------------------
    log("\n  [2.2] BOWLING FORMULA SENSITIVITY:")
    log(f"  {'Formula Scheme':<36}{'Spearman rho':>14}{'Top-10 Overlap':>16}{'Top Player':<22}{'Top Player Score':>18}")
    log("  " + "-" * 110)

    # Reference Bowling: Step 3 Provisional (60% RPAE + 40% WAE * 12, M0=150, Mw=100)
    shrunk_rpae_ref = (bowl_base["sum_rpae"] / (bowl_base["n_b"] + 150.0)) * 100.0
    shrunk_wae_ref = (bowl_base["sum_wae"] / (bowl_base["n_b"] + 100.0) * 100.0) * 12.0
    bowl_ref = 0.60 * shrunk_rpae_ref + 0.40 * shrunk_wae_ref
    ref_top10_bowl = set(bowl_ref.sort_values(ascending=False).head(10).index)

    bowl_schemes = {}
    # Baseline
    bowl_schemes["Step 3 Provisional (60/40, W=12) [Ref]"] = bowl_ref
    # Option 1: Pure RPAE (100% Run Prevention)
    bowl_schemes["Pure RPAE (100% Run Prevention)"] = shrunk_rpae_ref
    # Option 2: 80% RPAE / 20% WAE
    bowl_schemes["80% RPAE / 20% WAE (W=12)"] = 0.80 * shrunk_rpae_ref + 0.20 * shrunk_wae_ref
    # Option 3: 70% RPAE / 30% WAE
    bowl_schemes["70% RPAE / 30% WAE (W=12)"] = 0.70 * shrunk_rpae_ref + 0.30 * shrunk_wae_ref
    # Option 4: 50% RPAE / 50% WAE (Balanced)
    bowl_schemes["50% RPAE / 50% WAE (W=12)"] = 0.50 * shrunk_rpae_ref + 0.50 * shrunk_wae_ref
    # Option 5: 40% RPAE / 60% WAE (Wicket-Biased)
    bowl_schemes["40% RPAE / 60% WAE (W=12)"] = 0.40 * shrunk_rpae_ref + 0.60 * shrunk_wae_ref
    # Option 6: 30% RPAE / 70% WAE
    bowl_schemes["30% RPAE / 70% WAE (W=12)"] = 0.30 * shrunk_rpae_ref + 0.70 * shrunk_wae_ref

    # Option 7: Wicket Equivalence Factor Sensitivity (W_equiv in 8, 10, 15, 20 with 60/40)
    for w in [8, 10, 15, 20]:
        wae_w = (bowl_base["sum_wae"] / (bowl_base["n_b"] + 100.0) * 100.0) * float(w)
        bowl_schemes[f"60/40 Split (WktEquiv={w} runs)"] = 0.60 * shrunk_rpae_ref + 0.40 * wae_w

    # Option 8: Alternative Priors M0 in [75, 100, 200] (with 60/40, W=12)
    for m in [75, 100, 200]:
        rpae_m = (bowl_base["sum_rpae"] / (bowl_base["n_b"] + float(m))) * 100.0
        wae_m = (bowl_base["sum_wae"] / (bowl_base["n_b"] + float(m) * (100.0 / 150.0)) * 100.0) * 12.0
        bowl_schemes[f"60/40 Split (M0={m})"] = 0.60 * rpae_m + 0.40 * wae_m

    for name, s_series in bowl_schemes.items():
        s_rho = float(spearmanr(bowl_ref, s_series).statistic)
        t10_cnt = len(ref_top10_bowl.intersection(set(s_series.sort_values(ascending=False).head(10).index)))
        top_pid = s_series.sort_values(ascending=False).index[0]
        top_name = p_names.get(top_pid, f"Player {top_pid}")
        top_score = s_series.loc[top_pid]

        log(f"  {name:<36}{s_rho:>14.4f}{f'{t10_cnt}/10':>16}{top_name:<22}{top_score:>18.2f}")

        weight_records.append({
            "discipline": "Bowling",
            "scheme_name": name,
            "spearman_rho_vs_ref": round(s_rho, 4),
            "top10_overlap": f"{t10_cnt}/10",
            "top_player": top_name,
            "top_player_score": round(top_score, 2)
        })

    pd.DataFrame(weight_records).to_csv(os.path.join(VAL_DIR, "SCORING_WEIGHT_SENSITIVITY.csv"), index=False)
    log(f"\nSaved scoring weight sensitivity table to {os.path.join(VAL_DIR, 'SCORING_WEIGHT_SENSITIVITY.csv')}")

    # Write report text
    with open(os.path.join(VAL_DIR, "04_ranking_stability_and_scoring_sensitivity_report.txt"), "w") as f:
        f.write("\n".join(lines))
    log(f"Saved text report to {os.path.join(VAL_DIR, '04_ranking_stability_and_scoring_sensitivity_report.txt')}")


if __name__ == "__main__":
    main()

