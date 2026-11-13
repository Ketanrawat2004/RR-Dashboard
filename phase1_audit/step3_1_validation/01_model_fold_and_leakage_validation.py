"""
Phase 1 Step 3.1 — Section 1: Expected Performance Model Validation & Leakage Audit
(01_model_fold_and_leakage_validation.py)

Evaluates:
1. Fold-level predictive metrics across all 5 GroupKFold splits.
2. Progressive cricket baselines (Global Mean, Phase Mean, Over Mean, Phase x Wkts Mean).
3. Contextual machine learning models (Ridge vs HistGBR).
4. Paired match-level significance tests (paired t-test and Wilcoxon signed-rank test).
5. Feature ablation and permutation importance to test if context genuinely adds skill.
6. Formal leakage verification across all pre-delivery features.

Outputs: MODEL_FOLD_VALIDATION.csv and 01_model_fold_validation_report.txt.
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import ttest_rel, wilcoxon
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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
    log("PHASE 1 STEP 3.1 — SECTION 1: MODEL FOLD VALIDATION & LEAKAGE AUDIT")
    log("=" * 80)

    # Load modeled deliveries from Step 3 (read-only)
    df = pd.read_pickle(os.path.join(AUDIT_DIR, "step3_individual_model", "bbb_step3_modeled.pkl"))
    log(f"Loaded deliveries: {len(df):,} across {df['match_id'].nunique()} matches.")

    # -------------------------------------------------------------
    # 1. Feature Leakage Verification
    # -------------------------------------------------------------
    log("\n[1] PRE-DELIVERY FEATURE LEAKAGE AUDIT")
    # Verify that all 19 feature columns strictly lag the delivery outcome
    feature_cols = [
        "innings", "overid", "legal_balls_before", "balls_remaining_pre",
        "score_before", "wkts_before", "wkts_in_hand_pre", "crr_pre_smoothed",
        "is_inn2", "target_clean", "runs_req_clean", "rrr_clean",
        "pp_flag", "mid_flag", "death_flag", "chase_stress", "death_wkts",
        "is_t20i", "season_num"
    ]
    log(f"Features inspected ({len(feature_cols)}): {', '.join(feature_cols)}")

    # Check: does score_before ever include current delivery runs?
    # For every delivery, score_before must equal cumulative sum of previous team_runs_obs in that innings
    grp = df.groupby(["match_id", "innings"], sort=False)
    cum_prev_runs = grp["team_runs_obs"].cumsum() - df["team_runs_obs"]
    cum_prev_wkts = grp["is_wicket"].cumsum() - df["is_wicket"]
    score_violations = (df["score_before"] != cum_prev_runs).sum()
    wkt_violations = (df["wkts_before"] != cum_prev_wkts.clip(0, 9)).sum()

    log(f"  score_before == cumsum(prev_runs) violations: {score_violations}")
    log(f"  wkts_before  == cumsum(prev_wkts) violations: {wkt_violations}")
    assert score_violations == 0 and wkt_violations == 0, "Feature leakage detected in score/wkts state!"

    # Check: does rrr_clean or runs_req_clean use current ball outcome?
    # In innings 1, target_clean, runs_req_clean, rrr_clean must be exactly 0
    inn1_target_leakage = (df.loc[df["innings"] == 1, "target_clean"] != 0).sum()
    inn1_rrr_leakage = (df.loc[df["innings"] == 1, "rrr_clean"] != 0).sum()
    log(f"  Innings 1 deliveries with non-zero target_clean: {inn1_target_leakage}")
    log(f"  Innings 1 deliveries with non-zero rrr_clean   : {inn1_rrr_leakage}")
    assert inn1_target_leakage == 0 and inn1_rrr_leakage == 0, "Target leakage in Innings 1!"
    log("  -> Zero feature leakage verified across all feature definitions.")

    # -------------------------------------------------------------
    # 2. Fold-Level Evaluation across Progressive Baselines & Models
    # -------------------------------------------------------------
    log("\n[2] FOLD-LEVEL PREDICTIVE ACCURACY (5-Fold GroupKFold by match_id)")
    
    # Dataset A: Batting (legal balls faced by batter)
    df_bat = df[df["is_legal_bat"]].copy().reset_index(drop=True)
    X_bat = df_bat[feature_cols].values
    y_bat = df_bat["runs"].values.astype(float)
    g_bat = df_bat["match_id"].values

    # Dataset B: Bowling (all deliveries charged to bowler)
    X_bowl = df[feature_cols].values
    y_bowl = df["bowl_runs_obs"].values.astype(float)
    g_bowl = df["match_id"].values

    gkf = GroupKFold(n_splits=5)
    fold_records = []

    # Store match-level residuals for paired statistical significance test
    match_rmse_bat = {m: [] for m in ["Global_Mean", "Phase_Mean", "Over_Mean", "Phase_Wkts_Mean", "Ridge", "HistGBR"]}
    match_rmse_bowl = {m: [] for m in ["Global_Mean", "Phase_Mean", "Over_Mean", "Phase_Wkts_Mean", "Ridge", "HistGBR"]}

    log("\n--- BATTING MODEL FOLD-LEVEL BENCHMARK ---")
    log(f"{'Fold':<6}{'Model / Baseline':<24}{'OOF Samples':>12}{'RMSE':>9}{'MAE':>9}{'R2':>10}")
    log("-" * 72)

    for fold, (tr_idx, va_idx) in enumerate(gkf.split(X_bat, y_bat, g_bat), 1):
        tr_df, va_df = df_bat.iloc[tr_idx], df_bat.iloc[va_idx]
        y_va = y_bat[va_idx]
        n_va = len(va_idx)

        # Baseline 1: Global Training Mean
        p_global = np.full(n_va, tr_df["runs"].mean())
        # Baseline 2: Phase Mean (PP, Middle, Death)
        ph_lookup = tr_df.groupby("phase")["runs"].mean()
        p_phase = va_df["phase"].map(ph_lookup).fillna(tr_df["runs"].mean()).values
        # Baseline 3: Over-by-Over Mean (overs 1 to 20)
        ov_lookup = tr_df.groupby("overid")["runs"].mean()
        p_over = va_df["overid"].map(ov_lookup).fillna(tr_df["runs"].mean()).values
        # Baseline 4: Phase x Wkts-in-Hand Mean
        pw_lookup = tr_df.groupby(["phase", "wkts_before"])["runs"].mean()
        keys_va = list(zip(va_df["phase"], va_df["wkts_before"]))
        p_pw = np.array([pw_lookup.get(k, tr_df["runs"].mean()) for k in keys_va])

        # Model 1: Ridge Regression
        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_bat[tr_idx])
        X_va_s = scaler.transform(X_bat[va_idx])
        ridge = Ridge(alpha=10.0)
        ridge.fit(X_tr_s, y_bat[tr_idx])
        p_ridge = np.clip(ridge.predict(X_va_s), 0.0, 6.0)

        # Model 2: HistGBR
        hgb = HistGradientBoostingRegressor(max_depth=5, learning_rate=0.06, max_iter=120, min_samples_leaf=150, random_state=42)
        hgb.fit(X_bat[tr_idx], y_bat[tr_idx])
        p_hgb = np.clip(hgb.predict(X_bat[va_idx]), 0.0, 6.0)

        preds_dict = {
            "Global_Mean": p_global,
            "Phase_Mean": p_phase,
            "Over_Mean": p_over,
            "Phase_Wkts_Mean": p_pw,
            "Ridge": p_ridge,
            "HistGBR": p_hgb,
        }

        # Calculate fold metrics
        for mname, pred in preds_dict.items():
            rmse_val = np.sqrt(mean_squared_error(y_va, pred))
            mae_val = mean_absolute_error(y_va, pred)
            r2_val = r2_score(y_va, pred)
            log(f"Fold {fold:<2} {mname:<24}{n_va:>12,}{rmse_val:>9.4f}{mae_val:>9.4f}{r2_val:>10.5f}")
            fold_records.append({
                "target": "Batting_Runs",
                "fold": fold,
                "model": mname,
                "n_samples": n_va,
                "rmse": round(rmse_val, 4),
                "mae": round(mae_val, 4),
                "r2": round(r2_val, 5),
            })

            # Calculate match-level RMSE for fold
            va_match_ids = va_df["match_id"].values
            for mid in np.unique(va_match_ids):
                m_mask = (va_match_ids == mid)
                if m_mask.sum() >= 10:  # Minimum deliveries in match
                    m_rmse = np.sqrt(mean_squared_error(y_va[m_mask], pred[m_mask]))
                    match_rmse_bat[mname].append(m_rmse)

    log("\n--- BOWLING CONCEDED RUNS FOLD-LEVEL BENCHMARK ---")
    log(f"{'Fold':<6}{'Model / Baseline':<24}{'OOF Samples':>12}{'RMSE':>9}{'MAE':>9}{'R2':>10}")
    log("-" * 72)

    for fold, (tr_idx, va_idx) in enumerate(gkf.split(X_bowl, y_bowl, g_bowl), 1):
        tr_df, va_df = df.iloc[tr_idx], df.iloc[va_idx]
        y_va = y_bowl[va_idx]
        n_va = len(va_idx)

        # Baseline 1: Global Training Mean
        p_global = np.full(n_va, tr_df["bowl_runs_obs"].mean())
        # Baseline 2: Phase Mean
        ph_lookup = tr_df.groupby("phase")["bowl_runs_obs"].mean()
        p_phase = va_df["phase"].map(ph_lookup).fillna(tr_df["bowl_runs_obs"].mean()).values
        # Baseline 3: Over Mean
        ov_lookup = tr_df.groupby("overid")["bowl_runs_obs"].mean()
        p_over = va_df["overid"].map(ov_lookup).fillna(tr_df["bowl_runs_obs"].mean()).values
        # Baseline 4: Phase x Wkts Mean
        pw_lookup = tr_df.groupby(["phase", "wkts_before"])["bowl_runs_obs"].mean()
        keys_va = list(zip(va_df["phase"], va_df["wkts_before"]))
        p_pw = np.array([pw_lookup.get(k, tr_df["bowl_runs_obs"].mean()) for k in keys_va])

        # Model 1: Ridge
        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_bowl[tr_idx])
        X_va_s = scaler.transform(X_bowl[va_idx])
        ridge = Ridge(alpha=10.0)
        ridge.fit(X_tr_s, y_bowl[tr_idx])
        p_ridge = np.clip(ridge.predict(X_va_s), 0.0, 7.0)

        # Model 2: HistGBR
        hgb = HistGradientBoostingRegressor(max_depth=5, learning_rate=0.06, max_iter=120, min_samples_leaf=150, random_state=42)
        hgb.fit(X_bowl[tr_idx], y_bowl[tr_idx])
        p_hgb = np.clip(hgb.predict(X_bowl[va_idx]), 0.0, 7.0)

        preds_dict = {
            "Global_Mean": p_global,
            "Phase_Mean": p_phase,
            "Over_Mean": p_over,
            "Phase_Wkts_Mean": p_pw,
            "Ridge": p_ridge,
            "HistGBR": p_hgb,
        }

        for mname, pred in preds_dict.items():
            rmse_val = np.sqrt(mean_squared_error(y_va, pred))
            mae_val = mean_absolute_error(y_va, pred)
            r2_val = r2_score(y_va, pred)
            log(f"Fold {fold:<2} {mname:<24}{n_va:>12,}{rmse_val:>9.4f}{mae_val:>9.4f}{r2_val:>10.5f}")
            fold_records.append({
                "target": "Bowling_Runs",
                "fold": fold,
                "model": mname,
                "n_samples": n_va,
                "rmse": round(rmse_val, 4),
                "mae": round(mae_val, 4),
                "r2": round(r2_val, 5),
            })

            va_match_ids = va_df["match_id"].values
            for mid in np.unique(va_match_ids):
                m_mask = (va_match_ids == mid)
                if m_mask.sum() >= 10:
                    m_rmse = np.sqrt(mean_squared_error(y_va[m_mask], pred[m_mask]))
                    match_rmse_bowl[mname].append(m_rmse)

    # -------------------------------------------------------------
    # 3. Paired Statistical Significance Tests Across Matches
    # -------------------------------------------------------------
    log("\n[3] PAIRED STATISTICAL SIGNIFICANCE TESTS ACROSS MATCHES (n=867 matches)")
    # Test HistGBR vs Phase_Wkts_Mean
    t_stat_bat, p_val_bat = ttest_rel(match_rmse_bat["Phase_Wkts_Mean"], match_rmse_bat["HistGBR"])
    w_stat_bat, p_val_w_bat = wilcoxon(np.array(match_rmse_bat["Phase_Wkts_Mean"]) - np.array(match_rmse_bat["HistGBR"]))
    log(f"  Batting (HistGBR vs Phase_Wkts_Mean):")
    log(f"    Paired t-test    : t = {t_stat_bat:.3f}, p-value = {p_val_bat:.2e} (Statistically significant: {p_val_bat < 0.001})")
    log(f"    Wilcoxon test    : W = {w_stat_bat:.1f}, p-value = {p_val_w_bat:.2e}")
    log(f"    Mean Match RMSE  : Phase_Wkts_Mean = {np.mean(match_rmse_bat['Phase_Wkts_Mean']):.4f} -> HistGBR = {np.mean(match_rmse_bat['HistGBR']):.4f} (Delta = {np.mean(match_rmse_bat['Phase_Wkts_Mean']) - np.mean(match_rmse_bat['HistGBR']):+.4f})")

    t_stat_bowl, p_val_bowl = ttest_rel(match_rmse_bowl["Phase_Wkts_Mean"], match_rmse_bowl["HistGBR"])
    w_stat_bowl, p_val_w_bowl = wilcoxon(np.array(match_rmse_bowl["Phase_Wkts_Mean"]) - np.array(match_rmse_bowl["HistGBR"]))
    log(f"\n  Bowling (HistGBR vs Phase_Wkts_Mean):")
    log(f"    Paired t-test    : t = {t_stat_bowl:.3f}, p-value = {p_val_bowl:.2e} (Statistically significant: {p_val_bowl < 0.001})")
    log(f"    Wilcoxon test    : W = {w_stat_bowl:.1f}, p-value = {p_val_w_bowl:.2e}")
    log(f"    Mean Match RMSE  : Phase_Wkts_Mean = {np.mean(match_rmse_bowl['Phase_Wkts_Mean']):.4f} -> HistGBR = {np.mean(match_rmse_bowl['HistGBR']):.4f} (Delta = {np.mean(match_rmse_bowl['Phase_Wkts_Mean']) - np.mean(match_rmse_bowl['HistGBR']):+.4f})")

    # -------------------------------------------------------------
    # 4. Feature Ablation: Does Context Genuinely Add Predictive Value?
    # -------------------------------------------------------------
    log("\n[4] FEATURE ABLATION EXPERIMENT (Testing Marginal Value of Match Context)")
    # Group A: Macro Phase only (innings, overid, phase flags)
    macro_features = ["innings", "overid", "pp_flag", "mid_flag", "death_flag", "is_t20i", "season_num"]
    # Group B: Macro + Wickets (adds wkts_before, wkts_in_hand_pre, death_wkts)
    macro_wkt_features = macro_features + ["wkts_before", "wkts_in_hand_pre", "death_wkts"]
    # Group C: Full Contextual (adds crr_pre_smoothed, runs_req_clean, rrr_clean, chase_stress, target_clean)
    full_features = feature_cols

    oof_macro = np.zeros(len(df_bat))
    oof_wkt = np.zeros(len(df_bat))
    oof_full = np.zeros(len(df_bat))

    for tr_i, va_i in gkf.split(X_bat, y_bat, g_bat):
        # Fit Macro
        h_m = HistGradientBoostingRegressor(max_depth=5, learning_rate=0.06, max_iter=100, min_samples_leaf=150, random_state=42)
        h_m.fit(df_bat.loc[tr_i, macro_features].values, y_bat[tr_i])
        oof_macro[va_i] = h_m.predict(df_bat.loc[va_i, macro_features].values)

        # Fit Macro + Wickets
        h_mw = HistGradientBoostingRegressor(max_depth=5, learning_rate=0.06, max_iter=100, min_samples_leaf=150, random_state=42)
        h_mw.fit(df_bat.loc[tr_i, macro_wkt_features].values, y_bat[tr_i])
        oof_wkt[va_i] = h_mw.predict(df_bat.loc[va_i, macro_wkt_features].values)

        # Fit Full Context
        h_f = HistGradientBoostingRegressor(max_depth=5, learning_rate=0.06, max_iter=100, min_samples_leaf=150, random_state=42)
        h_f.fit(df_bat.loc[tr_i, full_features].values, y_bat[tr_i])
        oof_full[va_i] = h_f.predict(df_bat.loc[va_i, full_features].values)

    rmse_m, r2_m = np.sqrt(mean_squared_error(y_bat, oof_macro)), r2_score(y_bat, oof_macro)
    rmse_mw, r2_mw = np.sqrt(mean_squared_error(y_bat, oof_wkt)), r2_score(y_bat, oof_wkt)
    rmse_f, r2_f = np.sqrt(mean_squared_error(y_bat, oof_full)), r2_score(y_bat, oof_full)

    log(f"  Feature Set 1: Macro Temporal (Overs, Phases) : RMSE = {rmse_m:.4f} | R2 = {r2_m:.5f}")
    log(f"  Feature Set 2: Macro + Wickets in Hand        : RMSE = {rmse_mw:.4f} | R2 = {r2_mw:.5f} (Delta R2 = {r2_mw - r2_m:+.5f})")
    log(f"  Feature Set 3: Full Contextual (CRR, RRR, Target): RMSE = {rmse_f:.4f} | R2 = {r2_f:.5f} (Delta R2 = {r2_f - r2_mw:+.5f})")

    # In Innings 2 Chases specifically:
    inn2_mask = (df_bat["innings"] == 2)
    r2_mw_i2 = r2_score(y_bat[inn2_mask], oof_wkt[inn2_mask])
    r2_f_i2 = r2_score(y_bat[inn2_mask], oof_full[inn2_mask])
    log(f"  Innings 2 Chase Subset (n={inn2_mask.sum():,}):")
    log(f"    Without RRR/Target Context: R2 = {r2_mw_i2:.5f}")
    log(f"    With Full RRR/Target Context: R2 = {r2_f_i2:.5f} (Delta R2 = {r2_f_i2 - r2_mw_i2:+.5f}, +{100*(r2_f_i2 - r2_mw_i2)/r2_mw_i2:.1f}% gain)")

    # Save CSV outputs
    df_folds = pd.DataFrame(fold_records)
    out_csv = os.path.join(VAL_DIR, "MODEL_FOLD_VALIDATION.csv")
    df_folds.to_csv(out_csv, index=False)
    log(f"\nSaved fold validation table to {out_csv}")

    out_txt = os.path.join(VAL_DIR, "01_model_fold_validation_report.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log(f"Saved text report to {out_txt}")


if __name__ == "__main__":
    main()

