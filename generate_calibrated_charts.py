import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(r"C:\Rajasthan Royals\pressure_output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# RR Colors
RR_PINK = "#E91E8C"
RR_NAVY = "#0A1424"
RR_CARD = "#122036"
RR_BLUE = "#0F1F38"
RR_GOLD = "#FFD700"
RR_CYAN = "#00B0FF"
RR_GREEN = "#00C853"
RR_WHITE = "#FFFFFF"
RR_MUTED = "#94A3B8"
BORDER_COL = "#2A4A6B"

# Load players
with open(r"C:\Rajasthan Royals\players_db.json", "r", encoding="utf-8") as f:
    players = json.load(f)

batters = [p for p in players if p["category"] == "Batter"]
bowlers = [p for p in players if p["category"] == "Bowler"]

# Sort by rank
batters.sort(key=lambda x: x["rank"])
bowlers.sort(key=lambda x: x["rank"])

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["text.color"] = RR_WHITE
plt.rcParams["axes.labelcolor"] = RR_WHITE
plt.rcParams["xtick.color"] = RR_MUTED
plt.rcParams["ytick.color"] = RR_WHITE

# ═══════════════════════════════════════════════════════════════
# CHART 1: TOP 10 BATTERS & BOWLERS CPPI RANKINGS
# ═══════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.5), facecolor=RR_NAVY)
fig.suptitle("RAJASTHAN ROYALS WAR ROOM — CALIBRATED CPPI RANKINGS (IPL 2027 TARGETS)",
             fontsize=14, fontweight="bold", color=RR_GOLD, y=0.98)

# Batters
ax1.set_facecolor(RR_CARD)
b_names = [f"#{p['rank']} {p['name']}" for p in batters][::-1]
b_cppi = [p["cppi"] for p in batters][::-1]
b_wr = [p["hp_wr"] for p in batters][::-1]
b_lift = [p["lift"] for p in batters][::-1]

y_pos = np.arange(len(b_names))
bars1 = ax1.barh(y_pos, b_cppi, color=RR_PINK, alpha=0.88, edgecolor=RR_GOLD, linewidth=0.8, height=0.68)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(b_names, fontsize=9.5, fontweight="bold")
ax1.set_xlim(0, 85)
ax1.set_title("TOP 10 BATTERS (CPPI)", color=RR_PINK, fontsize=12, fontweight="bold", pad=10)
ax1.set_xlabel("Composite Pressure Performance Index (0-100)", fontsize=9, color=RR_MUTED)
ax1.grid(axis="x", alpha=0.2, color=RR_MUTED, linestyle="--")

for bar, cppi_val, wr_val, lift_val in zip(bars1, b_cppi, b_wr, b_lift):
    lift_str = f"+{lift_val:.1f}%" if lift_val > 0 else f"{lift_val:.1f}%"
    ax1.text(bar.get_width() + 1.0, bar.get_y() + bar.get_height()/2,
             f"{cppi_val:.2f}  (HP WR: {wr_val:.1f}%, Δ: {lift_str})",
             va="center", fontsize=8.2, fontweight="bold", color=RR_WHITE)

# Bowlers
ax2.set_facecolor(RR_CARD)
bw_names = [f"#{p['rank']} {p['name']}" for p in bowlers][::-1]
bw_cppi = [p["cppi"] for p in bowlers][::-1]
bw_wr = [p["hp_wr"] for p in bowlers][::-1]
bw_lift = [p["lift"] for p in bowlers][::-1]

bars2 = ax2.barh(y_pos, bw_cppi, color=RR_CYAN, alpha=0.88, edgecolor=RR_GOLD, linewidth=0.8, height=0.68)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(bw_names, fontsize=9.5, fontweight="bold")
ax2.set_xlim(0, 85)
ax2.set_title("TOP 10 BOWLERS (CPPI)", color=RR_CYAN, fontsize=12, fontweight="bold", pad=10)
ax2.set_xlabel("Composite Pressure Performance Index (0-100)", fontsize=9, color=RR_MUTED)
ax2.grid(axis="x", alpha=0.2, color=RR_MUTED, linestyle="--")

for bar, cppi_val, wr_val, lift_val in zip(bars2, bw_cppi, bw_wr, bw_lift):
    lift_str = f"+{lift_val:.1f}%" if lift_val > 0 else f"{lift_val:.1f}%"
    ax2.text(bar.get_width() + 1.0, bar.get_y() + bar.get_height()/2,
             f"{cppi_val:.2f}  (HP WR: {wr_val:.1f}%, Δ: {lift_str})",
             va="center", fontsize=8.2, fontweight="bold", color=RR_WHITE)

plt.tight_layout(rect=[0.02, 0.03, 0.98, 0.94])
chart1_path = OUTPUT_DIR / "chart_01_top10_rankings.png"
plt.savefig(chart1_path, dpi=200, bbox_inches="tight", facecolor=RR_NAVY)
plt.close()
print(f"✓ Generated Chart 1: {chart1_path}")

# ═══════════════════════════════════════════════════════════════
# CHART 2: PRESSURE LIFT ALPHA MATRIX (QUADRANTS)
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 8), facecolor=RR_NAVY)
ax.set_facecolor(RR_CARD)

