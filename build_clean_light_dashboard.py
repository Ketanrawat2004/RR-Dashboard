import os
import json
import base64
from pathlib import Path

# 1. Load RR Logo
with open("rr_logo.png", "rb") as f:
    rr_logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

# 2. Load all 20 player images as base64
img_dir = Path("player_images")
player_images = {}
for p in img_dir.glob("*.png"):
    with open(p, "rb") as f:
        player_images[p.stem] = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

print(f"Loaded {len(player_images)} player images.")

top10_batters = [
    {
        "rank": 1,
        "name": "Rajat Patidar",
        "key": "rajat_patidar",
        "teams": "Royal Challengers Bengaluru",
        "hp_m": 14,
        "hp_wr": 71.4,
        "base_wr": 60.3,
        "lift": 11.1,
        "mom_hp": 2,
        "ko_wr": 71.4,
        "cppi": 63.28,
        "role_desc": "Elite Middle-Overs Spin Enforcer (#3/#4)",
        "rr_fit": "Target Signing for RR (Solves SMS Stadium spin choke in overs 7–15)"
    },
    {
        "rank": 2,
        "name": "Rinku Singh",
        "key": "rinku_singh",
        "teams": "India, Kolkata Knight Riders",
        "hp_m": 26,
        "hp_wr": 69.2,
        "base_wr": 63.8,
        "lift": 5.4,
        "mom_hp": 1,
        "ko_wr": 100.0,
        "cppi": 58.39,
        "role_desc": "Ice-Cold Death Finisher (#6/#7)",
        "rr_fit": "Target Signing for RR (100% KO Win Rate; pairs with Jurel & Hetmyer)"
    },
    {
        "rank": 3,
        "name": "Devon Conway",
        "key": "devon_conway",
        "teams": "Chennai Super Kings, New Zealand",
        "hp_m": 14,
        "hp_wr": 64.3,
        "base_wr": 46.2,
        "lift": 18.1,
        "mom_hp": 2,
        "ko_wr": 66.7,
        "cppi": 58.10,
        "role_desc": "Tactical Anchor & Wicketkeeper",
        "rr_fit": "IPL Final Man-of-the-Match; highest positive pressure lift (+18.1%)"
    },
    {
        "rank": 4,
        "name": "Sediqullah Atal",
        "key": "sediqullah_atal",
        "teams": "Afghanistan, Afghanistan A",
        "hp_m": 8,
        "hp_wr": 50.0,
        "base_wr": 57.9,
        "lift": -7.9,
        "mom_hp": 2,
        "ko_wr": 66.7,
        "cppi": 57.84,
        "role_desc": "Aggressive Powerplay Enforcer",
        "rr_fit": "2 Match-winning HP MOM awards across 8 pressure appearances"
    },
    {
        "rank": 5,
        "name": "Ruturaj Gaikwad",
        "key": "ruturaj_gaikwad",
        "teams": "Chennai Super Kings, India",
        "hp_m": 14,
        "hp_wr": 57.1,
        "base_wr": 50.6,
        "lift": 6.5,
        "mom_hp": 2,
        "ko_wr": 100.0,
        "cppi": 57.32,
        "role_desc": "Top-Order Anchor & Captain",
        "rr_fit": "100% Knockout Win Rate; 2 HP MOMs; immaculate game pacing"
    },
    {
        "rank": 6,
        "name": "Shivam Dube",
        "key": "shivam_dube",
        "teams": "Chennai Super Kings, India",
        "hp_m": 18,
        "hp_wr": 66.7,
        "base_wr": 54.3,
        "lift": 12.4,
        "mom_hp": 1,
        "ko_wr": 100.0,
        "cppi": 57.32,
        "role_desc": "Middle-Overs Spin Destructor",
        "rr_fit": "100% Knockout record; +12.4% Pressure Lift in high-leverage chases"
    },
    {
        "rank": 7,
        "name": "Shreyas Iyer",
        "key": "shreyas_iyer",
        "teams": "India, Kolkata Knight Riders",
        "hp_m": 18,
        "hp_wr": 55.6,
        "base_wr": 54.5,
        "lift": 1.1,
        "mom_hp": 3,
        "ko_wr": 60.0,
        "cppi": 56.82,
        "role_desc": "Championship Captain & Middle Order Anchor",
        "rr_fit": "3 High-Pressure MOM awards; title-winning pressure management"
    },
    {
        "rank": 8,
        "name": "Virat Kohli",
        "key": "virat_kohli",
        "teams": "India, Royal Challengers Bengaluru",
        "hp_m": 20,
        "hp_wr": 70.0,
        "base_wr": 62.4,
        "lift": 7.6,
        "mom_hp": 1,
        "ko_wr": 71.4,
        "cppi": 56.76,
        "role_desc": "Master Chase Anchor",
        "rr_fit": "70.0% High-Pressure Win Rate across 20 matches; benchmark baseline"
    },
    {
        "rank": 9,
        "name": "Axar Patel",
        "key": "axar_patel",
        "teams": "Delhi Capitals, India",
        "hp_m": 28,
        "hp_wr": 64.3,
        "base_wr": 56.5,
        "lift": 7.8,
        "mom_hp": 2,
        "ko_wr": 100.0,
        "cppi": 56.12,
        "role_desc": "Clutch All-Rounder (Crisis Stabilizer)",
        "rr_fit": "100% Knockout Win Rate across 28 pressure appearances"
    },
    {
        "rank": 10,
        "name": "Bhanuka Rajapaksa",
        "key": "bhanuka_rajapaksa",
        "teams": "Punjab Kings, Sri Lanka",
        "hp_m": 11,
        "hp_wr": 54.5,
        "base_wr": 44.1,
        "lift": 10.4,
        "mom_hp": 1,
        "ko_wr": 100.0,
        "cppi": 55.90,
        "role_desc": "Fearless Left-Hand Middle Order Counter",
        "rr_fit": "100% Knockout Win Rate; +10.4% Lift; high impact vs off-spin"
    }
]

