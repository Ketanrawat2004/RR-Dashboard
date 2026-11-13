"""
Phase 1 Step 3 — Tasks 2 & 3: Batting and Bowling Expected Performance Models
(02_train_batting_bowling_models.py)

Trains contextual expected performance models strictly pre-delivery:
1. Batting Expected Runs Model (E[runs_bat] on legal balls faced)
2. Bowling Expected Runs Conceded Model (E[runs_bowl] on all bowler deliveries)
3. Bowling Expected Wicket Model (P(bowler_wkt) on all bowler deliveries)

Evaluates via GroupKFold(5) by match_id across:
- Baseline (Empirical Context Mean)
- Regularized Linear / Logistic Regression (Ridge / LogisticRegression)
- Contextual Tree Model (HistGradientBoosting)

Outputs model metrics, phase & pressure segmentations, and enriched predictions.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, log_loss, brier_score_loss, roc_auc_score

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit")
STEP3_DIR = os.path.join(AUDIT_DIR, "step3_individual_model")
os.makedirs(STEP3_DIR, exist_ok=True)


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
    log("PHASE 1 STEP 3 — TASKS 2 & 3: EXPECTED PERFORMANCE MODELING")
    log("=" * 80)

    # 1. Load Enriched Delivery Dataset
    df = pd.read_pickle(os.path.join(AUDIT_DIR, "bbb_enriched.pkl"))
    log(f"Loaded bbb_enriched.pkl: {len(df):,} deliveries across {df['match_id'].nunique()} matches.")

    # High-pressure definition established in Step 2:
    cut_b = df["BPI"].quantile(0.75)
    cut_bw = df["BWPI"].quantile(0.75)
    df["is_hp_bat"] = df["BPI"] >= cut_b
    df["is_hp_bowl"] = df["BWPI"] >= cut_bw
    log(f"High-Pressure Thresholds (25% Cutoff): BPI >= {cut_b:.3f} | BWPI >= {cut_bw:.3f}")

    # Feature Engineering (strictly pre-delivery)
    df["is_inn2"] = (df["innings"] == 2).astype(int)
    df["target_clean"] = df["target"].fillna(0.0)
    df["runs_req_clean"] = df["runs_required_pre"].fillna(0.0)
    df["rrr_clean"] = np.clip(df["rrr_pre"].fillna(0.0), 0.0, 36.0)
    df["pp_flag"] = (df["phase"] == "PP").astype(int)
    df["mid_flag"] = (df["phase"] == "Middle").astype(int)
    df["death_flag"] = (df["phase"] == "Death").astype(int)
    df["chase_stress"] = df["is_inn2"] * df["rrr_clean"]
    df["death_wkts"] = df["death_flag"] * df["wkts_in_hand_pre"]

    feature_cols = [
        "innings", "overid", "legal_balls_before", "balls_remaining_pre",
        "score_before", "wkts_before", "wkts_in_hand_pre", "crr_pre_smoothed",
        "is_inn2", "target_clean", "runs_req_clean", "rrr_clean",
        "pp_flag", "mid_flag", "death_flag", "chase_stress", "death_wkts",
        "is_t20i", "season_num"
    ]

    gkf = GroupKFold(n_splits=5)
    model_comparison_results = []

    # =========================================================================
    # TASK 2: BATTING EXPECTED RUNS MODEL (E[runs_bat])
    # Evaluated strictly on legal balls faced by batter (excludes wides)
    # =========================================================================
    log("\n" + "=" * 60)
    log("[TASK 2] BATTING EXPECTED RUNS MODEL (Target: df['runs'])")
    log("=" * 60)

    bat_mask = df["is_legal_bat"].values
    df_bat = df[bat_mask].copy().reset_index(drop=True)
    X_bat = df_bat[feature_cols].values
    y_bat = df_bat["runs"].values.astype(float)
    g_bat = df_bat["match_id"].values

    log(f"Batting dataset size: {len(df_bat):,} legal balls faced across {len(np.unique(g_bat))} matches.")

    oof_bat_base = np.zeros(len(df_bat))
    oof_bat_ridge = np.zeros(len(df_bat))
    oof_bat_hgb = np.zeros(len(df_bat))

    for fold, (tr_idx, va_idx) in enumerate(gkf.split(X_bat, y_bat, g_bat), 1):
        tr_df, va_df = df_bat.iloc[tr_idx], df_bat.iloc[va_idx]
        
        # 1. Simple Baseline: Mean by (innings, phase, wkts_before)
        mean_lookup = tr_df.groupby(["innings", "phase", "wkts_before"])["runs"].mean()
        global_mean = tr_df["runs"].mean()
        keys_va = list(zip(va_df["innings"], va_df["phase"], va_df["wkts_before"]))
        oof_bat_base[va_idx] = np.array([mean_lookup.get(k, global_mean) for k in keys_va])

        # 2. Regularized Regression (Ridge with StandardScaler)
        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_bat[tr_idx])
        X_va_s = scaler.transform(X_bat[va_idx])
        ridge = Ridge(alpha=10.0)
        ridge.fit(X_tr_s, y_bat[tr_idx])
        oof_bat_ridge[va_idx] = np.clip(ridge.predict(X_va_s), 0.0, 6.0)

        # 3. Contextual Tree Model (HistGradientBoostingRegressor)
        hgb = HistGradientBoostingRegressor(max_depth=5, learning_rate=0.06, max_iter=120, min_samples_leaf=150, random_state=42)
        hgb.fit(X_bat[tr_idx], y_bat[tr_idx])
        oof_bat_hgb[va_idx] = np.clip(hgb.predict(X_bat[va_idx]), 0.0, 6.0)

    # Evaluate Batting Models
    for name, pred in [("Bat Baseline (Phase+Wkts)", oof_bat_base), ("Bat Ridge Regression", oof_bat_ridge), ("Bat HistGBR (Contextual)", oof_bat_hgb)]:
        rmse = np.sqrt(mean_squared_error(y_bat, pred))
        mae = mean_absolute_error(y_bat, pred)
        r2 = r2_score(y_bat, pred)
        log(f"  {name:<26}: RMSE={rmse:.4f} | MAE={mae:.4f} | R2={r2:.5f}")
        model_comparison_results.append({"task": "Batting_Runs", "model": name, "rmse": round(rmse, 4), "mae": round(mae, 4), "r2": round(r2, 5)})

    df_bat["exp_bat_runs"] = oof_bat_hgb
    df_bat["rae"] = df_bat["runs"] - df_bat["exp_bat_runs"]

    # Phase Breakdown of Batting Model
    log("\n  Batting Model Performance Across Innings Phases:")
    for ph in ["PP", "Middle", "Death"]:
        m_ph = (df_bat["phase"] == ph)
        y_p, pr_p = y_bat[m_ph], oof_bat_hgb[m_ph]
        rmse_p = np.sqrt(mean_squared_error(y_p, pr_p))
        mae_p = mean_absolute_error(y_p, pr_p)
        actual_sr = 100.0 * y_p.mean()
        exp_sr = 100.0 * pr_p.mean()
        log(f"    Phase {ph:<6} (n={m_ph.sum():>6,}): Actual SR={actual_sr:5.1f} | Exp SR={exp_sr:5.1f} | RMSE={rmse_p:.4f} | MAE={mae_p:.4f}")

    # Pressure Category Breakdown of Batting Model
    log("\n  Batting Model Performance Across Pressure Categories:")
    for cat_name, m_cat in [("Non-Pressure (<25% BPI)", ~df_bat["is_hp_bat"]), ("High-Pressure (>=25% BPI)", df_bat["is_hp_bat"])]:
        y_c, pr_c = y_bat[m_cat], oof_bat_hgb[m_cat]
        rmse_c = np.sqrt(mean_squared_error(y_c, pr_c))
        actual_sr = 100.0 * y_c.mean()
        exp_sr = 100.0 * pr_c.mean()
        dot_pct = 100.0 * (y_c == 0).mean()
        bnd_pct = 100.0 * np.isin(y_c, [4, 6]).mean()
        log(f"    {cat_name:<28} (n={m_cat.sum():>6,}): Actual SR={actual_sr:5.1f} | Exp SR={exp_sr:5.1f} | Dot%={dot_pct:4.1f}% | Bnd%={bnd_pct:4.1f}% | RMSE={rmse_c:.4f}")

    # =========================================================================
    # TASK 3: BOWLING EXPECTED CONCEDED RUNS MODEL (E[runs_bowl])
    # Evaluated on all deliveries bowled (includes wides & no-balls)
    # =========================================================================
    log("\n" + "=" * 60)
    log("[TASK 3A] BOWLING EXPECTED RUNS CONCEDED MODEL (Target: df['bowl_runs_obs'])")
    log("=" * 60)

    X_bowl = df[feature_cols].values
    y_bowl_runs = df["bowl_runs_obs"].values.astype(float)
    g_bowl = df["match_id"].values

    oof_bowl_base = np.zeros(len(df))
    oof_bowl_ridge = np.zeros(len(df))
    oof_bowl_hgb = np.zeros(len(df))

    for fold, (tr_idx, va_idx) in enumerate(gkf.split(X_bowl, y_bowl_runs, g_bowl), 1):
        tr_df, va_df = df.iloc[tr_idx], df.iloc[va_idx]
        
        # 1. Simple Baseline: Mean by (innings, phase, wkts_before)
        mean_lookup = tr_df.groupby(["innings", "phase", "wkts_before"])["bowl_runs_obs"].mean()
        global_mean = tr_df["bowl_runs_obs"].mean()
        keys_va = list(zip(va_df["innings"], va_df["phase"], va_df["wkts_before"]))
        oof_bowl_base[va_idx] = np.array([mean_lookup.get(k, global_mean) for k in keys_va])

        # 2. Regularized Regression (Ridge with StandardScaler)
        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_bowl[tr_idx])
        X_va_s = scaler.transform(X_bowl[va_idx])
        ridge = Ridge(alpha=10.0)
        ridge.fit(X_tr_s, y_bowl_runs[tr_idx])
        oof_bowl_ridge[va_idx] = np.clip(ridge.predict(X_va_s), 0.0, 7.0)

        # 3. Contextual Tree Model (HistGradientBoostingRegressor)
        hgb = HistGradientBoostingRegressor(max_depth=5, learning_rate=0.06, max_iter=120, min_samples_leaf=150, random_state=42)
        hgb.fit(X_bowl[tr_idx], y_bowl_runs[tr_idx])
        oof_bowl_hgb[va_idx] = np.clip(hgb.predict(X_bowl[va_idx]), 0.0, 7.0)

    for name, pred in [("BowlRuns Baseline", oof_bowl_base), ("BowlRuns Ridge", oof_bowl_ridge), ("BowlRuns HistGBR", oof_bowl_hgb)]:
        rmse = np.sqrt(mean_squared_error(y_bowl_runs, pred))
        mae = mean_absolute_error(y_bowl_runs, pred)
        r2 = r2_score(y_bowl_runs, pred)
        log(f"  {name:<26}: RMSE={rmse:.4f} | MAE={mae:.4f} | R2={r2:.5f}")
        model_comparison_results.append({"task": "Bowling_Runs_Conceded", "model": name, "rmse": round(rmse, 4), "mae": round(mae, 4), "r2": round(r2, 5)})

    df["exp_bowl_runs"] = oof_bowl_hgb
    df["rpae"] = df["exp_bowl_runs"] - df["bowl_runs_obs"]

    # =========================================================================
    # TASK 3B: BOWLER-CREDITED WICKET PROBABILITY MODEL (P(bowler_wkt))
    # Evaluated on all deliveries; target is 1 for bowler-credited dismissals
    # =========================================================================
    log("\n" + "=" * 60)
    log("[TASK 3B] BOWLER-CREDITED WICKET PROBABILITY MODEL (Target: df['is_bowler_wicket'])")
    log("=" * 60)

    y_bowl_wkt = df["is_bowler_wicket"].values.astype(float)

    oof_wkt_base = np.zeros(len(df))
    oof_wkt_lr = np.zeros(len(df))
    oof_wkt_hgb = np.zeros(len(df))

    for fold, (tr_idx, va_idx) in enumerate(gkf.split(X_bowl, y_bowl_wkt, g_bowl), 1):
        tr_df, va_df = df.iloc[tr_idx], df.iloc[va_idx]
        
        # 1. Baseline: Phase + Wickets empirical wkt rate
        wkt_lookup = tr_df.groupby(["innings", "phase", "wkts_before"])["is_bowler_wicket"].mean()
        global_wkt = tr_df["is_bowler_wicket"].mean()
        keys_va = list(zip(va_df["innings"], va_df["phase"], va_df["wkts_before"]))
        oof_wkt_base[va_idx] = np.array([wkt_lookup.get(k, global_wkt) for k in keys_va])

        # 2. Regularized Logistic Regression
        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_bowl[tr_idx])
        X_va_s = scaler.transform(X_bowl[va_idx])
        lr = LogisticRegression(C=0.5, max_iter=300)
        lr.fit(X_tr_s, y_bowl_wkt[tr_idx])
        oof_wkt_lr[va_idx] = lr.predict_proba(X_va_s)[:, 1]

        # 3. Contextual Tree Classifier (HistGradientBoostingClassifier)
        clf = HistGradientBoostingClassifier(max_depth=4, learning_rate=0.05, max_iter=100, min_samples_leaf=200, random_state=42)
        clf.fit(X_bowl[tr_idx], y_bowl_wkt[tr_idx])
        oof_wkt_hgb[va_idx] = clf.predict_proba(X_bowl[va_idx])[:, 1]

    for name, pred in [("Wkt Baseline", oof_wkt_base), ("Wkt Logistic Regression", oof_wkt_lr), ("Wkt HistGBC", oof_wkt_hgb)]:
        ll = log_loss(y_bowl_wkt, pred)
        bs = brier_score_loss(y_bowl_wkt, pred)
        auc = roc_auc_score(y_bowl_wkt, pred)
        ece = expected_calibration_error(y_bowl_wkt, pred)
        log(f"  {name:<26}: LogLoss={ll:.5f} | Brier={bs:.5f} | AUC={auc:.4f} | ECE={ece:.4f}")
        model_comparison_results.append({"task": "Bowling_Wickets", "model": name, "log_loss": round(ll, 5), "brier": round(bs, 5), "auc": round(auc, 4), "ece": round(ece, 4)})

    df["exp_bowl_wkt"] = oof_wkt_hgb
    df["wae"] = df["is_bowler_wicket"].astype(float) - df["exp_bowl_wkt"]

    # Phase Breakdown of Bowling Metrics
    log("\n  Bowling Conceded Runs & Wickets Across Innings Phases:")
    for ph in ["PP", "Middle", "Death"]:
        m_ph = (df["phase"] == ph)
        act_econ = 6.0 * df.loc[m_ph, "bowl_runs_obs"].sum() / df.loc[m_ph, "is_legal_bowl"].sum()
        exp_econ = 6.0 * df.loc[m_ph, "exp_bowl_runs"].sum() / df.loc[m_ph, "is_legal_bowl"].sum()
        wkt_cnt = df.loc[m_ph, "is_bowler_wicket"].sum()
        exp_wkt_cnt = df.loc[m_ph, "exp_bowl_wkt"].sum()
        log(f"    Phase {ph:<6} (n={m_ph.sum():>6,}): Actual Econ={act_econ:5.2f} | Exp Econ={exp_econ:5.2f} | Wkts={wkt_cnt:>4} (Exp={exp_wkt_cnt:6.1f})")

    # Pressure Breakdown of Bowling Metrics
    log("\n  Bowling Conceded Runs & Wickets Across Pressure Categories:")
    for cat_name, m_cat in [("Non-Pressure (<25% BWPI)", ~df["is_hp_bowl"]), ("High-Pressure (>=25% BWPI)", df["is_hp_bowl"])]:
        act_econ = 6.0 * df.loc[m_cat, "bowl_runs_obs"].sum() / df.loc[m_cat, "is_legal_bowl"].sum()
        exp_econ = 6.0 * df.loc[m_cat, "exp_bowl_runs"].sum() / df.loc[m_cat, "is_legal_bowl"].sum()
        wkt_cnt = df.loc[m_cat, "is_bowler_wicket"].sum()
        exp_wkt_cnt = df.loc[m_cat, "exp_bowl_wkt"].sum()
        dot_pct = 100.0 * (df.loc[m_cat, "bowl_runs_obs"] == 0).mean()
        log(f"    {cat_name:<28} (n={m_cat.sum():>6,}): Actual Econ={act_econ:5.2f} | Exp Econ={exp_econ:5.2f} | Dot%={dot_pct:4.1f}% | Wkts={wkt_cnt:>4} (Exp={exp_wkt_cnt:6.1f})")

    # Save model comparison summary table
    df_comp = pd.DataFrame(model_comparison_results)
    comp_csv = os.path.join(STEP3_DIR, "MODEL_COMPARISON.csv")
    df_comp.to_csv(comp_csv, index=False)
    log(f"\nSaved model comparison table to {comp_csv}")

    # Merge batting predictions back to df (for rows with is_legal_bat == True)
    # df_bat has exact same index as df.loc[bat_mask]
    df["exp_bat_runs"] = np.nan
    df["rae"] = np.nan
    df.loc[bat_mask, "exp_bat_runs"] = oof_bat_hgb
    df.loc[bat_mask, "rae"] = df_bat["rae"].values

    # Save enriched delivery data with model predictions
    out_scored_pkl = os.path.join(STEP3_DIR, "bbb_step3_modeled.pkl")
    df.to_pickle(out_scored_pkl)
    log(f"Saved modeled delivery dataset to {out_scored_pkl} ({len(df):,} deliveries)")

    # Save text log
    out_txt = os.path.join(STEP3_DIR, "02_model_training_report.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log(f"Saved training report to {out_txt}")


if __name__ == "__main__":
    main()

