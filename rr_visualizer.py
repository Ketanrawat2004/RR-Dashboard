"""
==============================================================================
RAJASTHAN ROYALS — WAR ROOM VISUALIZATIONS
SupeRR Selector Season 2 | Submission-Ready Charts
==============================================================================

Run AFTER the main pipeline:
    python rr_scout_pipeline.py         (generates output/rr_top10_targets.csv)
    python rr_visualizer.py             (generates charts for your submission)

OUTPUT:
    output/charts/
    ├── 01_tdsi_ranking_bar.png         Top 10 TDSI scores
    ├── 02_age_vs_tdsi_scatter.png      Age vs TDSI bubble chart
    ├── 03_role_distribution_pie.png    Tactical role split
    ├── 04_radar_charts.png             Player radar charts
    └── 05_format_weight_sankey.png     Format weight breakdown
==============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import os
import warnings

warnings.filterwarnings('ignore')

# =============================================================================
# CONFIG
# =============================================================================

# RR Color Palette
RR_PINK   = '#EA1A85'   # Primary pink
RR_NAVY   = '#1A1F71'   # Primary navy
RR_GOLD   = '#F5B800'   # Accent gold
RR_WHITE  = '#FFFFFF'
RR_LIGHT  = '#F5F5F5'
RR_GREY   = '#888888'

ROLE_COLORS = {
    '🔴 Powerplay Enforcer':     RR_PINK,
    '🟢 Spin-Hitting Finisher':  '#00B050',
    '🔵 Death Bowler':           '#1A6EBD',
    '🟡 Impact/Mystery Spinner': RR_GOLD,
    '⚪ Utility Player':         RR_GREY,
}

OUTPUT_DIR = 'output/charts'


def set_rr_style():
    """Apply RR branding to all matplotlib figures."""
    plt.rcParams.update({
        'figure.facecolor': RR_NAVY,
        'axes.facecolor': '#1E2340',
        'axes.edgecolor': '#3A4080',
        'axes.labelcolor': RR_WHITE,
        'text.color': RR_WHITE,
        'xtick.color': RR_WHITE,
        'ytick.color': RR_WHITE,
        'grid.color': '#3A4080',
        'grid.alpha': 0.5,
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
    })


def add_rr_header(fig, title, subtitle="SupeRR Selector Season 2 | IPL 2027 Auction Intelligence"):
    """Add a consistent RR-branded header to each figure."""
    fig.text(0.5, 0.97, title, ha='center', va='top',
             fontsize=18, fontweight='bold', color=RR_WHITE,
             transform=fig.transFigure)
    fig.text(0.5, 0.94, subtitle, ha='center', va='top',
             fontsize=10, color=RR_PINK, style='italic',
             transform=fig.transFigure)
    # Pink underline
    line = plt.Line2D([0.05, 0.95], [0.925, 0.925], transform=fig.transFigure,
                      color=RR_PINK, linewidth=1.5)
    fig.add_artist(line)


def load_top10():
    """Load the top 10 results from the pipeline."""
    path = 'output/rr_top10_targets.csv'
    if not os.path.exists(path):
        print(f"  ✗ {path} not found. Run rr_scout_pipeline.py first.")
        return None
    df = pd.read_csv(path)
    print(f"  ✓ Loaded {len(df)} players from {path}")
    return df


# =============================================================================
# CHART 1: TDSI Ranking Bar Chart
# =============================================================================

def chart_tdsi_ranking(df):
    """Horizontal bar chart of Top 10 TDSI scores, colored by role."""
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor(RR_NAVY)
    ax.set_facecolor('#1E2340')
    
    # Sort by TDSI
    df_sorted = df.sort_values('TDSI', ascending=True)
    
    # Map roles to colors
    colors = [ROLE_COLORS.get(str(r), RR_GREY) for r in df_sorted.get('tactical_role', [RR_GREY]*len(df_sorted))]
    
    # Player labels
    if 'player_name' in df_sorted.columns:
        labels = df_sorted['player_name'].tolist()
    else:
        labels = [f"Player {i}" for i in range(len(df_sorted))]
    
    # Add age to label if available
    if 'age' in df_sorted.columns:
        labels = [f"{n}  (Age {int(a)})" if pd.notna(a) else n 
                  for n, a in zip(labels, df_sorted['age'])]
    
    bars = ax.barh(labels, df_sorted['TDSI'], color=colors, 
                   height=0.6, alpha=0.9, edgecolor=RR_WHITE, linewidth=0.3)
    
    # Value labels
    for bar, val in zip(bars, df_sorted['TDSI']):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}', va='center', ha='left', 
                color=RR_GOLD, fontweight='bold', fontsize=11)
    
    ax.set_xlim(0, min(100, df['TDSI'].max() * 1.15))
    ax.set_xlabel('Three-Dimensional Selection Index (TDSI) / 100', color=RR_WHITE, fontsize=12)
    ax.set_title('', pad=20)
    ax.grid(axis='x', alpha=0.3, color=RR_GREY)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(RR_GREY)
    ax.spines['left'].set_color(RR_GREY)
    
    # Legend
    legend_handles = [mpatches.Patch(color=c, label=r) 
                      for r, c in ROLE_COLORS.items() if c != RR_GREY]
    ax.legend(handles=legend_handles, loc='lower right', 
              facecolor='#1E2340', edgecolor=RR_PINK, labelcolor=RR_WHITE, fontsize=9)
    
    add_rr_header(fig, '🏆 TOP 10 UNCAPPED TARGETS — TDSI RANKING')
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    
    path = f'{OUTPUT_DIR}/01_tdsi_ranking_bar.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=RR_NAVY)
    plt.close()
    print(f"  ✓ Chart saved: {path}")


# =============================================================================
# CHART 2: Age vs TDSI Scatter (Bubble Chart)
# =============================================================================

def chart_age_vs_tdsi(df):
    """Scatter plot of Age vs TDSI — younger + higher TDSI = top-left = best targets."""
    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor(RR_NAVY)
    ax.set_facecolor('#1E2340')
    
    if 'age' not in df.columns or 'TDSI' not in df.columns:
        print("  ⚠ Skipping age/TDSI scatter — missing columns")
        return
    
    # Bubble size proportional to TDSI
    sizes = (df['TDSI'] / df['TDSI'].max() * 300 + 50).fillna(50)
    colors_list = [ROLE_COLORS.get(str(r), RR_GREY) 
                   for r in df.get('tactical_role', [RR_GREY]*len(df))]
    
    scatter = ax.scatter(df['age'], df['TDSI'], s=sizes, 
                         c=colors_list, alpha=0.85, 
                         edgecolors=RR_WHITE, linewidth=1.5, zorder=5)
    
    # Player name labels
    name_col = 'player_name' if 'player_name' in df.columns else df.columns[0]
    for _, row in df.iterrows():
        if pd.notna(row.get('age')) and pd.notna(row.get('TDSI')):
            ax.annotate(row[name_col], 
                        (row['age'], row['TDSI']),
                        textcoords='offset points', xytext=(10, 5),
                        fontsize=8.5, color=RR_WHITE, alpha=0.9,
                        fontweight='bold')
    
    # Sweet spot box — young AND high TDSI
    sweet_x = ax.get_xlim() if hasattr(ax, '_xlim') else (df['age'].min()-0.5, 21.5)
    sweet_y = df['TDSI'].quantile(0.5)
    ax.axhspan(sweet_y, df['TDSI'].max()*1.05, 
               alpha=0.08, color=RR_PINK, label='★ Sweet Spot Zone')
    ax.axvspan(df['age'].min()-0.5, 21.5, 
               alpha=0.05, color=RR_GOLD)
    
    ax.set_xlabel('Player Age (years)', fontsize=12, color=RR_WHITE)
    ax.set_ylabel('TDSI Score (out of 100)', fontsize=12, color=RR_WHITE)
    ax.grid(alpha=0.3, color=RR_GREY)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(RR_GREY)
    ax.spines['left'].set_color(RR_GREY)
    
    # Annotations for quadrant
    ax.text(0.03, 0.97, '◀ Younger', transform=ax.transAxes, 
            fontsize=9, color=RR_GOLD, va='top', style='italic')
    ax.text(0.03, 0.92, '▲ Higher TDSI', transform=ax.transAxes, 
            fontsize=9, color=RR_PINK, va='top', style='italic')
    
    legend_handles = [mpatches.Patch(color=c, label=r) 
                      for r, c in ROLE_COLORS.items() if c != RR_GREY]
    ax.legend(handles=legend_handles, loc='lower right',
              facecolor='#1E2340', edgecolor=RR_PINK, labelcolor=RR_WHITE, fontsize=9)
    
    add_rr_header(fig, '🎯 AGE vs TDSI — TARGET IDENTIFICATION MAP')
    plt.tight_layout(rect=[0, 0, 1, 0.91])
    
    path = f'{OUTPUT_DIR}/02_age_vs_tdsi_scatter.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=RR_NAVY)
    plt.close()
    print(f"  ✓ Chart saved: {path}")


# =============================================================================
# CHART 3: Role Distribution Donut
# =============================================================================

def chart_role_distribution(df):
    """Donut chart of tactical role distribution."""
    fig, ax = plt.subplots(figsize=(9, 7))
    fig.patch.set_facecolor(RR_NAVY)
    ax.set_facecolor(RR_NAVY)
    
    if 'tactical_role' not in df.columns:
        print("  ⚠ Skipping role distribution — missing column")
        return
    
    role_counts = df['tactical_role'].value_counts()
    colors_donut = [ROLE_COLORS.get(r, RR_GREY) for r in role_counts.index]
    
    wedges, texts, autotexts = ax.pie(
        role_counts.values,
        labels=None,
        colors=colors_donut,
        autopct='%1.0f%%',
        pctdistance=0.75,
        startangle=90,
        wedgeprops=dict(width=0.55, edgecolor=RR_NAVY, linewidth=2),
    )
    
    for autotext in autotexts:
        autotext.set_color(RR_WHITE)
        autotext.set_fontweight('bold')
        autotext.set_fontsize(13)
    
    # Center label
    ax.text(0, 0, f'Top\n{len(df)}\nTargets', ha='center', va='center',
            fontsize=14, fontweight='bold', color=RR_WHITE)
    
    # Legend
    legend_handles = [mpatches.Patch(color=ROLE_COLORS.get(r, RR_GREY), label=f"{r}\n({v} players)")
                      for r, v in role_counts.items()]
    ax.legend(handles=legend_handles, loc='lower center', 
              bbox_to_anchor=(0.5, -0.08),
              facecolor='#1E2340', edgecolor=RR_PINK, labelcolor=RR_WHITE, 
              fontsize=10, ncol=2)
    
    add_rr_header(fig, '⚡ TACTICAL ROLE DISTRIBUTION')
    plt.tight_layout(rect=[0, 0, 1, 0.91])
    
    path = f'{OUTPUT_DIR}/03_role_distribution_pie.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=RR_NAVY)
    plt.close()
    print(f"  ✓ Chart saved: {path}")


# =============================================================================
# CHART 4: Radar Charts for Top 5 Players
# =============================================================================

def chart_radar(df):
    """Radar/spider charts for top 5 players — submission-ready player cards."""
    
    # Radar metrics (use whatever is available)
    candidate_metrics = [
        ('SMAT_bat_strike_rate', 'T20 Strike Rate', False),
        ('SMAT_bat_boundary_pct', 'Boundary %', False),
        ('SMAT_bat_finishing_accel_index', 'Finishing Index', False),
        ('SMAT_bowl_dot_ball_pct', 'Dot Ball %', False),
        ('SMAT_bowl_economy', 'Economy (inverted)', True),   # True = invert (lower is better)
        ('TDSI', 'TDSI Score', False),
    ]
    
    # Find which metrics are available
    available = [(col, label, inv) for col, label, inv in candidate_metrics 
                 if col in df.columns and df[col].notna().any()]
    
    if len(available) < 3:
        print("  ⚠ Insufficient metrics for radar charts — using TDSI bar only")
        # Fallback: simple bar chart per player
        return chart_simple_player_bars(df)
    
    top5 = df.nlargest(5, 'TDSI').reset_index(drop=True)
    
    n_metrics = len(available)
    angles = np.linspace(0, 2 * np.pi, n_metrics, endpoint=False).tolist()
    angles += angles[:1]  # Close the polygon
    
    metric_labels = [label for _, label, _ in available]
    
    fig = plt.figure(figsize=(18, 8))
    fig.patch.set_facecolor(RR_NAVY)
    
    for idx, (_, player) in enumerate(top5.iterrows()):
        ax = fig.add_subplot(1, 5, idx + 1, polar=True)
        ax.set_facecolor('#1E2340')
        
        # Normalize values to 0-1 for radar
        values = []
        for col, label, invert in available:
            val = player.get(col, np.nan)
            if pd.isna(val):
                values.append(0.5)
                continue
            col_min = df[col].min()
            col_max = df[col].max()
            if col_max == col_min:
                normalized = 0.5
            else:
                normalized = (val - col_min) / (col_max - col_min)
            if invert:
                normalized = 1 - normalized
            values.append(normalized)
        
        values += values[:1]  # Close polygon
        
        # Role color
        role = str(player.get('tactical_role', ''))
        color = ROLE_COLORS.get(role, RR_PINK)
        
        ax.plot(angles, values, 'o-', linewidth=2, color=color)
        ax.fill(angles, values, alpha=0.25, color=color)
        
        # Metric labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metric_labels, size=7, color=RR_WHITE)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(['', '', '', ''], color=RR_GREY, size=6)
        ax.grid(color=RR_GREY, alpha=0.4)
        ax.spines['polar'].set_color(RR_GREY)
        
        # Player name
        name = str(player.get('player_name', f'Player {idx+1}'))
        age = player.get('age', '?')
        tdsi = player.get('TDSI', 0)
        ax.set_title(f"{name}\n(Age {int(age) if pd.notna(age) else '?'})\nTDSI: {tdsi:.1f}", 
                     size=9, color=RR_WHITE, fontweight='bold', pad=20)
    
    add_rr_header(fig, '📊 PLAYER PROFILE RADAR — TOP 5 TARGETS')
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    
    path = f'{OUTPUT_DIR}/04_radar_charts.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=RR_NAVY)
    plt.close()
    print(f"  ✓ Chart saved: {path}")


def chart_simple_player_bars(df):
    """Fallback: simple TDSI bar per player if radar metrics are unavailable."""
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor(RR_NAVY)
    ax.set_facecolor('#1E2340')
    
    top5 = df.nlargest(5, 'TDSI')
    names = top5.get('player_name', top5.index.astype(str))
    colors_list = [ROLE_COLORS.get(str(r), RR_PINK) 
                   for r in top5.get('tactical_role', [RR_PINK]*len(top5))]
    
    ax.bar(names, top5['TDSI'], color=colors_list, edgecolor=RR_WHITE, linewidth=0.5)
    ax.set_ylabel('TDSI Score', color=RR_WHITE)
    ax.grid(axis='y', alpha=0.3)
    
    path = f'{OUTPUT_DIR}/04_radar_charts.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=RR_NAVY)
    plt.close()
    print(f"  ✓ Chart saved: {path} (fallback mode)")


# =============================================================================
# CHART 5: TDSI Formula Infographic
# =============================================================================

def chart_methodology_infographic():
    """Visual explanation of the TDSI methodology."""
    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor(RR_NAVY)
    ax = fig.add_subplot(111)
    ax.set_facecolor(RR_NAVY)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'THREE-DIMENSIONAL SELECTION INDEX (TDSI)', 
            ha='center', va='center', fontsize=16, fontweight='bold', color=RR_WHITE)
    ax.text(5, 9.0, 'TDSI = (Format-Weighted Performance) × Age Bias Multiplier', 
            ha='center', va='center', fontsize=12, color=RR_PINK, style='italic')
    
    # --- Dimension 1: Format Weights ---
    dim1_x = 1.5
    ax.add_patch(FancyBboxPatch((0.3, 4.5), 2.8, 4.0, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#1E2340', edgecolor=RR_PINK, linewidth=2))
    ax.text(dim1_x, 8.2, 'DIMENSION 1', ha='center', fontsize=10, 
            color=RR_PINK, fontweight='bold')
    ax.text(dim1_x, 7.85, 'Format Suitability', ha='center', fontsize=11, 
            color=RR_WHITE, fontweight='bold')
    
    formats = [
        ('SMAT (T20)', 60, RR_PINK),
        ('VHT (List-A)', 30, RR_GOLD),
        ('Ranji (FC)', 10, '#00BFFF'),
    ]
    for i, (fmt, pct, col) in enumerate(formats):
        y = 7.3 - i * 0.85
        bar_w = pct / 100 * 2.6
        ax.add_patch(FancyBboxPatch((0.4, y - 0.25), bar_w, 0.4, 
                                    boxstyle="round,pad=0.05", facecolor=col, alpha=0.8))
        ax.text(dim1_x, y, f'{fmt}: {pct}%', ha='center', fontsize=9, 
                color=RR_WHITE, fontweight='bold')
    
    # --- Dimension 2: Recency Decay ---
    dim2_x = 5.0
    ax.add_patch(FancyBboxPatch((3.6, 4.5), 2.8, 4.0, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#1E2340', edgecolor=RR_GOLD, linewidth=2))
    ax.text(dim2_x, 8.2, 'DIMENSION 2', ha='center', fontsize=10, 
            color=RR_GOLD, fontweight='bold')
    ax.text(dim2_x, 7.85, 'Recency & Form', ha='center', fontsize=11, 
            color=RR_WHITE, fontweight='bold')
    
    seasons = [
        ('2026/27 Cycle', '× 1.00', '#00C853'),
        ('2025 Cycle', '× 0.60', RR_GOLD),
        ('≤2024 Cycle', '× 0.30', '#FF5252'),
    ]
    for i, (season, mult, col) in enumerate(seasons):
        y = 7.3 - i * 0.85
        ax.text(dim2_x - 1.2, y, season, ha='left', fontsize=9, 
                color=RR_WHITE)
        ax.text(dim2_x + 1.1, y, mult, ha='right', fontsize=10, 
                color=col, fontweight='bold')
    
    # --- Dimension 3: Age Multiplier ---
    dim3_x = 8.5
    ax.add_patch(FancyBboxPatch((6.9, 4.5), 2.8, 4.0, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#1E2340', edgecolor='#00BFFF', linewidth=2))
    ax.text(dim3_x, 8.2, 'DIMENSION 3', ha='center', fontsize=10, 
            color='#00BFFF', fontweight='bold')
    ax.text(dim3_x, 7.85, 'Age Bias Multiplier', ha='center', fontsize=11, 
            color=RR_WHITE, fontweight='bold')
    
    ages = [
        ('Age 17–19', '× 1.00', '#00C853'),
        ('Age 20–21', '× 0.85', '#69F0AE'),
        ('Age 22–23', '× 0.60', RR_GOLD),
        ('Age 24+',   '× 0.35', '#FF5252'),
    ]
    for i, (age_range, mult, col) in enumerate(ages):
        y = 7.3 - i * 0.70
        ax.text(dim3_x - 1.2, y, age_range, ha='left', fontsize=9, 
                color=RR_WHITE)
        ax.text(dim3_x + 1.1, y, mult, ha='right', fontsize=10, 
                color=col, fontweight='bold')
    
    # --- Bottom: Output ---
    ax.add_patch(FancyBboxPatch((2.5, 1.5), 5.0, 2.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor=RR_PINK, edgecolor=RR_GOLD, linewidth=2.5, alpha=0.9))
    ax.text(5, 3.3, '★  OUTPUT  ★', ha='center', fontsize=12, 
            color=RR_GOLD, fontweight='bold')
    ax.text(5, 2.75, 'Top 10 Youngest Uncapped Domestic Anomalies', 
            ha='center', fontsize=11, color=RR_WHITE, fontweight='bold')
    ax.text(5, 2.2, 'Ranked by TDSI · Clustered by Tactical Role', 
            ha='center', fontsize=10, color=RR_WHITE)
    ax.text(5, 1.75, 'Filtered: Age ≤23 · Uncapped · Min. Matches Qualified', 
            ha='center', fontsize=9, color=RR_WHITE, alpha=0.85)
    
    # Arrows
    for x in [1.5, 5.0, 8.5]:
        ax.annotate('', xy=(5, 3.95), xytext=(x, 4.5),
                    arrowprops=dict(arrowstyle='->', color=RR_WHITE, lw=1.5))
    
    add_rr_header(fig, '⚙️ TDSI METHODOLOGY FRAMEWORK')
    ax.set_position([0, 0, 1, 0.92])
    
    path = f'{OUTPUT_DIR}/05_tdsi_methodology.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=RR_NAVY)
    plt.close()
    print(f"  ✓ Chart saved: {path}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║   RAJASTHAN ROYALS — WAR ROOM VISUALIZER                       ║
    ║   Generating Submission-Ready Charts...                        ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    set_rr_style()
    
    df = load_top10()
    
    if df is None:
        print("  → Run rr_scout_pipeline.py first to generate player data.")
        print("  → Generating methodology infographic only...")
        chart_methodology_infographic()
        return
    
    print("\n  Generating charts:")
    chart_tdsi_ranking(df)
    chart_age_vs_tdsi(df)
    chart_role_distribution(df)
    chart_radar(df)
    chart_methodology_infographic()
    
    print(f"\n  ✓ ALL CHARTS SAVED TO: {OUTPUT_DIR}/")
    print("\n  Include these in your submission:")
    print("    01_tdsi_ranking_bar.png       → Section: Final Rankings")
    print("    02_age_vs_tdsi_scatter.png    → Section: Methodology Validation")
    print("    03_role_distribution_pie.png  → Section: Tactical Balance")
    print("    04_radar_charts.png           → Section: Player Profiles")
    print("    05_tdsi_methodology.png       → Section: Framework Overview")


if __name__ == "__main__":
    main()