top10_bowlers = [
    {
        "rank": 1,
        "name": "Mitchell Starc",
        "key": "mitchell_starc",
        "teams": "Australia, Delhi Capitals, KKR",
        "hp_m": 10,
        "hp_wr": 60.0,
        "base_wr": 68.3,
        "lift": -8.3,
        "mom_hp": 3,
        "ko_wr": 100.0,
        "cppi": 66.63,
        "role_desc": "Big-Match Knockout Spearhead",
        "rr_fit": "3 High-Pressure MOMs in 10 matches; 100% Knockout Win Rate (IPL Playoffs)"
    },
    {
        "rank": 2,
        "name": "Josh Hazlewood",
        "key": "josh_hazlewood",
        "teams": "Australia, Royal Challengers Bengaluru",
        "hp_m": 14,
        "hp_wr": 78.6,
        "base_wr": 63.7,
        "lift": 14.9,
        "mom_hp": 1,
        "ko_wr": 83.3,
        "cppi": 62.65,
        "role_desc": "Robotic Metronome & Length Specialist",
        "rr_fit": "Target Signing for RR (78.6% HP WR, +14.9% Lift; controls SMS Stadium pitch)"
    },
    {
        "rank": 3,
        "name": "Jacob Duffy",
        "key": "jacob_duffy",
        "teams": "New Zealand, Royal Challengers Bengaluru",
        "hp_m": 8,
        "hp_wr": 75.0,
        "base_wr": 54.5,
        "lift": 20.5,
        "mom_hp": 1,
        "ko_wr": 100.0,
        "cppi": 60.68,
        "role_desc": "Hit-the-Deck Seamer & Enforcer",
        "rr_fit": "100% Knockout Win Rate; tournament-high +20.5% Pressure Lift"
    },
    {
        "rank": 4,
        "name": "Suyash Sharma",
        "key": "suyash_sharma",
        "teams": "India A, KKR, RCB",
        "hp_m": 11,
        "hp_wr": 72.7,
        "base_wr": 65.1,
        "lift": 7.6,
        "mom_hp": 1,
        "ko_wr": 66.7,
        "cppi": 57.87,
        "role_desc": "Rapid Leg-Break Mystery Spinner",
        "rr_fit": "72.7% HP Win Rate; deceptive fast arm action choking middle overs"
    },
    {
        "rank": 5,
        "name": "Lockie Ferguson",
        "key": "lockie_ferguson",
        "teams": "GT, KKR, NZ, PBKS, RCB",
        "hp_m": 9,
        "hp_wr": 55.6,
        "base_wr": 49.1,
        "lift": 6.5,
        "mom_hp": 2,
        "ko_wr": 50.0,
        "cppi": 56.21,
        "role_desc": "150kph Express Pace Enforcer",
        "rr_fit": "2 High-Pressure MOM awards; extreme pace unsettling top orders"
    },
    {
        "rank": 6,
        "name": "Yash Dayal",
        "key": "yash_dayal",
        "teams": "Gujarat Titans, India, RCB",
        "hp_m": 10,
        "hp_wr": 80.0,
        "base_wr": 69.8,
        "lift": 10.2,
        "mom_hp": 0,
        "ko_wr": 80.0,
        "cppi": 55.49,
        "role_desc": "Indian Left-Arm Death Specialist",
        "rr_fit": "Target Signing for RR (80.0% HP Win Rate, +10.2% Lift; clutch 20th over execution)"
    },
    {
        "rank": 7,
        "name": "Romario Shepherd",
        "key": "romario_shepherd",
        "teams": "LSG, MI, RCB, SRH, West Indies",
        "hp_m": 25,
        "hp_wr": 56.0,
        "base_wr": 49.0,
        "lift": 7.0,
        "mom_hp": 2,
        "ko_wr": 100.0,
        "cppi": 55.08,
        "role_desc": "Heavy Ball Pacer & Power All-Rounder",
        "rr_fit": "100% Knockout Win Rate across 25 games; 2 HP MOM awards"
    },
    {
        "rank": 8,
        "name": "Varun Chakravarthy",
        "key": "varun_chakravarthy",
        "teams": "India, Kolkata Knight Riders",
        "hp_m": 21,
        "hp_wr": 61.9,
        "base_wr": 58.6,
        "lift": 3.3,
        "mom_hp": 1,
        "ko_wr": 100.0,
        "cppi": 54.91,
        "role_desc": "Championship Mystery Spinner",
        "rr_fit": "Target Signing for RR (100% KO Win Rate; suffocating middle-overs mystery spin)"
    },
    {
        "rank": 9,
        "name": "Bhuvneshwar Kumar",
        "key": "bhuvneshwar_kumar",
        "teams": "India, RCB, Sunrisers Hyderabad",
        "hp_m": 25,
        "hp_wr": 60.0,
        "base_wr": 57.3,
        "lift": 2.7,
        "mom_hp": 2,
        "ko_wr": 71.4,
        "cppi": 54.40,
        "role_desc": "Powerplay & Death Swing Veteran",
        "rr_fit": "25 HP appearances; 71.4% Knockout Win Rate; 2 clutch MOM awards"
    },
    {
        "rank": 10,
        "name": "Arshdeep Singh",
        "key": "arshdeep_singh",
        "teams": "India, Punjab Kings",
        "hp_m": 25,
        "hp_wr": 68.0,
        "base_wr": 56.9,
        "lift": 11.1,
        "mom_hp": 2,
        "ko_wr": 33.3,
        "cppi": 54.15,
        "role_desc": "Premier Indian Left-Arm Death Yorker Specialist",
        "rr_fit": "Target Signing for RR (68.0% HP WR, +11.1% Lift; solves overseas quota constraint)"
    }
]

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

