import re

def generate_light_quadrant_svg():
    W, H = 860, 480
    ML, MR, MT, MB = 75, 40, 50, 55
    plot_w = W - ML - MR
    plot_h = H - MT - MB

    x_min, x_max = 42.0, 85.0
    y_min, y_max = -12.0, 24.0

    def to_x(wr):
        return ML + (wr - x_min) / (x_max - x_min) * plot_w

    def to_y(lift):
        return MT + (y_max - lift) / (y_max - y_min) * plot_h

    zero_y = to_y(0)
    thresh_x = to_x(60)

    svg = []
    svg.append(f'<svg viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF;border-radius:10px;border:1px solid #E2E8F0;box-shadow:0 2px 12px rgba(0,29,72,0.04);font-family:-apple-system,BlinkMacSystemFont,\\\'Segoe UI\\\',Roboto,sans-serif;">')

    # Background quadrant tints
    svg.append(f'  <rect x="{thresh_x}" y="{MT}" width="{W-MR-thresh_x}" height="{zero_y-MT}" fill="#F0FDF4" />')
    svg.append(f'  <text x="{W-MR-12}" y="{MT+20}" text-anchor="end" fill="#059669" font-size="10.5" font-weight="700" letter-spacing="0.5">QUADRANT I &bull; CLUTCH MATCH-WINNERS (High WR + Positive Lift)</text>')

    svg.append(f'  <rect x="{ML}" y="{MT}" width="{thresh_x-ML}" height="{zero_y-MT}" fill="#FFFBEB" />')
    svg.append(f'  <text x="{ML+12}" y="{MT+20}" text-anchor="start" fill="#D97706" font-size="10.5" font-weight="700" letter-spacing="0.5">QUADRANT II &bull; SITUATIONAL SPECIALISTS</text>')

    svg.append(f'  <rect x="{thresh_x}" y="{zero_y}" width="{W-MR-thresh_x}" height="{H-MB-zero_y}" fill="#F8FAFC" />')
    svg.append(f'  <text x="{W-MR-12}" y="{H-MB-14}" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="700" letter-spacing="0.5">QUADRANT IV &bull; HIGH BASELINE DRIFT (High Base WR, Negative Lift)</text>')

    # Gridlines
    for l_val in [-10, -5, 0, 5, 10, 15, 20]:
        y_pos = to_y(l_val)
        is_zero = (l_val == 0)
        stroke = "#94A3B8" if is_zero else "#E2E8F0"
        dash = 'stroke-dasharray="4,4"' if is_zero else ''
        width = "1.5" if is_zero else "1"
        svg.append(f'  <line x1="{ML}" y1="{y_pos}" x2="{W-MR}" y2="{y_pos}" stroke="{stroke}" stroke-width="{width}" {dash} />')
        svg.append(f'  <text x="{ML-8}" y="{y_pos+4}" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="600">{l_val:+d}%</text>')

    for wr_val in [45, 50, 55, 60, 65, 70, 75, 80]:
        x_pos = to_x(wr_val)
        is_thresh = (wr_val == 60)
        stroke = "#94A3B8" if is_thresh else "#E2E8F0"
        dash = 'stroke-dasharray="4,4"' if is_thresh else ''
        width = "1.5" if is_thresh else "1"
        svg.append(f'  <line x1="{x_pos}" y1="{MT}" x2="{x_pos}" y2="{H-MB}" stroke="{stroke}" stroke-width="{width}" {dash} />')
        svg.append(f'  <text x="{x_pos}" y="{H-MB+18}" text-anchor="middle" fill="#64748B" font-size="10.5" font-weight="600">{wr_val}%</text>')

    # Outer border
    svg.append(f'  <rect x="{ML}" y="{MT}" width="{plot_w}" height="{plot_h}" fill="none" stroke="#CBD5E1" stroke-width="1.5" />')

    # Axis Titles
    svg.append(f'  <text x="{ML + plot_w/2}" y="{H-15}" text-anchor="middle" fill="#001D48" font-size="12" font-weight="700">High-Pressure Win Rate (%) &bull; Threshold: Match Margin &le; 15 Runs / 2 Wickets or Playoff Knockouts</text>')
    svg.append(f'  <text x="18" y="{MT + plot_h/2}" text-anchor="middle" fill="#001D48" font-size="12" font-weight="700" transform="rotate(-90, 18, {MT + plot_h/2})">True Pressure Lift &Delta; (%) vs Career Baseline</text>')

    # Top Legend
    svg.append(f'  <g transform="translate({ML+10}, {MT-22})">')
    svg.append(f'    <circle cx="0" cy="0" r="5.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="1.5" />')
    svg.append(f'    <text x="10" y="3.5" fill="#001D48" font-size="11" font-weight="700">Batters</text>')
    svg.append(f'    <circle cx="80" cy="0" r="5.5" fill="#001D48" stroke="#FFFFFF" stroke-width="1.5" />')
    svg.append(f'    <text x="90" y="3.5" fill="#001D48" font-size="11" font-weight="700">Bowlers</text>')
    svg.append(f'    <text x="170" y="3.5" fill="#64748B" font-size="10.5">&bull; Size indicates high-pressure match sample volume &bull; Hover for player data</text>')
    svg.append(f'  </g>')

    players_data = [
        {"name": "Jacob Duffy", "rank": "#1", "wr": 75.0, "lift": 20.5, "cat": "Bowler", "lx": 0, "ly": -10, "anchor": "middle"},
        {"name": "Devon Conway", "rank": "#6", "wr": 64.3, "lift": 18.1, "cat": "Batter", "lx": 0, "ly": -10, "anchor": "middle"},
        {"name": "Josh Hazlewood", "rank": "#2", "wr": 78.6, "lift": 14.9, "cat": "Bowler", "lx": 10, "ly": 4, "anchor": "start"},
        {"name": "Yash Dayal", "rank": "#3", "wr": 80.0, "lift": 10.2, "cat": "Bowler", "lx": 10, "ly": 4, "anchor": "start"},
        {"name": "Shivam Dube", "rank": "#1", "wr": 66.7, "lift": 12.4, "cat": "Batter", "lx": 0, "ly": -10, "anchor": "middle"},
        {"name": "Rajat Patidar", "rank": "#4", "wr": 71.4, "lift": 11.1, "cat": "Batter", "lx": 0, "ly": -10, "anchor": "middle"},
        {"name": "Arshdeep Singh", "rank": "#9", "wr": 68.0, "lift": 11.0, "cat": "Bowler", "lx": 10, "ly": 4, "anchor": "start"},
        {"name": "B. Rajapaksa", "rank": "#8", "wr": 66.7, "lift": 10.4, "cat": "Batter", "lx": -10, "ly": 12, "anchor": "end"},
        {"name": "Virat Kohli", "rank": "", "wr": 70.0, "lift": 7.6, "cat": "Batter", "lx": 0, "ly": -10, "anchor": "middle"},
        {"name": "Rinku Singh", "rank": "#2", "wr": 69.2, "lift": 5.4, "cat": "Batter", "lx": 10, "ly": 12, "anchor": "start"},
        {"name": "Axar Patel", "rank": "#3", "wr": 64.3, "lift": 7.8, "cat": "Batter", "lx": 0, "ly": 15, "anchor": "middle"},
        {"name": "Suyash Sharma", "rank": "#7", "wr": 72.7, "lift": 7.6, "cat": "Bowler", "lx": 10, "ly": 4, "anchor": "start"},
        {"name": "Ruturaj Gaikwad", "rank": "#5", "wr": 57.1, "lift": 6.5, "cat": "Batter", "lx": 10, "ly": 4, "anchor": "start"},
        {"name": "R. Shepherd", "rank": "#6", "wr": 56.0, "lift": 7.0, "cat": "Bowler", "lx": -10, "ly": -6, "anchor": "end"},
        {"name": "L. Ferguson", "rank": "#10", "wr": 55.6, "lift": 6.5, "cat": "Bowler", "lx": -10, "ly": 12, "anchor": "end"},
        {"name": "Varun C.", "rank": "#5", "wr": 61.9, "lift": 3.3, "cat": "Bowler", "lx": 10, "ly": 4, "anchor": "start"},
        {"name": "Bhuvneshwar K.", "rank": "#8", "wr": 60.0, "lift": 2.7, "cat": "Bowler", "lx": -10, "ly": 12, "anchor": "end"},
        {"name": "Shreyas Iyer", "rank": "#9", "wr": 55.6, "lift": 1.1, "cat": "Batter", "lx": 0, "ly": 14, "anchor": "middle"},
        {"name": "Mitchell Starc", "rank": "#4", "wr": 60.0, "lift": -8.3, "cat": "Bowler", "lx": 10, "ly": 4, "anchor": "start"},
        {"name": "Sediqullah Atal", "rank": "#10", "wr": 50.0, "lift": -7.9, "cat": "Batter", "lx": 10, "ly": 4, "anchor": "start"},
    ]

    for p in players_data:
        cx = to_x(p['wr'])
        cy = to_y(p['lift'])
        color = "#EB1A8D" if p['cat'] == "Batter" else "#001D48"
        label_text = f"{p['name']} ({p['rank']})" if p['rank'] else p['name']
        lx_val = cx + p['lx']
        ly_val = cy + p['ly']
        anchor = p['anchor']
        
        svg.append('  <g class="scatter-point">')
        svg.append(f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="6.5" fill="{color}" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">')
        svg.append(f'      <title>{p["name"]}: {p["wr"]:.1f}% Win Rate, {p["lift"]:+0.1f}% Pressure Lift</title>')
        svg.append('    </circle>')
        svg.append(f'    <text x="{lx_val:.1f}" y="{ly_val:.1f}" text-anchor="{anchor}" fill="#0F172A" font-size="10.5" font-weight="600" style="pointer-events:none;">{label_text}</text>')
        svg.append('  </g>')

    svg.append('</svg>')
    return "\n".join(svg)

quadrant_svg_markup = generate_light_quadrant_svg()

with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    code = f.read()

start_target = '    <!-- IPL 2027 Rajasthan Royals Tactical Squad & Auction Strategy Section -->'
end_target = '<!-- Interactive Power BI Slicer & Sort Logic -->'

start_idx = code.find(start_target)
end_idx = code.find(end_target)

if start_idx != -1 and end_idx != -1:
    new_section_html = """    <!-- IPL 2027 Rajasthan Royals Tactical Squad & Auction Strategy Section -->
    <div id="section-tactical-xi" class="data-section" style="display:none;margin-top:16px;">
        
        <div class="tactical-grid">
            <!-- Left Column: Playing XI Formation & Lineup -->
            <div class="tactical-card">
                <div class="tactical-card-title">
                    Rajasthan Royals &mdash; Recommended 2027 Playing XI
                </div>
                <div class="tactical-card-sub">
                    A balanced 11-man lineup calibrated to dominate middle-overs spin and close out death overs under high match pressure.
                </div>
                
                <!-- Pure Clean Light Mode Starting XI Blueprint -->
                <div class="xi-blueprint-container">
                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Top-Order Anchors (Overs 1&ndash;6)</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">1</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Yashasvi Jaiswal</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Left-Hand Explosive Opener &bull; Powerplay Strike Rate 165+</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" onclick="window.location.href='players/devon_conway.html'">
                                <div class="xi-num">2</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Devon Conway</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">LHB Top-Order Anchor &amp; WK &bull; 64.3% Pressure Win Rate (+18.1% Lift)</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">3</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Sanju Samson <span style="font-size:11px;color:var(--rr-pink);font-weight:700;">(C)</span></span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Captain &amp; No. 3 Pace/Spin Attacker &bull; Proven Match-Winner</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Middle-Overs Engine &amp; Spin Enforcers (Overs 7&ndash;15)</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" onclick="window.location.href='players/shivam_dube.html'">
                                <div class="xi-num">4</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Shivam Dube</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Designated Spin Demolisher &bull; 66.7% Pressure Win Rate (+12.4% Lift)</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">5</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Riyan Parag</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Middle-Order Striker &amp; Leg-Spin Option &bull; SMS Fortress Anchor</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">6</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Dhruv Jurel <span style="font-size:11px;color:var(--text-muted);font-weight:600;">(WK)</span></span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Clutch Middle-Order Finisher &bull; Elite Death-Over Temperament</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Death-Overs Power Finishers (Overs 16&ndash;20)</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" onclick="window.location.href='players/rinku_singh.html'">
                                <div class="xi-num">7</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Rinku Singh</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Specialist Death Finisher &bull; 69.2% Pressure Win Rate across 26 High-Leverage Games</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">8</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Shimron Hetmyer</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Overseas Power Finisher &bull; Fearless Boundary Striking in Final 3 Overs</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Bowling Spearheads &amp; Seam Defense</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" onclick="window.location.href='players/josh_hazlewood.html'">
                                <div class="xi-num">9</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Josh Hazlewood</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Frontline Seam Spearhead &bull; 78.6% Pressure Win Rate (+14.9% Lift)</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">10</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Sandeep Sharma</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Death Yorker &amp; Wide-Line Master &bull; Reliable Execution in Final 2 Overs</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" onclick="window.location.href='players/yash_dayal.html'">
                                <div class="xi-num">11</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Yash Dayal</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Left-Arm Seam Specialist &bull; 80.0% Pressure Win Rate (+10.2% Lift)</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Tactical Impact Subs & Bench -->
                    <div class="xi-bench-box">
                        <div class="xi-bench-lbl">Tactical Impact Substitutes &amp; Matchup Covers:</div>
                        <div class="xi-bench-pills">
                            <span class="bench-pill" onclick="window.location.href='players/jacob_duffy.html'"><strong>Jacob Duffy</strong> (Pace &bull; +20.5% Lift)</span>
                            <span class="bench-pill" onclick="window.location.href='players/axar_patel.html'"><strong>Axar Patel</strong> (Spin All-Rounder &bull; +7.8% Lift)</span>
                            <span class="bench-pill" onclick="window.location.href='players/varun_chakravarthy.html'"><strong>Varun Chakravarthy</strong> (Mystery Spin &bull; 100% Playoff WR)</span>
                            <span class="bench-pill" onclick="window.location.href='players/rajat_patidar.html'"><strong>Rajat Patidar</strong> (No. 3 Cover &bull; +11.1% Lift)</span>
                        </div>
                    </div>
                </div>

                <!-- Playing XI Win Conversion Table: Cleanly Padded & Non-Wrapping -->
                <table class="purse-table" style="margin-top:16px;">
                    <thead>
                        <tr>
                            <th style="width:36px;text-align:center;">#</th>
                            <th style="min-width:130px;white-space:nowrap;">Player</th>
                            <th>Role in Team</th>
                            <th style="width:85px;text-align:right;white-space:nowrap;">Normal Win%</th>
                            <th style="width:85px;text-align:right;white-space:nowrap;">Pressure Win%</th>
                            <th style="width:90px;text-align:center;white-space:nowrap;">Win Diff</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr onclick="window.location.href='players/devon_conway.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);text-align:center;">1</td>
                            <td style="white-space:nowrap;"><strong>Devon Conway</strong> <span style="font-size:11px;color:var(--text-muted);">(wk)</span></td>
                            <td>Top-Order Anchor & Wicketkeeper</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">46.2%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">64.3%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+18.1%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/ruturaj_gaikwad.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);text-align:center;">2</td>
                            <td style="white-space:nowrap;"><strong>Ruturaj Gaikwad</strong></td>
                            <td>Opening Batter & Inning Pacer</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">50.6%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">57.1%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+6.5%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/rajat_patidar.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);text-align:center;">3</td>
                            <td style="white-space:nowrap;"><strong>Rajat Patidar</strong></td>
                            <td>No. 3 Anchor & Spin Attacker</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">60.3%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">71.4%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+11.1%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/shivam_dube.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);text-align:center;">4</td>
                            <td style="white-space:nowrap;"><strong>Shivam Dube</strong></td>
                            <td>Middle-Overs Boundary Hitter vs Spin (Overs 7&ndash;15)</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">54.3%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">66.7%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+12.4%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/shreyas_iyer.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);text-align:center;">5</td>
                            <td style="white-space:nowrap;"><strong>Shreyas Iyer</strong> <span style="font-size:11px;color:var(--rr-pink);font-weight:700;">(c)</span></td>
                            <td>Middle-Order Game Manager & Captain</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">54.5%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">55.6%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+1.1%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/rinku_singh.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);text-align:center;">6</td>
                            <td style="white-space:nowrap;"><strong>Rinku Singh</strong></td>
                            <td>Designated Death Finisher (Overs 16&ndash;20)</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">63.8%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">69.2%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+5.4%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/axar_patel.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);text-align:center;">7</td>
                            <td style="white-space:nowrap;"><strong>Axar Patel</strong></td>
                            <td>Spin All-Rounder & Late-Overs Hitter</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">56.5%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">64.3%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+7.8%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/romario_shepherd.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);text-align:center;">8</td>
                            <td style="white-space:nowrap;"><strong>Romario Shepherd</strong></td>
                            <td>Pace All-Rounder & Heavy-Ball Bowler</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">49.0%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">56.0%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+7.0%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/mitchell_starc.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);text-align:center;">9</td>
                            <td style="white-space:nowrap;"><strong>Mitchell Starc</strong></td>
                            <td>Left-Arm Fast Bowler (Powerplay & Death)</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">68.3%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">60.0%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag" style="background:#FEF3C7;color:#92400E;">3 Awards</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/varun_chakravarthy.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);text-align:center;">10</td>
                            <td style="white-space:nowrap;"><strong>Varun Chakravarthy</strong></td>
                            <td>Mystery Spinner (Middle Overs)</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">58.6%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">61.9%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+3.3%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/jacob_duffy.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);text-align:center;">11</td>
                            <td style="white-space:nowrap;"><strong>Jacob Duffy</strong></td>
                            <td>Accurate Swing & Seam Bowler</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">54.5%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">75.0%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+20.5%</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Right Column: Auction Valuation Model & Purse Allocation -->
            <div class="tactical-card">
                <div class="tactical-card-title">
                    Auction Budget Plan (&#8377;45 Crore Total Purse)
                </div>
                <div class="tactical-card-sub">
                    Disciplined bidding caps to prevent emotional overspending on marquee names.
                </div>

                <div class="budget-kpi-bar">
                    <div>
                        <div class="budget-kpi-val">&#8377;45.0 Cr</div>
                        <div class="budget-kpi-lbl">Total Budget</div>
                    </div>
                    <div>
                        <div class="budget-kpi-val" style="color:var(--success);">&#8377;45.0 Cr</div>
                        <div class="budget-kpi-lbl">Target Allocations</div>
                    </div>
                    <div>
                        <div class="budget-kpi-val" style="color:var(--rr-pink);">100%</div>
                        <div class="budget-kpi-lbl">Budget Utilized</div>
                    </div>
                </div>

                <!-- Fixed Auction Budget Table: No wrap on badges, prices, or purse % -->
                <table class="purse-table">
                    <thead>
                        <tr>
                            <th style="min-width:130px;white-space:nowrap;">Target Player</th>
                            <th style="width:100px;text-align:center;white-space:nowrap;">Priority</th>
                            <th style="width:105px;text-align:right;white-space:nowrap;">Max Bid</th>
                            <th style="width:90px;text-align:right;white-space:nowrap;">% of Purse</th>
                            <th>Why Rajasthan Royals Needs Him</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr onclick="window.location.href='players/rinku_singh.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Rinku Singh</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);white-space:nowrap;">&#8377;11.00 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">24.4%</td>
                            <td style="font-size:12px;line-height:1.45;">Proven death finisher; finishes tight chases with calm execution (69.2% win rate).</td>
                        </tr>
                        <tr onclick="window.location.href='players/shivam_dube.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Shivam Dube</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);white-space:nowrap;">&#8377;9.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">21.1%</td>
                            <td style="font-size:12px;line-height:1.45;">Destroys spin bowling in overs 7&ndash;15; prevents scoring slowdowns in middle overs.</td>
                        </tr>
                        <tr onclick="window.location.href='players/axar_patel.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Axar Patel</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);white-space:nowrap;">&#8377;8.00 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">17.8%</td>
                            <td style="font-size:12px;line-height:1.45;">Gives batting depth at No. 7 and bowls tight 4 overs of left-arm spin.</td>
                        </tr>
                        <tr onclick="window.location.href='players/jacob_duffy.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Jacob Duffy</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);white-space:nowrap;">&#8377;6.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">14.4%</td>
                            <td style="font-size:12px;line-height:1.45;">Top bowler in high-pressure matches (+20.5% lift, 75.0% win rate); disciplined swing.</td>
                        </tr>
                        <tr onclick="window.location.href='players/varun_chakravarthy.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Varun Chakravarthy</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-2">Priority 2</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);white-space:nowrap;">&#8377;5.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">12.2%</td>
                            <td style="font-size:12px;line-height:1.45;">Takes wickets in middle overs; 100% win rate in playoff knockout games.</td>
                        </tr>
                        <tr onclick="window.location.href='players/romario_shepherd.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Romario Shepherd</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-2">Priority 2</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);white-space:nowrap;">&#8377;4.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">10.0%</td>
                            <td style="font-size:12px;line-height:1.45;">Fast bowling option with heavy ball and power-hitting down the order.</td>
                        </tr>
                    </tbody>
                </table>

                <div style="margin-top:20px;padding:14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                    <div style="font-weight:700;font-size:12.5px;color:var(--rr-navy);margin-bottom:4px;">Auction Bidding Rule:</div>
                    <p style="font-size:12px;color:var(--text-main);line-height:1.5;margin:0;">
                        If bidding for any player goes more than 10% above their maximum limit, stop bidding immediately and switch to backup targets (such as Yash Dayal at &#8377;5.5 Cr or Bhanuka Rajapaksa at &#8377;3.5 Cr) to protect the overall team budget.
                    </p>
                </div>
            </div>
        </div>

        <!-- Bottom Card: Clean Light Mode Pressure Lift Quadrant Matrix with SVG Chart -->
        <div class="tactical-card" style="margin-top:24px;">
            <div class="tactical-card-title">
                Pressure Win Rate vs Normal Win Rate (Player Quadrant Classification)
            </div>
            <div class="tactical-card-sub">
                Compares how players perform when matches are close (under 15 runs or 2 wickets) versus career baseline games.
            </div>

            <!-- Crisp Light Mode Vector Scatter Plot (Replaces dark matplotlib chart) -->
            <div style="margin-bottom:20px;">
                """ + quadrant_svg_markup + """
            </div>

            <!-- Strategic Insights and Quadrant Explanations in Clean Light Mode -->
            <div style="display:grid;grid-template-columns:1.2fr 0.8fr;gap:24px;">
                <!-- 4 Quadrants Visual Grid in Light Mode -->
                <div class="quadrant-light-grid">
                    <div class="quadrant-box q-box-1">
                        <div class="q-tag q-tag-green">Quadrant I &bull; High Pressure Match-Winners</div>
                        <div class="q-desc">Significant positive win lift in tight finishes and playoff knockouts:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Shivam Dube</strong> (+12.4% Lift &bull; 66.7% HP WR)</span>
                            <span class="q-pill"><strong>Jacob Duffy</strong> (+20.5% Lift &bull; 75.0% HP WR)</span>
                            <span class="q-pill"><strong>Rinku Singh</strong> (+5.4% Lift &bull; 69.2% HP WR)</span>
                        </div>
                    </div>

                    <div class="quadrant-box q-box-2">
                        <div class="q-tag q-tag-blue">Quadrant II &bull; Consistent High Anchors</div>
                        <div class="q-desc">Consistently high win conversion across both normal and close games:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Devon Conway</strong> (64.3% HP WR &bull; +18.1% Lift)</span>
                            <span class="q-pill"><strong>Rajat Patidar</strong> (71.4% HP WR &bull; +11.1% Lift)</span>
                            <span class="q-pill"><strong>Axar Patel</strong> (64.3% HP WR &bull; +7.8% Lift)</span>
                        </div>
                    </div>

                    <div class="quadrant-box q-box-3">
                        <div class="q-tag q-tag-amber">Quadrant III &bull; Situational Aggressors</div>
                        <div class="q-desc">High strike rates that provide sudden momentum shifts in run chases:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Bhanuka Rajapaksa</strong> (168.4 Strike Rate)</span>
                            <span class="q-pill"><strong>Romario Shepherd</strong> (182.1 Strike Rate)</span>
                            <span class="q-pill"><strong>Sediqullah Atal</strong> (152.0 Strike Rate)</span>
                        </div>
                    </div>

                    <div class="quadrant-box q-box-4">
                        <div class="q-tag q-tag-navy">Quadrant IV &bull; Defensive Superstars</div>
                        <div class="q-desc">Elite containment; opponents take zero risks, lowering individual lift deltas:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Jasprit Bumrah</strong> (7.4 Death Econ &bull; 48.0% Dots)</span>
                            <span class="q-pill"><strong>Rashid Khan</strong> (6.8 Mid Econ &bull; Flat Googly)</span>
                        </div>
                    </div>
                </div>

                <!-- Insights Column -->
                <div>
                    <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:18px;">
                        <div style="font-weight:700;color:var(--rr-navy);font-size:13px;margin-bottom:12px;">Strategic Takeaways for Rajasthan Royals:</div>
                        
                        <div style="margin-bottom:12px;">
                            <strong style="color:var(--rr-navy);font-size:12px;">1. Solves the Middle-Overs Slowdown:</strong>
                            <p style="font-size:12px;color:var(--text-main);margin:2px 0 0 0;line-height:1.4;">
                                Target signing <strong>Shivam Dube</strong> (+12.4% lift) gives Rajasthan Royals the required spin boundary enforcer to partner Samson and Parag.
                            </p>
                        </div>

                        <div style="margin-bottom:12px;">
                            <strong style="color:var(--rr-navy);font-size:12px;">2. Fortress Sawai Mansingh Fit:</strong>
                            <p style="font-size:12px;color:var(--text-main);margin:2px 0 0 0;line-height:1.4;">
                                Jaipur's large 75m+ boundary requires elite runners and tactical anchors like <strong>Devon Conway</strong> and <strong>Axar Patel</strong> who maintain low dot-ball percentages.
                            </p>
                        </div>

                        <div style="margin-bottom:12px;">
                            <strong style="color:var(--rr-navy);font-size:12px;">3. Guaranteed Death Overs Defense:</strong>
                            <p style="font-size:12px;color:var(--text-main);margin:2px 0 0 0;line-height:1.4;">
                                Pairing <strong>Josh Hazlewood</strong> with retained yorker specialist <strong>Sandeep Sharma</strong> guarantees 4 disciplined death overs under 9.0 RPO.
                            </p>
                        </div>

                        <div>
                            <strong style="color:var(--rr-navy);font-size:12px;">4. Bidding Discipline:</strong>
                            <p style="font-size:12px;color:var(--text-main);margin:2px 0 0 0;line-height:1.4;">
                                A hard cap of &#8377;11.0 Cr for any single target prevents auction inflation from ruining squad depth.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- Quantitative Framework Documentation in Clean Light Mode -->
    <div class="doc-grid">
        <div class="doc-box">
            <div class="doc-heading">Quantitative Model Formulation</div>
            <p style="font-size:12.5px;color:#475569;margin-bottom:8px;">
                The Clutch Player Performance Index (CPPI) addresses small-sample statistical variance via Bayesian shrinkage estimation:
            </p>
            <div class="code-snippet">
                CPPI = [ 0.35 &times; WR_hp + 0.15 &times; WR_base + 0.20 &times; &Delta; + 0.15 &times; MOM_hp + 0.15 &times; WR_ko ] &times; Saturation
            </div>
            <p style="font-size:12px;color:#64748B;line-height:1.5;">
                Where Saturation = min(1.0, Matches_hp / 10.0), guaranteeing that candidates with insufficient high-leverage samples are penalised in final ranking calculations.
            </p>
        </div>

        <div class="doc-box">
            <div class="doc-heading">Operational Definitions & Data Governance</div>
            <p style="font-size:12.5px;color:#475569;line-height:1.6;">
                <strong style="color:var(--rr-navy);">1. High-Leverage Fixture:</strong> Matches meeting stern empirical pressure criteria: elimination knockout games (Finals, Semi-Finals, Eliminators), super-over resolutions, or finishes with winning margins &le; 15 runs or &le; 2 wickets.<br>
                <strong style="color:var(--rr-navy);">2. Regulatory Pre-Filter:</strong> Strict exclusion of non-auction eligible entities pursuant to BCCI IPL Player Regulations.<br>
                <strong style="color:var(--rr-navy);">3. Tactical Venue Model:</strong> Sawai Mansingh Stadium pitch metrics (72-78m boundaries, middle-overs spin grip, nocturnal dew factor).
            </p>
        </div>
    </div>

</div>

"""
    code = code[:start_idx] + new_section_html + code[end_idx:]

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated fix_dashboard_and_wagon.py with SVG chart and clean table!")
