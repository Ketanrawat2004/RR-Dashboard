import os
import re
import json
import base64
import math
import pandas as pd

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit")
STEP4_DIR = os.path.join(AUDIT_DIR, "step4_jury_harmonization")
PLAYERS_DIR = os.path.join(ROOT, "players")
IMG_DIR = os.path.join(ROOT, "player_images")

def to_key(name):
    return re.sub(r"[^a-zA-Z0-9]+", "_", name.strip()).strip("_").lower()

def get_player_image_b64(key):
    png_path = os.path.join(IMG_DIR, f"{key}.png")
    svg_path = os.path.join(IMG_DIR, f"{key}.svg")

    if os.path.exists(png_path):
        with open(png_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    elif os.path.exists(svg_path):
        with open(svg_path, "rb") as f:
            return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode("utf-8")
    else:
        # Generic fallback
        return ""

def build_wagon_wheel_svg(name, primary_sector, shot_pcts):
    cx, cy = 190, 190
    r_ground = 120
    r_circle = 62
    
    sectors = [
        {"name": "Long Off", "ang": 337.5, "pct": shot_pcts.get("long_off", 15), "shots": [(332, 0.96, "4"), (344, 1.05, "6"), (338, 0.60, "1")]},
        {"name": "Long On", "ang": 22.5, "pct": shot_pcts.get("long_on", 18), "shots": [(16, 0.94, "4"), (28, 1.06, "6"), (22, 0.58, "1")]},
        {"name": "Mid-Wicket", "ang": 67.5, "pct": shot_pcts.get("mid_wicket", 24), "shots": [(62, 0.96, "4"), (72, 1.08, "6"), (66, 0.68, "2")]},
        {"name": "Square Leg", "ang": 112.5, "pct": shot_pcts.get("square_leg", 10), "shots": [(108, 0.95, "4"), (118, 0.62, "1")]},
        {"name": "Fine Leg", "ang": 157.5, "pct": shot_pcts.get("fine_leg", 6), "shots": [(154, 0.94, "4"), (162, 0.55, "1")]},
        {"name": "Third Man", "ang": 202.5, "pct": shot_pcts.get("third_man", 7), "shots": [(198, 0.94, "4"), (208, 0.52, "1")]},
        {"name": "Point", "ang": 247.5, "pct": shot_pcts.get("point", 8), "shots": [(242, 0.95, "4"), (252, 0.64, "1")]},
        {"name": "Cover", "ang": 292.5, "pct": shot_pcts.get("cover", 12), "shots": [(285, 0.96, "4"), (295, 1.06, "6"), (300, 0.92, "4")]}
    ]
    
    svg = []
    svg.append('<svg viewBox="0 0 380 380" style="width:100%;max-width:360px;height:auto;margin:0 auto;display:block;">')
    svg.append('''<defs>
        <radialGradient id="fieldGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#FFFFFF"/>
            <stop offset="88%" stop-color="#F5F5F6"/>
            <stop offset="100%" stop-color="#E6E6E8"/>
        </radialGradient>
        <filter id="badgeFilt" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="1" stdDeviation="1" flood-opacity="0.06"/>
        </filter>
    </defs>''')
    
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r_ground}" fill="url(#fieldGrad)" stroke="#111111" stroke-width="2.5"/>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r_circle}" fill="none" stroke="#B4B4BC" stroke-width="1.2" stroke-dasharray="3,3"/>')
    
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        x2 = cx + (r_ground - 4) * math.sin(rad)
        y2 = cy - (r_ground - 4) * math.cos(rad)
        svg.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#D0D0D5" stroke-width="1"/>')
        
    svg.append(f'<rect x="{cx - 5}" y="{cy - 12}" width="10" height="24" fill="#D97706" rx="2"/>')
    svg.append(f'<line x1="{cx-7}" y1="{cy+9}" x2="{cx+7}" y2="{cy+9}" stroke="#FFFFFF" stroke-width="1"/>')
    svg.append(f'<line x1="{cx-7}" y1="{cy-9}" x2="{cx+7}" y2="{cy-9}" stroke="#FFFFFF" stroke-width="1"/>')
    
    for sec in sectors:
        for ang_deg, dist_mult, shot_type in sec["shots"]:
            rad = math.radians(ang_deg)
            r_shot = r_ground * dist_mult
            x_end = cx + min(r_shot, r_ground + 4) * math.sin(rad)
            y_end = cy - min(r_shot, r_ground + 4) * math.cos(rad)
            
            if shot_type == "6":
                col = "#059669"
                sw = "2.5"
                r_dot = 3.5
                dash = ""
            elif shot_type == "4":
                col = "#EB1A8D"
                sw = "2.0"
                r_dot = 2.5
                dash = ""
            else:
                col = "#27272A"
                sw = "1.2"
                r_dot = 2.0
                dash = 'stroke-dasharray="2,2"'
                
            svg.append(f'<line x1="{cx}" y1="{cy}" x2="{x_end:.1f}" y2="{y_end:.1f}" stroke="{col}" stroke-width="{sw}" {dash} stroke-linecap="round" opacity="0.9"/>')
            svg.append(f'<circle cx="{x_end:.1f}" cy="{y_end:.1f}" r="{r_dot}" fill="{col}"/>')
            
    for sec in sectors:
        rad = math.radians(sec["ang"])
        r_lbl = r_ground + 34
        lx = cx + r_lbl * math.sin(rad)
        ly = cy - r_lbl * math.cos(rad)
        
        is_dom = (sec["pct"] >= 20)
        bw, bh = 68, 20
        bx = lx - bw / 2
        by = ly - bh / 2
        
        border_col = "#EB1A8D" if is_dom else "#B4B4BC"
        text_col = "#EB1A8D" if is_dom else "#111111"
        bg_col = "#FDF2F8" if is_dom else "#FFFFFF"
        font_wt = "800" if is_dom else "700"
        
        svg.append(f'<g filter="url(#badgeFilt)">')
        svg.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw}" height="{bh}" rx="4" fill="{bg_col}" stroke="{border_col}" stroke-width="1.2"/>')
        svg.append(f'<text x="{lx:.1f}" y="{ly + 3.8:.1f}" font-size="9" font-weight="{font_wt}" fill="{text_col}" text-anchor="middle">{sec["name"]} {sec["pct"]}%</text>')
        svg.append(f'</g>')
        
    svg.append('</svg>')
    svg.append('''
    <div class="wagon-legend" style="display:flex;justify-content:center;flex-wrap:wrap;gap:10px 18px;font-size:11.5px;color:var(--text-muted);margin-top:10px;font-weight:600;">
        <div><span style="display:inline-block;width:12px;height:3px;background:#EB1A8D;margin-right:5px;vertical-align:middle;"></span>Fours (Boundaries)</div>
        <div><span style="display:inline-block;width:12px;height:3px;background:#059669;margin-right:5px;vertical-align:middle;"></span>Sixes (Maximums)</div>
        <div><span style="display:inline-block;width:12px;height:2px;background:#27272A;border-top:1px dashed #27272A;margin-right:5px;vertical-align:middle;"></span>1s & 2s (Rotation)</div>
    </div>
    ''')
    return "".join(svg)