html_template = f"""<!DOCTYPE html>
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
        html, body {{
            width: 100%;
            overflow-x: hidden;
        }}
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

        /* KPI Cards Ribbon (Power BI Responsive Grid) */
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

        .kpi-card.highlight::after {{
            background: var(--rr-pink);
        }}

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

        /* Section Pill Header (Tableau / Power BI Slide Style) */
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
            display: none;
            font-size: 11px;
            color: var(--rr-pink);
            font-weight: 600;
        }}

        /* Visuals Grid (Donut + Bar Charts) */
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

        .donut-svg {{
            max-width: 100%;
            height: auto;
        }}

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

        .tab-btn:hover {{
            background: #E2E8F0;
        }}

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

        /* Responsive Table Container (Touch Scrolling for Mobile/Laptops) */
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
            min-width: 820px; /* guarantees columns never collapse on mobile */
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
        }}

        tbody tr:hover {{
            background: #F8FAFC;
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

        /* Player Avatar & Info Cell */
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

        /* Metrics & Badges */
        .metric-cell {{
            font-weight: 600;
            white-space: nowrap;
        }}

        .lift-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            text-align: center;
            white-space: nowrap;
        }}

        .lift-positive {{
            background: var(--badge-green-bg);
            color: var(--badge-green);
        }}

        .lift-negative {{
            background: var(--badge-red-bg);
            color: var(--badge-red);
        }}

        .cppi-score {{
            font-size: 15px;
            font-weight: 800;
            color: var(--rr-navy);
        }}

        .score-bar-bg {{
            width: 70px;
            height: 6px;
            background: #E2E8F0;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 4px;
        }}

        .score-bar-fill {{
            height: 100%;
            background: var(--rr-pink);
            border-radius: 3px;
        }}

        /* Methodology & References Card (2 Columns) */
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
            word-break: break-word;
        }}

        .doc-list {{
            list-style: none;
            font-size: 13px;
            color: var(--text-main);
        }}

        .doc-list li {{
            margin-bottom: 8px;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }}

        .doc-list li strong {{
            color: var(--rr-navy);
            min-width: 130px;
        }}

        .ref-item {{
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 10px;
            padding-left: 12px;
            border-left: 2px solid var(--border-card);
            line-height: 1.4;
        }}

        .ref-item strong {{
            color: var(--rr-navy);
        }}

        /* Footer */
        footer {{
            text-align: center;
            font-size: 12px;
            color: var(--text-muted);
            padding: 20px 0;
            border-top: 1px solid var(--border-card);
            margin-top: 20px;
        }}

        /* ═══════════════════════════════════════════════════════ */
        /* RESPONSIVE MEDIA QUERIES (LAPTOP, TABLET & MOBILE)      */
        /* ═══════════════════════════════════════════════════════ */

        /* 1. Standard Laptops (1024px – 1280px) */
        @media (max-width: 1280px) {{
            .kpi-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
            .kpi-card:nth-child(4), .kpi-card:nth-child(5) {{
                grid-column: span 1;
            }}
            .visuals-row {{
                grid-template-columns: 1fr 1fr;
            }}
            .visual-card:nth-child(1) {{
                grid-column: span 2;
            }}
        }}

        /* 2. Tablets & Small Laptops (768px – 1024px) */
        @media (max-width: 1024px) {{
            body {{
                padding: 16px;
            }}
            .header-card {{
                padding: 16px 20px;
            }}
            .header-brand {{
                gap: 14px;
            }}
            .rr-logo-img {{
                height: 58px;
            }}
            .header-title-box h1 {{
                font-size: 20px;
            }}
            .kpi-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .kpi-card:last-child {{
                grid-column: span 2;
            }}
            .visuals-row {{
                grid-template-columns: 1fr;
            }}
            .visual-card:nth-child(1) {{
                grid-column: span 1;
            }}
            .grid-2col {{
                grid-template-columns: 1fr;
            }}
            .scroll-tip {{
                display: inline-block;
            }}
        }}

        /* 3. Mobile Devices (<= 768px) */
        @media (max-width: 768px) {{
            body {{
                padding: 10px 8px;
            }}
            .header-card {{
                padding: 16px 14px;
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }}
            .header-brand {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
                width: 100%;
            }}
            .rr-logo-img {{
                height: 48px;
            }}
            .header-title-box h1 {{
                font-size: 17px;
            }}
            .header-title-box p {{
                font-size: 12px;
            }}
            .header-meta {{
                border-left: none;
                border-top: 1px solid var(--border-card);
                padding-left: 0;
                padding-top: 10px;
                width: 100%;
                text-align: left;
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 8px;
            }}
            .kpi-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
            }}
            .kpi-card {{
                padding: 12px 14px;
            }}
            .kpi-label {{
                font-size: 10px;
            }}
            .kpi-value {{
                font-size: 22px;
            }}
            .kpi-sub {{
                font-size: 11px;
            }}
            .filter-bar {{
                flex-direction: column;
                align-items: stretch;
                padding: 12px 14px;
                gap: 12px;
            }}
            .tab-btn-group {{
                flex-direction: column;
                width: 100%;
            }}
            .tab-btn {{
                width: 100%;
                text-align: center;
                padding: 10px;
                font-size: 12px;
            }}
            .search-box {{
                width: 100%;
            }}
            .pill-header {{
                font-size: 12px;
                padding: 6px 16px;
            }}
            .doc-card {{
                padding: 16px;
            }}
            .doc-title {{
                font-size: 14px;
            }}
            .doc-list li {{
                flex-direction: column;
                gap: 2px;
            }}
            .doc-list li strong {{
                min-width: unset;
            }}
            .player-cell {{
                gap: 8px;
            }}
            .player-img-wrapper {{
                width: 36px;
                height: 36px;
            }}
            .player-name {{
                font-size: 13px;
            }}
            .scroll-tip {{
                display: inline-block;
            }}
        }}

        /* 4. Ultra-Small Mobile Phones (<= 400px) */
        @media (max-width: 400px) {{
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}
            .kpi-card:last-child {{
                grid-column: span 1;
            }}
        }}
    </style>
</head>
<body>

<div class="dashboard-container">

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
                    <!-- Close Contests 42% -->
                    <circle cx="95" cy="85" r="60" fill="transparent" stroke="#001D48" stroke-width="24" stroke-dasharray="158 219" stroke-dashoffset="0"/>
                    <!-- Knockouts/Finals 35% -->
                    <circle cx="95" cy="85" r="60" fill="transparent" stroke="#EB1A8D" stroke-width="24" stroke-dasharray="132 245" stroke-dashoffset="-158"/>
                    <!-- Super Overs 15% -->
                    <circle cx="95" cy="85" r="60" fill="transparent" stroke="#0284C7" stroke-width="24" stroke-dasharray="56 321" stroke-dashoffset="-290"/>
                    <!-- DLS Rain 8% -->
                    <circle cx="95" cy="85" r="60" fill="transparent" stroke="#16A34A" stroke-width="24" stroke-dasharray="30 347" stroke-dashoffset="-346"/>
                    <text x="95" y="82" text-anchor="middle" font-size="16" font-weight="800" fill="#001D48">180</text>
                    <text x="95" y="98" text-anchor="middle" font-size="10" font-weight="600" fill="#64748B">GAMES</text>
                    <!-- Legend -->
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

    <!-- 4. MASTER DATA TABLE SECTION WITH TOGGLES & SEARCH -->
    <div class="section-pill-wrapper">
        <div class="pill-header">SupeRR Selector Official Leaderboards</div>
        <div class="scroll-tip">👉 Swipe table to view all metrics</div>
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
                    <th>Player</th>
                    <th>Franchise / Teams</th>
                    <th style="text-align:center;">HP M</th>
                    <th style="text-align:right;">HP Win%</th>
                    <th style="text-align:right;">Base Win%</th>
                    <th style="text-align:center;">Lift (∆)</th>
                    <th style="text-align:center;">HP MOM</th>
                    <th style="text-align:right;">KO Win%</th>
                    <th style="text-align:right;">CPPI Rating</th>
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
    
    html_template += f"""
                <tr>
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
                </tr>
