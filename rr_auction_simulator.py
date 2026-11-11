#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
RAJASTHAN ROYALS — AUCTION WAR ROOM GAME THEORY & MONTE CARLO SIMULATOR
SupeRR Selector Season 2 | Franchise Purse & Paddle-Raise Modeling
==============================================================================

PURPOSE:
    Simulates auction bidding wars across all 10 IPL franchises to determine:
    1. Win Probability as a function of bid amount (₹30L to ₹1.00 Cr).
    2. Rival Franchise Interference Probability (Which franchise is most likely to bid against RR).
    3. Optimal Bid Ceilings to maximize Economic Surplus without overpaying.
    4. Outputs high-resolution visualization for the final submission deck.

USAGE:
    python rr_auction_simulator.py
==============================================================================
"""

import os
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# RR Color Branding
RR_PINK   = '#EA1A85'
RR_NAVY   = '#1A1F71'
RR_GOLD   = '#F5B800'
RR_WHITE  = '#FFFFFF'
RR_GREY   = '#888888'

FRANCHISES = {
    "CSK":  {"purse_weight": 0.85, "role_interest": {"Spin-Hitting Finisher": 0.90, "Impact/Mystery Spinner": 0.85, "Powerplay Enforcer": 0.40, "Death Bowler": 0.50}},
    "MI":   {"purse_weight": 0.90, "role_interest": {"Death Bowler": 0.95, "Powerplay Enforcer": 0.80, "Spin-Hitting Finisher": 0.60, "Impact/Mystery Spinner": 0.50}},
    "KKR":  {"purse_weight": 0.80, "role_interest": {"Impact/Mystery Spinner": 0.95, "Spin-Hitting Finisher": 0.85, "Death Bowler": 0.60, "Powerplay Enforcer": 0.50}},
    "RCB":  {"purse_weight": 0.85, "role_interest": {"Death Bowler": 0.90, "Spin-Hitting Finisher": 0.75, "Powerplay Enforcer": 0.70, "Impact/Mystery Spinner": 0.65}},
    "SRH":  {"purse_weight": 0.95, "role_interest": {"Powerplay Enforcer": 0.90, "Death Bowler": 0.70, "Impact/Mystery Spinner": 0.60, "Spin-Hitting Finisher": 0.50}},
    "PBKS": {"purse_weight": 1.20, "role_interest": {"Powerplay Enforcer": 0.85, "Death Bowler": 0.85, "Impact/Mystery Spinner": 0.80, "Spin-Hitting Finisher": 0.80}},
    "DC":   {"purse_weight": 0.85, "role_interest": {"Powerplay Enforcer": 0.80, "Death Bowler": 0.75, "Impact/Mystery Spinner": 0.75, "Spin-Hitting Finisher": 0.60}},
    "GT":   {"purse_weight": 0.90, "role_interest": {"Death Bowler": 0.85, "Powerplay Enforcer": 0.65, "Spin-Hitting Finisher": 0.70, "Impact/Mystery Spinner": 0.65}},
    "LSG":  {"purse_weight": 0.85, "role_interest": {"Spin-Hitting Finisher": 0.75, "Death Bowler": 0.70, "Impact/Mystery Spinner": 0.70, "Powerplay Enforcer": 0.60}},
}

def simulate_bidding(target_df: pd.DataFrame, n_sims=1000, seed=42):
    rng = np.random.default_rng(seed)
    results = []

    print("=" * 80)
    print("🎲 RUNNING MONTE CARLO AUCTION BIDDING SIMULATION (1,000 Iterations per Player)")
    print("=" * 80)

    for _, player in target_df.iterrows():
        p_name = player["player"]
        role = player["role"]
        tdsi = player["tdsi"]
        target_bid = player.get("expected_bid_lakhs", 45)
        walk_away = player.get("walk_away_limit_lakhs", 80)

        # Base price in Lakhs
        base_price = 30

        # Simulate rival interest and maximum rival bids
        rival_max_bids = np.zeros(n_sims)
        rival_primary_threat = []

        for f_name, f_profile in FRANCHISES.items():
            # Demand factor
            demand = f_profile["role_interest"].get(role, 0.5) * f_profile["purse_weight"]
            # Probability this franchise enters the bidding
            prob_bid = np.clip((tdsi / 100.0) * demand * 0.75, 0.05, 0.85)

            # Random draws for whether franchise bids
            enters = rng.random(n_sims) < prob_bid
            # Willingness to pay (in Lakhs): Log-normal distribution centered around player valuation
            mu_bid = np.clip(30 + (tdsi - 50) * 1.2 * demand, 30, 110)
            sim_bids = np.where(enters, rng.normal(mu_bid, 15, n_sims), 0)
            sim_bids = np.round(np.clip(sim_bids, 0, 150) / 5) * 5  # IPL bid increments of 5 Lakhs

            # Update maximum rival bids
            higher = sim_bids > rival_max_bids
            rival_max_bids = np.maximum(rival_max_bids, sim_bids)

        # Compute Win Probabilities for RR
        win_at_base = np.mean(rival_max_bids < base_price)
        win_at_target = np.mean(rival_max_bids <= target_bid)
        win_at_walkaway = np.mean(rival_max_bids <= walk_away)
        expected_final_price = np.mean(np.where(rival_max_bids < base_price, base_price, np.minimum(rival_max_bids + 5, walk_away)))

        results.append({
            "Player": p_name,
            "Role": role,
            "TDSI": round(tdsi, 1),
            "Base (₹30L) Win%": f"{win_at_base * 100:.1f}%",
            "Target Bid": f"₹{target_bid}L",
            "Target Win%": f"{win_at_target * 100:.1f}%",
            "Walk-Away Limit": f"₹{walk_away}L",
            "Walk-Away Win%": f"{win_at_walkaway * 100:.1f}%",
            "Expected Price": f"₹{expected_final_price:.1f}L",
            "Target_Win_Float": win_at_target,
            "WalkAway_Win_Float": win_at_walkaway
        })

    res_df = pd.DataFrame(results)
    print(res_df[["Player", "Role", "TDSI", "Base (₹30L) Win%", "Target Bid", "Target Win%", "Walk-Away Limit", "Walk-Away Win%", "Expected Price"]].to_string(index=False))
    print("=" * 80 + "\n")
    return res_df

def plot_auction_curves(res_df: pd.DataFrame, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 6.5))
    fig.patch.set_facecolor(RR_NAVY)
    ax.set_facecolor('#1E2340')

    players = res_df["Player"].tolist()[::-1]
    y_pos = np.arange(len(players))
    target_probs = (res_df["Target_Win_Float"] * 100).tolist()[::-1]
    walkaway_probs = (res_df["WalkAway_Win_Float"] * 100).tolist()[::-1]

    bar_width = 0.38
    rects1 = ax.barh(y_pos + bar_width/2, target_probs, bar_width, label='Win Probability at Target Bid', color=RR_PINK, alpha=0.9, edgecolor=RR_WHITE, linewidth=0.5)
    rects2 = ax.barh(y_pos - bar_width/2, walkaway_probs, bar_width, label='Win Probability at Walk-Away Limit', color=RR_GOLD, alpha=0.9, edgecolor=RR_WHITE, linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(players, color=RR_WHITE, fontweight='bold', fontsize=11)
    ax.set_xlabel('Auction Acquisition Probability (%)', color=RR_WHITE, fontsize=12)
    ax.set_xlim(0, 105)
    ax.grid(axis='x', color=RR_GREY, alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(RR_GREY)
    ax.spines['left'].set_color(RR_GREY)
    ax.tick_params(colors=RR_WHITE)

    for bar in rects1:
        w = bar.get_width()
        ax.text(w + 1.5, bar.get_y() + bar.get_height()/2, f'{w:.0f}%', va='center', ha='left', color=RR_PINK, fontweight='bold', fontsize=9.5)

    for bar in rects2:
        w = bar.get_width()
        ax.text(w + 1.5, bar.get_y() + bar.get_height()/2, f'{w:.0f}%', va='center', ha='left', color=RR_GOLD, fontweight='bold', fontsize=9.5)

    ax.legend(loc='lower right', facecolor='#1E2340', edgecolor=RR_PINK, labelcolor=RR_WHITE, fontsize=10)

    # Header
    fig.text(0.5, 0.96, "AUCTION WAR ROOM: ACQUISITION WIN PROBABILITY CURVES", ha='center', va='top', fontsize=15, fontweight='bold', color=RR_WHITE)
    fig.text(0.5, 0.92, "Monte Carlo Simulation (1,000 Runs vs 10 Rival IPL Franchise Purses)", ha='center', va='top', fontsize=10, color=RR_PINK, style='italic')

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    out_path = out_dir / "chart_auction_win_probability.png"
    plt.savefig(out_path, dpi=160, bbox_inches='tight', facecolor=RR_NAVY)
    plt.close()
    print(f"✅ Simulation chart saved: {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", type=Path, default=Path("demo_out/04_top10_targets.csv"))
    parser.add_argument("--out", type=Path, default=Path("output/charts"))
    args = parser.parse_args()

    if not args.targets.exists():
        args.targets = Path("out/04_top10_targets.csv")
    if not args.targets.exists():
        args.targets = Path("output/rr_top10_targets.csv")

    if args.targets.exists():
        df = pd.read_csv(args.targets)
        sim_df = simulate_bidding(df)
        plot_auction_curves(sim_df, args.out)
    else:
        print(f"❌ Targets file not found at {args.targets}. Run rr_scout_pipeline.py first.")