fig.suptitle("PRESSURE LIFT ALPHA MATRIX: True Clutch Elevation vs High-Pressure Win Rate",
             fontsize=14, fontweight="bold", color=RR_GOLD, y=0.97)

# Quadrant dividing lines
ax.axhline(0, color=BORDER_COL, linestyle="-", linewidth=1.5, alpha=0.8)
ax.axvline(60, color=BORDER_COL, linestyle="--", linewidth=1.2, alpha=0.6)

# Background highlights for quadrants
ax.axhspan(0, 27.5, xmin=0.33, xmax=1.0, color="#00C853", alpha=0.06)
ax.axhspan(-15.5, 0, xmin=0.33, xmax=1.0, color="#D50000", alpha=0.06)

# Quadrant labels
ax.text(83.5, 26.2, "QUADRANT I: ELITE CLUTCH MATCH-WINNERS\n(Elevates Above Baseline Under Pressure)",
        fontsize=9.5, fontweight="bold", color=RR_GREEN, ha="right", va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=RR_BLUE, edgecolor=RR_GREEN, alpha=0.9))

ax.text(83.5, -13.8, "QUADRANT IV: HIGH BASELINE DRIFT\n(Dominant Base Team, Negative Leverage Lift)",
        fontsize=9.5, fontweight="bold", color="#FF5252", ha="right", va="bottom",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=RR_BLUE, edgecolor="#FF5252", alpha=0.9))

ax.text(42.5, 26.2, "QUADRANT II: RESILIENT FIGHTERS\n(High Lift in Tough Game Conditions)",
        fontsize=9.0, fontweight="bold", color=RR_GOLD, ha="left", va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=RR_BLUE, edgecolor=RR_GOLD, alpha=0.85))

# Specific non-colliding offsets (with thin leader lines so tight clusters stay unambiguous)
batter_offsets = {
    "Shivam Dube": (-1.4, 2.0, "right"),
    "Rinku Singh": (-1.6, -2.2, "right"),
    "Axar Patel": (-1.4, -1.6, "right"),
    "Rajat Patidar": (1.2, 1.5, "left"),
    "Ruturaj Gaikwad": (0.0, 6.2, "center"),
    "Devon Conway": (-1.4, 1.0, "right"),
    "Virat Kohli": (0.8, -5.4, "center"),
    "Bhanuka Rajapaksa": (-1.4, -0.4, "right"),
    "Shreyas Iyer": (-1.2, -1.0, "right"),
    "Sediqullah Atal": (1.0, 1.2, "left"),
}

for p in batters:
    sz = p["hp_m"] * 18
    ax.scatter(p["hp_wr"], p["lift"], s=sz, color=RR_PINK, alpha=0.85, edgecolors=RR_WHITE, linewidth=1.2, zorder=5)
    ox, oy, ha = batter_offsets.get(p["name"], (0.8, 0.8, "left"))
    ax.annotate(f"{p['name']} (#{p['rank']})", (p["hp_wr"], p["lift"]),
                xytext=(p["hp_wr"] + ox, p["lift"] + oy),
                ha=ha, va="center", fontsize=8.0, fontweight="bold", color=RR_WHITE,
                arrowprops=dict(arrowstyle="-", color=RR_PINK, lw=0.8, alpha=0.75, shrinkA=0, shrinkB=4),
                bbox=dict(boxstyle="round,pad=0.18", facecolor=RR_BLUE, edgecolor=RR_PINK, alpha=0.88),
                zorder=6)

# Specific non-colliding offsets for bowlers
bowler_offsets = {
    "Jacob Duffy": (-1.2, 0.8, "right"),
    "Josh Hazlewood": (1.2, 0.2, "left"),
    "Yash Dayal": (0.8, -1.6, "left"),
    "Mitchell Starc": (1.2, 0.2, "left"),
    "Varun Chakravarthy": (1.4, -3.2, "left"),
    "Romario Shepherd": (-1.2, 2.2, "right"),
    "Suyash Sharma": (1.4, -1.8, "left"),
    "Bhuvneshwar Kumar": (0.0, -5.2, "center"),
    "Arshdeep Singh": (0.2, 4.4, "left"),
    "Lockie Ferguson": (-1.4, -0.5, "right"),
}

