import os
import json
import base64
from pathlib import Path

# Load RR Logo
with open("rr_logo.png", "rb") as f:
    rr_logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

# Load all 20 player images
img_dir = Path("player_images")
player_images = {}
for p in img_dir.glob("*.png"):
    with open(p, "rb") as f:
        player_images[p.stem] = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

with open("players_db.json", "r", encoding="utf-8") as f:
    players_db = json.load(f)

# Create players directory for standalone pages
os.makedirs("players", exist_ok=True)

# Generate individual standalone pages for each player
for idx, p in enumerate(players_db):
    prev_p = players_db[idx - 1] if idx > 0 else players_db[-1]
    next_p = players_db[idx + 1] if idx < len(players_db) - 1 else players_db[0]
    
    img_b64 = player_images.get(p["key"], "")
    lift_sign = f"+{p['lift']:.1f}%" if p['lift'] >= 0 else f"{p['lift']:.1f}%"
    lift_class = "lift-positive" if p['lift'] >= 0 else "lift-negative"
    
    player_page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p['name']} — Player Dossier | Rajasthan Royals Analytics</title>
    <style>
        :root {{
            --rr-pink: #EB1A8D;
            --rr-navy: #001D48;
            --bg-page: #F4F6F9;
            --bg-card: #FFFFFF;
            --border: #E2E8F0;
            --text-main: #0F172A;
            --text-muted: #64748B;
            --badge-green: #16A34A;
            --badge-green-bg: #DCFCE7;
            --badge-red: #DC2626;
            --badge-red-bg: #FEE2E2;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            padding: 24px;
            line-height: 1.5;
        }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        .nav-back {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--rr-navy);
            color: #FFFFFF;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 20px;
            transition: transform 0.15s ease;
        }}
        .nav-back:hover {{ transform: translateX(-3px); }}
        .hero-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 28px;
            display: flex;
            align-items: center;
            gap: 28px;
            margin-bottom: 24px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
            flex-wrap: wrap;
        }}
        .hero-avatar {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 4px solid var(--rr-pink);
            overflow: hidden;
            background: #F8FAFC;
            box-shadow: 0 4px 12px rgba(235,26,141,0.2);
            flex-shrink: 0;
        }}
        .hero-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}
        .hero-info {{ flex: 1; min-width: 260px; }}
        .rank-pill {{
            display: inline-block;
            background: var(--rr-pink);
            color: #FFFFFF;
            font-size: 12px;
            font-weight: 800;
            padding: 4px 12px;
            border-radius: 20px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}
        .hero-name {{ font-size: 28px; font-weight: 800; color: var(--rr-navy); }}
        .hero-teams {{ font-size: 14px; color: var(--text-muted); margin-bottom: 8px; }}
        .hero-role {{ font-size: 13px; font-weight: 700; color: var(--rr-pink); }}
        .hero-score-box {{
            background: #F8FAFC;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 24px;
            text-align: center;
            min-width: 140px;
        }}
        .hero-score-val {{ font-size: 32px; font-weight: 900; color: var(--rr-navy); line-height: 1; }}
        .hero-score-lbl {{ font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-top: 4px; }}
        
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 12px;
            margin-bottom: 24px;
        }}
        .metric-tile {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px;
            text-align: center;
        }}
        .metric-tile-val {{ font-size: 20px; font-weight: 800; color: var(--rr-navy); }}
        .metric-tile-lbl {{ font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-top: 4px; }}
        
        .section-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }}
        .section-title {{
            font-size: 16px;
            font-weight: 800;
            color: var(--rr-navy);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid #F1F5F9;
            padding-bottom: 8px;
        }}
        .section-body {{ font-size: 14px; color: var(--text-main); line-height: 1.6; }}
        
        .chart-box {{
            background: #F8FAFC;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            margin-top: 14px;
        }}
        .bar-row {{ display: flex; align-items: center; margin-bottom: 10px; font-size: 12px; }}
        .bar-lbl {{ width: 140px; font-weight: 700; color: var(--rr-navy); }}
        .bar-track {{ flex: 1; height: 12px; background: #E2E8F0; border-radius: 6px; overflow: hidden; margin: 0 12px; }}
        .bar-fill {{ height: 100%; border-radius: 6px; }}
        .bar-val {{ width: 60px; font-weight: 800; text-align: right; }}

        .bottom-nav {{
            display: flex;
            justify-content: space-between;
            margin-top: 32px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
        }}
        .bottom-nav a {{
            color: var(--rr-navy);
            text-decoration: none;
            font-weight: 700;
            font-size: 13px;
            padding: 8px 16px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: #FFFFFF;
        }}
        @media (max-width: 768px) {{
            .kpi-row {{ grid-template-columns: repeat(2, 1fr); }}
            .hero-card {{ flex-direction: column; text-align: center; }}
            .hero-info {{ text-align: center; }}
        }}
    </style>
</head>
<body>
<div class="container">
    <a href="../rr_pressure_dashboard.html" class="nav-back">← Back to Master Leaderboard</a>
    
    <div class="hero-card">
        <div class="hero-avatar">
            <img src="{img_b64}" alt="{p['name']}">
        </div>
        <div class="hero-info">
            <span class="rank-pill">Rank #{p['rank']} {p['category']} Under Pressure</span>
            <h1 class="hero-name">{p['name']}</h1>
            <div class="hero-teams">{p['teams']}</div>
            <div class="hero-role">🎯 Tactical Role: {p['tactical_role']}</div>
        </div>
        <div class="hero-score-box">
            <div class="hero-score-val">{p['cppi']:.2f}</div>
            <div class="hero-score-lbl">CPPI Score</div>
            <div style="font-size:11px;color:var(--rr-pink);font-weight:700;margin-top:4px;">Bid Ceiling: {p['bid_ceiling']}</div>
        </div>
    </div>

    <div class="kpi-row">
        <div class="metric-tile">
            <div class="metric-tile-val">{p['hp_m']}</div>
            <div class="metric-tile-lbl">HP Matches</div>
        </div>
        <div class="metric-tile">
            <div class="metric-tile-val" style="color:var(--rr-pink);">{p['hp_wr']:.1f}%</div>
            <div class="metric-tile-lbl">HP Win Rate</div>
        </div>
        <div class="metric-tile">
            <div class="metric-tile-val">{p['base_wr']:.1f}%</div>
            <div class="metric-tile-lbl">Base Win Rate</div>
        </div>
        <div class="metric-tile">
            <div class="metric-tile-val" style="color:{'var(--badge-green)' if p['lift']>=0 else 'var(--badge-red)'};">{lift_sign}</div>
            <div class="metric-tile-lbl">Pressure Lift (∆)</div>
        </div>
        <div class="metric-tile">
            <div class="metric-tile-val">{p['mom_hp']}</div>
            <div class="metric-tile-lbl">HP MOMs</div>
        </div>
        <div class="metric-tile">
            <div class="metric-tile-val">{p['ko_wr']:.1f}%</div>
            <div class="metric-tile-lbl">Knockout Win%</div>
        </div>
    </div>

    <!-- Comparative Visual Chart -->
    <div class="section-card">
        <div class="section-title">📊 Leverage Performance Comparative Breakdown</div>
        <div class="chart-box">
            <div class="bar-row">
                <span class="bar-lbl">High-Pressure Win Rate</span>
                <div class="bar-track"><div class="bar-fill" style="width:{p['hp_wr']}%;background:var(--rr-pink);"></div></div>
                <span class="bar-val" style="color:var(--rr-pink);">{p['hp_wr']:.1f}%</span>
            </div>
            <div class="bar-row">
                <span class="bar-lbl">Career Baseline Win Rate</span>
                <div class="bar-track"><div class="bar-fill" style="width:{p['base_wr']}%;background:#64748B;"></div></div>
                <span class="bar-val" style="color:#64748B;">{p['base_wr']:.1f}%</span>
            </div>
            <div class="bar-row">
                <span class="bar-lbl">Knockout / Playoff Win%</span>
                <div class="bar-track"><div class="bar-fill" style="width:{p['ko_wr']}%;background:var(--rr-navy);"></div></div>
                <span class="bar-val" style="color:var(--rr-navy);">{p['ko_wr']:.1f}%</span>
            </div>
        </div>
    </div>

    <!-- Strategic Deep Dives -->
    <div class="section-card">
        <div class="section-title">🎯 Why We Chose Him (Clutch Proof & Evidence)</div>
        <div class="section-body">{p['why_chose']}</div>
    </div>

    <div class="section-card">
        <div class="section-title">⚖️ Why Not Others & Positional Ranking Rationale</div>
        <div class="section-body">{p['why_not_others']}</div>
    </div>

    <div class="section-card">
        <div class="section-title">🏟️ Rajasthan Royals Fit for IPL 2027 Auction (SMS Stadium Dynamics)</div>
        <div class="section-body">{p['rr_fit']}</div>
        <div style="margin-top:12px;background:#F8FAFC;padding:12px;border-radius:8px;font-weight:700;color:var(--rr-navy);font-size:13px;">
            💰 Recommended Bid Ceiling: <span style="color:var(--rr-pink);">{p['bid_ceiling']}</span> | Verdict: {p['verdict']}
        </div>
    </div>

    <div class="bottom-nav">
        <a href="{prev_p['key']}.html">← #{prev_p['rank']} {prev_p['name']}</a>
        <a href="../rr_pressure_dashboard.html">🏠 Back to Dashboard</a>
        <a href="{next_p['key']}.html">#{next_p['rank']} {next_p['name']} →</a>
    </div>
</div>
</body>
</html>
"""
    with open(f"players/{p['key']}.html", "w", encoding="utf-8") as pf:
        pf.write(player_page_html)

print(f"Generated 20 standalone player pages in /players/ directory.")

# Now, generate the master dashboard with in-app SPA dossier routing
top10_batters = [p for p in players_db if p["category"] == "Batter"]
top10_bowlers = [p for p in players_db if p["category"] == "Bowler"]

superstars_audit = [
    {
        "name": "Jasprit Bumrah",
        "total_m": 56,
        "base_wr": 52.0,
        "hp_m": 14,
        "hp_wr": 42.9,
        "lift": -9.1,
        "mom_hp": 4,
        "ko_wr": 40.0,
        "reason": "Oppositions strategically play out his 4 overs with zero risk, aggressively targeting auxiliary bowlers. While individual economy remains elite, team pressure win rate dips by 9.1%."
    },
    {
        "name": "Mohammed Siraj",
        "total_m": 67,
        "base_wr": 55.4,
        "hp_m": 18,
        "hp_wr": 38.9,
        "lift": -16.5,
        "mom_hp": 1,
        "ko_wr": 28.6,
        "reason": "Severe negative pressure sensitivity. Win rate plummets from 55.4% to 38.9% in high-leverage contests, with elevated boundary concessions in death overs."
    },
    {
        "name": "Rashid Khan",
        "total_m": 122,
        "base_wr": 57.4,
        "hp_m": 26,
        "hp_wr": 38.5,
        "lift": -18.9,
        "mom_hp": 1,
        "ko_wr": 42.9,
        "reason": "Dramatic 18.9% pressure lift deficit across 26 high-pressure matches. Batters refuse to attack him, mitigating wicket-taking upside in close finishes."
    },
    {
        "name": "Heinrich Klaasen",
        "total_m": 68,
        "base_wr": 48.7,
        "hp_m": 15,
        "hp_wr": 40.0,
        "lift": -8.7,
        "mom_hp": 1,
        "ko_wr": 25.0,
        "reason": "Ultra-aggressive intent suffers from high variance under elimination stakes (25.0% Knockout Win Rate across 4 playoff fixtures)."
    },
    {
        "name": "Rohit Sharma",
        "total_m": 95,
        "base_wr": 51.1,
        "hp_m": 19,
        "hp_wr": 47.4,
        "lift": -3.7,
        "mom_hp": 1,
        "ko_wr": 40.0,
        "reason": "High-risk powerplay exploitation yields negative pressure lift (-3.7%), with early dismissals exposing fragile middle orders in knockout fixtures."
    }
]

# Write Master Dashboard HTML
master_dashboard_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>Rajasthan Royals — Pressure Performance BI Dashboard</title>
    <style>
        :root {{
            --rr-pink: #EB1A8D;
            --rr-pink-light: #FDF2F8;
            --rr-navy: #001D48;
            --rr-navy-light: #0A2540;
            --bg-page: #F4F6F9;
            --bg-card: #FFFFFF;
            --border-card: #E2E8F0;
            --text-main: #0F172A;
            --text-muted: #64748B;
            --badge-green: #16A34A;
            --badge-green-bg: #DCFCE7;
            --badge-red: #DC2626;
            --badge-red-bg: #FEE2E2;
            --badge-blue: #0284C7;
            --badge-blue-bg: #E0F2FE;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ width: 100%; overflow-x: hidden; }}
        body {{
            font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            padding: 24px;
            line-height: 1.45;
            -webkit-font-smoothing: antialiased;
        }}

        .dashboard-container {{
            max-width: 1440px;
            margin: 0 auto;
            width: 100%;
        }}

        /* Header / Brand Banner */
        .header-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 20px 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            flex-wrap: wrap;
            gap: 16px;
        }}

        .header-brand {{
            display: flex;
            align-items: center;
            gap: 20px;
            flex: 1 1 auto;
            min-width: 280px;
        }}

        .rr-logo-img {{
            height: 68px;
            width: auto;
            object-fit: contain;
            flex-shrink: 0;
        }}

        .header-title-box h1 {{
            font-size: 22px;
            font-weight: 800;
            color: var(--rr-navy);
            letter-spacing: -0.3px;
            margin-bottom: 4px;
            line-height: 1.25;
        }}

        .header-title-box p {{
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .header-title-box .analyst-tag {{
            color: var(--rr-pink);
            font-weight: 700;
        }}

        .header-meta {{
            text-align: right;
            border-left: 2px solid var(--border-card);
            padding-left: 20px;
            flex-shrink: 0;
        }}

        .header-meta .status-badge {{
            display: inline-block;
            background: var(--badge-green-bg);
            color: var(--badge-green);
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }}

        .header-meta .meta-text {{
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 600;
            white-space: nowrap;
        }}

        /* KPI Cards Ribbon */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}

        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 10px;
            padding: 16px 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .kpi-card::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--rr-navy);
        }}

        .kpi-card.highlight::after {{ background: var(--rr-pink); }}

        .kpi-label {{
            font-size: 12px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}

        .kpi-value {{
            font-size: 28px;
            font-weight: 800;
            color: var(--rr-navy);
            line-height: 1.1;
            margin-bottom: 4px;
        }}

        .kpi-sub {{
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 500;
        }}

        /* Section Pill Header */
        .section-pill-wrapper {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .pill-header {{
            display: inline-flex;
            align-items: center;
            background: var(--rr-navy);
            color: #FFFFFF;
            font-size: 13px;
            font-weight: 700;
            padding: 8px 22px;
            border-radius: 24px;
            letter-spacing: 0.3px;
            box-shadow: 0 2px 4px rgba(0,29,72,0.15);
        }}

        .scroll-tip {{
            font-size: 11px;
            color: var(--rr-pink);
            font-weight: 700;
        }}

        /* Visuals Grid */
        .visuals-row {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}

        .visual-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .visual-card-title {{
            font-size: 14px;
            font-weight: 700;
            color: var(--rr-navy);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #F1F5F9;
            padding-bottom: 10px;
        }}

        .donut-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 180px;
            width: 100%;
        }}

        .donut-svg {{ max-width: 100%; height: auto; }}

        /* Interactive Filter Bar */
        .filter-bar {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 10px;
            padding: 12px 20px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .tab-btn-group {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .tab-btn {{
            background: var(--bg-page);
            border: 1px solid var(--border-card);
            color: var(--text-main);
            padding: 9px 18px;
            font-size: 13px;
            font-weight: 700;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .tab-btn:hover {{ background: #E2E8F0; }}
        .tab-btn.active {{
            background: var(--rr-pink);
            color: #FFFFFF;
            border-color: var(--rr-pink);
            box-shadow: 0 2px 4px rgba(235,26,141,0.25);
        }}

        .search-box {{
            display: flex;
            align-items: center;
            background: var(--bg-page);
            border: 1px solid var(--border-card);
            border-radius: 8px;
            padding: 8px 14px;
            width: 280px;
        }}

        .search-box input {{
            border: none;
            background: transparent;
            outline: none;
            font-size: 13px;
            width: 100%;
            color: var(--text-main);
            font-family: inherit;
        }}

        /* Responsive Table */
        .table-responsive {{
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            border-radius: 12px;
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            margin-bottom: 24px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
            min-width: 860px;
        }}

        thead tr {{
            background: #F8FAFC;
            border-bottom: 2px solid var(--border-card);
        }}

        th {{
            padding: 12px 14px;
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }}

        tbody tr {{
            border-bottom: 1px solid #F1F5F9;
            transition: background 0.12s ease;
            cursor: pointer;
        }}

        tbody tr:hover {{
            background: #FDF2F8 !important;
        }}

        td {{
            padding: 12px 14px;
            vertical-align: middle;
            color: var(--text-main);
        }}

        /* Rank Badge */
        .rank-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            font-size: 12px;
            font-weight: 800;
            background: #F1F5F9;
            color: var(--text-main);
            flex-shrink: 0;
        }}

        .rank-1 {{ background: #FEF3C7; color: #B45309; border: 1px solid #FCD34D; }}
        .rank-2 {{ background: #F1F5F9; color: #475569; border: 1px solid #CBD5E1; }}
        .rank-3 {{ background: #FFEDD5; color: #C2410C; border: 1px solid #FDBA74; }}

        /* Player Cell */
        .player-cell {{
            display: flex;
            align-items: center;
            gap: 12px;
            min-width: 200px;
        }}

        .player-img-wrapper {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: #F1F5F9;
            border: 2px solid #E2E8F0;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}

        .player-img-wrapper img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .player-name {{
            font-weight: 700;
            color: var(--rr-navy);
            font-size: 14px;
            line-height: 1.2;
        }}

        .player-teams {{
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 2px;
            line-height: 1.3;
        }}

        .metric-cell {{ font-weight: 600; white-space: nowrap; }}

        .lift-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            text-align: center;
            white-space: nowrap;
        }}

        .lift-positive {{ background: var(--badge-green-bg); color: var(--badge-green); }}
        .lift-negative {{ background: var(--badge-red-bg); color: var(--badge-red); }}

        .cppi-score {{ font-size: 15px; font-weight: 800; color: var(--rr-navy); }}
        .score-bar-bg {{ width: 70px; height: 6px; background: #E2E8F0; border-radius: 3px; overflow: hidden; margin-top: 4px; }}
        .score-bar-fill {{ height: 100%; background: var(--rr-pink); border-radius: 3px; }}

        .btn-view-dossier {{
            background: #F8FAFC;
            border: 1px solid var(--border-card);
            color: var(--rr-navy);
            font-weight: 700;
            font-size: 11px;
            padding: 6px 12px;
            border-radius: 6px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .btn-view-dossier:hover {{
            background: var(--rr-pink);
            color: #FFFFFF;
            border-color: var(--rr-pink);
        }}

        /* Methodology & References Card */
        .grid-2col {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}

        .doc-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 22px 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }}

        .doc-title {{
            font-size: 16px;
            font-weight: 800;
            color: var(--rr-navy);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .formula-box {{
            background: #F8FAFC;
            border: 1px solid var(--border-card);
            border-left: 4px solid var(--rr-pink);
            padding: 12px 16px;
            border-radius: 6px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 12px;
            color: var(--rr-navy);
            margin-bottom: 14px;
            line-height: 1.5;
            overflow-x: auto;
        }}

        .doc-list {{ list-style: none; font-size: 13px; color: var(--text-main); }}
        .doc-list li {{ margin-bottom: 8px; display: flex; align-items: flex-start; gap: 8px; }}
        .doc-list li strong {{ color: var(--rr-navy); min-width: 130px; }}

        .ref-item {{
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 10px;
            padding-left: 12px;
            border-left: 2px solid var(--border-card);
            line-height: 1.4;
        }}
        .ref-item strong {{ color: var(--rr-navy); }}

        /* ═══════════════════════════════════════════════════════ */
        /* DEDICATED FULL-PAGE IN-APP PLAYER DOSSIER VIEW          */
        /* ═══════════════════════════════════════════════════════ */
        #player-dossier-view {{
            display: none;
            width: 100%;
            animation: fadeIn 0.2s ease-in-out;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .dossier-nav-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .btn-back-main {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--rr-navy);
            color: #FFFFFF;
            padding: 10px 22px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
            border: none;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,29,72,0.15);
        }}

        .btn-back-main:hover {{ background: #0A2540; }}

        .btn-open-ext {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #FFFFFF;
            color: var(--rr-navy);
            padding: 9px 18px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
            border: 1px solid var(--border-card);
            text-decoration: none;
        }}

        .btn-open-ext:hover {{ border-color: var(--rr-pink); color: var(--rr-pink); }}

        .dossier-hero {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 14px;
            padding: 28px;
            display: flex;
            align-items: center;
            gap: 28px;
            margin-bottom: 24px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
            flex-wrap: wrap;
        }}

        .dossier-avatar {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 4px solid var(--rr-pink);
            overflow: hidden;
            background: #F8FAFC;
            box-shadow: 0 4px 12px rgba(235,26,141,0.2);
            flex-shrink: 0;
        }}

        .dossier-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}
        .dossier-info {{ flex: 1; min-width: 260px; }}
        .dossier-rank-badge {{
            display: inline-block;
            background: var(--rr-pink);
            color: #FFFFFF;
            font-size: 12px;
            font-weight: 800;
            padding: 4px 12px;
            border-radius: 20px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}
        .dossier-name {{ font-size: 28px; font-weight: 800; color: var(--rr-navy); margin-bottom: 4px; }}
        .dossier-teams {{ font-size: 14px; color: var(--text-muted); margin-bottom: 8px; }}
        .dossier-role {{ font-size: 13px; font-weight: 700; color: var(--rr-pink); }}

        .dossier-score-card {{
            background: #F8FAFC;
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 16px 24px;
            text-align: center;
            min-width: 140px;
        }}

        .dossier-score-val {{ font-size: 32px; font-weight: 900; color: var(--rr-navy); line-height: 1; }}
        .dossier-score-lbl {{ font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-top: 4px; }}

        .dossier-kpis {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 12px;
            margin-bottom: 24px;
        }}

        .dossier-kpi-tile {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 10px;
            padding: 14px;
            text-align: center;
        }}

        .dossier-kpi-val {{ font-size: 20px; font-weight: 800; color: var(--rr-navy); }}
        .dossier-kpi-lbl {{ font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-top: 4px; }}

        .dossier-section {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }}

        .dossier-sec-title {{
            font-size: 16px;
            font-weight: 800;
            color: var(--rr-navy);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid #F1F5F9;
            padding-bottom: 8px;
        }}

        .dossier-sec-body {{ font-size: 14px; color: var(--text-main); line-height: 1.6; }}

        /* Responsive Media Queries */
        @media (max-width: 1280px) {{
            .kpi-grid {{ grid-template-columns: repeat(3, 1fr); }}
            .visuals-row {{ grid-template-columns: 1fr 1fr; }}
            .visual-card:nth-child(1) {{ grid-column: span 2; }}
        }}

        @media (max-width: 1024px) {{
            body {{ padding: 16px; }}
            .header-card {{ padding: 16px 20px; }}
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .kpi-card:last-child {{ grid-column: span 2; }}
            .visuals-row {{ grid-template-columns: 1fr; }}
            .visual-card:nth-child(1) {{ grid-column: span 1; }}
            .grid-2col {{ grid-template-columns: 1fr; }}
            .dossier-kpis {{ grid-template-columns: repeat(3, 1fr); }}
        }}

        @media (max-width: 768px) {{
            body {{ padding: 10px 8px; }}
            .header-card {{ padding: 16px 14px; flex-direction: column; align-items: flex-start; }}
            .header-brand {{ flex-direction: column; align-items: flex-start; gap: 10px; width: 100%; }}
            .rr-logo-img {{ height: 48px; }}
            .header-title-box h1 {{ font-size: 17px; }}
            .header-meta {{ border-left: none; border-top: 1px solid var(--border-card); padding-left: 0; padding-top: 10px; width: 100%; text-align: left; }}
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
            .filter-bar {{ flex-direction: column; align-items: stretch; gap: 12px; }}
            .tab-btn-group {{ flex-direction: column; width: 100%; }}
            .tab-btn {{ width: 100%; text-align: center; }}
            .search-box {{ width: 100%; }}
            .dossier-hero {{ flex-direction: column; text-align: center; }}
            .dossier-info {{ text-align: center; }}
            .dossier-kpis {{ grid-template-columns: repeat(2, 1fr); }}
        }}

        @media (max-width: 400px) {{
            .kpi-grid {{ grid-template-columns: 1fr; }}
            .kpi-card:last-child {{ grid-column: span 1; }}
            .dossier-kpis {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>

<div class="dashboard-container">

    <!-- ═══════════════════════════════════════════════════════ -->
    <!-- VIEW A: MASTER DASHBOARD LEADERBOARD                   -->
    <!-- ═══════════════════════════════════════════════════════ -->
    <div id="master-dashboard-view">

        <!-- 1. HEADER BRAND BANNER -->
        <header class="header-card">
            <div class="header-brand">
                <img src="{rr_logo_b64}" alt="Rajasthan Royals" class="rr-logo-img">
                <div class="header-title-box">
                    <h1>Rajasthan Royals — Pressure Performance BI Dashboard</h1>
                    <p>SupeRR Selector Season 2 · Round 1 Analytics Engine | Analyst: <span class="analyst-tag">Ketan Rawat</span> (B.Tech ECE, NIT Jamshedpur | Season 1 Top 36 Finalist)</p>
                </div>
            </div>
            <div class="header-meta">
                <span class="status-badge">Certified Dossier Output</span>
                <div class="meta-text">Scope: 883 Matches (IPL 2022–2026 + T20Is)</div>
                <div class="meta-text" style="color:var(--rr-pink);font-weight:700;">100% BCCI Auction Eligible</div>
            </div>
        </header>

        <!-- 2. POWER BI / TABLEAU KPI RIBBON -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Matches Screened</div>
                <div class="kpi-value">883</div>
                <div class="kpi-sub">IPL & T20I (2022–2026)</div>
            </div>
            <div class="kpi-card highlight">
                <div class="kpi-label">High-Pressure Matches</div>
                <div class="kpi-value">180</div>
                <div class="kpi-sub">Match Leverage Index ≥ 30 (20.4%)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Players Evaluated</div>
                <div class="kpi-value">1,217</div>
                <div class="kpi-sub">Mapped in Master Database</div>
            </div>
            <div class="kpi-card highlight">
                <div class="kpi-label">Auction Realism</div>
                <div class="kpi-value">100%</div>
                <div class="kpi-sub">BCCI Policy Compliant (IPL 2027)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Model Stability</div>
                <div class="kpi-value">ρ = 0.884</div>
                <div class="kpi-sub">Leave-One-Season-Out (LOSO)</div>
            </div>
        </div>

        <!-- 3. VISUALS ROW (MATCH STAKES DONUT + TOP LIFT BARS) -->
        <div class="section-pill-wrapper">
            <div class="pill-header">Performance Metrics & Context Breakdown</div>
        </div>

        <div class="visuals-row">
            <!-- Visual 1: Match Stakes Donut -->
            <div class="visual-card">
                <div class="visual-card-title">
                    <span>Pressure Context Distribution</span>
                    <span style="font-size:11px;color:var(--text-muted);">180 High-Pressure Games</span>
                </div>
                <div class="donut-container">
                    <svg width="240" height="170" viewBox="0 0 240 170" class="donut-svg">
                        <circle cx="95" cy="85" r="60" fill="transparent" stroke="#E2E8F0" stroke-width="24"/>
                        <circle cx="95" cy="85" r="60" fill="transparent" stroke="#001D48" stroke-width="24" stroke-dasharray="158 219" stroke-dashoffset="0"/>
                        <circle cx="95" cy="85" r="60" fill="transparent" stroke="#EB1A8D" stroke-width="24" stroke-dasharray="132 245" stroke-dashoffset="-158"/>
                        <circle cx="95" cy="85" r="60" fill="transparent" stroke="#0284C7" stroke-width="24" stroke-dasharray="56 321" stroke-dashoffset="-290"/>
                        <circle cx="95" cy="85" r="60" fill="transparent" stroke="#16A34A" stroke-width="24" stroke-dasharray="30 347" stroke-dashoffset="-346"/>
                        <text x="95" y="82" text-anchor="middle" font-size="16" font-weight="800" fill="#001D48">180</text>
                        <text x="95" y="98" text-anchor="middle" font-size="10" font-weight="600" fill="#64748B">GAMES</text>
                        <g transform="translate(170, 30)" font-size="11" font-weight="600">
                            <circle cx="6" cy="6" r="5" fill="#001D48"/>
                            <text x="16" y="10" fill="#0F172A">Close (42%)</text>
                            <circle cx="6" cy="32" r="5" fill="#EB1A8D"/>
                            <text x="16" y="36" fill="#0F172A">Finals (35%)</text>
                            <circle cx="6" cy="58" r="5" fill="#0284C7"/>
                            <text x="16" y="62" fill="#0F172A">Elim (15%)</text>
                            <circle cx="6" cy="84" r="5" fill="#16A34A"/>
                            <text x="16" y="88" fill="#0F172A">DLS (8%)</text>
                        </g>
                    </svg>
                </div>
                <p style="font-size:11px;color:var(--text-muted);text-align:center;margin-top:4px;">Multi-Axis Match Leverage Index (MLI) distribution across 883 matches.</p>
            </div>

            <!-- Visual 2: Top Batters Pressure Lift Bar -->
            <div class="visual-card">
                <div class="visual-card-title">
                    <span>Top Batters — Pressure Lift (∆%)</span>
                    <span style="font-size:11px;color:var(--badge-green);font-weight:700;">High Clutch</span>
                </div>
                <div style="font-size:12px;">
                    <div style="margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                            <span style="font-weight:700;">1. Devon Conway</span>
                            <span style="font-weight:800;color:var(--badge-green);">+18.1%</span>
                        </div>
                        <div style="background:#F1F5F9;height:6px;border-radius:3px;"><div style="background:var(--badge-green);width:90%;height:100%;border-radius:3px;"></div></div>
                    </div>
                    <div style="margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                            <span style="font-weight:700;">2. Shivam Dube</span>
                            <span style="font-weight:800;color:var(--badge-green);">+12.4%</span>
                        </div>
                        <div style="background:#F1F5F9;height:6px;border-radius:3px;"><div style="background:var(--badge-green);width:68%;height:100%;border-radius:3px;"></div></div>
                    </div>
                    <div style="margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                            <span style="font-weight:700;">3. Rajat Patidar</span>
                            <span style="font-weight:800;color:var(--rr-pink);">+11.1%</span>
                        </div>
                        <div style="background:#F1F5F9;height:6px;border-radius:3px;"><div style="background:var(--rr-pink);width:62%;height:100%;border-radius:3px;"></div></div>
                    </div>
                    <div style="margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                            <span style="font-weight:700;">4. Bhanuka Rajapaksa</span>
                            <span style="font-weight:800;color:var(--badge-green);">+10.4%</span>
                        </div>
                        <div style="background:#F1F5F9;height:6px;border-radius:3px;"><div style="background:var(--badge-green);width:58%;height:100%;border-radius:3px;"></div></div>
                    </div>
                    <div style="margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                            <span style="font-weight:700;">5. Axar Patel</span>
                            <span style="font-weight:800;color:var(--badge-green);">+7.8%</span>
                        </div>
                        <div style="background:#F1F5F9;height:6px;border-radius:3px;"><div style="background:var(--badge-green);width:43%;height:100%;border-radius:3px;"></div></div>
                    </div>
                </div>
                <p style="font-size:11px;color:var(--text-muted);margin-top:10px;">Pressure Lift ∆ = High-Pressure Win Rate % − Career Baseline Win Rate %.</p>
            </div>

            <!-- Visual 3: Top Bowlers Pressure Lift Bar -->
            <div class="visual-card">
                <div class="visual-card-title">
                    <span>Top Bowlers — Pressure Lift (∆%)</span>
                    <span style="font-size:11px;color:var(--badge-green);font-weight:700;">High Clutch</span>
                </div>
                <div style="font-size:12px;">
                    <div style="margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                            <span style="font-weight:700;">1. Jacob Duffy</span>
                            <span style="font-weight:800;color:var(--badge-green);">+20.5%</span>
                        </div>
                        <div style="background:#F1F5F9;height:6px;border-radius:3px;"><div style="background:var(--badge-green);width:95%;height:100%;border-radius:3px;"></div></div>
                    </div>
                    <div style="margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                            <span style="font-weight:700;">2. Josh Hazlewood</span>
                            <span style="font-weight:800;color:var(--rr-pink);">+14.9%</span>
                        </div>
                        <div style="background:#F1F5F9;height:6px;border-radius:3px;"><div style="background:var(--rr-pink);width:73%;height:100%;border-radius:3px;"></div></div>
                    </div>
                    <div style="margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                            <span style="font-weight:700;">3. Arshdeep Singh</span>
                            <span style="font-weight:800;color:var(--rr-navy);">+11.1%</span>
                        </div>
                        <div style="background:#F1F5F9;height:6px;border-radius:3px;"><div style="background:var(--rr-navy);width:55%;height:100%;border-radius:3px;"></div></div>
                    </div>
                    <div style="margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                            <span style="font-weight:700;">4. Yash Dayal</span>
                            <span style="font-weight:800;color:var(--badge-green);">+10.2%</span>
                        </div>
                        <div style="background:#F1F5F9;height:6px;border-radius:3px;"><div style="background:var(--badge-green);width:50%;height:100%;border-radius:3px;"></div></div>
                    </div>
                    <div style="margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                            <span style="font-weight:700;">5. Suyash Sharma</span>
                            <span style="font-weight:800;color:var(--badge-green);">+7.6%</span>
                        </div>
                        <div style="background:#F1F5F9;height:6px;border-radius:3px;"><div style="background:var(--badge-green);width:37%;height:100%;border-radius:3px;"></div></div>
                    </div>
                </div>
                <p style="font-size:11px;color:var(--text-muted);margin-top:10px;">Identifies bowling metronomes that restrict run flow under severe leverage.</p>
            </div>
        </div>

        <!-- 4. MASTER DATA TABLE SECTION -->
        <div class="section-pill-wrapper">
            <div class="pill-header">SupeRR Selector Official Leaderboards</div>
            <div class="scroll-tip">👉 Click any player to open in-depth profile dossier</div>
        </div>

        <div class="filter-bar">
            <div class="tab-btn-group">
                <button class="tab-btn active" onclick="switchTable('batters', this)">🏏 Top 10 Batters (Official)</button>
                <button class="tab-btn" onclick="switchTable('bowlers', this)">🎯 Top 10 Bowlers (Official)</button>
                <button class="tab-btn" onclick="switchTable('superstars', this)">⚠️ Superstar Dip Audit</button>
            </div>
            <div class="search-box">
                <span style="color:var(--text-muted);margin-right:8px;">🔍</span>
                <input type="text" id="tableSearch" placeholder="Search player or team..." onkeyup="filterTable()">
            </div>
        </div>

        <!-- Table: Batters -->
        <div id="table-batters" class="table-responsive table-section">
            <table>
                <thead>
                    <tr>
                        <th style="width:45px;">Rank</th>
                        <th>Player (Click to view Profile)</th>
                        <th>Franchise / Teams</th>
                        <th style="text-align:center;">HP M</th>
                        <th style="text-align:right;">HP Win%</th>
                        <th style="text-align:right;">Base Win%</th>
                        <th style="text-align:center;">Lift (∆)</th>
                        <th style="text-align:center;">HP MOM</th>
                        <th style="text-align:right;">KO Win%</th>
                        <th style="text-align:right;">CPPI Rating</th>
                        <th style="text-align:center;">Dossier</th>
                    </tr>
                </thead>
                <tbody>
"""

# Populate Batters
for b in top10_batters:
    img_b64 = player_images.get(b["key"], "")
    rank_class = f"rank-{b['rank']}" if b['rank'] <= 3 else ""
    lift_sign = f"+{b['lift']:.1f}%" if b['lift'] >= 0 else f"{b['lift']:.1f}%"
    lift_class = "lift-positive" if b['lift'] >= 0 else "lift-negative"
    
    master_dashboard_html += f"""
                    <tr onclick="openPlayerDossier('{b['key']}')">
                        <td><div class="rank-badge {rank_class}">{b['rank']}</div></td>
                        <td>
                            <div class="player-cell">
                                <div class="player-img-wrapper">
                                    <img src="{img_b64}" alt="{b['name']}">
                                </div>
                                <div>
                                    <div class="player-name">{b['name']}</div>
                                    <div class="player-teams">{b['role_desc']}</div>
                                </div>
                            </div>
                        </td>
                        <td><span style="font-weight:600;font-size:12px;">{b['teams']}</span></td>
                        <td style="text-align:center;" class="metric-cell">{b['hp_m']}</td>
                        <td style="text-align:right;font-weight:700;">{b['hp_wr']:.1f}%</td>
                        <td style="text-align:right;color:var(--text-muted);">{b['base_wr']:.1f}%</td>
                        <td style="text-align:center;"><span class="lift-badge {lift_class}">{lift_sign}</span></td>
                        <td style="text-align:center;font-weight:700;">{b['mom_hp']}</td>
                        <td style="text-align:right;font-weight:700;">{b['ko_wr']:.1f}%</td>
                        <td style="text-align:right;">
                            <div class="cppi-score">{b['cppi']:.2f}</div>
                            <div class="score-bar-bg"><div class="score-bar-fill" style="width:{b['cppi']}%;"></div></div>
                        </td>
                        <td style="text-align:center;">
                            <span class="btn-view-dossier">View Profile →</span>
                        </td>
                    </tr>
"""

master_dashboard_html += """
                </tbody>
            </table>
        </div>

        <!-- Table: Bowlers -->
        <div id="table-bowlers" class="table-responsive table-section" style="display:none;">
            <table>
                <thead>
                    <tr>
                        <th style="width:45px;">Rank</th>
                        <th>Player (Click to view Profile)</th>
                        <th>Franchise / Teams</th>
                        <th style="text-align:center;">HP M</th>
                        <th style="text-align:right;">HP Win%</th>
                        <th style="text-align:right;">Base Win%</th>
                        <th style="text-align:center;">Lift (∆)</th>
                        <th style="text-align:center;">HP MOM</th>
                        <th style="text-align:right;">KO Win%</th>
                        <th style="text-align:right;">CPPI Rating</th>
                        <th style="text-align:center;">Dossier</th>
                    </tr>
                </thead>
                <tbody>
"""

# Populate Bowlers
for b in top10_bowlers:
    img_b64 = player_images.get(b["key"], "")
    rank_class = f"rank-{b['rank']}" if b['rank'] <= 3 else ""
    lift_sign = f"+{b['lift']:.1f}%" if b['lift'] >= 0 else f"{b['lift']:.1f}%"
    lift_class = "lift-positive" if b['lift'] >= 0 else "lift-negative"
    
    master_dashboard_html += f"""
                    <tr onclick="openPlayerDossier('{b['key']}')">
                        <td><div class="rank-badge {rank_class}">{b['rank']}</div></td>
                        <td>
                            <div class="player-cell">
                                <div class="player-img-wrapper">
                                    <img src="{img_b64}" alt="{b['name']}">
                                </div>
                                <div>
                                    <div class="player-name">{b['name']}</div>
                                    <div class="player-teams">{b['role_desc']}</div>
                                </div>
                            </div>
                        </td>
                        <td><span style="font-weight:600;font-size:12px;">{b['teams']}</span></td>
                        <td style="text-align:center;" class="metric-cell">{b['hp_m']}</td>
                        <td style="text-align:right;font-weight:700;">{b['hp_wr']:.1f}%</td>
                        <td style="text-align:right;color:var(--text-muted);">{b['base_wr']:.1f}%</td>
                        <td style="text-align:center;"><span class="lift-badge {lift_class}">{lift_sign}</span></td>
                        <td style="text-align:center;font-weight:700;">{b['mom_hp']}</td>
                        <td style="text-align:right;font-weight:700;">{b['ko_wr']:.1f}%</td>
                        <td style="text-align:right;">
                            <div class="cppi-score">{b['cppi']:.2f}</div>
                            <div class="score-bar-bg"><div class="score-bar-fill" style="width:{b['cppi']}%;"></div></div>
                        </td>
                        <td style="text-align:center;">
                            <span class="btn-view-dossier">View Profile →</span>
                        </td>
                    </tr>
"""

master_dashboard_html += """
                </tbody>
            </table>
        </div>

        <!-- Table: Superstars Audit -->
        <div id="table-superstars" class="table-responsive table-section" style="display:none;">
            <table>
                <thead>
                    <tr>
                        <th>Omitted Superstar</th>
                        <th style="text-align:center;">Total M</th>
                        <th style="text-align:right;">Base Win%</th>
                        <th style="text-align:center;">HP M</th>
                        <th style="text-align:right;">HP Win%</th>
                        <th style="text-align:center;">Lift (∆)</th>
                        <th style="text-align:center;">KO Win%</th>
                        <th style="width:40%;">Data-Backed De-Selection Rationale</th>
                    </tr>
                </thead>
                <tbody>
"""

# Populate Superstars Audit
for s in superstars_audit:
    lift_sign = f"{s['lift']:.1f}%"
    master_dashboard_html += f"""
                    <tr>
                        <td><strong style="color:var(--rr-navy);font-size:14px;">{s['name']}</strong></td>
                        <td style="text-align:center;" class="metric-cell">{s['total_m']}</td>
                        <td style="text-align:right;color:var(--text-muted);">{s['base_wr']:.1f}%</td>
                        <td style="text-align:center;" class="metric-cell">{s['hp_m']}</td>
                        <td style="text-align:right;font-weight:700;color:var(--badge-red);">{s['hp_wr']:.1f}%</td>
                        <td style="text-align:center;"><span class="lift-badge lift-negative">{lift_sign}</span></td>
                        <td style="text-align:center;font-weight:600;">{s['ko_wr']:.1f}%</td>
                        <td style="font-size:12px;color:var(--text-main);line-height:1.4;">{s['reason']}</td>
                    </tr>
"""

master_dashboard_html += """
                </tbody>
            </table>
        </div>

        <!-- 5. METHODOLOGY & ACADEMIC REFERENCES SECTION -->
        <div class="section-pill-wrapper">
            <div class="pill-header">Analytical Framework & Academic References</div>
        </div>

        <div class="grid-2col">
            <!-- Card 1: Mathematical Architecture -->
            <div class="doc-card">
                <div class="doc-title">
                    <span>📐 Mathematical Architecture & Formulas</span>
                </div>
                <div class="formula-box">
                    // Match Leverage Index (MLI) [0–100 Scale]<br>
                    MLI = Stage_Stakes(0–40) + Contest_Closeness(0–40) + Elimination_Bonus(0–20) + DLS_Revision(0–5)<br>
                    High-Pressure Threshold: MLI ≥ 30 (Top 20.4% Leverage Games)
                </div>
                <div class="formula-box">
                    // Composite Pressure Performance Index (CPPI) [0–100 Scale]<br>
                    CPPI = [ 0.35 × Bayes_HP_WR + 0.20 × Bayes_KO_WR + 0.20 × MOM_Density<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ 0.15 × Lift_Norm + 0.10 × Base_WR ] × Credibility(n_HP)
                </div>
                <ul class="doc-list">
                    <li><strong>Empirical Bayes Shrinkage:</strong> Shrinks small-sample win rates towards baseline with prior strength M = 5.0 matches.</li>
                    <li><strong>Pressure Lift (∆):</strong> Calculates Delta = HP_Win_Rate − Base_Win_Rate to reward players who escalate output in clutch games.</li>
                    <li><strong>Credibility Saturation:</strong> Sigmoid logistic scaling S(n) = 0.85 + 0.15 / [1 + exp(−0.25 × (n − 8))] to penalize noisy samples.</li>
                </ul>
            </div>

            <!-- Card 2: Formal References & Tournament Compliance -->
            <div class="doc-card">
                <div class="doc-title">
                    <span>📚 Academic Citations & Tournament References</span>
                </div>
                <div class="ref-item">
                    <strong>[1] Leverage Index & Sabermetrics:</strong><br>
                    Tango, T. M., Lichtman, M. G., & Dolphin, A. E. (2006). <em>The Book: Playing the Percentages in Baseball</em>. Potomac Books. Foundational mathematical framework for quantifying win probability swings across innings leverage.
                </div>
                <div class="ref-item">
                    <strong>[2] Small-Sample Empirical Bayes Shrinkage:</strong><br>
                    Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). <em>Bayesian Data Analysis</em> (3rd ed.). Chapman and Hall/CRC. Stabilizes win probability metrics across players with variable fixture counts.
                </div>
                <div class="ref-item">
                    <strong>[3] Tournament Regulatory Framework & Auction Policy:</strong><br>
                    Board of Control for Cricket in India (BCCI). <em>IPL Match Playing Conditions and Player Auction Regulations (2022–2026)</em>. Applied to filter foreign-player quotas and strict BCCI auction eligibility parameters.
                </div>
                <div style="background:#F1F5F9;padding:10px 14px;border-radius:8px;font-size:12px;color:var(--rr-navy);margin-top:10px;">
                    <strong>War Room Sign-off:</strong> Analytical model fully validated across 883 matches. Reproducible code and dataset mappings preserved in project dossier.
                </div>
            </div>
        </div>

        <!-- 6. FOOTER -->
        <footer>
            Rajasthan Royals Performance Analytics & War Room Strategy · SupeRR Selector Season 2 Hackathon · Ketan Rawat (B.Tech ECE, NIT Jamshedpur)
        </footer>

    </div>

    <!-- ═══════════════════════════════════════════════════════ -->
    <!-- VIEW B: DEDICATED IN-APP FULL-PAGE PLAYER DOSSIER VIEW   -->
    <!-- ═══════════════════════════════════════════════════════ -->
    <div id="player-dossier-view">
        <div class="dossier-nav-bar">
            <button class="btn-back-main" onclick="closePlayerDossier()">← Back to Master Leaderboard</button>
            <a id="btn-standalone-link" href="#" target="_blank" class="btn-open-ext">🔗 Open Standalone Page ↗</a>
        </div>

        <div class="dossier-hero">
            <div class="dossier-avatar">
                <img id="dossier-img" src="" alt="Player Avatar">
            </div>
            <div class="dossier-info">
                <span id="dossier-rank-badge" class="dossier-rank-badge">RANK #1</span>
                <h1 id="dossier-name" class="dossier-name">Player Name</h1>
                <div id="dossier-teams" class="dossier-teams">Franchise / Teams</div>
                <div id="dossier-role" class="dossier-role">🎯 Tactical Role</div>
            </div>
            <div class="dossier-score-card">
                <div id="dossier-score-val" class="dossier-score-val">00.00</div>
                <div class="dossier-score-lbl">CPPI Score</div>
                <div id="dossier-bid-ceiling" style="font-size:11px;color:var(--rr-pink);font-weight:700;margin-top:4px;">Bid: INR 0.0 Cr</div>
            </div>
        </div>

        <div class="dossier-kpis">
            <div class="dossier-kpi-tile">
                <div id="dossier-hp-m" class="dossier-kpi-val">0</div>
                <div class="dossier-kpi-lbl">HP Matches</div>
            </div>
            <div class="dossier-kpi-tile">
                <div id="dossier-hp-wr" class="dossier-kpi-val" style="color:var(--rr-pink);">0.0%</div>
                <div class="dossier-kpi-lbl">HP Win Rate</div>
            </div>
            <div class="dossier-kpi-tile">
                <div id="dossier-base-wr" class="dossier-kpi-val">0.0%</div>
                <div class="dossier-kpi-lbl">Base Win Rate</div>
            </div>
            <div class="dossier-kpi-tile">
                <div id="dossier-lift" class="dossier-kpi-val">+0.0%</div>
                <div class="dossier-kpi-lbl">Pressure Lift (∆)</div>
            </div>
            <div class="dossier-kpi-tile">
                <div id="dossier-mom" class="dossier-kpi-val">0</div>
                <div class="dossier-kpi-lbl">HP MOMs</div>
            </div>
            <div class="dossier-kpi-tile">
                <div id="dossier-ko-wr" class="dossier-kpi-val">0.0%</div>
                <div class="dossier-kpi-lbl">Knockout Win%</div>
            </div>
        </div>

        <!-- Comparative Chart -->
        <div class="dossier-section">
            <div class="dossier-sec-title">📊 Leverage Performance Comparative Breakdown</div>
            <div style="background:#F8FAFC;border:1px solid var(--border-card);border-radius:10px;padding:16px;">
                <div style="display:flex;align-items:center;margin-bottom:10px;font-size:12px;">
                    <span style="width:160px;font-weight:700;color:var(--rr-navy);">High-Pressure Win Rate</span>
                    <div style="flex:1;height:12px;background:#E2E8F0;border-radius:6px;overflow:hidden;margin:0 12px;">
                        <div id="dossier-chart-hp" style="height:100%;background:var(--rr-pink);border-radius:6px;width:0%;"></div>
                    </div>
                    <span id="dossier-chart-hp-val" style="width:60px;font-weight:800;text-align:right;color:var(--rr-pink);">0%</span>
                </div>
                <div style="display:flex;align-items:center;margin-bottom:10px;font-size:12px;">
                    <span style="width:160px;font-weight:700;color:var(--rr-navy);">Career Baseline Win Rate</span>
                    <div style="flex:1;height:12px;background:#E2E8F0;border-radius:6px;overflow:hidden;margin:0 12px;">
                        <div id="dossier-chart-base" style="height:100%;background:#64748B;border-radius:6px;width:0%;"></div>
                    </div>
                    <span id="dossier-chart-base-val" style="width:60px;font-weight:800;text-align:right;color:#64748B;">0%</span>
                </div>
                <div style="display:flex;align-items:center;font-size:12px;">
                    <span style="width:160px;font-weight:700;color:var(--rr-navy);">Knockout / Playoff Win%</span>
                    <div style="flex:1;height:12px;background:#E2E8F0;border-radius:6px;overflow:hidden;margin:0 12px;">
                        <div id="dossier-chart-ko" style="height:100%;background:var(--rr-navy);border-radius:6px;width:0%;"></div>
                    </div>
                    <span id="dossier-chart-ko-val" style="width:60px;font-weight:800;text-align:right;color:var(--rr-navy);">0%</span>
                </div>
            </div>
        </div>

        <!-- Strategic Cards -->
        <div class="dossier-section">
            <div class="dossier-sec-title">🎯 Why We Chose Him (Clutch Proof & Evidence)</div>
            <div id="dossier-why-chose" class="dossier-sec-body">...</div>
        </div>

        <div class="dossier-section">
            <div class="dossier-sec-title">⚖️ Why Not Others & Positional Ranking Rationale</div>
            <div id="dossier-why-not" class="dossier-sec-body">...</div>
        </div>

        <div class="dossier-section">
            <div class="dossier-sec-title">🏟️ Rajasthan Royals Fit for IPL 2027 Auction (SMS Stadium Dynamics)</div>
            <div id="dossier-rr-fit" class="dossier-sec-body">...</div>
            <div style="margin-top:14px;background:#F8FAFC;padding:12px 16px;border-radius:8px;font-weight:700;color:var(--rr-navy);font-size:13px;">
                💰 Recommended Bid Ceiling: <span id="dossier-bid-tag" style="color:var(--rr-pink);">INR 0.0 Cr</span> | <span id="dossier-verdict">Verdict</span>
            </div>
        </div>

        <div style="display:flex;justify-content:space-between;margin-top:32px;padding-top:20px;border-top:1px solid var(--border-card);">
            <button id="btn-prev-player" class="btn-back-main" style="background:#F1F5F9;color:var(--rr-navy);" onclick="">← Previous</button>
            <button class="btn-back-main" onclick="closePlayerDossier()">🏠 Back to Master Leaderboard</button>
            <button id="btn-next-player" class="btn-back-main" style="background:#F1F5F9;color:var(--rr-navy);" onclick="">Next →</button>
        </div>
    </div>

</div>

<!-- Player Data Embedded in Client Script -->
<script>
const PLAYERS_DATA = {players_json_str};
const PLAYER_IMAGES = {player_images_json_str};

function switchTable(type, btn) {{
    document.querySelectorAll('.table-section').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('table-' + type).style.display = 'block';
    btn.classList.add('active');
    document.getElementById('tableSearch').value = '';
    filterTable();
}}

function filterTable() {{
    const query = document.getElementById('tableSearch').value.toLowerCase();
    const activeTable = document.querySelector('.table-section:not([style*="display: none"])');
    if (!activeTable) return;
    const rows = activeTable.querySelectorAll('tbody tr');
    rows.forEach(row => {{
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
    }});
}}

function openPlayerDossier(playerKey) {{
    const player = PLAYERS_DATA.find(p => p.key === playerKey);
    if (!player) return;

    // Set hash in URL so back button works and links are shareable!
    window.location.hash = 'player=' + playerKey;

    // Populate data
    document.getElementById('dossier-img').src = PLAYER_IMAGES[player.key] || '';
    document.getElementById('dossier-rank-badge').innerText = `RANK #${{player.rank}} ${{player.category.toUpperCase()}} UNDER PRESSURE`;
    document.getElementById('dossier-name').innerText = player.name;
    document.getElementById('dossier-teams').innerText = player.teams;
    document.getElementById('dossier-role').innerText = '🎯 Tactical Role: ' + player.tactical_role;
    document.getElementById('dossier-score-val').innerText = player.cppi.toFixed(2);
    document.getElementById('dossier-bid-ceiling').innerText = 'Bid Ceiling: ' + player.bid_ceiling;

    // KPIs
    document.getElementById('dossier-hp-m').innerText = player.hp_m;
    document.getElementById('dossier-hp-wr').innerText = player.hp_wr.toFixed(1) + '%';
    document.getElementById('dossier-base-wr').innerText = player.base_wr.toFixed(1) + '%';
    
    const liftEl = document.getElementById('dossier-lift');
    const liftSign = player.lift >= 0 ? `+${{player.lift.toFixed(1)}}%` : `${{player.lift.toFixed(1)}}%`;
    liftEl.innerText = liftSign;
    liftEl.style.color = player.lift >= 0 ? 'var(--badge-green)' : 'var(--badge-red)';

    document.getElementById('dossier-mom').innerText = player.mom_hp;
    document.getElementById('dossier-ko-wr').innerText = player.ko_wr.toFixed(1) + '%';

    // Comparative Visual Bars
    document.getElementById('dossier-chart-hp').style.width = player.hp_wr + '%';
    document.getElementById('dossier-chart-hp-val').innerText = player.hp_wr.toFixed(1) + '%';

    document.getElementById('dossier-chart-base').style.width = player.base_wr + '%';
    document.getElementById('dossier-chart-base-val').innerText = player.base_wr.toFixed(1) + '%';

    document.getElementById('dossier-chart-ko').style.width = player.ko_wr + '%';
    document.getElementById('dossier-chart-ko-val').innerText = player.ko_wr.toFixed(1) + '%';

    // Deep Dive Texts
    document.getElementById('dossier-why-chose').innerText = player.why_chose;
    document.getElementById('dossier-why-not').innerText = player.why_not_others;
    document.getElementById('dossier-rr-fit').innerText = player.rr_fit;
    document.getElementById('dossier-bid-tag').innerText = player.bid_ceiling;
    document.getElementById('dossier-verdict').innerText = 'Verdict: ' + player.verdict;

    // Standalone link
    document.getElementById('btn-standalone-link').href = 'players/' + player.key + '.html';

    // Previous and Next buttons
    const curIdx = PLAYERS_DATA.findIndex(p => p.key === playerKey);
    const prevPlayer = PLAYERS_DATA[curIdx > 0 ? curIdx - 1 : PLAYERS_DATA.length - 1];
    const nextPlayer = PLAYERS_DATA[curIdx < PLAYERS_DATA.length - 1 ? curIdx + 1 : 0];

    const prevBtn = document.getElementById('btn-prev-player');
    prevBtn.innerText = `← #${{prevPlayer.rank}} ${{prevPlayer.name}}`;
    prevBtn.onclick = () => openPlayerDossier(prevPlayer.key);

    const nextBtn = document.getElementById('btn-next-player');
    nextBtn.innerText = `#{nextPlayer.rank} ${{nextPlayer.name}} →`;
    nextBtn.onclick = () => openPlayerDossier(nextPlayer.key);

    // Toggle view
    document.getElementById('master-dashboard-view').style.display = 'none';
    document.getElementById('player-dossier-view').style.display = 'block';
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function closePlayerDossier() {{
    window.location.hash = '';
    document.getElementById('player-dossier-view').style.display = 'none';
    document.getElementById('master-dashboard-view').style.display = 'block';
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

// Handle URL Hash on load & back button
window.addEventListener('hashchange', checkHash);
window.addEventListener('DOMContentLoaded', checkHash);

function checkHash() {{
    const hash = window.location.hash;
    if (hash && hash.startsWith('#player=')) {{
        const playerKey = hash.replace('#player=', '');
        openPlayerDossier(playerKey);
    }} else {{
        document.getElementById('player-dossier-view').style.display = 'none';
        document.getElementById('master-dashboard-view').style.display = 'block';
    }}
}}
</script>

</body>
</html>
"""

# Write to official dashboard file
dash_fp = Path("rr_pressure_dashboard.html")
with open(dash_fp, "w", encoding="utf-8") as f:
    f.write(master_dashboard_html)
print(f"✓ Master Responsive BI Dashboard Generated: {dash_fp.resolve()} ({dash_fp.stat().st_size} bytes)")

# Synchronize with index.html and rr_war_room_terminal.html
shutil_fp = Path("index.html")
with open(shutil_fp, "w", encoding="utf-8") as f:
    f.write(master_dashboard_html)
print(f"✓ Synchronized index.html ({shutil_fp.stat().st_size} bytes)")

term_fp = Path("rr_war_room_terminal.html")
with open(term_fp, "w", encoding="utf-8") as f:
    f.write(master_dashboard_html)
print(f"✓ Synchronized rr_war_room_terminal.html ({term_fp.stat().st_size} bytes)")
