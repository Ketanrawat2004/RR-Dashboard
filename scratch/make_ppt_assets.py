import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

SCRATCH = Path(r"C:\Rajasthan Royals\scratch")
SCRATCH.mkdir(parents=True, exist_ok=True)

# 1. Trim transparent padding around official RR logo
with Image.open(r"C:\Rajasthan Royals\rr_logo.png") as im:
    bbox = im.getbbox()
    cropped = im.crop(bbox)
    cropped.save(SCRATCH / "rr_corner_logo.png")
    print("Corner logo size:", cropped.size)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Calibri", "Arial", "DejaVu Sans"]

# 2. Clean White-Mode Fixture Distribution Donut (matching Image #2, updated to 178 matches)
fig, ax = plt.subplots(figsize=(4.4, 3.2), dpi=300, facecolor="#FFFFFF")
ax.set_facecolor("#FFFFFF")

sizes = [118, 35, 25]  # 66.3% Defend <=15r, 19.7% KO/Playoffs, 14.0% Chase <=2 wkts/SO
cols = ["#D91B7A", "#001D48", "#059669"]
wedges, _ = ax.pie(
    sizes,
    colors=cols,
    startangle=90,
    counterclock=False,
    wedgeprops=dict(width=0.36, edgecolor="#FFFFFF", linewidth=2.5),
)
ax.text(0, 0.08, "178", ha="center", va="center", fontsize=22, fontweight="bold", color="#111827")
ax.text(0, -0.20, "MATCHES", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#64748B")
ax.set_aspect("equal")
plt.tight_layout(pad=0.1)
plt.savefig(SCRATCH / "ppt_chart_donut.png", dpi=300, facecolor="#FFFFFF", bbox_inches="tight")
plt.close()

# 3. Clean White-Mode Pressure Lift Quadrant Scatter Plot (matching Image #12 & #13)
with open(r"C:\Rajasthan Royals\players_db.json", encoding="utf-8") as f:
    players = json.load(f)

batters = [p for p in players if p["category"] == "Batter"]
bowlers = [p for p in players if p["category"] == "Bowler"]

fig, ax = plt.subplots(figsize=(11.2, 5.2), dpi=300, facecolor="#FFFFFF")
ax.set_facecolor("#FFFFFF")

# Subtle quadrant background tints matching Image #12
ax.axvspan(41.5, 60, ymin=13.5/37.0, ymax=1.0, color="#FFFBEB", alpha=0.85, zorder=0)   # Q II (y >= 0)
ax.axvspan(60, 85, ymin=13.5/37.0, ymax=1.0, color="#F0FDF4", alpha=0.85, zorder=0)     # Q I (y >= 0)
ax.axvspan(60, 85, ymin=0, ymax=13.5/37.0, color="#F8FAFC", alpha=0.95, zorder=0)       # Q IV (y < 0)

# Axes grid
ax.grid(True, which="major", color="#E2E8F0", linewidth=0.8, zorder=1)
ax.axhline(0, color="#94A3B8", linestyle="--", linewidth=1.2, zorder=2)
ax.axvline(60, color="#94A3B8", linestyle="--", linewidth=1.2, zorder=2)

# Clean Quadrant titles (no boxes, plain readable labels like Image #12)
ax.text(42.5, 22.8, "QUADRANT II  |  SITUATIONAL SPECIALISTS", fontsize=8.8, fontweight="bold", color="#B45309", ha="left")
ax.text(84.0, 22.8, "QUADRANT I  |  HIGH-PRESSURE MATCH-WINNERS", fontsize=8.8, fontweight="bold", color="#047857", ha="right")
ax.text(84.0, -11.5, "QUADRANT IV  |  HIGH BASELINE DRIFT", fontsize=8.5, fontweight="bold", color="#64748B", ha="right")

offsets = {
    "Shivam Dube": (-1.3, 1.8, "right"),
    "Rinku Singh": (-1.3, -2.0, "right"),
    "Axar Patel": (-1.3, -1.4, "right"),
    "Rajat Patidar": (1.1, 1.4, "left"),
    "Ruturaj Gaikwad": (0.0, 5.8, "center"),
    "Devon Conway": (-1.3, 0.9, "right"),
    "Virat Kohli": (0.8, -4.8, "center"),
    "Bhanuka Rajapaksa": (-1.3, -0.3, "right"),
    "Shreyas Iyer": (-1.1, -0.8, "right"),
    "Sediqullah Atal": (1.0, 0.8, "left"),
    "Jacob Duffy": (-1.1, 0.6, "right"),
    "Josh Hazlewood": (1.1, 0.2, "left"),
    "Yash Dayal": (0.8, -1.5, "left"),
    "Mitchell Starc": (1.0, 0.2, "left"),
    "Varun Chakravarthy": (1.3, -2.8, "left"),
    "Romario Shepherd": (-1.1, 2.0, "right"),
    "Suyash Sharma": (1.2, -1.5, "left"),
    "Bhuvneshwar Kumar": (0.0, -4.6, "center"),
    "Arshdeep Singh": (0.2, 4.1, "left"),
    "Lockie Ferguson": (-1.3, -0.5, "right"),
}

for p in batters:
    sz = p["hp_m"] * 12 + 30
    ax.scatter(p["hp_wr"], p["lift"], s=sz, color="#D91B7A", edgecolors="#FFFFFF", linewidth=1.2, alpha=0.92, zorder=4)
    ox, oy, ha = offsets[p["name"]]
    ax.annotate(
        f"{p['name']} (#{p['rank']})",
        (p["hp_wr"], p["lift"]),
        xytext=(p["hp_wr"] + ox, p["lift"] + oy),
        ha=ha, va="center",
        fontsize=8.2, fontweight="bold", color="#111827",
        arrowprops=dict(arrowstyle="-", color="#CBD5E1", lw=0.8, shrinkA=0, shrinkB=4),
        zorder=5,
    )

for p in bowlers:
    sz = p["hp_m"] * 12 + 30
    ax.scatter(p["hp_wr"], p["lift"], s=sz, color="#001D48", edgecolors="#FFFFFF", linewidth=1.2, alpha=0.92, zorder=4)
    ox, oy, ha = offsets[p["name"]]
    ax.annotate(
        f"{p['name']} (#{p['rank']})",
        (p["hp_wr"], p["lift"]),
        xytext=(p["hp_wr"] + ox, p["lift"] + oy),
        ha=ha, va="center",
        fontsize=8.2, fontweight="bold", color="#111827",
        arrowprops=dict(arrowstyle="-", color="#CBD5E1", lw=0.8, shrinkA=0, shrinkB=4),
        zorder=5,
    )

ax.set_xlim(41.5, 85.0)
ax.set_ylim(-13.5, 24.5)
ax.set_xticks([45, 50, 55, 60, 65, 70, 75, 80])
ax.set_xticklabels(["45%", "50%", "55%", "60%", "65%", "70%", "75%", "80%"], fontsize=8.8, color="#475569")
ax.set_yticks([-10, -5, 0, 5, 10, 15, 20])
ax.set_yticklabels(["-10%", "-5%", "0%", "+5%", "+10%", "+15%", "+20%"], fontsize=8.8, color="#475569")

ax.set_xlabel("High-Pressure Win Rate (%) — Matches with MLI ≥ 30 (Close Finishes & Knockouts)", fontsize=9.5, fontweight="bold", color="#111827", labelpad=8)
ax.set_ylabel("True Pressure Lift Δ (%) vs Career Baseline", fontsize=9.5, fontweight="bold", color="#111827", labelpad=8)

for sp in ["top", "right", "bottom", "left"]:
    ax.spines[sp].set_color("#CBD5E1")
    ax.spines[sp].set_linewidth(1.0)

bat_h = plt.Line2D([0], [0], marker="o", color="w", label="Batters (dot size = HP match count)", markerfacecolor="#D91B7A", markersize=8.5)
bowl_h = plt.Line2D([0], [0], marker="o", color="w", label="Bowlers (dot size = HP match count)", markerfacecolor="#001D48", markersize=8.5)
ax.legend(handles=[bat_h, bowl_h], loc="lower left", frameon=True, facecolor="#FFFFFF", edgecolor="#E2E8F0", fontsize=8.5)

plt.tight_layout(pad=0.3)
plt.savefig(SCRATCH / "ppt_chart_quadrants.png", dpi=300, facecolor="#FFFFFF", bbox_inches="tight")
plt.close()
print("Saved clean white charts.")