for p in bowlers:
    sz = p["hp_m"] * 18
    ax.scatter(p["hp_wr"], p["lift"], s=sz, color=RR_CYAN, alpha=0.85, edgecolors=RR_GOLD, linewidth=1.2, zorder=5)
    ox, oy, ha = bowler_offsets.get(p["name"], (0.8, 0.8, "left"))
    ax.annotate(f"{p['name']} (#{p['rank']})", (p["hp_wr"], p["lift"]),
                xytext=(p["hp_wr"] + ox, p["lift"] + oy),
                ha=ha, va="center", fontsize=8.0, fontweight="bold", color=RR_WHITE,
                arrowprops=dict(arrowstyle="-", color=RR_CYAN, lw=0.8, alpha=0.75, shrinkA=0, shrinkB=4),
                bbox=dict(boxstyle="round,pad=0.18", facecolor=RR_BLUE, edgecolor=RR_CYAN, alpha=0.88),
                zorder=6)

ax.set_xlim(41, 86.5)
ax.set_ylim(-15.5, 27.5)
ax.set_xlabel("High-Pressure Win Rate (%) — Threshold: Match Leverage Index ≥ 30", fontsize=10.5, color=RR_WHITE, labelpad=8)
ax.set_ylabel("True Pressure Lift Δ (%) = [HP Win Rate - Career Baseline Win Rate]", fontsize=10.5, color=RR_WHITE, labelpad=8)
ax.grid(alpha=0.15, color=RR_MUTED, linestyle=":")

# Legend placed in empty bottom-left pocket below Sediqullah Atal
pink_circle = plt.Line2D([0], [0], marker='o', color='w', label='Batters (Bubble Size ~ HP Matches)',
                         markerfacecolor=RR_PINK, markersize=10)
cyan_circle = plt.Line2D([0], [0], marker='o', color='w', label='Bowlers (Bubble Size ~ HP Matches)',
                         markerfacecolor=RR_CYAN, markersize=10)
ax.legend(handles=[pink_circle, cyan_circle], loc="lower left", facecolor=RR_CARD, edgecolor=BORDER_COL, fontsize=9.0)

plt.tight_layout(rect=[0.02, 0.03, 0.98, 0.94])
chart2_path = OUTPUT_DIR / "chart_02_pressure_lift_quadrants.png"
plt.savefig(chart2_path, dpi=200, bbox_inches="tight", facecolor=RR_NAVY)
plt.close()
print(f"✓ Generated Chart 2: {chart2_path}")

# ═══════════════════════════════════════════════════════════════
# CHART 3: RAJASTHAN ROYALS IPL 2027 TACTICAL STARTING XI
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(15.5, 8.8), facecolor=RR_NAVY)
ax.set_facecolor(RR_NAVY)
ax.axis("off")

fig.suptitle("RAJASTHAN ROYALS — IPL 2027 TACTICAL PLAYING-XI BLUEPRINT",
             fontsize=14.5, fontweight="bold", color=RR_GOLD, y=0.96)

xi_lineup = [
    {"pos": "1", "name": "Yashasvi Jaiswal", "type": "Retained Core", "role": "Left-Hand Explosive Opener", "stat": "IPL Strike Rate: 165+ | Aggressive PP Tempo", "color": RR_PINK},
    {"pos": "2", "name": "Devon Conway", "type": "Auction Target (#6)", "role": "LHB Top-Order Anchor & WK", "stat": "CPPI: 61.97 | Lift: +18.1% | HP WR: 64.3%", "color": RR_CYAN},
    {"pos": "3", "name": "Sanju Samson (C)", "type": "Retained Core", "role": "Captain & Pace/Spin Demolisher", "stat": "RR Captain | Proven Match-Winning Pivot", "color": RR_PINK},
    {"pos": "4", "name": "Shivam Dube", "type": "Auction Target (#1)", "role": "Middle-Overs Spin Enforcer (#4)", "stat": "CPPI: 66.81 | Lift: +12.4% | KO WR: 100.0%", "color": RR_GOLD},
    {"pos": "5", "name": "Riyan Parag", "type": "Retained Core", "role": "Middle-Order Striker & Seam Option", "stat": "Retained Core | Proven SMS Jaipur Dominance", "color": RR_PINK},
    {"pos": "6", "name": "Dhruv Jurel (WK)", "type": "Retained Core", "role": "Designated Clutch Finisher & Keeper", "stat": "Retained Core | Elite Death-Over Composure", "color": RR_PINK},
    {"pos": "7", "name": "Rinku Singh", "type": "Auction Target (#2)", "role": "Specialist Death Finisher (#7)", "stat": "CPPI: 66.26 | 26 HP Games | KO WR: 100.0%", "color": RR_GOLD},
    {"pos": "8", "name": "Shimron Hetmyer", "type": "Retained Core", "role": "Overseas Power-Finishing Dynamo", "stat": "Retained Core | Fearless Boundary Range", "color": RR_PINK},
    {"pos": "9", "name": "Josh Hazlewood", "type": "Auction Target (#2)", "role": "Frontline Overseas Seam Spearhead", "stat": "CPPI: 68.59 | Lift: +14.9% | HP WR: 78.6%", "color": RR_CYAN},
    {"pos": "10", "name": "Sandeep Sharma", "type": "Retained Core", "role": "Death Yorker & Wide-Line Specialist", "stat": "Retained Core | Master of Final 2 Overs", "color": RR_PINK},
    {"pos": "11", "name": "Yash Dayal", "type": "Auction Target (#3)", "role": "Indian Left-Arm Seam Specialist", "stat": "CPPI: 63.09 | Lift: +10.2% | HP WR: 80.0%", "color": RR_CYAN},
]