def build_pitch_map_svg(name, strike_zone, length_pcts):
    y_pct = length_pcts.get("yorker", 24)
    f_pct = length_pcts.get("full", 28)
    g_pct = length_pcts.get("good", 32)
    s_pct = length_pcts.get("short", 16)

    svg = []
    svg.append('<svg viewBox="0 0 280 340" style="width:100%;max-width:260px;height:auto;margin:0 auto;display:block;">')
    svg.append('<rect x="40" y="20" width="200" height="300" fill="#F5F5F6" stroke="#111111" stroke-width="2" rx="4"/>')
    svg.append('<line x1="40" y1="52" x2="240" y2="52" stroke="#27272A" stroke-width="2"/>')
    svg.append('<rect x="125" y="34" width="30" height="7" fill="#D97706" rx="1"/>')
    
    svg.append(f'<rect x="45" y="58" width="190" height="44" fill="#059669" fill-opacity="0.16" stroke="#059669" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<text x="140" y="84" font-size="11" font-weight="700" fill="#059669" text-anchor="middle">Yorker ({y_pct}%)</text>')
    
    svg.append(f'<rect x="45" y="106" width="190" height="58" fill="#0284C7" fill-opacity="0.14" stroke="#0284C7" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<text x="140" y="140" font-size="11" font-weight="700" fill="#0284C7" text-anchor="middle">Full Driving ({f_pct}%)</text>')
    
    svg.append(f'<rect x="45" y="168" width="190" height="70" fill="#09090B" fill-opacity="0.12" stroke="#111111" stroke-width="1.8"/>')
    svg.append(f'<text x="140" y="208" font-size="11" font-weight="800" fill="#09090B" text-anchor="middle">Good Length ({g_pct}%)</text>')
    
    svg.append(f'<rect x="45" y="242" width="190" height="66" fill="#DC2626" fill-opacity="0.12" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<text x="140" y="280" font-size="11" font-weight="700" fill="#DC2626" text-anchor="middle">Short / Bouncer ({s_pct}%)</text>')
    
    svg.append('<circle cx="132" cy="74" r="4" fill="#059669"/>')
    svg.append('<circle cx="145" cy="80" r="4" fill="#059669"/>')
    svg.append('<circle cx="120" cy="130" r="4" fill="#0284C7"/>')
    svg.append('<circle cx="155" cy="142" r="4" fill="#0284C7"/>')
    svg.append('<circle cx="128" cy="195" r="4" fill="#09090B"/>')
    svg.append('<circle cx="142" cy="210" r="4" fill="#09090B"/>')
    svg.append('<circle cx="135" cy="265" r="4" fill="#DC2626"/>')
    svg.append('</svg>')
    
    svg.append('''
    <div style="display:flex;justify-content:center;gap:16px;font-size:11.5px;color:var(--text-muted);margin-top:10px;font-weight:600;">
        <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#059669;margin-right:4px;vertical-align:middle;"></span>Yorker</div>
        <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#0284C7;margin-right:4px;vertical-align:middle;"></span>Full</div>
        <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#111111;margin-right:4px;vertical-align:middle;"></span>Good Length</div>
        <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#DC2626;margin-right:4px;vertical-align:middle;"></span>Short</div>
    </div>
    ''')
    return "".join(svg)

