"""
Phase 1 Delivery-Level State Reconstruction, Counterfactual WP Leverage & Pressure Threshold Sensitivity
(03_delivery_state_and_pressure.py)

Strictly uses PRE-DELIVERY state only (zero outcome leakage, zero retrospective margin leakage).
Separates Super Overs, Abandoned/No-Result, and DLS/shortened matches explicitly.
Evaluates Counterfactual Win Probability & Expected Run Rate via GroupKFold(5) by match_id.
Builds separate Batting Pressure Index (BPI) and Bowling Pressure Index (BWPI).
Evaluates 15%, 20%, 25%, and 30% pressure thresholds on volume, interpretability, reliability,
Spearman rank correlation, Top-10 overlap, and cluster bootstrap stability.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.metrics import log_loss, brier_score_loss, roc_auc_score, mean_squared_error, r2_score
from scipy.stats import spearmanr

ROOT = r"c:\Rajasthan Royals"
OUT_DIR = os.path.join(ROOT, "phase1_audit")
CHART_DIR = os.path.join(OUT_DIR, "charts")
os.makedirs(CHART_DIR, exist_ok=True)


def expected_calibration_error(y_true, y_prob, n_bins=10):
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    n = len(y_true)
    for i in range(n_bins):
        mask = (y_prob >= bins[i]) & (y_prob < bins[i + 1] if i < n_bins - 1 else y_prob <= bins[i + 1])
        if mask.sum() > 0:
            ece += (mask.sum() / n) * abs(y_true[mask].mean() - y_prob[mask].mean())
    return float(ece)


def main():
    lines = []
    def log(msg=""):
        lines.append(msg)
        print(msg)

    log("=" * 80)
    log("PHASE 1 — DELIVERY-LEVEL STATE RECONSTRUCTION & PRESSURE MODELING")
    log("=" * 80)

    bbb = pd.read_csv(os.path.join(ROOT, "ball_by_ball.csv"), low_memory=False)
    matches = pd.read_csv(os.path.join(ROOT, "matches.csv"))
    comps = pd.read_csv(os.path.join(ROOT, "competitions.csv"))

    matches = matches.merge(comps[["comp_id", "comp_name", "match_format", "season"]], on="comp_id", how="left")
    matches["is_ko_or_playoff"] = (
        (matches["knock_out"].fillna(0).astype(int) == 1)
        | matches["stage"].astype(str).str.lower().str.contains("final|semi|qualifier|eliminator", na=False)
    ).astype(int)
    matches["is_final"] = (
        matches["stage"].astype(str).str.lower().str.contains("final", na=False)
        & ~matches["stage"].astype(str).str.lower().str.contains("semi|quarter", na=False)
    ).astype(int)
    matches["is_dls_or_revised"] = (
        matches["first_inn_revised_overs"].notna()
        | matches["second_inn_revised_overs"].notna()
        | matches["revised_target"].notna()
        | matches["result"].astype(str).str.contains("D/L|DLS", case=False, na=False)
    )
    matches["has_winner"] = matches["win_team_id"].notna()
    matches["is_super_over_match"] = matches["match_id"].isin(set(bbb.loc[bbb["innings"].isin([3, 4]), "match_id"]))

    # Separate Super Over deliveries first
    so_bbb = bbb[bbb["innings"].isin([3, 4])].copy()
    log(f"\n[1] SCOPE SEPARATION")
    log(f"  Total deliveries in ball_by_ball.csv: {len(bbb):,}")
    log(f"  Super Over deliveries (innings 3 & 4 across {so_bbb['match_id'].nunique()} matches): {len(so_bbb)} (isolated for separate peak-pressure summary)")

    df = bbb[bbb["innings"].isin([1, 2])].copy()
    df = df.merge(
        matches[[
            "match_id", "comp_id", "comp_name", "match_format", "season", "match_date",
            "venue_id", "stage", "knock_out", "is_ko_or_playoff", "is_final",
            "first_inn_revised_overs", "second_inn_revised_overs", "revised_target",
            "is_dls_or_revised", "win_team_id", "has_winner", "result", "is_super_over_match"
        ]],
        on="match_id", how="left"
    )

    # Sort chronologically within each (match_id, innings)
    # Check ordering consistency between innings_ball_num vs (overid, over_ball_num)
    df = df.sort_values(["match_id", "innings", "overid", "over_ball_num", "innings_ball_num"]).reset_index(drop=True)
    df["order_check"] = df.groupby(["match_id", "innings"])["innings_ball_num"].diff().fillna(1)
    log(f"  Innings deliveries (1 & 2): {len(df):,} across {df['match_id'].nunique()} matches")
    log(f"  Rows where innings_ball_num decreases after (overid, over_ball_num) sort: {(df['order_check'] < 0).sum()}")

    # Construct verified observable runs per delivery & legal-ball indicators
    ext = df["extras_type"].fillna("")
    df["is_wide"] = (ext == "wide")
    df["is_noball"] = ext.isin(["Overstep", "other"])
    df["is_bye"] = (ext == "byes")
    df["is_legbye"] = (ext == "legbyes")
    df["is_penalty"] = (ext == "Penalty")
    df["is_legal_bowl"] = (~df["is_wide"]) & (~df["is_noball"])
    df["is_legal_bat"] = (~df["is_wide"])  # Cricket law: no-balls ARE balls faced by batter; wides are NOT

    # Verified minimal observable team runs on this delivery
    # Note: extras1_runs is enum 1..7, NOT runs! Only lower-bound extras (1 on wide/nb/b/lb, 5 on Penalty) + extras_2_runs are directly observable.
    min_ext_team = np.where(ext.isin(["wide", "Overstep", "other", "byes", "legbyes"]), 1,
                   np.where(ext == "Penalty", 5, 0))
    df["team_runs_obs"] = df["runs"] + min_ext_team + df["extras_2_runs"].fillna(0).astype(int)
    # Bowler-conceded minimal observable runs (excludes byes, legbyes, team penalty runs; excludes extras_2_runs if non-NB)
    df["bowl_runs_obs"] = df["runs"] + np.where(df["is_wide"] | df["is_noball"], 1, 0) + np.where(df["is_noball"], df["extras_2_runs"].fillna(0).astype(int), 0)

    # Bowler-credited wicket strictly excludes RunOut, Retire Out, Obstructing/Obstracting the field
    dt = df["dismissal_type"].fillna("")
    non_bowler_dismissals = {"RunOut", "Retire Out", "Obstracting the field", "Obstructing the field"}
    df["is_bowler_wicket"] = df["is_wicket"] & (~dt.isin(non_bowler_dismissals))
    df["is_batter_out"] = df["is_wicket"]  # note: includes non-striker runouts as inning wickets, batter dismissal tracked via dismissed_player_id == striker_id
    df["is_striker_out"] = df["is_wicket"] & (df["dismissed_player_id"] == df["striker_id"]) & (~dt.isin({"Retire Out"}))

    # Allocated legal balls per innings (verified in Part 2: revised_overs are stored in LEGAL BALLS!)
    inn1_alloc = np.where(df["first_inn_revised_overs"].notna(), df["first_inn_revised_overs"].fillna(120), 120.0)
    inn2_alloc = np.where(
        df["second_inn_revised_overs"].notna(), df["second_inn_revised_overs"].fillna(120),
        np.where(df["first_inn_revised_overs"].notna(), df["first_inn_revised_overs"].fillna(120), 120.0)
    )
    df["alloc_balls"] = np.where(df["innings"] == 1, inn1_alloc, inn2_alloc).astype(int)

    # Reconstruct strict PRE-DELIVERY cumulative states within each (match_id, innings)
    grp = df.groupby(["match_id", "innings"], sort=False)
    df["legal_balls_before"] = (grp["is_legal_bowl"].cumsum() - df["is_legal_bowl"].astype(int)).astype(int)
    df["score_before"] = (grp["team_runs_obs"].cumsum() - df["team_runs_obs"]).astype(int)
    df["wkts_before"] = (grp["is_wicket"].cumsum() - df["is_wicket"].astype(int)).clip(0, 9).astype(int)
    df["wkts_in_hand_pre"] = (10 - df["wkts_before"]).astype(int)

    # Check if any innings exceeded alloc_balls (e.g. scoring error or unflagged revised match)
    over_alloc = (df["legal_balls_before"] >= df["alloc_balls"]).sum()
    log(f"  Deliveries where legal_balls_before >= alloc_balls: {over_alloc}")
    df["balls_remaining_pre"] = np.maximum(1, df["alloc_balls"] - df["legal_balls_before"]).astype(int)
    df["frac_innings_done"] = df["legal_balls_before"] / np.maximum(1, df["alloc_balls"])

    # Attach 1st-innings final observable total & target for Innings 2
    inn1_totals = df[df["innings"] == 1].groupby("match_id").agg(
        inn1_obs_total=("team_runs_obs", "sum"),
        inn1_wickets=("is_wicket", "sum"),
        inn1_legal_balls=("is_legal_bowl", "sum"),
    ).reset_index()
    df = df.merge(inn1_totals, on="match_id", how="left")

    # Target for innings 2: revised_target if present, else inn1_obs_total + 1
    df["target"] = np.where(
        df["innings"] == 2,
        np.where(df["revised_target"].notna(), df["revised_target"].fillna(0), df["inn1_obs_total"].fillna(0) + 1.0),
        np.nan
    )
    df["runs_required_pre"] = np.where(df["innings"] == 2, np.maximum(0.0, df["target"] - df["score_before"]), np.nan)

    # Pre-delivery Current Run Rate (smoothed with 6-ball / 8-RPO prior early) & Required Run Rate
    df["crr_pre"] = np.where(df["legal_balls_before"] > 0, 6.0 * df["score_before"] / df["legal_balls_before"], 8.0)
    df["crr_pre_smoothed"] = 6.0 * (df["score_before"] + 8.0) / (df["legal_balls_before"] + 6.0)
    df["rrr_pre"] = np.where(df["innings"] == 2, 6.0 * df["runs_required_pre"] / df["balls_remaining_pre"], np.nan)
    df["phase"] = np.where(df["overid"] <= 6, "PP", np.where(df["overid"] <= 15, "Middle", "Death"))
    df["is_decided_inning"] = df["has_winner"] & (~df["is_super_over_match"]) & (~df["result"].astype(str).str.contains("Tied", case=False, na=False))
    df["batting_team_won"] = np.where(df["has_winner"], (df["batting_team_id"] == df["win_team_id"]).astype(float), np.nan)

    log(f"  Standard decided deliveries (has_winner & non-Super-Over): {df['is_decided_inning'].sum():,} ({df.loc[df['is_decided_inning'], 'match_id'].nunique()} matches)")

    # 2. Match-Grouped Out-Of-Fold Par Run Rate & Innings Total Expectation Model
    log("\n[2] CONTEXTUAL PAR / REMAINING-RUN-RATE MODEL (GroupKFold by match_id)")
    # Estimate remaining runs per ball / expected remaining runs from state strictly pre-delivery (grouped by match_id!)
    # First compute actual remaining runs scored AFTER (and including) current delivery in the innings
    inn_final_scores = df.groupby(["match_id", "innings"])["team_runs_obs"].transform("sum")
    df["actual_rem_runs_from_pre"] = inn_final_scores - df["score_before"]
    df["actual_rem_rpo_from_pre"] = np.where(df["balls_remaining_pre"] > 0, 6.0 * df["actual_rem_runs_from_pre"] / df["balls_remaining_pre"], np.nan)

    # Fit on full non-NR/non-abandoned completed innings (inn1 or full inn2, using alloc_balls & state)
    # Better: fit separate Innings 1 expected final total (par) & expected remaining RPO by state using GroupKFold!
    model_features = [
        "innings", "overid", "legal_balls_before", "balls_remaining_pre", "alloc_balls",
        "score_before", "wkts_before", "crr_pre_smoothed", "is_t20i", "season_num", "is_dls"
    ]
    df["is_t20i"] = (df["match_format"] == "T20I").astype(int)
    df["season_num"] = df["season"].astype(str).str[:4].astype(int)
    df["is_dls"] = df["is_dls_or_revised"].astype(int)

    # For expected remaining runs, only train on matches that weren't abandoned/NR mid-innings (i.e. has_winner==True)
    valid_state_mask = df["has_winner"] & (df["balls_remaining_pre"] > 0)
    gkf = GroupKFold(n_splits=5)

    # Expected remaining runs given state (baseline: league-average phase RPO * balls_rem)
    X_rem = df.loc[valid_state_mask, model_features].values
    y_rem = df.loc[valid_state_mask, "actual_rem_runs_from_pre"].values
    groups_rem = df.loc[valid_state_mask, "match_id"].values

    oof_rem_hgb = np.zeros(valid_state_mask.sum())
    oof_rem_base = np.zeros(valid_state_mask.sum())
    for tr_idx, va_idx in gkf.split(X_rem, y_rem, groups_rem):
        # Simple phase/overs-wickets group mean baseline
        tr_df = df.loc[valid_state_mask].iloc[tr_idx]
        mean_rpo_by_iw = tr_df.groupby(["innings", "overid", "wkts_before"])["actual_rem_rpo_from_pre"].mean()
        global_rpo = tr_df["actual_rem_rpo_from_pre"].mean()
        va_df = df.loc[valid_state_mask].iloc[va_idx]
        va_keys = list(zip(va_df["innings"], va_df["overid"], va_df["wkts_before"]))
        va_rpo = np.array([mean_rpo_by_iw.get(k, global_rpo) for k in va_keys])
        oof_rem_base[va_idx] = va_rpo * va_df["balls_remaining_pre"].values / 6.0

        hgb = HistGradientBoostingRegressor(max_depth=5, learning_rate=0.06, max_iter=150, min_samples_leaf=100, random_state=42)
        hgb.fit(X_rem[tr_idx], y_rem[tr_idx])
        oof_rem_hgb[va_idx] = np.clip(hgb.predict(X_rem[va_idx]), 0.0, 300.0)

    rmse_base = np.sqrt(mean_squared_error(y_rem, oof_rem_base))
    r2_base = r2_score(y_rem, oof_rem_base)
    rmse_hgb = np.sqrt(mean_squared_error(y_rem, oof_rem_hgb))
    r2_hgb = r2_score(y_rem, oof_rem_hgb)
    log(f"  Remaining Runs (State -> Final Score - Score_pre) OOF GroupKFold:")
    log(f"    Simple (innings, over, wkts) baseline: RMSE={rmse_base:.2f} runs, R2={r2_base:.4f}")
    log(f"    HistGBR state model                  : RMSE={rmse_hgb:.2f} runs, R2={r2_hgb:.4f}")

    # Assign expected remaining RPO to ALL rows (fit full model on decided rows for any NR/tie rows, strictly using OOF for decided rows)
    full_hgb_rem = HistGradientBoostingRegressor(max_depth=5, learning_rate=0.06, max_iter=150, min_samples_leaf=100, random_state=42)
    full_hgb_rem.fit(X_rem, y_rem)
    df["exp_rem_runs"] = np.clip(full_hgb_rem.predict(df[model_features].values), 0.0, 300.0)
    df.loc[valid_state_mask, "exp_rem_runs"] = oof_rem_hgb
    df["exp_rem_rpo"] = np.clip(6.0 * df["exp_rem_runs"] / np.maximum(1, df["balls_remaining_pre"]), 3.0, 18.0)
    df["exp_final_score_pre"] = df["score_before"] + df["exp_rem_runs"]

    # League-average Innings 1 par score by balls_before & format (for Innings 1 scoring deficit signal)
    par_1st_by_over = df[(df["innings"] == 1) & (df["has_winner"])].groupby(["is_t20i", "overid"])["score_before"].mean()
    # Expected final 1st innings par by format
    par_1st_final = df[(df["innings"] == 1) & (df["has_winner"])].groupby("is_t20i")["inn1_obs_total"].mean().to_dict()
    df["format_par_final"] = df["is_t20i"].map(par_1st_final)
    df["inn1_deficit_vs_par"] = np.where(df["innings"] == 1, df["format_par_final"] - df["exp_final_score_pre"], np.nan)

    # 3. Pre-Delivery Win Probability Model & Counterfactual Delivery Leverage (GroupKFold by match_id)
    log("\n[3] WIN PROBABILITY & COUNTERFACTUAL LEVERAGE MODEL (GroupKFold by match_id)")
    # Build unified features so we can evaluate counterfactual WP after hypothetical delivery outcomes!
    # Crucially, separate Inn1 and Inn2 models cleanly so counterfactual chase math (target - score) vs Inn1 par works naturally!
    wp_mask = df["is_decided_inning"] & (df["balls_remaining_pre"] > 0)
    df["wp_pre_oof"] = np.nan
    df["wp_dot_cf"] = np.nan
    df["wp_four_cf"] = np.nan
    df["wp_six_cf"] = np.nan
    df["wp_wkt_cf"] = np.nan

    for inn in [1, 2]:
        sub_mask = wp_mask & (df["innings"] == inn)
        sub_all_inn = (df["innings"] == inn)
        if inn == 1:
            wp_cols = ["overid", "legal_balls_before", "balls_remaining_pre", "alloc_balls", "score_before", "wkts_before", "crr_pre_smoothed", "is_t20i", "season_num"]
        else:
            wp_cols = ["overid", "legal_balls_before", "balls_remaining_pre", "alloc_balls", "score_before", "wkts_before", "crr_pre_smoothed", "target", "runs_required_pre", "rrr_pre", "is_t20i", "season_num"]

        def make_cf_df(base_df, add_runs=0, add_wkt=0, add_ball=1):
            d = base_df[wp_cols].copy()
            d["legal_balls_before"] = d["legal_balls_before"] + add_ball
            d["balls_remaining_pre"] = np.maximum(0, d["balls_remaining_pre"] - add_ball)
            d["overid"] = np.minimum(20, (d["legal_balls_before"] // 6) + 1)
            d["score_before"] = d["score_before"] + add_runs
            d["wkts_before"] = np.minimum(10, d["wkts_before"] + add_wkt)
            d["crr_pre_smoothed"] = 6.0 * (d["score_before"] + 8.0) / (d["legal_balls_before"] + 6.0)
            if inn == 2:
                d["runs_required_pre"] = np.maximum(0.0, d["target"] - d["score_before"])
                d["rrr_pre"] = np.where(
                    d["runs_required_pre"] <= 0, 0.0,
                    np.where(d["balls_remaining_pre"] <= 0, 99.0, 6.0 * d["runs_required_pre"] / d["balls_remaining_pre"])
                )
            return d[wp_cols].values

        X_wp = df.loc[sub_mask, wp_cols].values
        y_wp = df.loc[sub_mask, "batting_team_won"].values
        g_wp = df.loc[sub_mask, "match_id"].values

        oof_hgb = np.zeros(sub_mask.sum())
        oof_lr = np.zeros(sub_mask.sum())
        cf_dot = np.zeros(sub_mask.sum())
        cf_four = np.zeros(sub_mask.sum())
        cf_six = np.zeros(sub_mask.sum())
        cf_wkt = np.zeros(sub_mask.sum())

        X_cf_dot = make_cf_df(df.loc[sub_mask], add_runs=0, add_wkt=0, add_ball=1)
        X_cf_four = make_cf_df(df.loc[sub_mask], add_runs=4, add_wkt=0, add_ball=1)
        X_cf_six = make_cf_df(df.loc[sub_mask], add_runs=6, add_wkt=0, add_ball=1)
        X_cf_wkt = make_cf_df(df.loc[sub_mask], add_runs=0, add_wkt=1, add_ball=1)

        # Simple baseline features: Inn1 -> score_before + wkts_before + legal_balls_before; Inn2 -> rrr_pre - 8 + wkts_before
        for tr_idx, va_idx in gkf.split(X_wp, y_wp, g_wp):
            # Simple logistic baseline
            if inn == 1:
                base_tr = np.column_stack([X_wp[tr_idx, 4], X_wp[tr_idx, 5], X_wp[tr_idx, 1]])
                base_va = np.column_stack([X_wp[va_idx, 4], X_wp[va_idx, 5], X_wp[va_idx, 1]])
            else:
                base_tr = np.column_stack([np.clip(X_wp[tr_idx, 9], 0, 36), X_wp[tr_idx, 5], X_wp[tr_idx, 2]])
                base_va = np.column_stack([np.clip(X_wp[va_idx, 9], 0, 36), X_wp[va_idx, 5], X_wp[va_idx, 2]])
            lr = LogisticRegression(C=0.5, max_iter=300)
            lr.fit(base_tr, y_wp[tr_idx])
            oof_lr[va_idx] = lr.predict_proba(base_va)[:, 1]

            # HistGradientBoosting Classifier (smooth monotonic-friendly regularized tree model)
            clf = HistGradientBoostingClassifier(max_depth=4, learning_rate=0.05, max_iter=150, min_samples_leaf=150, l2_regularization=2.0, random_state=42)
            clf.fit(X_wp[tr_idx], y_wp[tr_idx])
            oof_hgb[va_idx] = clf.predict_proba(X_wp[va_idx])[:, 1]
            cf_dot[va_idx] = clf.predict_proba(X_cf_dot[va_idx])[:, 1]
            cf_four[va_idx] = clf.predict_proba(X_cf_four[va_idx])[:, 1]
            cf_six[va_idx] = clf.predict_proba(X_cf_six[va_idx])[:, 1]
            cf_wkt[va_idx] = clf.predict_proba(X_cf_wkt[va_idx])[:, 1]

        # Enforce cricket terminal states identically for counterfactuals in Inn2:
        if inn == 2:
            sub_df_m = df.loc[sub_mask]
            # If after 4 or 6 runs required <= 0 -> WP = 1.0; if balls_rem==1 before delivery and dot/wkt fails target -> WP = 0.0; if wkt leads to 10 down -> WP = 0.0
            cf_four = np.where((sub_df_m["runs_required_pre"].values - 4) <= 0, 1.0, cf_four)
            cf_six = np.where((sub_df_m["runs_required_pre"].values - 6) <= 0, 1.0, cf_six)
            cf_dot = np.where((sub_df_m["balls_remaining_pre"].values == 1) & (sub_df_m["runs_required_pre"].values > 0), 0.0, cf_dot)
            cf_wkt = np.where(
                ((sub_df_m["balls_remaining_pre"].values == 1) & (sub_df_m["runs_required_pre"].values > 0))
                | (sub_df_m["wkts_before"].values >= 9),
                0.0, cf_wkt
            )

        ll_lr, bs_lr, auc_lr, ece_lr = log_loss(y_wp, oof_lr), brier_score_loss(y_wp, oof_lr), roc_auc_score(y_wp, oof_lr), expected_calibration_error(y_wp, oof_lr)
        ll_hg, bs_hg, auc_hg, ece_hg = log_loss(y_wp, oof_hgb), brier_score_loss(y_wp, oof_hgb), roc_auc_score(y_wp, oof_hgb), expected_calibration_error(y_wp, oof_hgb)
        log(f"  Innings {inn} WP OOF GroupKFold (n={sub_mask.sum():,}):")
        log(f"    Simple Logistic Baseline : LogLoss={ll_lr:.4f} | Brier={bs_lr:.4f} | AUC={auc_lr:.4f} | ECE={ece_lr:.4f}")
        log(f"    HistGBR Contextual Model : LogLoss={ll_hg:.4f} | Brier={bs_hg:.4f} | AUC={auc_hg:.4f} | ECE={ece_hg:.4f}")

        df.loc[sub_mask, "wp_pre_oof"] = oof_hgb
        df.loc[sub_mask, "wp_dot_cf"] = cf_dot
        df.loc[sub_mask, "wp_four_cf"] = cf_four
        df.loc[sub_mask, "wp_six_cf"] = cf_six
        df.loc[sub_mask, "wp_wkt_cf"] = cf_wkt

        # Also score non-decided rows (NR/abandoned/super-over matches' inn 1-2) using full fit ONLY for completeness
        rem_mask = sub_all_inn & (~sub_mask)
        if rem_mask.sum() > 0:
            full_clf = HistGradientBoostingClassifier(max_depth=4, learning_rate=0.05, max_iter=150, min_samples_leaf=150, l2_regularization=2.0, random_state=42)
            full_clf.fit(X_wp, y_wp)
            df.loc[rem_mask, "wp_pre_oof"] = full_clf.predict_proba(df.loc[rem_mask, wp_cols].values)[:, 1]
            df.loc[rem_mask, "wp_dot_cf"] = full_clf.predict_proba(make_cf_df(df.loc[rem_mask], 0, 0, 1))[:, 1]
            df.loc[rem_mask, "wp_four_cf"] = full_clf.predict_proba(make_cf_df(df.loc[rem_mask], 4, 0, 1))[:, 1]
            df.loc[rem_mask, "wp_six_cf"] = full_clf.predict_proba(make_cf_df(df.loc[rem_mask], 6, 0, 1))[:, 1]
            df.loc[rem_mask, "wp_wkt_cf"] = full_clf.predict_proba(make_cf_df(df.loc[rem_mask], 0, 1, 1))[:, 1]

    # Counterfactual Leverage Components (all strictly pre-delivery!)
    # Clip negative counterfactual artifacts slightly where tree step might make wp(4) < wp(0) due to sample discretization
    wp_dot = df["wp_dot_cf"].values
    wp_4 = np.maximum(df["wp_four_cf"].values, wp_dot)
    wp_6 = np.maximum(df["wp_six_cf"].values, wp_4)
    wp_w = np.minimum(df["wp_wkt_cf"].values, wp_dot)
    wp0 = df["wp_pre_oof"].values

    df["cf_wkt_drop"] = np.clip(wp0 - wp_w, 0.0, 1.0)         # cost to batting side of a wicket
    df["cf_bnd_gain"] = np.clip(0.65 * wp_4 + 0.35 * wp_6 - wp_dot, 0.0, 1.0)  # swing between boundary and dot
    df["cf_total_swing"] = np.clip(wp_6 - wp_w, 0.0, 1.0)
    # Fixed-weight counterfactual delivery leverage (probability-weighted expected |dWP| relative to pre-delivery WP)
    # Typical T20 frequencies: dot/1/2 (80%), four/six (15%), wicket (5%)
    df["cf_leverage"] = (
        0.80 * np.abs(wp_dot - wp0)
        + 0.15 * np.abs(0.65 * wp_4 + 0.35 * wp_6 - wp0)
        + 0.05 * np.abs(wp_w - wp0)
    )
    # Closeness weight 4*WP*(1-WP) peaks at 1.0 when match is 50-50, drops to 0 in 99%-decided blowouts
    df["wp_closeness"] = np.clip(4.0 * wp0 * (1.0 - wp0), 0.0, 1.0)

    # 4. Separate Cricket-Grounded Batting Pressure Index (BPI) & Bowling Pressure Index (BWPI)
    log("\n[4] SEPARATE BATTING & BOWLING PRESSURE INDICES")

    # Normalize counterfactual components to robust percentiles [0, 1] for index composition
    cf_lev_pct = df["cf_leverage"].rank(pct=True).values
    cf_wkt_pct = df["cf_wkt_drop"].rank(pct=True).values
    cf_bnd_pct = df["cf_bnd_gain"].rank(pct=True).values
    wp_close = df["wp_closeness"].values

    # Domain cricket signals (strictly pre-delivery!):
    # Collapse signal: early/severe wicket loss given balls elapsed
    exp_wkts_par = 4.5 * df["frac_innings_done"].values
    wkt_excess = np.clip((df["wkts_before"].values - exp_wkts_par) / 2.5, 0.0, 1.0)
    early_collapse = np.where(
        ((df["overid"] <= 6) & (df["wkts_before"] >= 2))
        | ((df["overid"] <= 10) & (df["wkts_before"] >= 3))
        | ((df["overid"] <= 15) & (df["wkts_before"] >= 4)),
        1.0, 0.0
    )
    collapse_score = np.clip(0.55 * early_collapse + 0.45 * wkt_excess, 0.0, 1.0)

    # Chase Run-Rate Pressure (Innings 2): RRR minus expected scoring rate & RRR intensity
    # Downweight mathematically dead garbage chases (e.g., needing 42 off 6 -> WP < 0.02, game already lost) EXCEPT partial competitive stress
    rrr_excess = np.where(df["innings"] == 2, np.clip((df["rrr_pre"] - df["exp_rem_rpo"]) / 4.5, 0.0, 1.0), 0.0)
    rrr_level = np.where(df["innings"] == 2, np.clip((df["rrr_pre"] - 7.5) / 5.5, 0.0, 1.0), 0.0)
    live_chase_mult = np.where(df["innings"] == 2, np.clip(df["wp_pre_oof"] / 0.08, 0.15, 1.0), 1.0)
    chase_bat_score = live_chase_mult * np.clip(0.55 * rrr_level + 0.45 * rrr_excess, 0.0, 1.0)

    # Innings 1 scoring deficit vs par + death urgency
    inn1_lag = np.where(df["innings"] == 1, np.clip(df["inn1_deficit_vs_par"] / 28.0, 0.0, 1.0), 0.0)
    death_flag = (df["overid"] >= 16).astype(float)
    stage_bonus = np.where(df["is_final"] == 1, 1.0, np.where(df["is_ko_or_playoff"] == 1, 0.75, np.where(df["stage"].astype(str).str.contains("Super", case=False, na=False), 0.35, 0.0)))

    # BATTING PRESSURE INDEX (BPI, 0-100):
    # Combines Counterfactual WP Leverage & Wicket Hazard + Chase/Collapse/Deficit Stress + Death Endgame + Stage
    bpi_raw = (
        0.35 * (0.55 * cf_lev_pct + 0.45 * cf_wkt_pct) * (0.35 + 0.65 * wp_close)
        + 0.30 * np.where(df["innings"] == 2, chase_bat_score, 0.50 * collapse_score + 0.50 * inn1_lag)
        + 0.20 * collapse_score
        + 0.10 * death_flag * (0.40 + 0.60 * wp_close)
        + 0.05 * stage_bonus * (0.30 + 0.70 * wp_close)
    )
    df["BPI"] = np.round(100.0 * bpi_raw / np.percentile(bpi_raw, 99.5) * 0.92, 2).clip(0.0, 100.0)

    # BOWLING PRESSURE INDEX (BWPI, 0-100):
    # High when: defending contested chase (WP closeness high, boundary cost cf_bnd_pct high, wickets in hand),
    # death overs with live contest, OR defending against rampaging batters (few wickets taken, high CRR vs par)!
    wickets_unbroken = np.clip((1.0 - df["wkts_before"].values / 6.0), 0.0, 1.0)
    # Contested chase range for bowler: RRR between 6 and 13.5 AND batting WP in [0.15, 0.85]
    chase_bowl_danger = np.where(
        df["innings"] == 2,
        wp_close * np.clip(1.0 - np.abs(df["rrr_pre"] - 10.0) / 7.5, 0.1, 1.0) * (0.4 + 0.6 * wickets_unbroken),
        0.0
    )
    # Innings 1 assault / death bowling pressure: facing set batters (>=8.5 CRR or late death overs with wickets in hand)
    assault_inn1 = np.where(
        df["innings"] == 1,
        np.clip((df["crr_pre_smoothed"] - 7.8) / 3.5, 0.0, 1.0) * (0.35 + 0.65 * wickets_unbroken),
        0.0
    )
    bwpi_raw = (
        0.38 * (0.50 * cf_lev_pct + 0.50 * cf_bnd_pct) * (0.30 + 0.70 * wp_close)
        + 0.27 * np.where(df["innings"] == 2, chase_bowl_danger, assault_inn1)
        + 0.22 * death_flag * (0.35 + 0.65 * wp_close)
        + 0.08 * wickets_unbroken * (0.30 + 0.70 * wp_close)
        + 0.05 * stage_bonus * (0.30 + 0.70 * wp_close)
    )
    df["BWPI"] = np.round(100.0 * bwpi_raw / np.percentile(bwpi_raw, 99.5) * 0.92, 2).clip(0.0, 100.0)

    # Compare BPI & BWPI distributions across phases, innings, collapse, chase RRR, and playoff vs league
    log("  Summary of BPI & BWPI by Cricket Context:")
    for lbl, mask in [
        ("All Innings 1-2", pd.Series(True, index=df.index)),
        ("Innings 1", df["innings"] == 1),
        ("Innings 2", df["innings"] == 2),
        ("Powerplay (1-6)", df["phase"] == "PP"),
        ("Middle (7-15)", df["phase"] == "Middle"),
        ("Death (16-20)", df["phase"] == "Death"),
        ("Collapse (w>=3 & ov<=10)", (df["wkts_before"] >= 3) & (df["overid"] <= 10)),
        ("Tight Chase (Inn2 RRR 9-13 & w<=6)", (df["innings"] == 2) & (df["rrr_pre"].between(9, 13)) & (df["wkts_before"] <= 6)),
        ("Dead Blowout (Inn2 RRR>22 or <3)", (df["innings"] == 2) & ((df["rrr_pre"] > 22) | (df["rrr_pre"] < 3))),
        ("Playoffs / Knockouts", df["is_ko_or_playoff"] == 1),
    ]:
        log(f"    {lbl:<36} | n={mask.sum():>6,} | BPI mean={df.loc[mask,'BPI'].mean():5.1f} (p75={df.loc[mask,'BPI'].quantile(0.75):5.1f}) | BWPI mean={df.loc[mask,'BWPI'].mean():5.1f} (p75={df.loc[mask,'BWPI'].quantile(0.75):5.1f})")

    log(f"  Correlation BPI vs BWPI across all deliveries: Pearson r = {df['BPI'].corr(df['BWPI']):.3f}")

    # 5. Threshold Sensitivity Experiment (15%, 20%, 25%, 30% -> top quantiles 85, 80, 75, 70)
    # Plus compare Hybrid BPI/BWPI vs Pure Counterfactual WP Leverage (cf_leverage)!
    log("\n[5] PRESSURE THRESHOLD SENSITIVITY (15%, 20%, 25%, 30%)")
    # Build quick contextual expected runs residual (OOF by match_id) to measure threshold split-half reliability & rank correlation!
    feat_xr = ["innings", "overid", "legal_balls_before", "balls_remaining_pre", "wkts_before", "crr_pre_smoothed", "exp_rem_rpo", "is_t20i"]
    valid_xr = df["is_legal_bat"].values
    X_xr = df.loc[valid_xr, feat_xr].values
    y_xr = df.loc[valid_xr, "runs"].values
    g_xr = df.loc[valid_xr, "match_id"].values
    oof_xr_bat = np.zeros(valid_xr.sum())
    for tr_i, va_i in gkf.split(X_xr, y_xr, g_xr):
        m_xr = HistGradientBoostingRegressor(max_depth=4, learning_rate=0.05, max_iter=100, min_samples_leaf=200, random_state=42)
        m_xr.fit(X_xr[tr_i], y_xr[tr_i])
        oof_xr_bat[va_i] = np.clip(m_xr.predict(X_xr[va_i]), 0.1, 4.5)
    df["exp_runs_bat_quick"] = np.nan
    df.loc[valid_xr, "exp_runs_bat_quick"] = oof_xr_bat
    df["rae_quick"] = df["runs"] - df["exp_runs_bat_quick"]

    # Same quick OOF expected runs conceded for bowling (all deliveries incl wide/nb)
    X_xrb = df[feat_xr].values
    y_xrb = df["bowl_runs_obs"].values
    g_xrb = df["match_id"].values
    oof_xr_bowl = np.zeros(len(df))
    for tr_i, va_i in gkf.split(X_xrb, y_xrb, g_xrb):
        m_xr = HistGradientBoostingRegressor(max_depth=4, learning_rate=0.05, max_iter=100, min_samples_leaf=200, random_state=42)
        m_xr.fit(X_xrb[tr_i], y_xrb[tr_i])
        oof_xr_bowl[va_i] = np.clip(m_xr.predict(X_xrb[va_i]), 0.1, 4.5)
    df["exp_runs_bowl_quick"] = oof_xr_bowl
    df["rpae_quick"] = df["exp_runs_bowl_quick"] - df["bowl_runs_obs"]

    # Assign odd/even match parity per player by chronological match_id for split-half reliability test
    match_order = df[["match_id", "match_date"]].drop_duplicates().sort_values(["match_date", "match_id"]).reset_index(drop=True)
    match_order["match_seq"] = np.arange(len(match_order))
    df = df.merge(match_order[["match_id", "match_seq"]], on="match_id", how="left")

    thresh_rows = []
    # Store rankings for overlap & Spearman matrix
    rank_vectors_bat = {}
    rank_vectors_bowl = {}

    for model_tag, col_b, col_bw in [
        ("Domain_Hybrid_BPI_BWPI", "BPI", "BWPI"),
        ("Pure_Counterfactual_Lev", "cf_leverage", "cf_leverage"),
    ]:
        for pct in [15, 20, 25, 30]:
            q = 1.0 - pct / 100.0
            cut_b = df[col_b].quantile(q)
            cut_bw = df[col_bw].quantile(q)
            pb_mask = (df[col_b] >= cut_b) & df["is_legal_bat"]
            pbw_mask = (df[col_bw] >= cut_bw)

            # Evaluate batters with >= 300 career balls and >= 50 pressure balls at 25% (or min >=30 at 15%)
            bat_sub = df[df["is_legal_bat"]].assign(is_p=(df[col_b] >= cut_b))
            bat_tot = bat_sub.groupby("striker_id").agg(tot_bf=("runs", "count"), p_bf=("is_p", "sum")).reset_index()
            qual_bat_ids = set(bat_tot[(bat_tot["tot_bf"] >= 300) & (bat_tot["p_bf"] >= 40)]["striker_id"])

            # EB shrunk pressure RAE (M0=150)
            bat_p = bat_sub[bat_sub["is_p"] & bat_sub["striker_id"].isin(qual_bat_ids)].copy()
            # Split half by player's chronological match half
            bat_p["half"] = bat_p["match_seq"] % 2
            agg_b = bat_p.groupby("striker_id").agg(n=("rae_quick", "count"), sum_rae=("rae_quick", "sum")).reset_index()
            agg_b["eb_rae"] = agg_b["sum_rae"] / (agg_b["n"] + 150.0) * 100.0  # per 100 balls

            h0 = bat_p[bat_p["half"] == 0].groupby("striker_id").agg(n=("rae_quick", "count"), s=("rae_quick", "sum"))
            h1 = bat_p[bat_p["half"] == 1].groupby("striker_id").agg(n=("rae_quick", "count"), s=("rae_quick", "sum"))
            both_b = h0.join(h1, lsuffix="_0", rsuffix="_1").dropna()
            both_b = both_b[(both_b["n_0"] >= 15) & (both_b["n_1"] >= 15)]
            r0 = both_b["s_0"] / (both_b["n_0"] + 75.0)
            r1 = both_b["s_1"] / (both_b["n_1"] + 75.0)
            split_rho_b = float(spearmanr(r0, r1).statistic) if len(both_b) > 10 else np.nan
            # Spearman-Brown prophecy corrected full-sample reliability: 2*r / (1+r)
            sb_rel_b = (2 * split_rho_b / (1 + split_rho_b)) if split_rho_b > -1 else np.nan

            # Bowlers with >= 300 legal balls and >= 40 pressure deliveries
            bowl_sub = df.assign(is_p=(df[col_bw] >= cut_bw))
            bowl_tot = bowl_sub.groupby("bowler_id").agg(tot_b=("is_legal_bowl", "sum"), p_b=("is_p", "sum")).reset_index()
            qual_bowl_ids = set(bowl_tot[(bowl_tot["tot_b"] >= 300) & (bowl_tot["p_b"] >= 40)]["bowler_id"])

            bowl_p = bowl_sub[bowl_sub["is_p"] & bowl_sub["bowler_id"].isin(qual_bowl_ids)].copy()
            bowl_p["half"] = bowl_p["match_seq"] % 2
            agg_bw = bowl_p.groupby("bowler_id").agg(n=("rpae_quick", "count"), sum_rpae=("rpae_quick", "sum")).reset_index()
            agg_bw["eb_rpae"] = agg_bw["sum_rpae"] / (agg_bw["n"] + 150.0) * 100.0

            hb0 = bowl_p[bowl_p["half"] == 0].groupby("bowler_id").agg(n=("rpae_quick", "count"), s=("rpae_quick", "sum"))
            hb1 = bowl_p[bowl_p["half"] == 1].groupby("bowler_id").agg(n=("rpae_quick", "count"), s=("rpae_quick", "sum"))
            both_bw = hb0.join(hb1, lsuffix="_0", rsuffix="_1").dropna()
            both_bw = both_bw[(both_bw["n_0"] >= 15) & (both_bw["n_1"] >= 15)]
            rb0 = both_bw["s_0"] / (both_bw["n_0"] + 75.0)
            rb1 = both_bw["s_1"] / (both_bw["n_1"] + 75.0)
            split_rho_bw = float(spearmanr(rb0, rb1).statistic) if len(both_bw) > 10 else np.nan
            sb_rel_bw = (2 * split_rho_bw / (1 + split_rho_bw)) if split_rho_bw > -1 else np.nan

            # Bootstrap Top-10 match-cluster stability (200 replicates)
            rng = np.random.default_rng(42)
            # Pre-aggregate per match_id & player for fast cluster bootstrap!
            bp_m = bat_p.groupby(["match_id", "striker_id"])["rae_quick"].agg(["count", "sum"]).reset_index()
            m_ids_b = bp_m["match_id"].unique()
            top10_obs_b = set(agg_b.sort_values("eb_rae", ascending=False).head(10)["striker_id"])
            # Vectorized fast match bootstrap for batters
            ov_b = []
            # Create player->idx & match->list mapping
            pids_b_list = sorted(qual_bat_ids)
            pid_to_i_b = {p: i for i, p in enumerate(pids_b_list)}
            m_to_rows_b = {m: g for m, g in bp_m.groupby("match_id")}
            match_arr_b = np.array(m_ids_b)
            # Build sparse/tuple arrays per match
            m_data_b = [
                (np.array([pid_to_i_b[p] for p in g["striker_id"]]), g["count"].values, g["sum"].values)
                for g in [m_to_rows_b[m] for m in match_arr_b]
            ]
            n_m_b = len(m_data_b)
            n_p_b = len(pids_b_list)
            cnt_mat_b = np.zeros((n_m_b, n_p_b))
            sum_mat_b = np.zeros((n_m_b, n_p_b))
            for mi, (pi, c, s) in enumerate(m_data_b):
                cnt_mat_b[mi, pi] = c
                sum_mat_b[mi, pi] = s
            for _ in range(200):
                idx_m = rng.integers(0, n_m_b, size=n_m_b)
                c_b = cnt_mat_b[idx_m].sum(axis=0)
                s_b = sum_mat_b[idx_m].sum(axis=0)
                sc_b = s_b / (c_b + 150.0)
                t10 = set(pids_b_list[i] for i in np.argsort(-sc_b)[:10])
                ov_b.append(len(t10 & top10_obs_b) / 10.0)

            bwp_m = bowl_p.groupby(["match_id", "bowler_id"])["rpae_quick"].agg(["count", "sum"]).reset_index()
            m_ids_bw = bwp_m["match_id"].unique()
            top10_obs_bw = set(agg_bw.sort_values("eb_rpae", ascending=False).head(10)["bowler_id"])
            pids_bw_list = sorted(qual_bowl_ids)
            pid_to_i_bw = {p: i for i, p in enumerate(pids_bw_list)}
            m_to_rows_bw = {m: g for m, g in bwp_m.groupby("match_id")}
            n_m_bw = len(m_ids_bw)
            n_p_bw = len(pids_bw_list)
            cnt_mat_bw = np.zeros((n_m_bw, n_p_bw))
            sum_mat_bw = np.zeros((n_m_bw, n_p_bw))
            for mi, m in enumerate(m_ids_bw):
                g = m_to_rows_bw[m]
                pi = np.array([pid_to_i_bw[p] for p in g["bowler_id"]])
                cnt_mat_bw[mi, pi] = g["count"].values
                sum_mat_bw[mi, pi] = g["sum"].values
            ov_bw = []
            for _ in range(200):
                idx_m = rng.integers(0, n_m_bw, size=n_m_bw)
                c_w = cnt_mat_bw[idx_m].sum(axis=0)
                s_w = sum_mat_bw[idx_m].sum(axis=0)
                sc_w = s_w / (c_w + 150.0)
                t10 = set(pids_bw_list[i] for i in np.argsort(-sc_w)[:10])
                ov_bw.append(len(t10 & top10_obs_bw) / 10.0)

            rank_vectors_bat[(model_tag, pct)] = agg_b.set_index("striker_id")["eb_rae"]
            rank_vectors_bowl[(model_tag, pct)] = agg_bw.set_index("bowler_id")["eb_rpae"]

            # Cricket interpretability shares in high-pressure bucket:
            hp_b = df[df[col_b] >= cut_b]
            hp_bw = df[df[col_bw] >= cut_bw]
            row = {
                "model": model_tag,
                "top_pct": pct,
                "bpi_cutoff": round(float(cut_b), 3),
                "bwpi_cutoff": round(float(cut_bw), 3),
                "bat_p_deliveries": int(pb_mask.sum()),
                "bowl_p_deliveries": int(pbw_mask.sum()),
                "bat_qual_players": len(qual_bat_ids),
                "bowl_qual_players": len(qual_bowl_ids),
                "bat_median_p_balls": int(agg_b["n"].median()),
                "bowl_median_p_balls": int(agg_bw["n"].median()),
                "bat_split_half_rho": round(split_rho_b, 3),
                "bat_spearman_brown": round(sb_rel_b, 3),
                "bowl_split_half_rho": round(split_rho_bw, 3),
                "bowl_spearman_brown": round(sb_rel_bw, 3),
                "bat_boot_top10_retention": round(float(np.mean(ov_b)), 3),
                "bowl_boot_top10_retention": round(float(np.mean(ov_bw)), 3),
                "bat_pct_inn2": round(100.0 * (hp_b["innings"] == 2).mean(), 1),
                "bat_pct_death": round(100.0 * (hp_b["phase"] == "Death").mean(), 1),
                "bat_pct_playoff": round(100.0 * (hp_b["is_ko_or_playoff"] == 1).mean(), 1),
                "bowl_pct_inn2": round(100.0 * (hp_bw["innings"] == 2).mean(), 1),
                "bowl_pct_death": round(100.0 * (hp_bw["phase"] == "Death").mean(), 1),
            }
            thresh_rows.append(row)

    thresh_df = pd.DataFrame(thresh_rows)
    # Add pairwise Spearman correlation & Top-10 overlap vs 25% threshold within each model
    rho_vs_25_b, top10_vs_25_b = [], []
    rho_vs_25_bw, top10_vs_25_bw = [], []
    for _, r in thresh_df.iterrows():
        mt, pct = r["model"], int(r["top_pct"])
        ref_b = rank_vectors_bat[(mt, 25)]
        cur_b = rank_vectors_bat[(mt, pct)]
        common_b = ref_b.index.intersection(cur_b.index)
        rho_vs_25_b.append(round(float(spearmanr(ref_b.loc[common_b], cur_b.loc[common_b]).statistic), 3))
        t10_ref_b = set(ref_b.sort_values(ascending=False).head(10).index)
        t10_cur_b = set(cur_b.sort_values(ascending=False).head(10).index)
        top10_vs_25_b.append(len(t10_ref_b & t10_cur_b))

        ref_w = rank_vectors_bowl[(mt, 25)]
        cur_w = rank_vectors_bowl[(mt, pct)]
        common_w = ref_w.index.intersection(cur_w.index)
        rho_vs_25_bw.append(round(float(spearmanr(ref_w.loc[common_w], cur_w.loc[common_w]).statistic), 3))
        t10_ref_w = set(ref_w.sort_values(ascending=False).head(10).index)
        t10_cur_w = set(cur_w.sort_values(ascending=False).head(10).index)
        top10_vs_25_bw.append(len(t10_ref_w & t10_cur_w))

    thresh_df["bat_rho_vs_25pct"] = rho_vs_25_b
    thresh_df["bat_top10_overlap_vs_25pct"] = top10_vs_25_b
    thresh_df["bowl_rho_vs_25pct"] = rho_vs_25_bw
    thresh_df["bowl_top10_overlap_vs_25pct"] = top10_vs_25_bw

    # Also compare Domain_Hybrid 25% vs Pure_Counterfactual_Lev 25%
    c_b = rank_vectors_bat[("Domain_Hybrid_BPI_BWPI", 25)].index.intersection(rank_vectors_bat[("Pure_Counterfactual_Lev", 25)].index)
    c_w = rank_vectors_bowl[("Domain_Hybrid_BPI_BWPI", 25)].index.intersection(rank_vectors_bowl[("Pure_Counterfactual_Lev", 25)].index)
    log("\n  Threshold Sensitivity Table:")
    log(thresh_df.to_string(index=False))
    log(f"\n  Cross-Model Agreement at 25% Cutoff (Domain_Hybrid vs Pure_Counterfactual):")
    log(f"    Batting Spearman rho={spearmanr(rank_vectors_bat[('Domain_Hybrid_BPI_BWPI', 25)].loc[c_b], rank_vectors_bat[('Pure_Counterfactual_Lev', 25)].loc[c_b]).statistic:.3f}")
    log(f"    Bowling Spearman rho={spearmanr(rank_vectors_bowl[('Domain_Hybrid_BPI_BWPI', 25)].loc[c_w], rank_vectors_bowl[('Pure_Counterfactual_Lev', 25)].loc[c_w]).statistic:.3f}")

    thresh_df.to_csv(os.path.join(OUT_DIR, "THRESHOLD_SENSITIVITY.csv"), index=False)

    # Save enriched delivery DataFrame for 04_batting_bowling_models_and_cppi.py
    df.to_pickle(os.path.join(OUT_DIR, "bbb_enriched.pkl"))
    so_bbb.to_pickle(os.path.join(OUT_DIR, "so_bbb.pkl"))

    # Create Pressure & Threshold Sensitivity Diagnostic Chart
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), dpi=160)
    dom = thresh_df[thresh_df["model"] == "Domain_Hybrid_BPI_BWPI"]
    pcf = thresh_df[thresh_df["model"] == "Pure_Counterfactual_Lev"]

    axes[0].plot(dom["top_pct"], dom["bat_spearman_brown"], "o-", lw=2, label="Bat (Domain BPI)")
    axes[0].plot(dom["top_pct"], dom["bowl_spearman_brown"], "s-", lw=2, label="Bowl (Domain BWPI)")
    axes[0].plot(pcf["top_pct"], pcf["bat_spearman_brown"], "o--", alpha=0.7, label="Bat (Pure CF Lev)")
    axes[0].plot(pcf["top_pct"], pcf["bowl_spearman_brown"], "s--", alpha=0.7, label="Bowl (Pure CF Lev)")
    axes[0].set_title("Split-Half Spearman-Brown Reliability")
    axes[0].set_xlabel("High-Pressure Top Percentile (%)")
    axes[0].set_ylabel("Reliability (2r / (1+r))")
    axes[0].set_xticks([15, 20, 25, 30])
    axes[0].grid(alpha=0.25)
    axes[0].legend(fontsize=8)

    axes[1].plot(dom["top_pct"], dom["bat_boot_top10_retention"], "o-", lw=2, label="Bat Top-10 Stability")
    axes[1].plot(dom["top_pct"], dom["bowl_boot_top10_retention"], "s-", lw=2, label="Bowl Top-10 Stability")
    axes[1].set_title("Match-Cluster Bootstrap Top-10 Retention")
    axes[1].set_xlabel("High-Pressure Top Percentile (%)")
    axes[1].set_ylabel("Mean Overlap Fraction (0-1)")
    axes[1].set_xticks([15, 20, 25, 30])
    axes[1].grid(alpha=0.25)
    axes[1].legend(fontsize=8)

    # WP Pre calibration curve (Inn 2)
    inn2_m = wp_mask & (df["innings"] == 2)
    bins = np.linspace(0, 1, 11)
    y_i2 = df.loc[inn2_m, "batting_team_won"].values
    p_i2 = df.loc[inn2_m, "wp_pre_oof"].values
    bx, by = [], []
    for i in range(10):
        m_b = (p_i2 >= bins[i]) & (p_i2 < bins[i+1] if i < 9 else p_i2 <= bins[i+1])
        if m_b.sum() > 20:
            bx.append(p_i2[m_b].mean())
            by.append(y_i2[m_b].mean())
    axes[2].plot([0, 1], [0, 1], "k--", lw=1, label="Perfect Calibration")
    axes[2].plot(bx, by, "o-", lw=2, color="#D11E68", label="OOF WP (Inn 2)")
    axes[2].set_title("Out-of-Fold Chase WP Calibration")
    axes[2].set_xlabel("Predicted Batting Win Probability")
    axes[2].set_ylabel("Observed Win Frequency")
    axes[2].grid(alpha=0.25)
    axes[2].legend(fontsize=8)

    plt.tight_layout()
    chart_path = os.path.join(CHART_DIR, "01_wp_calibration_and_thresholds.png")
    plt.savefig(chart_path)
    plt.close()

    out_txt = os.path.join(OUT_DIR, "03_delivery_state_and_pressure_report.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log(f"\nSaved: {out_txt}")
    log(f"Saved: {os.path.join(OUT_DIR, 'THRESHOLD_SENSITIVITY.csv')}")
    log(f"Saved: {chart_path}")


if __name__ == "__main__":
    main()