"""

html_template += """
            </tbody>
        </table>
    </div>

    <!-- Table: Bowlers -->
    <div id="table-bowlers" class="table-responsive table-section" style="display:none;">
        <table>
            <thead>
                <tr>
                    <th style="width:45px;">Rank</th>
                    <th>Player</th>
                    <th>Franchise / Teams</th>
                    <th style="text-align:center;">HP M</th>
                    <th style="text-align:right;">HP Win%</th>
                    <th style="text-align:right;">Base Win%</th>
                    <th style="text-align:center;">Lift (∆)</th>
                    <th style="text-align:center;">HP MOM</th>
                    <th style="text-align:right;">KO Win%</th>
                    <th style="text-align:right;">CPPI Rating</th>
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
    
    html_template += f"""
                <tr>
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
                </tr>
"""

html_template += """
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
    html_template += f"""
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

html_template += """
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

<script>
function switchTable(type, btn) {
    document.querySelectorAll('.table-section').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('table-' + type).style.display = 'block';
    btn.classList.add('active');
    document.getElementById('tableSearch').value = '';
    filterTable();
}

function filterTable() {
    const query = document.getElementById('tableSearch').value.toLowerCase();
    const activeTable = document.querySelector('.table-section:not([style*="display: none"])');
    if (!activeTable) return;
    const rows = activeTable.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
    });
}
</script>

</body>
</html>
"""

# Write to official dashboard file
dash_fp = Path("rr_pressure_dashboard.html")
with open(dash_fp, "w", encoding="utf-8") as f:
    f.write(html_template)
print(f"✓ Master Responsive BI Dashboard Generated: {dash_fp.resolve()} ({dash_fp.stat().st_size} bytes)")

# Synchronize with rr_war_room_terminal.html so both are identical
term_fp = Path("rr_war_room_terminal.html")
with open(term_fp, "w", encoding="utf-8") as f:
    f.write(html_template)
print(f"✓ Synchronized rr_war_room_terminal.html ({term_fp.stat().st_size} bytes)")