impact_subs = [
    {"pos": "SUB 1", "name": "Jacob Duffy", "type": "Target (#1 Bowler)", "role": "Overseas Pace Steal (Lift: +20.5%)", "stat": "CPPI: 68.83 | 100% KO Win Rate", "color": RR_GOLD},
    {"pos": "SUB 2", "name": "Axar Patel", "type": "Target (#3 Batter)", "role": "Elite Spin All-Rounder (Lift: +7.8%)", "stat": "CPPI: 65.82 | 100% KO Win Rate", "color": RR_CYAN},
    {"pos": "SUB 3", "name": "Varun Chakravarthy", "type": "Target (#5 Bowler)", "role": "Mystery Spin Choke Specialist", "stat": "CPPI: 62.38 | 100% KO Win Rate", "color": RR_GREEN},
    {"pos": "SUB 4", "name": "Rajat Patidar", "type": "Target (#4 Batter)", "role": "Middle Spin Enforcer (Lift: +11.1%)", "stat": "CPPI: 64.26 | 71.4% HP Win Rate", "color": RR_PINK},
]

# Draw 11 Cards in 2 columns (6 on left, 5 on right)
card_w = 7.0
card_h = 0.96
start_y = 7.1

for idx, p in enumerate(xi_lineup):
    col = 0 if idx < 6 else 1
    row = idx if idx < 6 else idx - 6
    x = 0.7 + col * 7.5
    y = start_y - row * 1.12

    rect = patches.FancyBboxPatch((x, y), card_w, card_h, boxstyle="round,pad=0.14",
                                   facecolor=RR_CARD, edgecolor=p["color"], linewidth=1.5)
    ax.add_patch(rect)

    # Position Number
    ax.text(x + 0.35, y + 0.48, p["pos"], fontsize=12, fontweight="bold", color=p["color"], va="center", ha="center")
    # Player Name (aligned left)
    ax.text(x + 0.80, y + 0.65, p["name"], fontsize=10.0, fontweight="bold", color=RR_WHITE, va="center", ha="left")
    # Status / Type Badge (aligned right at edge of card - ZERO overlap possible!)
    ax.text(x + card_w - 0.25, y + 0.65, f"[{p['type']}]", fontsize=7.8, fontweight="bold", color=p["color"], va="center", ha="right")
    # Role description
    ax.text(x + 0.80, y + 0.36, p["role"], fontsize=8.0, color=RR_GOLD, va="center", ha="left")
    # Metrics
    ax.text(x + 0.80, y + 0.12, p["stat"], fontsize=7.4, color=RR_MUTED, va="center", ha="left")

# Bottom Impact Subs Bar
sub_rect = patches.FancyBboxPatch((0.7, 0.18), 14.5, 0.95, boxstyle="round,pad=0.14",
                                   facecolor=RR_BLUE, edgecolor=RR_GOLD, linewidth=1.2)
ax.add_patch(sub_rect)

ax.text(0.95, 0.72, "TACTICAL IMPACT SUBS & ROTATION BENCH (HIGH-LEVERAGE COVERS):",
        fontsize=8.8, fontweight="bold", color=RR_GOLD, va="center")

sub_str = "   •   ".join([f"★ {s['name']} [{s['type']}]: {s['role']} ({s['stat']})" for s in impact_subs])
ax.text(0.95, 0.40, sub_str, fontsize=7.2, color=RR_WHITE, va="center")

ax.set_xlim(0, 16)
ax.set_ylim(0, 8.6)

plt.tight_layout()
chart3_path = OUTPUT_DIR / "chart_03_rr_tactical_xi.png"
plt.savefig(chart3_path, dpi=200, bbox_inches="tight", facecolor=RR_NAVY)
plt.close()
print(f"✓ Generated Chart 3: {chart3_path}")