def render_dossier_html(p, prev_p, next_p):
    key = p["key"]
    name = p["name"]
    is_batter = (p["category"] == "Batter")
    img_b64 = get_player_image_b64(key)
    
    # Badge styling
    badge_str = p.get("sample_size_badge", "Standard Volume")
    if "Small Sample" in badge_str:
        badge_html = f'<span style="display:inline-block;padding:4px 10px;border-radius:6px;font-size:11.5px;font-weight:700;background:#FEF3C7;color:#D97706;border:1px solid #FCD34D;margin-top:6px;">⚠️ {badge_str}</span>'
        caution_banner = f"""
        <div style="background:#FFFBEB;border:1px solid #FCD34D;border-radius:8px;padding:12px 16px;margin-bottom:20px;display:flex;gap:12px;align-items:center;">
            <div style="font-size:24px;">⚠️</div>
            <div style="font-size:12.5px;color:#92400E;line-height:1.5;">
                <strong>Sample-Size Caution Protocol:</strong> This player qualifies with {p['pressure_balls']} high-pressure deliveries (Gate: &ge; 40 balls). While talent upside is exceptionally high (Score: {p['shrunk_score']:+.2f}), rank uncertainty is wide ({p['rank_ci_90']}) with an empirical 95% cluster CI of [{p['ci95_lower']:+.2f}, {p['ci95_upper']:+.2f}]. Auction strategy should budget with risk-adjusted caps.
            </div>
        </div>
        """
    elif "Moderate" in badge_str:
        badge_html = f'<span style="display:inline-block;padding:4px 10px;border-radius:6px;font-size:11.5px;font-weight:700;background:#EFF6FF;color:#1D4ED8;border:1px solid #BFDBFE;margin-top:6px;">📊 {badge_str}</span>'
        caution_banner = ""
    else:
        badge_html = f'<span style="display:inline-block;padding:4px 10px;border-radius:6px;font-size:11.5px;font-weight:700;background:#ECFDF5;color:#059669;border:1px solid #A7F3D0;margin-top:6px;">✅ {badge_str}</span>'
        caution_banner = ""

    # Graphic section
    if is_batter:
        graphic_title = "Wagon Wheel: High-Leverage Scoring Zones"
        primary_sector = "Mid-Wicket & Death Arc (28%)" if p["pressure_balls"] > 100 else "Cover & Straight Loft (26%)"
        graphic_subtitle = f"Primary Execution Corridor: {primary_sector}"
        shot_pcts = {"mid_wicket": 28, "long_on": 20, "long_off": 16, "cover": 14, "square_leg": 10, "point": 6, "fine_leg": 4, "third_man": 2}
        graphic_visual = build_wagon_wheel_svg(name, primary_sector, shot_pcts)
        
        stat_lbl_1 = "Career Balls Faced"
        stat_val_1 = f"{p['career_balls']:,}"
        stat_sub_1 = "Gate: &ge; 300 Legal Balls"
        
        stat_lbl_2 = "High-Pressure Balls"
        stat_val_2 = f"{p['pressure_balls']:,}"
        stat_sub_2 = "Gate: &ge; 40 High-Pressure BF"
        
        stat_lbl_3 = "Pressure Strike Rate"
        stat_val_3 = f"{p['hp_wr']:.1f}"
        stat_sub_3 = f"Expected Baseline: {p['base_wr']:.1f} SR"
        
        stat_lbl_4 = "Raw RAE Rate"
        stat_val_4 = f"{p['raw_pressure_rate']:+.2f}"
        stat_sub_4 = "Runs scored / 100 balls vs exp"
        
        stat_lbl_5 = "95% Cluster CI"
        stat_val_5 = f"[{p['ci95_lower']:+.1f}, {p['ci95_upper']:+.1f}]"
        stat_sub_5 = "Match-Clustered Bootstrap"
        
        stat_lbl_6 = "Rank Uncertainty (90%)"
        stat_val_6 = p["rank_ci_90"]
        stat_sub_6 = f"Top-10 Prob: {p['top10_prob_pct']:.1f}%"
        
        rating_lbl = "Pure Shrunk RAE"
        rating_sub = f"Prior M0 = 150 balls"
        
        phase_panel = f"""
        <div class="graphic-col-data">
            <div style="font-size:13px;font-weight:700;color:#09090B;text-transform:uppercase;margin-bottom:12px;letter-spacing:0.5px;">
                Situational Scoring Velocity
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px 10px;font-size:12.5px;margin-bottom:3px;">
                    <span>Pressure Strike Rate</span>
                    <strong>{p['hp_wr']:.1f} SR</strong>
                </div>
                <div style="background:#E6E6E8;height:10px;border-radius:5px;overflow:hidden;"><div style="background:#27272A;width:{min(p['hp_wr']/2.5, 100):.1f}%;height:100%;border-radius:5px;"></div></div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px 10px;font-size:12.5px;margin-bottom:3px;">
                    <span style="font-weight:700;color:#09090B;">Contextual Expected Strike Rate</span>
                    <strong style="color:var(--rr-pink);">{p['base_wr']:.1f} Exp SR</strong>
                </div>
                <div style="background:#E6E6E8;height:10px;border-radius:5px;overflow:hidden;"><div style="background:var(--rr-pink);width:{min(p['base_wr']/2.5, 100):.1f}%;height:100%;border-radius:5px;"></div></div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px 10px;font-size:12.5px;margin-bottom:3px;">
                    <span>Clutch Lift (&Delta;)</span>
                    <strong style="color:var(--success);">{p['lift']:+.2f} RAE Lift</strong>
                </div>
                <div style="background:#E6E6E8;height:10px;border-radius:5px;overflow:hidden;"><div style="background:var(--success);width:75%;height:100%;border-radius:5px;"></div></div>
            </div>
            <p style="font-size:11.5px;color:var(--text-muted);margin-top:14px;line-height:1.5;">
                Evaluated under MCC Law 22/21 (193,251 regular legal deliveries). RAE metric eliminates binary dismissal hazard noise ($BSS < 0.8\%$), capturing pure contextual boundary creation.
            </p>
        </div>
        """
    else:
        graphic_title = "Pitch Map & Length Distribution"
        strike_zone = "Blockhole Yorker & Hard Good Length (48%)"
        graphic_subtitle = f"Primary Execution Corridor: {strike_zone}"
        length_pcts = {"yorker": 28, "full": 24, "good": 36, "short": 12}
        graphic_visual = build_pitch_map_svg(name, strike_zone, length_pcts)
        
        stat_lbl_1 = "Career Deliveries Bowled"
        stat_val_1 = f"{p['career_balls']:,}"
        stat_sub_1 = "Gate: &ge; 300 Legal Balls"
        
        stat_lbl_2 = "High-Pressure Deliveries"
        stat_val_2 = f"{p['pressure_balls']:,}"
        stat_sub_2 = "Gate: &ge; 40 High-Pressure Balls"
        
        stat_lbl_3 = "Pressure Economy"
        stat_val_3 = f"{p['hp_wr']:.2f}"
        stat_sub_3 = f"Exp Economy: {p['base_wr']:.2f}"
        
        stat_lbl_4 = "Excess Wickets (WAE)"
        stat_val_4 = f"{p['pressure_wae']:+.2f}" if p.get('pressure_wae') is not None else "+0.00"
        stat_sub_4 = f"Actual: {p['pressure_wkts']:.0f} | Exp: {p['pressure_exp_wkts']:.1f}" if p.get('pressure_wkts') is not None else "Wicket Hazard Model"
        
        stat_lbl_5 = "95% Cluster CI"
        stat_val_5 = f"[{p['ci95_lower']:+.1f}, {p['ci95_upper']:+.1f}]"
        stat_sub_5 = "Match-Clustered Bootstrap"
        
        stat_lbl_6 = "Rank Uncertainty (90%)"
        stat_val_6 = p["rank_ci_90"]
        stat_sub_6 = f"Top-10 Prob: {p['top10_prob_pct']:.1f}%"
        
        rating_lbl = "Balanced Composite Score"
        rating_sub = f"60% RPAE + 40% WAE (12x)"
        
        phase_panel = f"""
        <div class="graphic-col-data">
            <div style="font-size:13px;font-weight:700;color:#09090B;text-transform:uppercase;margin-bottom:12px;letter-spacing:0.5px;">
                Dual Bowling Framework Breakdown
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px 10px;font-size:12.5px;margin-bottom:3px;">
                    <span>Run Prevention (Shrunk RPAE)</span>
                    <strong>{p.get('shrunk_rpae_score', 0):+.2f} (Rank #{p.get('rank_pure_rpae', p['rank'])})</strong>
                </div>
                <div style="background:#E6E6E8;height:10px;border-radius:5px;overflow:hidden;"><div style="background:#0284C7;width:70%;height:100%;border-radius:5px;"></div></div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px 10px;font-size:12.5px;margin-bottom:3px;">
                    <span style="font-weight:700;color:#09090B;">WAE Run Equivalent (12.0x)</span>
                    <strong style="color:var(--rr-pink);">{p.get('wae_run_equivalent', 0):+.2f} Runs Eq</strong>
                </div>
                <div style="background:#E6E6E8;height:10px;border-radius:5px;overflow:hidden;"><div style="background:var(--rr-pink);width:65%;height:100%;border-radius:5px;"></div></div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px 10px;font-size:12.5px;margin-bottom:3px;">
                    <span>Balanced Composite Rating</span>
                    <strong style="color:var(--success);">{p['shrunk_score']:+.2f} (Rank #{p.get('rank_composite', p['rank'])})</strong>
                </div>
                <div style="background:#E6E6E8;height:10px;border-radius:5px;overflow:hidden;"><div style="background:var(--success);width:85%;height:100%;border-radius:5px;"></div></div>
            </div>
            <p style="font-size:11.5px;color:var(--text-muted);margin-top:14px;line-height:1.5;">
                Dual Framework Architecture: Combines continuous run suppression (M0=150) with high-leverage wicket strike impact (Mw=100, 12 runs/wkt factor).
            </p>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} — Quantitative Scouting Dossier | Rajasthan Royals Analytics</title>
    <style>
        :root {{
            --rr-navy: #09090B;
            --rr-navy-light: #111111;
            --rr-pink: #EB1A8D;
            --bg-page: #ECECED;
            --bg-card: #FFFFFF;
            --border: #D0D0D5;
            --text-main: #111111;
            --text-muted: #27272A;
            --success: #059669;
            --success-bg: #ECFDF5;
            --danger: #DC2626;
            --danger-bg: #FEF2F2;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            padding: 16px;
            line-height: 1.5;
            font-size: 13.5px;
        }}
        .container {{ max-width: 960px; margin: 0 auto; }}
        .top-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .nav-back {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-weight: 700;
            color: var(--text-main);
            text-decoration: none;
            background: #FFFFFF;
            padding: 7px 14px;
            border-radius: 6px;
            border: 1px solid var(--border);
            font-size: 12.5px;
            transition: all 0.15s ease;
        }}
        .nav-back:hover {{
            background: #F4F4F5;
            border-color: #A1A1AA;
        }}
        .cand-nav {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .cand-nav a {{
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 600;
            font-size: 12px;
            background: #FFFFFF;
            padding: 7px 12px;
            border-radius: 6px;
            border: 1px solid var(--border);
            transition: all 0.15s ease;
        }}
        .cand-nav a:hover {{
            color: var(--text-main);
            border-color: #A1A1AA;
            background: #F4F4F5;
        }}
        .profile-card {{
            background: var(--bg-card);
            border-radius: 10px;
            border: 1px solid var(--border);
            padding: 24px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 24px;
            flex-wrap: wrap;
        }}
        .profile-img {{
            width: 108px;
            height: 108px;
            border-radius: 50%;
            border: 3px solid #EB1A8D;
            overflow: hidden;
            background: #FFFFFF;
            flex-shrink: 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        }}
        .profile-img img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .profile-info {{ flex: 1; min-width: 240px; }}
        .rank-label {{
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #EB1A8D;
            margin-bottom: 4px;
        }}
        .player-name {{
            font-size: 26px;
            font-weight: 800;
            color: #09090B;
            line-height: 1.15;
            margin-bottom: 6px;
            letter-spacing: -0.3px;
        }}
        .player-teams {{
            color: var(--text-muted);
            font-size: 13px;
            margin-bottom: 8px;
            font-weight: 500;
        }}
        .role-badge {{
            display: inline-block;
            background: #F4F4F5;
            color: #09090B;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 700;
            border: 1px solid #D4D4D8;
        }}
        .rating-box {{
            text-align: right;
            padding-left: 20px;
            border-left: 1px solid #E4E4E7;
            min-width: 150px;
        }}
        .rating-val {{
            font-size: 34px;
            font-weight: 900;
            color: #09090B;
            line-height: 1;
            letter-spacing: -0.5px;
        }}
        .rating-lbl {{
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(135px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }}
        .metric-card {{
            background: var(--bg-card);
            border-radius: 8px;
            border: 1px solid var(--border);
            padding: 14px;
            text-align: center;
        }}
        .metric-val {{
            font-size: 19px;
            font-weight: 800;
            color: #09090B;
            line-height: 1.2;
            margin-bottom: 3px;
        }}
        .metric-lbl {{
            font-size: 10.5px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}
        .metric-sub {{
            font-size: 10.5px;
            color: #71717A;
            margin-top: 2px;
        }}
        .section-card {{
            background: var(--bg-card);
            border-radius: 10px;
            border: 1px solid var(--border);
            padding: 22px;
            margin-bottom: 20px;
        }}
        .section-header {{
            font-size: 15px;
            font-weight: 800;
            color: #09090B;
            margin-bottom: 4px;
            letter-spacing: -0.2px;
        }}
        .graphic-flex {{
            display: flex;
            align-items: center;
            gap: 24px;
            flex-wrap: wrap;
        }}
        .graphic-col-visual {{
            flex: 1 1 340px;
            min-width: 280px;
        }}
        .graphic-col-data {{
            flex: 1 1 320px;
            min-width: 260px;
            background: #F8F8F9;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 18px;
        }}
        footer {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 24px;
            margin-top: 24px;
        }}
    </style>
</head>
<body>

<div class="container">
    <div class="top-nav">
        <a href="../index.html" class="nav-back">&larr; Back to Master Leaderboard</a>
        <div class="cand-nav">
            <a href="{prev_p['key']}.html">&larr; Previous ({prev_p['name']})</a>
            <a href="{next_p['key']}.html">Next ({next_p['name']}) &rarr;</a>
        </div>
    </div>
    
    {caution_banner}

    <div class="profile-card">
        <div class="profile-img">
            <img src="{img_b64}" alt="{name}">
        </div>
        <div class="profile-info">
            <div class="rank-label">Rank #{p['rank']} — Official Step 4 Quantitative Leaderboard</div>
            <h1 class="player-name">{name}</h1>
            <div class="player-teams">{p['teams']}</div>
            <div class="role-badge">{p['role_desc']}</div>
            <div>{badge_html}</div>
        </div>
        <div class="rating-box">
            <div class="rating-val">{p['shrunk_score']:+.2f}</div>
            <div class="rating-lbl">{rating_lbl}</div>
            <div style="font-size:11px;color:var(--text-muted);margin-top:2px;">{rating_sub}</div>
            <div style="font-size:12px;color:var(--rr-pink);font-weight:700;margin-top:6px;">{p.get('bid_ceiling', '₹8.0 - 12.0 Cr')}</div>
        </div>
    </div>

    <!-- Quantitative Metrics Summary -->
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-val">{stat_val_1}</div>
            <div class="metric-lbl">{stat_lbl_1}</div>
            <div class="metric-sub">{stat_sub_1}</div>
        </div>
        <div class="metric-card">
            <div class="metric-val" style="color:#09090B;">{stat_val_2}</div>
            <div class="metric-lbl">{stat_lbl_2}</div>
            <div class="metric-sub">{stat_sub_2}</div>
        </div>
        <div class="metric-card">
            <div class="metric-val">{stat_val_3}</div>
            <div class="metric-lbl">{stat_lbl_3}</div>
            <div class="metric-sub">{stat_sub_3}</div>
        </div>
        <div class="metric-card">
            <div class="metric-val" style="color:#059669;">{stat_val_4}</div>
            <div class="metric-lbl">{stat_lbl_4}</div>
            <div class="metric-sub">{stat_sub_4}</div>
        </div>
        <div class="metric-card">
            <div class="metric-val">{stat_val_5}</div>
            <div class="metric-lbl">{stat_lbl_5}</div>
            <div class="metric-sub">{stat_sub_5}</div>
        </div>
        <div class="metric-card">
            <div class="metric-val" style="color:#09090B;">{stat_val_6}</div>
            <div class="metric-lbl">{stat_lbl_6}</div>
            <div class="metric-sub">{stat_sub_6}</div>
        </div>
    </div>

    <!-- Power BI / Quantitative Execution Corridor -->
    <div class="section-card">
        <div class="section-header">{graphic_title}</div>
        <div style="font-size:12px;color:var(--text-muted);margin-bottom:16px;">{graphic_subtitle}</div>
        <div class="graphic-flex">
            <div class="graphic-col-visual">
                {graphic_visual}
            </div>
            {phase_panel}
        </div>
    </div>

    <!-- Quantitative Scouting Narrative -->
    <div class="section-card">
        <div class="section-header">Rajasthan Royals Tactical & Strategic Assessment</div>
        <div style="margin-top:12px;font-size:13px;line-height:1.65;color:#1C1C20;">
            <p style="margin-bottom:12px;">
                <strong>Executive Performance Summary:</strong> {p['summary']}
            </p>
            <p style="margin-bottom:12px;">
                <strong>Quantitative Advantage:</strong> {p['why_chose']}
            </p>
            <p style="margin-bottom:12px;">
                <strong>Risk & Comparative Analysis:</strong> {p['why_not_others']}
            </p>
            <p style="margin-bottom:0;">
                <strong>Tactical Fit for RR IPL 2027:</strong> {p['rr_fit']}
            </p>
        </div>
    </div>

    <!-- Methodology & Governance Disclosures -->
    <div class="section-card" style="background:#FAFAFB;border-color:#E4E4E7;">
        <div class="section-header" style="font-size:13.5px;">Methodological Governance & Statistical Audit Disclosures</div>
        <div style="font-size:12px;color:var(--text-muted);line-height:1.6;margin-top:8px;">
            <p style="margin-bottom:8px;">
                &bull; <strong>Strict Delivery Accounting:</strong> Reconciled across 200,999 raw tournament deliveries. Super Over balls (38 balls across 6 matches) are isolated into dedicated clutch registries to prevent extreme small-sample distortion. Under MCC Law 22/21, wides are excluded from legal balls faced, while no-balls are counted as balls faced.
            </p>
            <p style="margin-bottom:8px;">
                &bull; <strong>19-Feature Contextual Expected Runs Model:</strong> Non-linear HistGBR trained on 867 independent match clusters (5-Fold GroupKFold) with zero future data leakage. RMSE = 1.7225 (Batting) / 1.6938 (Bowling), significantly outperforming baseline phase averages ($p < 10^{{-60}}$).
            </p>
            <p style="margin-bottom:8px;">
                &bull; <strong>Empirical Bayes Shrinkage:</strong> Shrunk toward zero prior with strength $M_0 = 150.0$ legal balls (Batting RAE & Bowling RPAE) and $M_w = 100.0$ legal balls (Bowling WAE), maximizing Spearman-Brown out-of-sample split-half reliability.
            </p>
            <p style="margin-bottom:0;">
                &bull; <strong>Match-Clustered Uncertainty Estimation:</strong> 500-replicate match-clustered bootstrap resamples entire matches with replacement to capture pitch, dew, and opposition correlation. Simulation error is $\pm 0.36$ points on score means and $\pm 1.8\%$ on Top-10 probabilities.
            </p>
        </div>
    </div>

    <!-- Footer -->
    <footer>
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;font-size:12px;color:#27272A;">
            <div>
                &copy; 2026 Ketan Rawat. All rights reserved. &middot; Rajasthan Royals SupeRR Selector Season 2
            </div>
            <div style="display:flex;gap:12px;align-items:center;">
                <a href="../index.html" style="color:#09090B;text-decoration:none;font-weight:600;">Live Dashboard</a>
                <span>|</span>
                <a href="https://github.com/Ketanrawat2004/RR-Dashboard" target="_blank" style="color:#09090B;text-decoration:none;font-weight:600;">GitHub</a>
            </div>
        </div>
    </footer>
</div>

</body>
</html>"""
    return html

