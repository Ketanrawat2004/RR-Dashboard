import json
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

BASE_DIR = Path(".")
SCRATCH = BASE_DIR / "scratch"
LOGO_PATH = SCRATCH / "rr_corner_logo.png"
DONUT_PATH = SCRATCH / "donut_pressure_distribution.png"
QUAD_PATH = SCRATCH / "quadrant_scatter.png"
WAGON_WHEEL_PATH = SCRATCH / "dossier_wagon_wheel.jpg"
PITCH_MAP_PATH = SCRATCH / "dossier_pitch_map.png"

OUT_MAIN = BASE_DIR / "RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx"
OUT_OVERHAUL = BASE_DIR / "RR_SupeRR_Selector_Season2_Ketan_Rawat_Overhaul.pptx"
OUT_COPY = BASE_DIR / "pressure_output" / "RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx"

# Crisp High-Contrast Executive Palette
WHITE = RGBColor(255, 255, 255)
BG_SOFT = RGBColor(248, 250, 252)
BORDER_LIGHT = RGBColor(203, 213, 225)      # Stronger border so boxes pop clearly
DARK_TEXT = RGBColor(15, 23, 42)            # High contrast slate-900
BODY_TEXT = RGBColor(30, 41, 59)            # Deep slate-800 for maximum legibility
MUTED_TEXT = RGBColor(71, 85, 105)          # Slate-600
RR_NAVY = RGBColor(0, 29, 72)               # Official RR Navy
RR_PINK = RGBColor(235, 26, 141)            # Official RR Pink
GREEN = RGBColor(16, 149, 93)               # Crisp Emerald
RED = RGBColor(220, 38, 38)
AMBER = RGBColor(180, 83, 9)

FONT_MAIN = "Calibri"

def set_cell_border(cell, color_hex="CBD5E1", width_pt="9525"):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        for existing in tcPr.findall(qn(tag)):
            tcPr.remove(existing)
        ln = parse_xml(
            f'<{tag} xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="{width_pt}" cap="flat" cmpd="sng" algn="ctr">'
            f'<a:solidFill><a:srgbClr val="{color_hex}"/></a:solidFill>'
            f'</{tag}>'
        )
        tcPr.append(ln)

def style_cell(cell, text, font_size=11.0, bold=False, color=BODY_TEXT, fill=None, align=PP_ALIGN.LEFT, margins=(0.08, 0.08, 0.04, 0.04)):
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = Inches(margins[0])
    cell.margin_right = Inches(margins[1])
    cell.margin_top = Inches(margins[2])
    cell.margin_bottom = Inches(margins[3])
    if fill is not None:
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    p.text = str(text)
    p.font.name = FONT_MAIN
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    set_cell_border(cell)

def add_corner_logo(slide):
    if LOGO_PATH.exists():
        slide.shapes.add_picture(str(LOGO_PATH), Inches(12.30), Inches(0.20), height=Inches(0.85))

