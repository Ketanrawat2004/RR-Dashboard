"""
Phase 1 Step 3.1 — Section 10: Step 3.1 Diagnostic Visualizations
(05_generate_step3_1_charts.py)

Generates publication-quality diagnostic charts for the independent validation report:
1. 01_fold_error_and_context_ablation.png: Out-of-fold RMSE and R^2 across folds and contextual feature ablation.
2. 02_wicket_roc_pr_and_calibration.png: Wicket and dismissal hazard ROC/PR curves and decile calibration.
3. 03_randomized_splithalf_reliability.png: Monte Carlo randomized split-half reliability and sample-size scaling.
4. 04_bootstrap_cluster_ci_and_stability.png: Match-clustered bootstrap 95% CIs and threshold ranking stability.

Outputs saved to phase1_audit/step3_1_validation/charts/
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit")
VAL_DIR = os.path.join(AUDIT_DIR, "step3_1_validation")
CHARTS_DIR = os.path.join(VAL_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# Set standard styling
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "axes.labelweight": "bold",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.titlesize": 13,
    "figure.titleweight": "bold",
    "figure.dpi": 200,
    "savefig.bbox": "tight"
})

ROYAL_BLUE = "#0B2B66"
RR_PINK = "#E73895"
RR_GOLD = "#C29B38"
ACCENT_GREEN = "#1B8A5A"
ACCENT_GRAY = "#6C757D"
LIGHT_GRAY = "#E9ECEF"


def plot_01_fold_error():
    df_fold = pd.read_csv(os.path.join(VAL_DIR, "MODEL_FOLD_VALIDATION.csv"))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Batting
    bat_df = df_fold[df_fold["target"] == "Batting_Runs"]
    models = ["Global_Mean", "Phase_Mean", "Over_Mean", "Phase_Wkts_Mean", "Ridge", "HistGBR"]
    model_labels = ["Global Mean\nBaseline", "Phase Mean\nBaseline", "Over Mean\nBaseline", "Phase x Wkts\nBaseline", "Ridge\nRegression", "HistGBR\n(Contextual)"]
    
    rmse_means_bat = [bat_df[bat_df["model"] == m]["rmse"].mean() for m in models]
    r2_means_bat = [bat_df[bat_df["model"] == m]["r2"].mean() * 100 for m in models]
    
    # Bowling
    bowl_df = df_fold[df_fold["target"] == "Bowling_Runs"]
    rmse_means_bowl = [bowl_df[bowl_df["model"] == m]["rmse"].mean() for m in models]
    r2_means_bowl = [bowl_df[bowl_df["model"] == m]["r2"].mean() * 100 for m in models]

    x = np.arange(len(models))
    width = 0.35

    # Ax1: RMSE
    bars1 = ax1.bar(x - width/2, rmse_means_bat, width, label="Batting Expected Runs", color=RR_PINK, alpha=0.9, edgecolor="black")
    bars2 = ax1.bar(x + width/2, rmse_means_bowl, width, label="Bowling Expected Runs", color=ROYAL_BLUE, alpha=0.9, edgecolor="black")
    
    ax1.set_ylabel("Out-of-Fold RMSE (Runs / Delivery)")
    ax1.set_title("5-Fold Cross-Validation: Out-of-Fold RMSE by Model Complexity")
    ax1.set_xticks(x)
    ax1.set_xticklabels(model_labels)
    ax1.set_ylim(1.68, 1.76)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right")

    for b in bars1:
        h = b.get_height()
        ax1.annotate(f"{h:.4f}", (b.get_x() + b.get_width()/2, h), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=7.5)
    for b in bars2:
        h = b.get_height()
        ax1.annotate(f"{h:.4f}", (b.get_x() + b.get_width()/2, h), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=7.5)

    # Ax2: R^2 (%)
    b_r1 = ax2.bar(x - width/2, r2_means_bat, width, label="Batting R² (%)", color=RR_PINK, alpha=0.9, edgecolor="black")
    b_r2 = ax2.bar(x + width/2, r2_means_bowl, width, label="Bowling R² (%)", color=ROYAL_BLUE, alpha=0.9, edgecolor="black")
    
    ax2.set_ylabel("Out-of-Fold Explained Variance R² (%)")
    ax2.set_title("5-Fold Cross-Validation: R² (%) Improvement Over Baselines")
    ax2.set_xticks(x)
    ax2.set_xticklabels(model_labels)
    ax2.set_ylim(-0.2, 2.7)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    ax2.legend(loc="upper left")

    for b in b_r1:
        h = b.get_height()
        ax2.annotate(f"{h:.2f}%", (b.get_x() + b.get_width()/2, max(h, 0)), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=7.5)
    for b in b_r2:
        h = b.get_height()
        ax2.annotate(f"{h:.2f}%", (b.get_x() + b.get_width()/2, max(h, 0)), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=7.5)

    plt.suptitle("Phase 1 Step 3.1: Expected Performance Model 5-Fold Cross-Validation & Baseline Comparison", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "01_fold_error_and_context_ablation.png"))
    plt.close()
    print("Saved 01_fold_error_and_context_ablation.png")


def plot_02_wicket_calibration():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Decile calibration data from Section 2
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pred_bowl = [3.51, 3.92, 4.12, 4.29, 4.45, 4.67, 5.01, 5.52, 6.56, 9.09]
    obs_bowl = [3.42, 3.80, 4.07, 4.17, 4.51, 4.69, 5.15, 5.48, 6.70, 9.09]

    # Ax1: Decile Calibration
    ax1.plot([2, 10], [2, 10], linestyle="--", color="black", alpha=0.7, label="Perfect Calibration (y = x)")
    ax1.plot(pred_bowl, obs_bowl, marker="o", markersize=7, linewidth=2, color=ROYAL_BLUE, label="Bowler Wicket Deciles (HistGBC)")
    
    for i, (p, o) in enumerate(zip(pred_bowl, obs_bowl), 1):
        ax1.annotate(f"D{i}: {o:.1f}%", (p, o), textcoords="offset points", xytext=(5, -5), fontsize=8)

    ax1.set_xlabel("Mean Predicted Wicket Probability (%)")
    ax1.set_ylabel("Observed Wicket Frequency (%)")
    ax1.set_title("Bowler Wicket Model Decile Calibration (Near-Perfect Linearity)")
    ax1.set_xlim(2.5, 10.0)
    ax1.set_ylim(2.5, 10.0)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left")

    # Ax2: Discrimination vs Skill Comparison
    metrics = ["Constant Prior", "Phase Mean", "Phase x Wkts", "Logistic Reg", "HistGBC"]
    bss_bowl = [0.00, 0.28, 0.34, 0.52, 0.55]
    bss_bat = [0.00, 0.40, 0.49, 0.69, 0.77]
    auc_bowl = [0.5000, 0.5500, 0.5583, 0.5838, 0.5854]

    x = np.arange(len(metrics))
    width = 0.35

    ax2_r = ax2.twinx()
    b1 = ax2.bar(x - width/2, bss_bowl, width, label="Bowler Wicket BSS (%)", color=ROYAL_BLUE, alpha=0.85, edgecolor="black")
    b2 = ax2.bar(x + width/2, bss_bat, width, label="Batter Hazard BSS (%)", color=RR_PINK, alpha=0.85, edgecolor="black")
    line = ax2_r.plot(x, auc_bowl, color=RR_GOLD, marker="D", linewidth=2.5, markersize=7, label="Bowler ROC AUC")

    ax2.set_ylabel("Brier Skill Score BSS (%) — Primary Calibration Skill")
    ax2_r.set_ylabel("ROC AUC (Discrimination)")
    ax2.set_title("Wicket & Hazard Model Skill: BSS < 0.8% Demonstrates High Stochastic Noise")
    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics, rotation=15)
    ax2.set_ylim(-0.1, 1.0)
    ax2_r.set_ylim(0.48, 0.62)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    # Combined legend
    lines_1, labels_1 = ax2.get_legend_handles_labels()
    lines_2, labels_2 = ax2_r.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

    plt.suptitle("Phase 1 Step 3.1: Wicket Probability & Hazard Calibration Analysis", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "02_wicket_roc_pr_and_calibration.png"))
    plt.close()
    print("Saved 02_wicket_roc_pr_and_calibration.png")


def plot_03_reliability():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Data from Monte Carlo 50-split reliability
    m0_vals = [30, 50, 75, 100, 150, 200, 250]
    sb_bat = [0.1965, 0.1811, 0.1829, 0.1880, 0.1782, 0.1913, 0.1705]
    sb_bowl = [0.0759, 0.0837, 0.1103, 0.0930, 0.1196, 0.1184, 0.1139]

    # Ax1: Prior strength vs reliability
    ax1.plot(m0_vals, sb_bat, marker="o", linewidth=2.5, color=RR_PINK, label="Batting RAE Spearman-Brown Reliability")
    ax1.plot(m0_vals, sb_bowl, marker="s", linewidth=2.5, color=ROYAL_BLUE, label="Bowling RPAE Spearman-Brown Reliability")
    ax1.axvline(150, color="gray", linestyle="--", alpha=0.7, label="Chosen Optimal Prior (M0 = 150)")

    ax1.set_xlabel("Empirical Bayes Shrinkage Prior Strength M0 (Deliveries)")
    ax1.set_ylabel("Spearman-Brown Split-Half Reliability (50 Random Splits)")
    ax1.set_title("Split-Half Reliability across Shrinkage Prior Strengths M0")
    ax1.set_ylim(0.04, 0.25)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="lower right")

    # Ax2: Reliability scaling with sample threshold
    n_mins = [30, 40, 50, 75, 100, 150]
    sb_bat_n = [0.2022, 0.1756, 0.1070, 0.1791, 0.2298, 0.2679]
    sb_bowl_n = [0.1137, 0.1104, 0.0947, 0.1216, 0.0946, 0.1211]
    qual_bat_n = [337, 288, 237, 175, 140, 93]

    ax2_r = ax2.twinx()
    l1 = ax2.plot(n_mins, sb_bat_n, marker="o", linewidth=2.5, color=RR_PINK, label="Batting Reliability")
    l2 = ax2.plot(n_mins, sb_bowl_n, marker="s", linewidth=2.5, color=ROYAL_BLUE, label="Bowling Reliability")
    b1 = ax2_r.bar(n_mins, qual_bat_n, width=6, alpha=0.2, color="gray", label="Qualified Batters (N)")

    ax2.set_xlabel("Minimum Pressure Deliveries Required (N_min)")
    ax2.set_ylabel("Spearman-Brown Reliability (M0 = 150)")
    ax2_r.set_ylabel("Qualified Player Count")
    ax2.set_title("Reliability Gain vs Qualified Player Pool Tradeoff")
    ax2.set_ylim(0.05, 0.32)
    ax2_r.set_ylim(0, 400)
    ax2.grid(True, linestyle="--", alpha=0.5)

    lines_a, labels_a = ax2.get_legend_handles_labels()
    lines_b, labels_b = ax2_r.get_legend_handles_labels()
    ax2.legend(lines_a + lines_b, labels_a + labels_b, loc="upper right")

    plt.suptitle("Phase 1 Step 3.1: Bayesian Reliability & Sample-Size Threshold Sensitivity", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "03_randomized_splithalf_reliability.png"))
    plt.close()
    print("Saved 03_randomized_splithalf_reliability.png")


def plot_04_ci_and_stability():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # CI Audit Data for Top 10 Batters
    top_batters = [
        "Andre Russell", "Vaibhav Sooryavanshi", "Glenn Maxwell", "Tim David",
        "Abhishek Sharma", "Priyansh Arya", "Heinrich Klaasen", "Prabhsimran Singh",
        "Suryakumar Yadav", "Patrick Cummins"
    ]
    scores = [26.59, 22.48, 22.45, 20.11, 18.52, 18.11, 18.08, 17.76, 16.14, 15.30]
    ci_low = [9.23, 1.52, 6.27, 5.64, 0.51, -7.79, 6.96, 2.87, 7.08, -1.76]
    ci_high = [41.02, 39.77, 36.40, 36.32, 35.99, 46.37, 29.75, 31.48, 25.90, 30.25]
    top10_prob = [79.8, 56.0, 63.6, 51.0, 42.6, 44.6, 43.6, 40.2, 26.8, 30.8]

    y = np.arange(len(top_batters))
    y_rev = y[::-1]

    # Ax1: Forest plot of 95% Match-Clustered Bootstrap CIs
    ax1.errorbar(scores[::-1], y_rev, xerr=[np.array(scores[::-1]) - np.array(ci_low[::-1]), np.array(ci_high[::-1]) - np.array(scores[::-1])],
                 fmt="o", color=RR_PINK, ecolor=ROYAL_BLUE, elinewidth=2, capsize=4, capthick=1.5, markersize=6)
    
    ax1.axvline(0, color="red", linestyle="--", alpha=0.6)
    ax1.set_yticks(y_rev)
    ax1.set_yticklabels([f"{p} ({prob:.0f}%)" for p, prob in zip(top_batters, top10_prob)][::-1])
    ax1.set_xlabel("Pressure Pure RAE Score per 100 Balls faced (with 95% Cluster-Bootstrap CI)")
    ax1.set_title("Match-Clustered Bootstrap 95% Confidence Intervals\n(Top 10 Batters, with Top-10 Inclusion Probability %)")
    ax1.grid(axis="x", linestyle="--", alpha=0.5)

    # Ax2: Threshold stability bar chart
    thresh_labels = ["Top 15%\n(Extreme)", "Top 20%\n(High)", "Top 25%\n(Baseline)", "Top 30%\n(Moderate)"]
    rho_bat = [0.8097, 0.8999, 1.0000, 0.8971]
    rho_bowl = [0.8244, 0.8907, 1.0000, 0.9124]
    tau_bat = [0.6181, 0.7238, 1.0000, 0.7316]
    tau_bowl = [0.6426, 0.7186, 1.0000, 0.7436]

    x = np.arange(len(thresh_labels))
    width = 0.35

    ax2.bar(x - width/2, rho_bat, width, label="Batting Spearman rho vs 25%", color=RR_PINK, alpha=0.85, edgecolor="black")
    ax2.bar(x + width/2, rho_bowl, width, label="Bowling Spearman rho vs 25%", color=ROYAL_BLUE, alpha=0.85, edgecolor="black")
    
    ax2.plot(x - width/2, tau_bat, color="darkmagenta", marker="o", linewidth=1.5, linestyle=":", label="Batting Kendall tau")
    ax2.plot(x + width/2, tau_bowl, color="navy", marker="s", linewidth=1.5, linestyle=":", label="Bowling Kendall tau")

    ax2.set_ylabel("Rank Correlation vs 25% Baseline (rho / tau)")
    ax2.set_title("Ranking Stability Across Pressure Threshold Slices (15% to 30%)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(thresh_labels)
    ax2.set_ylim(0.5, 1.05)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    ax2.legend(loc="lower right", fontsize=8.5)

    for i in range(len(thresh_labels)):
        ax2.annotate(f"{rho_bat[i]:.3f}", (x[i] - width/2, rho_bat[i]), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=7.5)
        ax2.annotate(f"{rho_bowl[i]:.3f}", (x[i] + width/2, rho_bowl[i]), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=7.5)

    plt.suptitle("Phase 1 Step 3.1: Cluster-Robust Confidence Intervals & Threshold Stability", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "04_bootstrap_cluster_ci_and_stability.png"))
    plt.close()
    print("Saved 04_bootstrap_cluster_ci_and_stability.png")


if __name__ == "__main__":
    plot_01_fold_error()
    plot_02_wicket_calibration()
    plot_03_reliability()
    plot_04_ci_and_stability()
    print("All diagnostic charts successfully generated.")