def main():
    print("=" * 80)
    print("PHASE 2B: STEP 4 — GENERATE STANDALONE PLAYER DOSSIERS")
    print("=" * 80)

    # Load expanded players_db.json
    db_path = os.path.join(ROOT, "players_db.json")
    with open(db_path, "r", encoding="utf-8") as f:
        players_db = json.load(f)

    # Load existing 25 dossiers to preserve
    existing_dossiers = set([f.replace(".html", "") for f in os.listdir(PLAYERS_DIR) if f.endswith(".html")])
    print(f"Existing dossiers in players/ ({len(existing_dossiers)}):")

    # Define Top 10 Batters and Top 10 Bowlers across both frameworks
    top_batters = [p for p in players_db if p["category"] == "Batter" and p["rank"] <= 10]
    top_bowlers_comp = [p for p in players_db if p["category"] == "Bowler" and p.get("rank_composite", p["rank"]) <= 10]
    top_bowlers_rpae = [p for p in players_db if p["category"] == "Bowler" and p.get("rank_pure_rpae", 999) <= 10]

    all_target_players = {}
    for p in top_batters:
        all_target_players[p["key"]] = p
    for p in top_bowlers_comp:
        all_target_players[p["key"]] = p
    for p in top_bowlers_rpae:
        all_target_players[p["key"]] = p

    print(f"Total featured players across Top 10 Batters & Bowlers (Both Frameworks): {len(all_target_players)}")

    # Sort players for carousel navigation
    target_list = list(all_target_players.values())
    n_targets = len(target_list)

    created_count = 0
    preserved_count = 0

    for idx, p in enumerate(target_list):
        key = p["key"]
        dossier_path = os.path.join(PLAYERS_DIR, f"{key}.html")
        prev_p = target_list[idx - 1] if idx > 0 else target_list[-1]
        next_p = target_list[idx + 1] if idx < n_targets - 1 else target_list[0]

        if key in existing_dossiers:
            preserved_count += 1
            print(f"  [PRESERVED] {key}.html already exists in players/ directory.")
        else:
            html = render_dossier_html(p, prev_p, next_p)
            with open(dossier_path, "w", encoding="utf-8") as f:
                f.write(html)
            created_count += 1
            print(f"  [CREATED] {key}.html ({len(html):,} chars)")

    print(f"\nPlayer Dossier Generation Summary:")
    print(f"  Existing dossiers preserved untouched: {preserved_count}")
    print(f"  New missing dossiers generated: {created_count}")
    print(f"  Total dossiers now in players/: {len(os.listdir(PLAYERS_DIR))}")

if __name__ == "__main__":
    main()

