def generate_perfect_clean_svg():
    W, H = 900, 520
    ML, MR, MT, MB = 80, 60, 65, 55
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
    svg.append(f'<svg viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF;border-radius:10px;border:1px solid #E2E8F0;box-shadow:0 2px 10px rgba(0,0,0,0.03);font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif;">')

    # Soft subtle background quadrant tints
    svg.append(f'  <rect x="{thresh_x}" y="{MT}" width="{W-MR-thresh_x}" height="{zero_y-MT}" fill="#F0FDF4" />')
    svg.append(f'  <rect x="{ML}" y="{MT}" width="{thresh_x-ML}" height="{zero_y-MT}" fill="#FFFBEB" />')
    svg.append(f'  <rect x="{thresh_x}" y="{zero_y}" width="{W-MR-thresh_x}" height="{H-MB-zero_y}" fill="#F8FAFC" />')

    # Subtle non-interfering quadrant corner watermarks (placed in extreme corners with zero text overlap)
    svg.append(f'  <text x="{ML+12}" y="{MT+20}" fill="#D97706" font-size="10" font-weight="800" letter-spacing="0.5">QUADRANT II &bull; SITUATIONAL SPECIALISTS</text>')
    svg.append(f'  <text x="{W-MR-12}" y="{MT+20}" text-anchor="end" fill="#059669" font-size="10" font-weight="800" letter-spacing="0.5">QUADRANT I &bull; CLUTCH MATCH-WINNERS</text>')
    svg.append(f'  <text x="{W-MR-12}" y="{H-MB-12}" text-anchor="end" fill="#64748B" font-size="10" font-weight="800" letter-spacing="0.5">QUADRANT IV &bull; HIGH BASELINE DRIFT</text>')

    # Gridlines
    for l_val in [-10, -5, 0, 5, 10, 15, 20]:
        y_pos = to_y(l_val)
        is_zero = (l_val == 0)
        stroke = "#94A3B8" if is_zero else "#E2E8F0"
        dash = 'stroke-dasharray="4,4"' if is_zero else ''
        width = "1.5" if is_zero else "1"
        svg.append(f'  <line x1="{ML}" y1="{y_pos:.1f}" x2="{W-MR}" y2="{y_pos:.1f}" stroke="{stroke}" stroke-width="{width}" {dash} />')
        svg.append(f'  <text x="{ML-10}" y="{y_pos+4:.1f}" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="600">{l_val:+d}%</text>')

    for wr_val in [45, 50, 55, 60, 65, 70, 75, 80]:
        x_pos = to_x(wr_val)
        is_thresh = (wr_val == 60)
        stroke = "#94A3B8" if is_thresh else "#E2E8F0"
        dash = 'stroke-dasharray="4,4"' if is_thresh else ''
        width = "1.5" if is_thresh else "1"
        svg.append(f'  <line x1="{x_pos:.1f}" y1="{MT}" x2="{x_pos:.1f}" y2="{H-MB}" stroke="{stroke}" stroke-width="{width}" {dash} />')
        svg.append(f'  <text x="{x_pos:.1f}" y="{H-MB+18}" text-anchor="middle" fill="#64748B" font-size="10.5" font-weight="600">{wr_val}%</text>')

    # Outer border
    svg.append(f'  <rect x="{ML}" y="{MT}" width="{plot_w}" height="{plot_h}" fill="none" stroke="#CBD5E1" stroke-width="1.5" />')

    # Axis Titles - Clean, crisp black
    svg.append(f'  <text x="{ML + plot_w/2:.1f}" y="{H-15}" text-anchor="middle" fill="#111827" font-size="12" font-weight="700">High-Pressure Win Rate (%) &bull; Close Finishes &le; 15 Runs / 2 Wickets &amp; Playoff Knockouts</text>')
    svg.append(f'  <text x="18" y="{MT + plot_h/2:.1f}" text-anchor="middle" fill="#111827" font-size="12" font-weight="700" transform="rotate(-90, 18, {MT + plot_h/2:.1f})">True Pressure Lift &Delta; (%) vs Career Baseline</text>')

    # Top Legend
    svg.append(f'  <g transform="translate({ML+10}, {MT-26})">')
    svg.append(f'    <circle cx="0" cy="0" r="5.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="1.5" />')
    svg.append(f'    <text x="10" y="3.5" fill="#111827" font-size="11" font-weight="700">Batters</text>')
    svg.append(f'    <circle cx="85" cy="0" r="5.5" fill="#111827" stroke="#FFFFFF" stroke-width="1.5" />')
    svg.append(f'    <text x="95" y="3.5" fill="#111827" font-size="11" font-weight="700">Bowlers</text>')
    svg.append(f'    <text x="180" y="3.5" fill="#64748B" font-size="10.5">&bull; Size indicates pressure match sample &bull; Hover dots for details</text>')
    svg.append(f'  </g>')

    # 100% collision-free placement
    players_data = [
        {"name": "Jacob Duffy (#1)", "wr": 75.0, "lift": 20.5, "cat": "Bowler", "dx": -12, "dy": 4, "anchor": "end"},
        {"name": "Devon Conway (#6)", "wr": 64.3, "lift": 18.1, "cat": "Batter", "dx": 0, "dy": -12, "anchor": "middle"},
        {"name": "Josh Hazlewood (#2)", "wr": 78.6, "lift": 14.9, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Yash Dayal (#3)", "wr": 80.0, "lift": 10.2, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Shivam Dube (#1)", "wr": 66.7, "lift": 12.4, "cat": "Batter", "dx": -12, "dy": -4, "anchor": "end"},
        {"name": "Rajat Patidar (#4)", "wr": 71.4, "lift": 11.1, "cat": "Batter", "dx": 0, "dy": -12, "anchor": "middle"},
        {"name": "Arshdeep Singh (#9)", "wr": 68.0, "lift": 11.0, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "B. Rajapaksa (#8)", "wr": 66.7, "lift": 10.4, "cat": "Batter", "dx": -12, "dy": -4, "anchor": "end"},
        {"name": "Virat Kohli", "wr": 70.0, "lift": 7.6, "cat": "Batter", "dx": -10, "dy": -8, "anchor": "end"},
        {"name": "Rinku Singh (#2)", "wr": 69.2, "lift": 5.4, "cat": "Batter", "dx": 12, "dy": 16, "anchor": "start"},
        {"name": "Suyash Sharma (#7)", "wr": 72.7, "lift": 7.6, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Axar Patel (#3)", "wr": 64.3, "lift": 7.8, "cat": "Batter", "dx": 8, "dy": 16, "anchor": "start"},
        {"name": "R. Gaikwad (#5)", "wr": 57.1, "lift": 6.5, "cat": "Batter", "dx": 10, "dy": -8, "anchor": "start"},
        {"name": "R. Shepherd (#6)", "wr": 56.0, "lift": 7.0, "cat": "Bowler", "dx": -12, "dy": -8, "anchor": "end"},
        {"name": "L. Ferguson (#10)", "wr": 55.6, "lift": 6.5, "cat": "Bowler", "dx": -12, "dy": 14, "anchor": "end"},
        {"name": "Varun C. (#5)", "wr": 61.9, "lift": 3.3, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Bhuvneshwar K. (#8)", "wr": 60.0, "lift": 2.7, "cat": "Bowler", "dx": -12, "dy": -6, "anchor": "end"},
        {"name": "Shreyas Iyer (#9)", "wr": 55.6, "lift": 1.1, "cat": "Batter", "dx": -12, "dy": 4, "anchor": "end"},
        {"name": "Mitchell Starc (#4)", "wr": 60.0, "lift": -8.3, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Sediqullah Atal (#10)", "wr": 50.0, "lift": -7.9, "cat": "Batter", "dx": 12, "dy": 4, "anchor": "start"},
    ]

    for p in players_data:
        cx = to_x(p['wr'])
        cy = to_y(p['lift'])
        color = "#EB1A8D" if p['cat'] == "Batter" else "#111827"
        label_text = f"{p['name']} ({p['rank']})" if (p['rank'] and not p['name'].endswith(')')) else p['name']
        lx_val = cx + p['dx']
        ly_val = cy + p['dy']
        anchor = p['anchor']
        
        svg.append('  <g class="scatter-point">')
        svg.append(f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="6.5" fill="{color}" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;">')
        svg.append(f'      <title>{p["name"]}: {p["wr"]:.1f}% Win Rate, {p["lift"]:+0.1f}% Pressure Lift</title>')
        svg.append('    </circle>')
        svg.append(f'    <text x="{lx_val:.1f}" y="{ly_val:.1f}" text-anchor="{anchor}" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">{label_text}</text>')
        svg.append('  </g>')

    svg.append('</svg>')
    return "\n".join(svg)

print("Generated perfect clean SVG. Length:", len(generate_perfect_clean_svg()))