def add_slide_title(slide, title, subtitle=None):
    add_corner_logo(slide)
    tb = slide.shapes.add_textbox(Inches(0.60), Inches(0.25), Inches(11.4), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_MAIN
    p.font.size = Pt(23)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(12.5)
        p2.font.color.rgb = MUTED_TEXT
        p2.space_before = Pt(3)

def add_box(slide, left, top, width, height, fill=BG_SOFT, border=BORDER_LIGHT, line_w=1.0):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if border is not None:
        shp.line.color.rgb = border
        shp.line.width = Pt(line_w)
    else:
        shp.line.fill.background()
    return shp

def add_text(slide, left, top, width, height, text, size=11.5, bold=False, color=BODY_TEXT, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.font.name = FONT_MAIN
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    return tb

def build_grand_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    add_corner_logo(s1)

    add_text(s1, 0.90, 1.20, 11.0, 0.40, "Rajasthan Royals  |  SupeRR Selector Season 2", size=15, bold=True, color=RR_PINK)
    add_text(s1, 0.90, 1.70, 11.5, 1.45, "Evaluating Player Performance\nUnder Match Pressure", size=40, bold=True, color=DARK_TEXT)
    add_text(s1, 0.90, 3.35, 11.5, 0.70,
             "Contextual Ball-by-Ball Leverage Engine & Empirical Bayes Rankings for IPL 2027 Roster Architecture",
             size=16.0, color=BODY_TEXT)

    add_box(s1, 0.90, 4.25, 3.5, 0.04, fill=RR_NAVY, border=None)

    add_text(s1, 0.90, 4.45, 11.5, 0.38,
             "Dataset: 867 Senior T20 Fixtures (IPL & T20I, 2022–2026)  |  200,961 Deliveries  |  342 Qualified Candidates",
             size=12.5, bold=True, color=RR_NAVY)
    add_text(s1, 0.90, 4.88, 11.5, 0.35,
             "Candidate: Ketan Rawat  |  Role Track: Cricket Operations & Performance Analytics",
             size=12.5, color=MUTED_TEXT)

    # Big Prominent URL Cards filling bottom space
    add_box(s1, 0.90, 5.45, 5.60, 1.45, fill=WHITE, border=BORDER_LIGHT, line_w=1.2)
    add_text(s1, 1.15, 5.60, 5.1, 0.25, "LIVE PRODUCTION DASHBOARD", size=11.5, bold=True, color=RR_NAVY)
    add_text(s1, 1.15, 5.90, 5.1, 0.35, "https://rr-dashboard.onrender.com/", size=14.5, bold=True, color=RR_PINK)
    add_text(s1, 1.15, 6.35, 5.1, 0.40, "Explore interactive 342-player dossiers, 8-sector spray charts, and live war room terminal.", size=11.0, color=BODY_TEXT)

    add_box(s1, 6.80, 5.45, 5.60, 1.45, fill=WHITE, border=BORDER_LIGHT, line_w=1.2)
    add_text(s1, 7.05, 5.60, 5.1, 0.25, "OPEN-SOURCE CODEBASE & REPLICATION", size=11.5, bold=True, color=RR_NAVY)
    add_text(s1, 7.05, 5.90, 5.1, 0.35, "https://github.com/Ketanrawat2004/RR-Dashboard", size=14.5, bold=True, color=DARK_TEXT)
    add_text(s1, 7.05, 6.35, 5.1, 0.40, "Complete Python data pipelines, match-clustered bootstrap uncertainty models, and player dossier suite.", size=11.0, color=BODY_TEXT)

    # =========================================================================
    # SLIDE 2: TOURNAMENT SAMPLE & PRESSURE DELIVERY DISTRIBUTION
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    add_slide_title(s2, "Tournament Sample & Pressure Delivery Distribution",
                    "Overview of 200,961 deliveries across 867 fixtures isolating acute high-leverage match states")

    kpis = [
        ("MATCHES EVALUATED", "867", "IPL & T20I (2022–2026)", DARK_TEXT),
        ("DELIVERIES EVALUATED", "200,961", "Ball-by-ball records", DARK_TEXT),
        ("QUALIFIED CANVASS", "342", "163 Batters • 179 Bowlers", DARK_TEXT),
        ("TOP RANKED BATTER", "+26.59", "Andre Russell (165.6 SR)", RR_PINK),
        ("TOP RANKED BOWLER", "+28.45", "Jasprit Bumrah (7.79 Econ)", RR_NAVY),
        ("PEAK LEVERAGE LIFT", "+83.78", "V. Sooryavanshi (234.6 SR)", GREEN),
    ]
    kx = 0.60
    kw = 1.92
    for lbl, num, sub, ncol in kpis:
        add_box(s2, kx, 1.25, kw, 1.25, fill=BG_SOFT, border=BORDER_LIGHT)
        add_text(s2, kx + 0.08, 1.35, kw - 0.16, 0.25, lbl, size=10.5, bold=True, color=MUTED_TEXT, align=PP_ALIGN.CENTER)
        add_text(s2, kx + 0.08, 1.62, kw - 0.16, 0.45, num, size=24.0, bold=True, color=ncol, align=PP_ALIGN.CENTER)
        add_text(s2, kx + 0.08, 2.15, kw - 0.16, 0.28, sub, size=10.5, bold=True, color=BODY_TEXT, align=PP_ALIGN.CENTER)
        kx += kw + 0.12

    # Panel 1: Pressure Distribution Donut (Large Picture + Big Legend)
    add_box(s2, 0.60, 2.65, 3.85, 4.45, fill=WHITE, border=BORDER_LIGHT)
    add_text(s2, 0.80, 2.80, 3.45, 0.30, "PRESSURE DELIVERY DISTRIBUTION", size=12.0, bold=True, color=RR_NAVY)
    if DONUT_PATH.exists():
        s2.shapes.add_picture(str(DONUT_PATH), Inches(0.95), Inches(3.20), width=Inches(3.15))
    dist_rows = [
        ("Death Overs (16–20)", "42%", RR_PINK),
        ("Chases Requiring RRR >= 9.0", "38%", DARK_TEXT),
        ("Top-Order Collapse Phases", "20%", GREEN),
    ]
    dy = 5.75
    for dlabel, dval, dcol in dist_rows:
        add_box(s2, 0.85, dy + 0.05, 0.16, 0.16, fill=dcol, border=None)
        add_text(s2, 1.10, dy, 2.6, 0.28, dlabel, size=11.5, bold=True, color=BODY_TEXT)
        add_text(s2, 3.65, dy, 0.65, 0.28, dval, size=12.0, bold=True, color=DARK_TEXT, align=PP_ALIGN.RIGHT)
        dy += 0.35

    # Panel 2: Top Batting Pressure Lifts
    add_box(s2, 4.65, 2.65, 3.85, 4.45, fill=WHITE, border=BORDER_LIGHT)
    add_text(s2, 4.85, 2.80, 3.45, 0.30, "TOP BATTING PRESSURE LIFTS (SR Δ)", size=12.0, bold=True, color=RR_NAVY)
    add_text(s2, 4.85, 3.12, 3.45, 0.28, "True strike rate boost above contextual baseline:", size=11.0, color=MUTED_TEXT)
    lifts = [
        ("1. Vaibhav Sooryavanshi", "+83.78", 83.78),
        ("2. Priyansh Arya", "+70.34", 70.34),
        ("3. Andre Russell", "+38.94", 38.94),
        ("4. Prabhsimran Singh", "+33.90", 33.90),
        ("5. Glenn Maxwell", "+33.14", 33.14),
    ]
    ly = 3.52
    for lname, lval, lpct in lifts:
        add_text(s2, 4.85, ly, 2.5, 0.26, lname, size=11.5, bold=True, color=DARK_TEXT)
        add_text(s2, 7.35, ly, 0.95, 0.26, lval, size=12.0, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)
        add_box(s2, 4.85, ly + 0.30, 3.45, 0.10, fill=BORDER_LIGHT, border=None)
        add_box(s2, 4.85, ly + 0.30, 3.45 * (lpct / 88.0), 0.10, fill=GREEN, border=None)
        ly += 0.62

    # Panel 3: Leverage Situation Performance Matrix
    add_box(s2, 8.70, 2.65, 4.03, 4.45, fill=WHITE, border=BORDER_LIGHT)
    add_text(s2, 8.90, 2.80, 3.63, 0.30, "LEVERAGE SITUATION PERFORMANCE MATRIX", size=12.0, bold=True, color=RR_NAVY)
    add_text(s2, 8.90, 3.12, 3.63, 0.28, "Contextual performance across key high-pressure match phases:", size=11.0, color=MUTED_TEXT)

    t_mat = s2.shapes.add_table(4, 5, Inches(8.85), Inches(3.60), Inches(3.73), Inches(2.45)).table
    mat_widths = [1.25, 0.62, 0.62, 0.62, 0.62]
    for ci, cw in enumerate(mat_widths):
        t_mat.columns[ci].width = Inches(cw)
    m_headers = ["Phase", "Death", "RRR >= 10", "Playoffs", "Super Over"]
    for ci, h in enumerate(m_headers):
        style_cell(t_mat.cell(0, ci), h, 10.5, True, WHITE, RR_NAVY, PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER)
    m_rows = [
        ("Top 10 Batters (SR)", "186.2", "181.5", "172.4", "210.0", GREEN),
        ("Top 10 Bowlers (Econ)", "7.64", "7.92", "7.31", "6.00", GREEN),
        ("Peer Baseline", "136.4 / 9.85", "139.1 / 10.4", "130.2 / 9.60", "145.0 / 11.2", RED),
    ]
    for ri, row in enumerate(m_rows, 1):
        style_cell(t_mat.cell(ri, 0), row[0], 10.5, True, DARK_TEXT, BG_SOFT if ri == 3 else WHITE, PP_ALIGN.LEFT)
        for ci in range(1, 5):
            style_cell(t_mat.cell(ri, ci), row[ci], 10.5, True, row[5], BG_SOFT if ri == 3 else WHITE, PP_ALIGN.CENTER)

    add_text(s2, 8.90, 6.25, 3.63, 0.70,
             "Key Metric: Top-ranked performers score 45–65 runs/100 balls faster than peers and concede over 2.2 runs/over fewer at the death.",
             size=10.5, bold=True, color=BODY_TEXT)

    # =========================================================================
    # SLIDE 3: EVALUATION METHOD & DATA GOVERNANCE
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    add_slide_title(s3, "Evaluation Methodology & Thought Process",
                    "A delivery-level baseline isolating individual clutch execution from team outcomes")

    # Left Column: Method & Formulation
    add_box(s3, 0.60, 1.25, 5.95, 5.85, fill=WHITE, border=BORDER_LIGHT)
    add_text(s3, 0.85, 1.45, 5.45, 0.32, "QUANTITATIVE MODEL FORMULATION", size=13.0, bold=True, color=RR_NAVY)

    add_text(s3, 0.85, 1.85, 5.45, 0.75,
             "We isolate each delivery against contextual expectations rather than uncontextualized averages. Expected runs are modeled per delivery using match-clustered cross-validation across 200,961 balls, eliminating intra-match leakage.",
             size=11.5, color=BODY_TEXT)

    add_box(s3, 0.85, 2.75, 5.45, 0.75, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s3, 1.00, 2.85, 5.15, 0.55,
             "Batting Shrunk RAE = [ N_press / (N_press + 150) ] * Raw_RAE\n                    + [ 150 / (N_press + 150) ] * Mean",
             size=11.0, bold=True, color=DARK_TEXT)

    add_box(s3, 0.85, 3.65, 5.45, 0.55, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s3, 1.00, 3.75, 5.15, 0.35,
             "Bowling Composite = 0.60 * Shrunk_RPAE + 0.40 * (Shrunk_WAE * 12.0)",
             size=11.0, bold=True, color=DARK_TEXT)

    add_text(s3, 0.85, 4.35, 5.45, 0.30, "OPERATIONAL DEFINITIONS & GOVERNANCE", size=12.5, bold=True, color=RR_NAVY)

    gov_points = [
        ("1. Pre-Delivery Pressure Engine:", "Defines pressure strictly before the ball is bowled: Death overs (16–20), chases requiring RRR >= 9.0 or balls <= 30, and top-order powerplay collapses."),
        ("2. Context-Conditioned Baseline:", "Calculates expected runs based on pitch phase, wickets in hand, and required rate, preventing cross-match leakage."),
        ("3. Uncertainty Quantification:", "Match-clustered bootstrap (1,000 resamples) accounts for match correlation to produce verified 90% rank intervals."),
    ]
    gy = 4.70
    for gtitle, gbody in gov_points:
        add_text(s3, 0.85, gy, 5.45, 0.22, gtitle, size=11.5, bold=True, color=DARK_TEXT)
        add_text(s3, 0.85, gy + 0.22, 5.45, 0.45, gbody, size=10.5, color=BODY_TEXT)
        gy += 0.72

    # Right Column: Thought Process & Cricket Realities
    add_box(s3, 6.78, 1.25, 5.95, 5.85, fill=WHITE, border=BORDER_LIGHT)
    add_text(s3, 7.03, 1.45, 5.45, 0.32, "CRICKET OPERATIONS THOUGHT PROCESS", size=13.0, bold=True, color=RR_NAVY)

    thought_blocks = [
        ("Why Traditional Statistics Mislead:",
         "Standard season averages and strike rates reward players who score easily during low-pressure middle overs when fielders are back and games are settled. A batter scoring 40 off 35 in a blowout looks good on paper but adds minimal winning value."),
        ("Isolating True Pressure Performers:",
         "By measuring performance against delivery-level baselines, we identify players who consistently produce above expectation when the game is on the line. Andre Russell (+38.94 SR lift) and Jasprit Bumrah (-1.39 Econ lift) represent proven world-class clutch execution."),
        ("The Bowler Survival Phenomenon:",
         "Opposing batters frequently play out Jasprit Bumrah defensively at the death to avoid losing wickets. A model looking only at raw wickets would penalize him, whereas run prevention (RPAE) reveals his unmatched economic choke rate (7.79 Econ)."),
        ("Scouting High-Ceiling Young Talent:",
         "Young domestic players like Vaibhav Sooryavanshi (55 balls) and Priyansh Arya (52 balls) show extraordinary boundary hitting (+70 to +84 SR lift). We isolate them as developmental scouting targets without allowing small sample sizes to distort senior rankings."),
    ]
    ty = 1.85
    for ttitle, tbody in thought_blocks:
        add_text(s3, 7.03, ty, 5.45, 0.24, ttitle, size=11.5, bold=True, color=RR_NAVY)
        add_text(s3, 7.03, ty + 0.26, 5.45, 0.65, tbody, size=10.5, color=BODY_TEXT)
        ty += 1.20

    # =========================================================================
    # SLIDE 4: TOP 10 BATTERS UNDER PRESSURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    add_slide_title(s4, "Top 10 Batters Under Pressure",
                    "Senior-proven performers ranked by Shrunk Runs Above Expectation (RAE) with domestic breakout radar")

    # Interactive instruction bar - HIGH CONTRAST & BOLD
    add_box(s4, 0.60, 1.15, 12.13, 0.38, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s4, 0.80, 1.22, 11.7, 0.25,
             "Interactive Feature: In the live web dashboard (index.html), clicking on any player row or 'Dossier' opens their detailed scouting review.",
             size=11.0, bold=True, color=RR_NAVY)

    # 9-Column Optimized Table for maximum font size and legibility
    t_bat = s4.shapes.add_table(11, 9, Inches(0.60), Inches(1.58), Inches(12.13), Inches(3.40)).table
    b_widths = [0.45, 2.50, 2.18, 1.10, 1.20, 1.15, 1.15, 1.15, 1.25]
    for ci, cw in enumerate(b_widths):
        t_bat.columns[ci].width = Inches(cw)

    b_headers = ["#", "Player & Role", "Franchise / Origin", "Pressure Balls", "Pressure SR", "Expected SR", "SR Lift (Δ)", "90% Rank", "Shrunk RAE"]
    for ci, h in enumerate(b_headers):
        style_cell(t_bat.cell(0, ci), h, 11.0, True, WHITE, RR_PINK, PP_ALIGN.LEFT if ci in (1, 2) else PP_ALIGN.CENTER)

    batters_data = [
        ("1", "Andre Russell", "Specialist High-Leverage Batter", "Kolkata Knight Riders, WI", "323", "165.6", "126.7", "+38.94", "#1 to #12", "+26.59"),
        ("2", "Heinrich Klaasen", "Middle-Overs Spin Enforcer", "Sunrisers Hyderabad, SA", "487", "153.2", "129.5", "+23.65", "#1 to #15", "+24.15"),
        ("3", "Glenn Maxwell", "Middle 360° Disrupter", "Punjab Kings, RCB, AUS", "315", "164.1", "131.0", "+33.14", "#1 to #25", "+22.45"),
        ("4", "Suryakumar Yadav", "All-Phase Pressure Striker", "Mumbai Indians, India", "682", "150.6", "130.9", "+19.69", "#2 to #20", "+21.80"),
        ("5", "Tim David", "Death Boundary Finisher", "Mumbai Indians, RCB, AUS", "505", "162.8", "136.7", "+26.08", "#2 to #28", "+20.11"),
        ("6", "Abhishek Sharma", "Powerplay Intent Striker", "Sunrisers Hyderabad, India", "204", "168.1", "136.0", "+32.14", "#3 to #35", "+18.52"),
        ("7", "Rinku Singh", "Ice-Cool Death Finisher", "Kolkata Knight Riders, India", "268", "168.4", "138.2", "+30.20", "#3 to #38", "+18.15"),
        ("8", "Shivam Dube", "Middle-Overs Spin Enforcer", "Chennai Super Kings, India", "226", "162.8", "134.5", "+28.30", "#4 to #42", "+17.90"),
        ("9", "Prabhsimran Singh", "Top-Order Intent Striker", "Punjab Kings, India", "165", "175.8", "141.9", "+33.90", "#4 to #50", "+17.76"),
        ("10", "Donovan Ferreira", "Death Boundary Hitter", "Rajasthan Royals, DC, SA", "141", "158.2", "127.0", "+31.12", "#5 to #60", "+15.08"),
    ]
    for ri, r in enumerate(batters_data, 1):
        bg = WHITE if ri % 2 == 1 else BG_SOFT
        style_cell(t_bat.cell(ri, 0), r[0], 11.0, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 1), f"{r[1]}\n({r[2]})", 10.5, True, DARK_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_bat.cell(ri, 2), r[3], 10.5, False, BODY_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_bat.cell(ri, 3), r[4], 11.0, False, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 4), r[5], 11.5, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 5), r[6], 10.5, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 6), r[7], 11.0, True, GREEN, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 7), r[8], 10.5, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 8), r[9], 12.0, True, RR_PINK if ri <= 3 else DARK_TEXT, bg, PP_ALIGN.CENTER)

    # Bottom Container: High-Ceiling Breakout Radar
    add_box(s4, 0.60, 5.08, 12.13, 2.05, fill=WHITE, border=BORDER_LIGHT)
    add_text(s4, 0.85, 5.20, 6.0, 0.28, "DEVELOPMENTAL SCOUTING RADAR: UNDER-23 BREAKOUTS", size=12.0, bold=True, color=RR_PINK)
    add_text(s4, 7.50, 5.20, 5.0, 0.28, "Bayesian Sample Calibration Note (N <= 60 Balls)", size=11.0, bold=True, color=MUTED_TEXT, align=PP_ALIGN.RIGHT)

    # Vaibhav Box
    add_box(s4, 0.85, 5.55, 5.70, 1.40, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s4, 1.05, 5.65, 3.5, 0.28, "Vaibhav Sooryavanshi  |  Age 13", size=12.5, bold=True, color=DARK_TEXT)
    add_text(s4, 4.30, 5.65, 2.1, 0.28, "RR ACQUISITION", size=11.0, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)
    add_text(s4, 1.05, 5.95, 5.3, 0.25, "Rajasthan Royals & India U-19  •  55 Leverage Balls  •  676 Career Deliveries", size=10.5, color=MUTED_TEXT)
    add_text(s4, 1.05, 6.25, 5.3, 0.55, "Pressure SR: 234.6  |  Contextual SR Lift: +83.78\nDemonstrates generational power hitting and boundary conversion under pressure.", size=11.0, bold=True, color=DARK_TEXT)

    # Priyansh Box
    add_box(s4, 6.75, 5.55, 5.70, 1.40, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s4, 6.95, 5.65, 3.5, 0.28, "Priyansh Arya  |  Top-Order Striker", size=12.5, bold=True, color=DARK_TEXT)
    add_text(s4, 10.20, 5.65, 2.1, 0.28, "DPL BREAKOUT", size=11.0, bold=True, color=RR_NAVY, align=PP_ALIGN.RIGHT)
    add_text(s4, 6.95, 5.95, 5.3, 0.25, "Punjab Kings & Delhi  •  52 Leverage Balls  •  515 Career Deliveries", size=10.5, color=MUTED_TEXT)
    add_text(s4, 6.95, 6.25, 5.3, 0.55, "Pressure SR: 215.4  |  Contextual SR Lift: +70.33\nElite powerplay boundary aggression identified across high-leverage match phases.", size=11.0, bold=True, color=DARK_TEXT)

    # =========================================================================
    # SLIDE 5: TOP 10 BOWLERS UNDER PRESSURE
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    add_slide_title(s5, "Top 10 Bowlers Under Pressure",
                    "Senior-proven performers evaluated via Volume-Weighted Bayesian Choke Index (100% IPL-Eligible)")

    # Interactive instruction bar
    add_box(s5, 0.60, 1.15, 12.13, 0.38, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s5, 0.80, 1.22, 11.7, 0.25,
             "Interactive Feature: In the live web dashboard, clicking on any bowler row opens their Hawk-Eye pitch map and length breakdown.",
             size=11.0, bold=True, color=RR_NAVY)

    t_bowl = s5.shapes.add_table(11, 9, Inches(0.60), Inches(1.58), Inches(12.13), Inches(3.40)).table
    for ci, cw in enumerate(b_widths):
        t_bowl.columns[ci].width = Inches(cw)

    bowl_headers = ["#", "Player & Role", "Franchise / Origin", "Pressure Balls", "Pressure Econ", "Expected Econ", "Econ Diff (Δ)", "90% Rank", "Pressure Score"]
    for ci, h in enumerate(bowl_headers):
        style_cell(t_bowl.cell(0, ci), h, 11.0, True, WHITE, RR_NAVY, PP_ALIGN.LEFT if ci in (1, 2) else PP_ALIGN.CENTER)

    bowlers_data = [
        ("1", "Jasprit Bumrah", "Universal Death & All-Phase Choke", "Mumbai Indians, India", "469", "7.79", "9.18", "-1.39", "#1 to #5", "28.45"),
        ("2", "Matheesha Pathirana", "Sling-Arm Death Yorker Enforcer", "CSK, Sri Lanka", "290", "9.02", "10.95", "-1.93", "#1 to #8", "25.80"),
        ("3", "Umran Malik", "Express Middle Overs Striker", "KKR, SRH, India", "111", "7.68", "9.34", "-1.66", "#1 to #28", "24.75"),
        ("4", "Sunil Narine", "Concealed Boundary Denial", "Kolkata Knight Riders, WI", "353", "7.60", "9.15", "-1.55", "#2 to #15", "22.90"),
        ("5", "Josh Hazlewood", "Robotic Line & Hard Length Choke", "Royal Challengers Bengaluru, AUS", "399", "8.14", "8.92", "-0.78", "#3 to #18", "19.85"),
        ("6", "Mayank Yadav", "155+ km/h Hit-the-Deck Express", "Lucknow Super Giants, India", "49", "6.86", "8.88", "-2.02", "#1 to #42", "16.60"),
        ("7", "Jacob Duffy", "Powerplay Swing & Death Execution", "New Zealand (RR Priority Target)", "136", "8.07", "9.44", "-1.37", "#2 to #48", "14.16"),
        ("8", "Shoriful Islam", "Left-Arm Angles & Dipping Variations", "Bangladesh", "213", "7.94", "9.48", "-1.54", "#1 to #36", "13.95"),
        ("9", "Varun Chakravarthy", "Mystery Spin Overs 14–18 Choke", "Kolkata Knight Riders, India", "242", "7.82", "8.95", "-1.13", "#3 to #32", "13.50"),
        ("10", "Arshdeep Singh", "Left-Arm Death Yorker Specialist", "Punjab Kings, India", "385", "8.78", "9.82", "-1.04", "#4 to #45", "12.80"),
    ]
    for ri, r in enumerate(bowlers_data, 1):
        bg = WHITE if ri % 2 == 1 else BG_SOFT
        style_cell(t_bowl.cell(ri, 0), r[0], 11.0, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 1), f"{r[1]}\n({r[2]})", 10.5, True, DARK_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_bowl.cell(ri, 2), r[3], 10.5, False, BODY_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_bowl.cell(ri, 3), r[4], 11.0, False, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 4), r[5], 11.5, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 5), r[6], 10.5, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 6), r[7], 11.0, True, GREEN, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 7), r[8], 10.5, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 8), r[9], 12.0, True, RR_NAVY if ri <= 2 else DARK_TEXT, bg, PP_ALIGN.CENTER)

    # Bottom Callout Box (Big, Clear Takeaways)
    add_box(s5, 0.60, 5.08, 12.13, 2.05, fill=WHITE, border=BORDER_LIGHT)
    add_text(s5, 0.85, 5.20, 8.0, 0.28, "KEY BOWLING TAKEAWAYS & IPL ROSTER GOVERNANCE", size=12.0, bold=True, color=RR_NAVY)

    add_text(s5, 0.85, 5.50, 11.6, 0.42,
             "• 100% IPL-Eligible Talent: Non-eligible players (including Pakistani cricketers barred under BCCI policy) are excluded from actionable rankings. All ranked players are contractable for IPL franchise operations.",
             size=11.0, color=BODY_TEXT)
    add_text(s5, 0.85, 5.95, 11.6, 0.42,
             "• Jasprit Bumrah (#1) & Matheesha Pathirana (#2): Conceding 7.79 and 9.02 in death overs when baselines exceed 9.18 and 10.95 represents world-leading run suppression. Opponents actively avoid attacking Bumrah, preserving team win probability.",
             size=11.0, color=BODY_TEXT)
    add_text(s5, 0.85, 6.40, 11.6, 0.42,
             "• Jacob Duffy (#7) & Shoriful Islam (#8): Elite high-value targets under purse constraints. Duffy (+1.37 Econ lift) and Shoriful (+1.54 Econ lift) deliver premium death execution at standard base pricing.",
             size=11.0, color=BODY_TEXT)

    # =========================================================================
    # SLIDE 6: INTERACTIVE PLAYER DOSSIERS (MAXIMUM PICTURE SIZE & IMPACT)
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    add_slide_title(s6, "Interactive Player Dossiers: Delivery-Level Corridor Mapping",
                    "Clicking any player on the live dashboard opens their Hawk-Eye pitch map, 8-sector wagon wheel, and situational breakdown")

    # Left Card: Batting Dossier Feature (Wagon Wheel) - Large Image
    add_box(s6, 0.60, 1.25, 5.95, 4.35, fill=WHITE, border=BORDER_LIGHT)
    add_text(s6, 0.85, 1.38, 5.45, 0.28, "BATTING DOSSIER: 8-SECTOR WAGON WHEEL", size=13.0, bold=True, color=RR_PINK)
    add_text(s6, 0.85, 1.66, 5.45, 0.25, "Execution Corridor: Mid-Wicket & Death Arc (28%)  •  Off-Side Cover (22%)", size=11.0, color=MUTED_TEXT)
    if WAGON_WHEEL_PATH.exists():
        s6.shapes.add_picture(str(WAGON_WHEEL_PATH), Inches(0.70), Inches(1.98), width=Inches(5.75))

    # Right Card: Bowling Dossier Feature (Pitch Map) - Large Image
    add_box(s6, 6.78, 1.25, 5.95, 4.35, fill=WHITE, border=BORDER_LIGHT)
    add_text(s6, 7.03, 1.38, 5.45, 0.28, "BOWLING DOSSIER: HAWK-EYE PITCH LENGTHS", size=13.0, bold=True, color=RR_NAVY)
    add_text(s6, 7.03, 1.66, 5.45, 0.25, "Execution Corridor: Stump-to-Stump Yorker & Good Length (64%)", size=11.0, color=MUTED_TEXT)
    if PITCH_MAP_PATH.exists():
        s6.shapes.add_picture(str(PITCH_MAP_PATH), Inches(6.88), Inches(1.98), width=Inches(5.75))

    # Bottom Informational Card explaining what clicking a player does (Big, Bold)
    add_box(s6, 0.60, 5.75, 12.13, 1.45, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s6, 0.85, 5.88, 6.0, 0.28, "GRANULAR SCOUTING COVERAGE ACROSS ALL 342 CANDIDATES", size=12.0, bold=True, color=DARK_TEXT)
    add_text(s6, 7.50, 5.88, 5.0, 0.28, "Live Player Dossier Suite Enabled on Render Dashboard", size=11.0, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)

    add_text(s6, 0.85, 6.18, 11.6, 0.45,
             "• Full Delivery-Level Breakdown: Clicking any candidate row opens their standalone scouting dossier, detailing career strike rate vs. pressure strike rate, true contextual lift, and 1,000-resample bootstrap confidence intervals.\n"
             "• Visual Corridor Mapping: Batters feature 8-sector boundary distribution (6s, 4s, 1s/2s); bowlers feature 5-zone pitch lengths mapped to wicket vs. dot-ball execution.",
             size=10.5, color=BODY_TEXT)

    add_text(s6, 0.85, 6.82, 11.6, 0.32,
             "Live dossier URLs:  https://rr-dashboard.onrender.com/players/andre_russell.html   |   https://rr-dashboard.onrender.com/players/jasprit_bumrah.html",
             size=11.0, bold=True, color=RR_NAVY)

    # =========================================================================
    # SLIDE 7: PRE-AUCTION TRADE WINDOW & TRADE-OFF STRATEGY
    # =========================================================================
    s7 = prs.slides.add_slide(blank)
    add_slide_title(s7, "Pre-Auction Trade Window & Trade-Off Architecture",
                    "Purse conservation and trade strategies following Rajasthan Royals' 6-player core retention")

    # Retained Core Summary Banner
    add_box(s7, 0.60, 1.25, 12.13, 0.58, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s7, 0.85, 1.35, 7.5, 0.28,
             "Retained Core (6 Players • ₹79.0 Cr): Samson (₹18 Cr), Jaiswal (₹18 Cr), Parag (₹14 Cr), Jurel (₹14 Cr), Hetmyer (₹11 Cr), Sandeep (₹4 Cr)",
             size=11.0, bold=True, color=DARK_TEXT)
    add_text(s7, 8.50, 1.35, 4.0, 0.28,
             "Active Auction Purse: ₹41.0–45.0 Cr", size=11.5, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)

    # 3 Strategic Trade-Off Boxes - Big, Clear Text
    to_boxes = [
        ("TRADE-OFF 1: SPIN CHOKE VS DEATH SEAM",
         "Middle-Spin Enforcer Allocation (₹17.5 Cr)",
         "Rather than overpaying for inflated marquee seamers, allocating ₹17.5 Cr to domestic spin enforcers (Shivam Dube ₹9.5 Cr, Axar Patel ₹8.0 Cr) neutralizes overs 7–15 while reserving ₹11.0 Cr for disciplined pace buys (Jacob Duffy, Josh Hazlewood).",
         AMBER),
        ("TRADE-OFF 2: BLOCKBUSTER TRADE ARBITRAGE",
         "Mohammed Shami (LSG -> RR) • Traded for Sam Curran",
         "Trading Sam Curran to LSG delivers premier Indian seam spearhead Mohammed Shami (and M Siddharth) directly into RR's starting pace attack. This fixes RR's frontline Indian seam without purse spending, frees up a critical overseas slot for batting power, and insulates the purse.",
         GREEN),
        ("TRADE-OFF 3: JAIPUR SMS FORTRESS FIT",
         "Boundary Denial Over Flat-Track Power",
         "Sawai Mansingh Stadium has expansive 75m+ boundaries where flat-track power hitters struggle. Prioritizing boundary-suppression seamers (Duffy +1.37 lift, Yash Dayal 8.42 Econ) directly exploits Jaipur's large outfield conditions.",
         RR_NAVY),
    ]
    tox = 0.60
    tow = 3.90
    for htop, hmain, hbody, hcol in to_boxes:
        add_box(s7, tox, 1.95, tow, 2.45, fill=WHITE, border=BORDER_LIGHT)
        add_text(s7, tox + 0.15, 2.08, tow - 0.30, 0.24, htop, size=10.5, bold=True, color=hcol)
        add_text(s7, tox + 0.15, 2.34, tow - 0.30, 0.38, hmain, size=12.0, bold=True, color=DARK_TEXT)
        add_text(s7, tox + 0.15, 2.76, tow - 0.30, 1.55, hbody, size=10.5, color=BODY_TEXT)
        tox += tow + 0.21

    # Evaluation Matrix Table (Bigger rows & font)
    add_text(s7, 0.60, 4.52, 6.0, 0.28, "PRE-AUCTION TRADE-OFF EVALUATION MATRIX", size=12.0, bold=True, color=RR_NAVY)

    t_to = s7.shapes.add_table(6, 5, Inches(0.60), Inches(4.75), Inches(12.13), Inches(2.45)).table
    to_widths = [2.00, 1.80, 1.30, 5.43, 1.60]
    for ci, cw in enumerate(to_widths):
        t_to.columns[ci].width = Inches(cw)

    to_headers = ["Strategic Target / Asset", "Acquisition Route", "Target Value", "Tactical Justification", "Purse Impact"]
    for ci, h in enumerate(to_headers):
        style_cell(t_to.cell(0, ci), h, 10.5, True, WHITE, RR_NAVY, PP_ALIGN.LEFT if ci in (0, 3) else PP_ALIGN.CENTER)

    to_data = [
        ("Mohammed Shami", "Blockbuster Trade (LSG -> RR)", "Swap (Sam Curran)", "Frontline Indian seam spearhead (Purple Cap, 8.32 Econ); frees overseas slot and brings spinner M Siddharth.", "Overseas Slot Freed"),
        ("Donovan Ferreira", "Completed Trade (DC -> RR)", "₹1.00 Cr", "Locks in Top-10 pressure batter (+15.08 RAE) at base cost; eliminates need for expensive overseas finisher bidding.", "+₹8.0 Cr Saved"),
        ("Shivam Dube", "Auction Priority 1", "₹9.50 Cr", "Designated middle-overs spin enforcer (162.8 SR); prevents scoring slowdowns between overs 7–15.", "21.1% Purse"),
        ("Jacob Duffy", "Auction Priority 1", "₹6.50 Cr", "Top-5 composite bowler (+14.16 score, 17 pressure wkts); elite powerplay swing and death execution.", "High Value Choke"),
        ("Axar Patel", "Auction Priority 1", "₹8.00 Cr", "Provides batting depth at No. 7 (+7.15 RAE) and 4 tight overs of left-arm orthodox spin calibrated for Jaipur.", "17.8% Purse"),
    ]
    for ri, r in enumerate(to_data, 1):
        bg = WHITE if ri % 2 == 1 else BG_SOFT
        style_cell(t_to.cell(ri, 0), r[0], 11.0, True, DARK_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_to.cell(ri, 1), r[1], 10.5, False, GREEN if "Trade" in r[1] else DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_to.cell(ri, 2), r[2], 11.0, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_to.cell(ri, 3), r[3], 10.5, False, BODY_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_to.cell(ri, 4), r[4], 11.0, True, GREEN if "+" in r[4] else DARK_TEXT, bg, PP_ALIGN.CENTER)

    # =========================================================================
    # SLIDE 8: PRESSURE LIFT QUADRANT SCATTER PLOT
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    add_slide_title(s8, "Pressure Lift Alpha Matrix & Quadrant Classification",
                    "Plotting Bayesian Pressure Rating Score against Contextual Performance Lift (SR / Econ Equivalent)")

    if QUAD_PATH.exists():
        s8.shapes.add_picture(str(QUAD_PATH), Inches(0.60), Inches(1.20), width=Inches(7.30), height=Inches(5.15))

    q_x = 8.10
    q_w = 4.63

    add_box(s8, q_x, 1.20, q_w, 1.35, fill=WHITE, border=BORDER_LIGHT)
    add_text(s8, q_x + 0.15, 1.28, q_w - 0.3, 0.24, "QUADRANT I • ELITE MATCH-WINNERS", size=11.5, bold=True, color=GREEN)
    add_text(s8, q_x + 0.15, 1.55, q_w - 0.3, 0.95,
             "• Andre Russell (+26.59 RAE, 165.6 SR, +38.94 Lift)\n• Jasprit Bumrah (28.45 Score, 7.79 Econ Choke)\n• Matheesha Pathirana (25.80 Score, 9.02 Death Econ)\n• Umran Malik (24.75 Score, 14 Wkts, 7.68 Econ)",
             size=10.5, color=DARK_TEXT)

    add_box(s8, q_x, 2.65, q_w, 1.35, fill=WHITE, border=BORDER_LIGHT)
    add_text(s8, q_x + 0.15, 2.73, q_w - 0.3, 0.24, "QUADRANT II • HIGH-CEILING BREAKOUTS", size=11.5, bold=True, color=AMBER)
    add_text(s8, q_x + 0.15, 3.00, q_w - 0.3, 0.95,
             "• Vaibhav Sooryavanshi (234.6 SR under pressure, +83.78 Lift)\n• Priyansh Arya (215.4 SR under pressure, +70.33 Lift)\n• Mayank Yadav (6.86 Econ, 155+ km/h Express Pace)\n• Jacob Duffy (+14.16 Score, +1.37 Econ Lift)",
             size=10.5, color=DARK_TEXT)

    add_box(s8, q_x, 4.10, q_w, 1.35, fill=WHITE, border=BORDER_LIGHT)
    add_text(s8, q_x + 0.15, 4.18, q_w - 0.3, 0.24, "QUADRANT III • SITUATIONAL IMPACT BUYS", size=11.5, bold=True, color=MUTED_TEXT)
    add_text(s8, q_x + 0.15, 4.45, q_w - 0.3, 0.95,
             "• Donovan Ferreira (+15.08 RAE, 158.2 SR, Base Trade Asset)\n• Varun Chakravarthy (13.50 Score, 7.82 Econ Mystery Spin)\n• Arshdeep Singh (12.80 Score, 25 Wkts, Left-Arm Seam)",
             size=10.5, color=DARK_TEXT)

    add_box(s8, q_x, 5.55, q_w, 1.35, fill=WHITE, border=BORDER_LIGHT)
    add_text(s8, q_x + 0.15, 5.63, q_w - 0.3, 0.24, "QUADRANT IV • DISCIPLINED CHOKE SPECIALISTS", size=11.5, bold=True, color=RR_NAVY)
    add_text(s8, q_x + 0.15, 5.90, q_w - 0.3, 0.95,
             "• Heinrich Klaasen (+24.15 RAE, 487 Pressure Balls)\n• Glenn Maxwell (+22.45 RAE, 164.1 SR)\n• Suryakumar Yadav (+21.80 RAE, 682 Pressure Balls)\n• Tim David (+20.11 RAE) & Shivam Dube (+17.90 RAE)",
             size=10.5, color=DARK_TEXT)

    add_box(s8, 0.60, 6.45, 7.30, 0.55, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s8, 0.75, 6.52, 7.00, 0.40,
             "Key Insight: High pressure lift (Y-axis) separates true individual match-winners from players benefiting from dominant top orders or easy low-leverage overs.",
             size=10.5, color=BODY_TEXT)

    # =========================================================================
    # SLIDE 9: RECOMMENDED 2027 PLAYING XI (CAPTAIN RIYAN PARAG)
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    add_slide_title(s9, "Rajasthan Royals — Recommended 2027 Playing XI",
                    "A balanced 11-man lineup calibrated to dominate middle-overs spin and close out death overs under pressure")

    xi_groups = [
        ("TOP-ORDER ANCHORS (OVERS 1–6)", [
            ("1", "Yashasvi Jaiswal", "RETAINED CORE", "Left-Hand Explosive Opener • Powerplay Strike Rate 165+"),
            ("2", "Devon Conway", "AUCTION TARGET", "LHB Top-Order Anchor & Wicketkeeper • Pressure RAE +11.89"),
            ("3", "Sanju Samson", "RETAINED CORE", "Wicketkeeper & No. 3 Pace/Spin Attacker • Proven Match-Winner"),
        ]),
        ("MIDDLE-OVERS ENGINE & SPIN ENFORCERS (OVERS 7–15)", [
            ("4", "Shivam Dube", "AUCTION TARGET", "Designated Spin Enforcer • Shrunk RAE +11.54 (162.8 SR in middle overs)"),
            ("5", "Riyan Parag (C)", "RETAINED CORE", "Captain & Middle-Order Striker • SMS Fortress Tactical Anchor"),
            ("6", "Dhruv Jurel (WK)", "RETAINED CORE", "Clutch Middle-Order Finisher • Elite Death-Over Composure"),
        ]),
        ("DEATH-OVERS POWER FINISHERS (OVERS 16–20)", [
            ("7", "Rinku Singh", "AUCTION TARGET", "Specialist Death Finisher • Shrunk RAE +9.52 (168.4 SR under pressure)"),
            ("8", "Shimron Hetmyer", "RETAINED CORE", "Overseas Power Finisher • Fearless Boundary Striking in Final Overs"),
        ]),
        ("BOWLING SPEARHEADS & SEAM DEFENSE", [
            ("9", "Mohammed Shami", "TRADED ASSET (LSG -> RR)", "Frontline Indian Seam Spearhead • Upright Seam & Powerplay Breakthroughs (Traded for Curran)"),
            ("10", "Sandeep Sharma", "RETAINED CORE", "Death Yorker & Wide-Line Specialist • Reliable Death Execution"),
            ("11", "Yash Dayal", "AUCTION TARGET", "Left-Arm Seam Specialist • High-Leverage Economy 8.42 (-1.15 Econ Lift)"),
        ]),
    ]

    coords = [(0.60, 1.25), (6.78, 1.25), (0.60, 3.65), (6.78, 3.65)]
    gw = 5.95

    for idx, (gtitle, gplayers) in enumerate(xi_groups):
        cx, cy = coords[idx]
        ch = 2.25 if idx < 2 else 2.15
        add_box(s9, cx, cy, gw, ch, fill=WHITE, border=BORDER_LIGHT)
        add_text(s9, cx + 0.20, cy + 0.12, gw - 0.40, 0.24, gtitle, size=11.5, bold=True, color=RR_NAVY)

        py = cy + 0.40
        for pnum, pname, ptag, pdesc in gplayers:
            add_box(s9, cx + 0.20, py, gw - 0.40, 0.52, fill=BG_SOFT, border=BORDER_LIGHT)
            add_text(s9, cx + 0.30, py + 0.08, 0.28, 0.35, pnum, size=12.0, bold=True, color=DARK_TEXT)
            add_text(s9, cx + 0.65, py + 0.06, 3.2, 0.24, pname, size=12.0, bold=True, color=DARK_TEXT)
            tag_col = GREEN if "RETAINED" in ptag else RR_PINK
            add_text(s9, cx + 3.80, py + 0.06, 1.9, 0.24, ptag, size=10.5, bold=True, color=tag_col, align=PP_ALIGN.RIGHT)
            add_text(s9, cx + 0.65, py + 0.28, 5.1, 0.22, pdesc, size=10.0, color=MUTED_TEXT)
            py += 0.56

    # Bottom Impact Substitutes Box
    add_box(s9, 0.60, 6.00, 12.13, 1.10, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s9, 0.85, 6.12, 11.6, 0.24, "TACTICAL IMPACT SUBSTITUTES & MATCHUP COVERS:", size=11.5, bold=True, color=RR_NAVY)
    subs = [
        "Josh Hazlewood (Overseas Seam • Composite +12.27)",
        "Jacob Duffy (Pace • Composite Score +14.16)",
        "M Siddharth (Traded Spin Asset • Left-Arm Orthodox)",
        "Axar Patel (Spin All-Rounder • Shrunk RAE +7.15)",
    ]
    sx = 0.85
    for s in subs:
        add_box(s9, sx, 6.42, 2.75, 0.52, fill=WHITE, border=BORDER_LIGHT)
        add_text(s9, sx + 0.10, 6.54, 2.55, 0.30, s, size=10.5, bold=True, color=DARK_TEXT)
        sx += 2.92

    # =========================================================================
    # SLIDE 10: AUCTION PRIORITY TARGETS TABLE
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    add_slide_title(s10, "Auction Priority Targets Evaluation",
                    "Evaluation of calibrated targets across career rate, pressure rate, and pressure lift")

    t_auc = s10.shapes.add_table(11, 6, Inches(0.60), Inches(1.25), Inches(12.13), Inches(5.65)).table
    auc_widths = [0.50, 2.50, 3.43, 1.80, 1.90, 2.00]
    for ci, cw in enumerate(auc_widths):
        t_auc.columns[ci].width = Inches(cw)

    auc_headers = ["#", "Player", "Role in Team", "Career Rate", "Pressure Rate", "Lift (Δ) / Score"]
    for ci, h in enumerate(auc_headers):
        style_cell(t_auc.cell(0, ci), h, 11.5, True, WHITE, RR_NAVY, PP_ALIGN.LEFT if ci in (1, 2) else PP_ALIGN.CENTER)

    auc_data = [
        ("1", "Devon Conway (wk)", "Top-Order Anchor & Wicketkeeper", "134.2 SR", "148.5 SR", "+14.3 SR  (+11.89)"),
        ("2", "Ruturaj Gaikwad", "Opening Batter & Inning Pacer", "137.5 SR", "145.2 SR", "+7.7 SR  (+6.84)"),
        ("3", "Rajat Patidar", "No. 3 Anchor & Spin Attacker", "142.1 SR", "158.4 SR", "+16.3 SR  (+10.64)"),
        ("4", "Shivam Dube", "Middle-Overs Spin Enforcer (Overs 7–15)", "149.2 SR", "162.8 SR", "+13.6 SR  (+11.54)"),
        ("5", "Shreyas Iyer (c)", "Middle-Order Game Manager & Captain", "132.8 SR", "135.4 SR", "+2.6 SR  (+3.42)"),
        ("6", "Rinku Singh", "Designated Death Finisher (Overs 16–20)", "148.0 SR", "168.4 SR", "+20.4 SR  (+9.52)"),
        ("7", "Axar Patel", "Spin All-Rounder & Death Hitter", "135.6 SR", "146.2 SR", "+10.6 SR  (+7.15)"),
        ("8", "Josh Hazlewood", "Powerplay & Death Seam Choke Bowler", "7.62 Econ", "8.14 Econ", "+0.88 Econ  (+12.27)"),
        ("9", "Yash Dayal", "Left-Arm Death Overs Seam Enforcer", "8.85 Econ", "8.42 Econ", "+1.15 Econ  (+8.14)"),
        ("10", "Jacob Duffy", "Powerplay Swing & High-Leverage Enforcer", "8.92 Econ", "8.07 Econ", "+1.37 Econ  (+14.16)"),
    ]
    for ri, r in enumerate(auc_data, 1):
        bg = WHITE if ri % 2 == 1 else BG_SOFT
        style_cell(t_auc.cell(ri, 0), r[0], 11.0, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_auc.cell(ri, 1), r[1], 11.5, True, DARK_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_auc.cell(ri, 2), r[2], 10.5, False, BODY_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_auc.cell(ri, 3), r[3], 11.0, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_auc.cell(ri, 4), r[4], 11.5, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_auc.cell(ri, 5), r[5], 11.5, True, GREEN, bg, PP_ALIGN.CENTER)

    # =========================================================================
    # SLIDE 11: AUCTION BUDGET PLAN (₹45 CRORE PURSE)
    # =========================================================================
    s11 = prs.slides.add_slide(blank)
    add_slide_title(s11, "Auction Budget Plan (₹45 Crore Total Purse)",
                    "Disciplined bidding caps to prevent emotional overspending on marquee names")

    p_kpis = [
        ("TOTAL BUDGET", "₹45.0 Cr", "Available Auction Purse", DARK_TEXT),
        ("TARGET ALLOCATIONS", "₹45.0 Cr", "Sum of Target Max Bids", DARK_TEXT),
        ("BUDGET UTILIZATION", "100%", "Completely De-risked Purse", GREEN),
    ]
    px = 0.60
    pw = 3.90
    for plbl, pval, psub, pcol in p_kpis:
        add_box(s11, px, 1.25, pw, 1.15, fill=BG_SOFT, border=BORDER_LIGHT)
        add_text(s11, px + 0.20, 1.35, pw - 0.40, 0.24, plbl, size=10.5, bold=True, color=MUTED_TEXT, align=PP_ALIGN.CENTER)
        add_text(s11, px + 0.20, 1.60, pw - 0.40, 0.45, pval, size=26.0, bold=True, color=pcol, align=PP_ALIGN.CENTER)
        add_text(s11, px + 0.20, 2.05, pw - 0.40, 0.26, psub, size=10.5, bold=True, color=BODY_TEXT, align=PP_ALIGN.CENTER)
        px += pw + 0.21

    t_bud = s11.shapes.add_table(7, 5, Inches(0.60), Inches(2.60), Inches(12.13), Inches(4.55)).table
    b_col_widths = [2.20, 1.60, 1.50, 1.30, 5.53]
    for ci, cw in enumerate(b_col_widths):
        t_bud.columns[ci].width = Inches(cw)

    bud_headers = ["Target Player", "Priority", "Max Bid", "% of Purse", "Why Rajasthan Royals Needs Him"]
    for ci, h in enumerate(bud_headers):
        style_cell(t_bud.cell(0, ci), h, 11.5, True, WHITE, RR_NAVY, PP_ALIGN.LEFT if ci in (0, 4) else PP_ALIGN.CENTER)

    bud_data = [
        ("Rinku Singh", "PRIORITY 1", "₹11.00 Cr", "24.4%", "Proven death finisher; finishes tight chases with calm execution (+20.4 SR lift). Highest clutch win rate in close matches."),
        ("Shivam Dube", "PRIORITY 1", "₹9.50 Cr", "21.1%", "Destroys spin bowling in overs 7–15; prevents scoring slowdowns in middle overs. 162.8 SR against elite spin."),
        ("Axar Patel", "PRIORITY 1", "₹8.00 Cr", "17.8%", "Gives batting depth at No. 7 and bowls tight 4 overs of left-arm orthodox spin calibrated for Jaipur conditions."),
        ("Jacob Duffy", "PRIORITY 1", "₹6.50 Cr", "14.4%", "Elite powerplay swing and death execution (+1.37 Econ lift, Composite +14.16). Premium performance at non-marquee cost."),
        ("Varun Chakravarthy", "PRIORITY 2", "₹5.50 Cr", "12.2%", "Suffocates middle-overs spin scoring (7.82 RPAE choke rate). Provides crucial mystery spin variation."),
        ("Romario Shepherd", "PRIORITY 2", "₹4.50 Cr", "10.0%", "Fast bowling option with heavy ball and power-hitting down the order. Solid overseas backup at base valuation."),
    ]
    for ri, r in enumerate(bud_data, 1):
        bg = WHITE if ri % 2 == 1 else BG_SOFT
        style_cell(t_bud.cell(ri, 0), r[0], 11.5, True, DARK_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_bud.cell(ri, 1), r[1], 10.5, True, RR_PINK if "1" in r[1] else DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bud.cell(ri, 2), r[2], 11.5, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bud.cell(ri, 3), r[3], 11.0, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bud.cell(ri, 4), r[4], 10.5, False, BODY_TEXT, bg, PP_ALIGN.LEFT)

    # =========================================================================
    # SLIDE 12: WAR ROOM BIDDING RULES & CONTINGENCY MATRIX
    # =========================================================================
    s12 = prs.slides.add_slide(blank)
    add_slide_title(s12, "War Room Bidding Rules & Contingency Matrix",
                    "Real-time step-down protocols to maintain budget integrity during live auction bidding")

    # Left Column: Bidding Rules & Contingency Triggers
    add_box(s12, 0.60, 1.25, 5.95, 5.85, fill=WHITE, border=BORDER_LIGHT)
    add_text(s12, 0.85, 1.45, 5.45, 0.28, "AUCTION BIDDING RULE (10% CIRCUIT BREAKER)", size=12.5, bold=True, color=RR_NAVY)
    add_text(s12, 0.85, 1.78, 5.45, 0.65,
             "If bidding for any player goes more than 10% above their maximum limit, stop bidding immediately and switch to backup targets to protect the overall team budget.",
             size=11.0, color=BODY_TEXT)

    add_text(s12, 0.85, 2.50, 5.45, 0.28, "CONTINGENCY BIDDING MATRIX (LIVE STEP-DOWNS)", size=12.5, bold=True, color=RR_NAVY)

    triggers = [
        ("If Rinku Singh > ₹11.0 Cr:", "Pivot immediately to Bhanuka Rajapaksa (₹3.5 Cr) and promote Shimron Hetmyer to No. 6, freeing ₹7.5 Cr for the bowling reserve.", RR_PINK),
        ("If Shivam Dube > ₹9.5 Cr:", "Switch to Rajat Patidar (₹7.0 Cr) for spin boundary execution, reallocating ₹2.5 Cr to the overseas pace budget.", RR_NAVY),
        ("If Josh Hazlewood > ₹9.5 Cr:", "Lock Jacob Duffy (₹6.5 Cr) as primary overseas seamer and secure Yash Dayal (₹4.5 Cr) for domestic seam depth.", GREEN),
        ("If Axar Patel > ₹8.0 Cr:", "Pivot to Varun Chakravarthy (₹5.5 Cr) plus a domestic all-rounder backup to secure middle-overs spin choke.", AMBER),
    ]
    ty = 2.85
    for thdr, tbody, tcol in triggers:
        add_box(s12, 0.85, ty, 5.45, 0.90, fill=BG_SOFT, border=BORDER_LIGHT)
        add_box(s12, 0.85, ty, 0.10, 0.90, fill=tcol, border=None)
        add_text(s12, 1.05, ty + 0.10, 5.15, 0.24, thdr, size=11.5, bold=True, color=DARK_TEXT)
        add_text(s12, 1.05, ty + 0.36, 5.15, 0.50, tbody, size=10.5, color=BODY_TEXT)
        ty += 1.00

    # Right Column: Phase Distribution & Principles
    add_box(s12, 6.78, 1.25, 5.95, 5.85, fill=WHITE, border=BORDER_LIGHT)
    add_text(s12, 7.03, 1.45, 5.45, 0.28, "PHASE-BY-PHASE PURSE DISTRIBUTION (₹45.0 CR TOTAL)", size=12.5, bold=True, color=RR_NAVY)

    phases = [
        ("MIDDLE SPIN ATTACK", "₹17.50 Cr", "38.9%", "Shivam Dube (₹9.5 Cr) + Axar Patel (₹8.0 Cr)"),
        ("DEATH FINISHING", "₹11.00 Cr", "24.4%", "Rinku Singh (₹11.0 Cr - Priority 1)"),
        ("PACE SPEARHEADS", "₹11.00 Cr", "24.4%", "Jacob Duffy (₹6.5 Cr) + Romario Shepherd (₹4.5 Cr)"),
        ("MYSTERY SPIN CHOKE", "₹5.50 Cr", "12.2%", "Varun Chakravarthy (₹5.5 Cr - Priority 2)"),
    ]
    pyx = 7.03
    pyy = 1.80
    for ptitle, pval, ppct, pdesc in phases:
        add_box(s12, pyx, pyy, 2.62, 0.98, fill=BG_SOFT, border=BORDER_LIGHT)
        add_text(s12, pyx + 0.12, pyy + 0.08, 2.38, 0.22, ptitle, size=10.0, bold=True, color=MUTED_TEXT)
        add_text(s12, pyx + 0.12, pyy + 0.30, 1.50, 0.35, pval, size=16.0, bold=True, color=DARK_TEXT)
        add_text(s12, pyx + 1.62, pyy + 0.35, 0.88, 0.24, ppct, size=11.5, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)
        add_text(s12, pyx + 0.12, pyy + 0.66, 2.38, 0.26, pdesc, size=10.0, color=BODY_TEXT)
        if pyx == 7.03:
            pyx = 9.86
        else:
            pyx = 7.03
            pyy += 1.08

    add_text(s12, 7.03, 4.10, 5.45, 0.28, "WAR ROOM OPERATIONAL PRINCIPLES", size=12.5, bold=True, color=RR_NAVY)
    principles = [
        ("No Emotional Marquee Bidding:", "Resist brand-driven inflation on famous names whose clutch win differential is negative."),
        ("Jaipur SMS Fortress Fit:", "Prioritize players suited to 75m+ boundaries and middle-overs spin grip over flat-track sluggers."),
        ("Strict 2+2 Overseas Structure:", "Exactly 2 overseas players in the Starting XI (Conway, Hazlewood) and 2 impact covers (Duffy, Hetmyer)."),
        ("10% Circuit Breaker:", "The instant any target exceeds 10% above max valuation, immediately execute the step-down contingency."),
    ]
    pry = 4.45
    for prtitle, prbody in principles:
        add_text(s12, 7.03, pry, 5.45, 0.22, f"• {prtitle}", size=11.0, bold=True, color=DARK_TEXT)
        add_text(s12, 7.20, pry + 0.22, 5.28, 0.35, prbody, size=10.5, color=BODY_TEXT)
        pry += 0.58

    # =========================================================================
    # SLIDE 13: STRATEGIC SUMMARY & LIVE PRODUCTION RESOURCES (NO FOOTER)
    # =========================================================================
    s13 = prs.slides.add_slide(blank)
    add_slide_title(s13, "Executive Summary & Live Production Resources",
                    "Core strategic takeaways and interactive deployment resources for Rajasthan Royals Operations")

    takeaways = [
        ("1. Delivery-Level Residuals Over Win Percentage",
         "Traditional win-rate metrics credit batters for team wins even when they contributed very little. Delivery-level RAE isolates pure individual batting and bowling impact under acute match pressure, separating authentic match-winners from passengers.",
         RR_NAVY),
        ("2. Back High-Ceiling Domestic Upside with Bayesian Care",
         "Vaibhav Sooryavanshi (+83.78 SR lift) and Priyansh Arya (+70.33 SR lift) display generational boundary power. Isolating them on a developmental radar allows Rajasthan Royals to nurture them without distorting senior playing XI benchmarks.",
         RR_PINK),
        ("3. Distinct Roles: Pure Choke vs. Express Strike",
         "Distinguishing between pure run prevention (Jasprit Bumrah: 7.79 death economy choke) and wicket impact (Umran Malik: 14 pressure wickets) provides tactical clarity. A championship attack pairs economic strangulation with express pace.",
         GREEN),
        ("4. Disciplined Capital Deployment Under ₹45 Cr Budget",
         "Resist marquee name bidding wars. Allocating ₹45.0 Cr across targeted, high-lift executors (Shivam Dube, Rinku Singh, Jacob Duffy) while leveraging pre-auction trade acquisitions (Donovan Ferreira) builds a completely balanced, championship-ready squad.",
         AMBER),
    ]

    ty = 1.25
    for tnum, tbody, tcol in takeaways:
        add_box(s13, 0.60, ty, 12.13, 1.15, fill=WHITE, border=BORDER_LIGHT)
        add_box(s13, 0.60, ty, 0.10, 1.15, fill=tcol, border=None)
        add_text(s13, 0.85, ty + 0.12, 11.5, 0.28, tnum, size=12.5, bold=True, color=DARK_TEXT)
        add_text(s13, 0.85, ty + 0.42, 11.5, 0.68, tbody, size=11.0, color=BODY_TEXT)
        ty += 1.25

    # Dedicated Production Resources Container (Big URLs, bold text, no footer bar)
    add_box(s13, 0.60, 6.30, 5.95, 0.98, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s13, 0.80, 6.38, 5.5, 0.22, "LIVE WEB DASHBOARD & DOSSIER SUITE:", size=11.0, bold=True, color=RR_NAVY)
    add_text(s13, 0.80, 6.62, 5.5, 0.30, "https://rr-dashboard.onrender.com/", size=13.5, bold=True, color=RR_PINK)
    add_text(s13, 0.80, 6.94, 5.5, 0.28, "Full 342-player dossiers, interactive wagon wheels & live war room", size=10.0, color=MUTED_TEXT)

    add_box(s13, 6.78, 6.30, 5.95, 0.98, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s13, 6.98, 6.38, 5.5, 0.22, "OPEN-SOURCE CODEBASE & REPLICATION:", size=11.0, bold=True, color=RR_NAVY)
    add_text(s13, 6.98, 6.62, 5.5, 0.30, "https://github.com/Ketanrawat2004/RR-Dashboard", size=13.5, bold=True, color=DARK_TEXT)
    add_text(s13, 6.98, 6.94, 5.5, 0.28, "Complete pipeline scripts, bootstrap models & automated documentation", size=10.0, color=MUTED_TEXT)

    prs.save(str(OUT_OVERHAUL))
    print(f"Saved PPTX to: {OUT_OVERHAUL}")

    prs.save(str(OUT_COPY))
    print(f"Saved PPTX copy to: {OUT_COPY}")

    try:
        prs.save(str(OUT_MAIN))
        print(f"Saved PPTX to: {OUT_MAIN}")
    except PermissionError:
        print(f"Notice: {OUT_MAIN} is currently locked by a viewer. Saved to {OUT_OVERHAUL} and {OUT_COPY}.")

if __name__ == "__main__":
    build_grand_deck()
