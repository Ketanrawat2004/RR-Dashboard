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
OUT_COPY = BASE_DIR / "pressure_output" / "RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx"

# Clean Professional Palette - Minimalist & Crisp (No over-colouring)
WHITE = RGBColor(255, 255, 255)
BG_SOFT = RGBColor(248, 250, 252)
BORDER_LIGHT = RGBColor(226, 232, 240)
DARK_TEXT = RGBColor(15, 23, 42)
BODY_TEXT = RGBColor(51, 65, 85)
MUTED_TEXT = RGBColor(100, 116, 139)
RR_NAVY = RGBColor(0, 29, 72)
RR_PINK = RGBColor(235, 26, 141)
GREEN = RGBColor(5, 150, 105)
RED = RGBColor(220, 38, 38)
AMBER = RGBColor(180, 83, 9)

FONT_MAIN = "Calibri"

def set_cell_border(cell, color_hex="E2E8F0", width_pt="6350"):
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

def style_cell(cell, text, font_size=8.5, bold=False, color=BODY_TEXT, fill=None, align=PP_ALIGN.LEFT, margins=(0.06, 0.06, 0.03, 0.03)):
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
        slide.shapes.add_picture(str(LOGO_PATH), Inches(12.35), Inches(0.25), height=Inches(0.75))

def add_slide_title(slide, title, subtitle=None):
    add_corner_logo(slide)
    tb = slide.shapes.add_textbox(Inches(0.60), Inches(0.30), Inches(11.4), Inches(0.75))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_MAIN
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = MUTED_TEXT
        p2.space_before = Pt(3)

def add_box(slide, left, top, width, height, fill=BG_SOFT, border=BORDER_LIGHT, line_w=0.75):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if border is not None:
        shp.line.color.rgb = border
        shp.line.width = Pt(line_w)
    else:
        shp.line.fill.background()
    return shp

def add_text(slide, left, top, width, height, text, size=10.0, bold=False, color=BODY_TEXT, align=PP_ALIGN.LEFT):
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

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    add_corner_logo(s1)

    add_text(s1, 0.90, 1.35, 10.5, 0.35, "Rajasthan Royals  |  SupeRR Selector Season 2", size=13, bold=True, color=RR_PINK)
    add_text(s1, 0.90, 1.80, 11.2, 1.35, "Evaluating Player Performance\nUnder Match Pressure", size=36, bold=True, color=DARK_TEXT)
    add_text(s1, 0.90, 3.35, 11.0, 0.65,
             "Contextual Ball-by-Ball Leverage Engine & Empirical Bayes Rankings for IPL 2027 Roster Planning",
             size=14.5, color=BODY_TEXT)

    add_box(s1, 0.90, 4.15, 3.0, 0.03, fill=RR_NAVY, border=None)

    add_text(s1, 0.90, 4.40, 11.0, 0.35,
             "Dataset: 867 Senior T20 Fixtures (IPL & T20I, 2022–2026)  |  200,961 Deliveries  |  342 Qualified Candidates",
             size=11.0, bold=True, color=RR_NAVY)
    add_text(s1, 0.90, 4.80, 10.8, 0.30,
             "Candidate: Ketan Rawat  |  Track: Cricket Operations & Performance Analytics",
             size=11.0, color=MUTED_TEXT)

    # Prominent Live Link & GitHub Resource Cards
    add_box(s1, 0.90, 5.35, 5.40, 1.25, fill=WHITE, border=BORDER_LIGHT)
    add_text(s1, 1.10, 5.48, 5.0, 0.22, "LIVE PRODUCTION DASHBOARD", size=8.5, bold=True, color=RR_NAVY)
    add_text(s1, 1.10, 5.75, 5.0, 0.28, "https://rr-dashboard.onrender.com/", size=11.0, bold=True, color=RR_PINK)
    add_text(s1, 1.10, 6.10, 5.0, 0.35, "Interactive 342-player dossier explorer, quadrant filters & war room terminal", size=8.5, color=MUTED_TEXT)

    add_box(s1, 6.60, 5.35, 5.40, 1.25, fill=WHITE, border=BORDER_LIGHT)
    add_text(s1, 6.80, 5.48, 5.0, 0.22, "OPEN-SOURCE CODEBASE & REPRODUCIBILITY", size=8.5, bold=True, color=RR_NAVY)
    add_text(s1, 6.80, 5.75, 5.0, 0.28, "https://github.com/Ketanrawat2004/RR-Dashboard", size=11.0, bold=True, color=DARK_TEXT)
    add_text(s1, 6.80, 6.10, 5.0, 0.35, "End-to-end Python pipeline, bootstrap uncertainty models & full player dossiers", size=8.5, color=MUTED_TEXT)

    # =========================================================================
    # SLIDE 2: TOURNAMENT SAMPLE & PRESSURE DISTRIBUTION
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    add_slide_title(s2, "Tournament Sample & Pressure Delivery Distribution",
                    "Overview of 200,961 deliveries across 867 fixtures isolating high-leverage match states")

    kpis = [
        ("MATCHES EVALUATED", "867", "IPL & T20I (2022–2026)", DARK_TEXT),
        ("DELIVERIES EVALUATED", "200,961", "Ball-by-ball records", DARK_TEXT),
        ("QUALIFIED CANDIDATES", "342", "163 Batters • 179 Bowlers", DARK_TEXT),
        ("TOP RANKED BATTER", "+26.59", "Andre Russell (165.6 SR)", RR_PINK),
        ("TOP RANKED BOWLER", "+24.75", "Umran Malik (14 Wkts)", RR_NAVY),
        ("PEAK LEVERAGE LIFT", "+83.78", "V. Sooryavanshi (234.6 SR)", GREEN),
    ]
    kx = 0.60
    kw = 1.92
    for lbl, num, sub, ncol in kpis:
        add_box(s2, kx, 1.25, kw, 1.20, fill=BG_SOFT, border=BORDER_LIGHT)
        add_text(s2, kx + 0.10, 1.35, kw - 0.20, 0.22, lbl, size=8.0, bold=True, color=MUTED_TEXT, align=PP_ALIGN.CENTER)
        add_text(s2, kx + 0.10, 1.62, kw - 0.20, 0.38, num, size=19, bold=True, color=ncol, align=PP_ALIGN.CENTER)
        add_text(s2, kx + 0.10, 2.06, kw - 0.20, 0.25, sub, size=8.0, color=BODY_TEXT, align=PP_ALIGN.CENTER)
        kx += kw + 0.12

    # Panel 1: Pressure Distribution Donut
    add_box(s2, 0.60, 2.65, 3.85, 4.35, fill=WHITE, border=BORDER_LIGHT)
    add_text(s2, 0.80, 2.80, 3.45, 0.28, "PRESSURE DELIVERY DISTRIBUTION", size=10.0, bold=True, color=RR_NAVY)
    if DONUT_PATH.exists():
        s2.shapes.add_picture(str(DONUT_PATH), Inches(1.35), Inches(3.20), width=Inches(2.35))
    dist_rows = [
        ("Death Overs (16–20)", "42%", RR_PINK),
        ("Chases Requiring RRR >= 9.0", "38%", DARK_TEXT),
        ("Top-Order Collapse Phases", "20%", GREEN),
    ]
    dy = 5.75
    for dlabel, dval, dcol in dist_rows:
        add_box(s2, 0.85, dy + 0.04, 0.13, 0.13, fill=dcol, border=None)
        add_text(s2, 1.05, dy, 2.6, 0.22, dlabel, size=9.0, color=BODY_TEXT)
        add_text(s2, 3.65, dy, 0.6, 0.22, dval, size=9.0, bold=True, color=DARK_TEXT, align=PP_ALIGN.RIGHT)
        dy += 0.32

    # Panel 2: Top Batting Pressure Lifts
    add_box(s2, 4.65, 2.65, 3.85, 4.35, fill=WHITE, border=BORDER_LIGHT)
    add_text(s2, 4.85, 2.80, 3.45, 0.28, "TOP BATTING PRESSURE LIFTS (SR Δ)", size=10.0, bold=True, color=RR_NAVY)
    add_text(s2, 4.85, 3.10, 3.45, 0.25, "True strike rate boost above contextual baseline:", size=9.0, color=MUTED_TEXT)
    lifts = [
        ("1. Vaibhav Sooryavanshi", "+83.78", 83.78),
        ("2. Priyansh Arya", "+70.34", 70.34),
        ("3. Andre Russell", "+38.94", 38.94),
        ("4. Prabhsimran Singh", "+33.90", 33.90),
        ("5. Glenn Maxwell", "+33.14", 33.14),
    ]
    ly = 3.50
    for lname, lval, lpct in lifts:
        add_text(s2, 4.85, ly, 2.5, 0.22, lname, size=9.5, bold=True, color=DARK_TEXT)
        add_text(s2, 7.35, ly, 0.95, 0.22, lval, size=9.5, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)
        add_box(s2, 4.85, ly + 0.26, 3.45, 0.08, fill=BORDER_LIGHT, border=None)
        add_box(s2, 4.85, ly + 0.26, 3.45 * (lpct / 88.0), 0.08, fill=GREEN, border=None)
        ly += 0.58

    # Panel 3: Leverage Situation Performance Matrix
    add_box(s2, 8.70, 2.65, 4.03, 4.35, fill=WHITE, border=BORDER_LIGHT)
    add_text(s2, 8.90, 2.80, 3.63, 0.28, "LEVERAGE SITUATION PERFORMANCE MATRIX", size=10.0, bold=True, color=RR_NAVY)
    add_text(s2, 8.90, 3.10, 3.63, 0.25, "Contextual performance across key high-pressure match phases:", size=9.0, color=MUTED_TEXT)

    t_mat = s2.shapes.add_table(4, 5, Inches(8.85), Inches(3.60), Inches(3.73), Inches(2.30)).table
    mat_widths = [1.25, 0.62, 0.62, 0.62, 0.62]
    for ci, cw in enumerate(mat_widths):
        t_mat.columns[ci].width = Inches(cw)
    m_headers = ["Phase", "Death", "RRR >= 10", "Playoffs", "Super Over"]
    for ci, h in enumerate(m_headers):
        style_cell(t_mat.cell(0, ci), h, 8.5, True, WHITE, RR_NAVY, PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER)
    m_rows = [
        ("Top 10 Batters (SR)", "186.2", "181.5", "172.4", "210.0", GREEN),
        ("Top 10 Bowlers (Econ)", "7.64", "7.92", "7.31", "6.00", GREEN),
        ("Peer Baseline", "136.4 / 9.85", "139.1 / 10.4", "130.2 / 9.60", "145.0 / 11.2", RED),
    ]
    for ri, row in enumerate(m_rows, 1):
        style_cell(t_mat.cell(ri, 0), row[0], 8.0, True, DARK_TEXT, BG_SOFT if ri == 3 else WHITE, PP_ALIGN.LEFT)
        for ci in range(1, 5):
            style_cell(t_mat.cell(ri, ci), row[ci], 8.0, True, row[5], BG_SOFT if ri == 3 else WHITE, PP_ALIGN.CENTER)

    add_text(s2, 8.90, 6.25, 3.63, 0.55,
             "Top-ranked performers score 45–65 runs/100 balls faster than peers and concede over 2 runs/over fewer at the death.",
             size=9.0, color=BODY_TEXT)

    # =========================================================================
    # SLIDE 3: EVALUATION METHOD & DATA GOVERNANCE
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    add_slide_title(s3, "Evaluation Methodology & Thought Process",
                    "A delivery-level baseline isolating individual clutch execution from team outcomes")

    # Left Column: Method & Formulation
    add_box(s3, 0.60, 1.25, 5.95, 5.75, fill=WHITE, border=BORDER_LIGHT)
    add_text(s3, 0.85, 1.45, 5.45, 0.30, "QUANTITATIVE MODEL FORMULATION", size=11.0, bold=True, color=RR_NAVY)

    add_text(s3, 0.85, 1.85, 5.45, 0.65,
             "We isolate each delivery against contextual expectations rather than using uncontextualized averages. Expected runs are modeled per delivery using match-clustered cross-validation across 200,961 balls.",
             size=9.5, color=BODY_TEXT)

    add_box(s3, 0.85, 2.65, 5.45, 0.65, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s3, 0.95, 2.75, 5.25, 0.45,
             "Batting Shrunk RAE = [ N_press / (N_press + 150) ] * Raw_RAE + [ 150 / (N_press + 150) ] * Mean",
             size=8.5, bold=True, color=DARK_TEXT)

    add_box(s3, 0.85, 3.45, 5.45, 0.50, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s3, 0.95, 3.55, 5.25, 0.35,
             "Bowling Composite = 0.60 * Shrunk_RPAE + 0.40 * (Shrunk_WAE * 12.0)",
             size=8.5, bold=True, color=DARK_TEXT)

    add_text(s3, 0.85, 4.15, 5.45, 0.30, "OPERATIONAL DEFINITIONS & GOVERNANCE", size=10.5, bold=True, color=RR_NAVY)

    gov_points = [
        ("1. Pre-Delivery Pressure Engine:", "Defines pressure strictly before the ball is bowled: Death overs (16–20), chases requiring RRR >= 9.0 or balls <= 30, and top-order powerplay collapses."),
        ("2. Context-Conditioned Baseline:", "Calculates expected runs based on pitch phase, wickets in hand, and required rate, preventing cross-match leakage."),
        ("3. Uncertainty Quantification:", "Match-clustered bootstrap (1,000 resamples) accounts for match correlation to produce verified 90% rank intervals."),
    ]
    gy = 4.50
    for gtitle, gbody in gov_points:
        add_text(s3, 0.85, gy, 5.45, 0.20, gtitle, size=9.0, bold=True, color=DARK_TEXT)
        add_text(s3, 0.85, gy + 0.20, 5.45, 0.45, gbody, size=8.5, color=BODY_TEXT)
        gy += 0.72

    # Right Column: Thought Process & Cricket Realities
    add_box(s3, 6.78, 1.25, 5.95, 5.75, fill=WHITE, border=BORDER_LIGHT)
    add_text(s3, 7.03, 1.45, 5.45, 0.30, "CRICKET OPERATIONS THOUGHT PROCESS", size=11.0, bold=True, color=RR_NAVY)

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
        add_text(s3, 7.03, ty, 5.45, 0.22, ttitle, size=9.5, bold=True, color=RR_NAVY)
        add_text(s3, 7.03, ty + 0.24, 5.45, 0.65, tbody, size=8.5, color=BODY_TEXT)
        ty += 1.15

    # =========================================================================
    # SLIDE 4: TOP 10 BATTERS UNDER PRESSURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    add_slide_title(s4, "Top 10 Batters Under Pressure",
                    "Senior-proven performers ranked by Shrunk Runs Above Expectation (RAE) with domestic breakout radar")

    # Interactive instruction bar
    add_box(s4, 0.60, 1.15, 12.13, 0.32, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s4, 0.75, 1.20, 11.8, 0.22,
             "Interactive Feature: In the live web dashboard (index.html), clicking on any player row or 'View Wagon Wheel' navigates to their detailed review dossier.",
             size=8.5, bold=True, color=RR_NAVY)

    t_bat = s4.shapes.add_table(11, 10, Inches(0.60), Inches(1.52), Inches(12.13), Inches(3.35)).table
    b_widths = [0.40, 1.95, 2.30, 0.95, 0.95, 0.95, 0.95, 0.95, 1.25, 1.48]
    for ci, cw in enumerate(b_widths):
        t_bat.columns[ci].width = Inches(cw)

    b_headers = ["#", "Player & Role", "Franchise / State", "Lev. Balls", "Press. SR", "Exp. SR", "Lift (Δ)", "Career", "90% Rank", "Shrunk RAE"]
    for ci, h in enumerate(b_headers):
        style_cell(t_bat.cell(0, ci), h, 8.5, True, WHITE, RR_PINK, PP_ALIGN.LEFT if ci in (1, 2) else PP_ALIGN.CENTER)

    batters_data = [
        ("1", "Andre Russell", "Specialist High-Leverage Batter", "Kolkata Knight Riders, West Indies", "323", "165.6", "126.7", "+38.94", "733", "#1 to #12", "+26.59"),
        ("2", "Heinrich Klaasen", "Middle-Overs Spin Enforcer", "South Africa, Sunrisers Hyderabad", "487", "153.2", "129.5", "+23.65", "1417", "#1 to #15", "+24.15"),
        ("3", "Glenn Maxwell", "Middle-Overs 360° Disruption", "Australia, Punjab Kings, RCB", "315", "164.1", "131.0", "+33.14", "958", "#1 to #25", "+22.45"),
        ("4", "Suryakumar Yadav", "All-Phase Pressure Striker", "India, Mumbai Indians", "682", "150.6", "130.9", "+19.69", "2759", "#2 to #20", "+21.80"),
        ("5", "Tim David", "Death Overs Boundary Finisher", "Australia, Mumbai Indians, RCB", "505", "162.8", "136.7", "+26.08", "1226", "#2 to #28", "+20.11"),
        ("6", "Abhishek Sharma", "Powerplay Intent Striker", "India, India A, Sunrisers Hyderabad", "204", "168.1", "136.0", "+32.14", "2317", "#3 to #35", "+18.52"),
        ("7", "Rinku Singh", "Ice-Cool Death Chase Finisher", "India, Kolkata Knight Riders", "268", "168.4", "138.2", "+30.20", "1140", "#3 to #38", "+18.15"),
        ("8", "Shivam Dube", "Middle-Overs Spin Enforcer", "Chennai Super Kings, India", "226", "162.8", "134.5", "+28.30", "1385", "#4 to #42", "+17.90"),
        ("9", "Prabhsimran Singh", "Top-Order High-Intent Striker", "India, India A, Punjab Kings", "165", "175.8", "141.9", "+33.90", "1172", "#4 to #50", "+17.76"),
        ("10", "Donovan Ferreira", "Middle & Death Boundary Hitter", "Delhi Capitals, Rajasthan Royals, SA", "141", "158.2", "127.0", "+31.12", "343", "#5 to #60", "+15.08"),
    ]
    for ri, r in enumerate(batters_data, 1):
        bg = WHITE if ri % 2 == 1 else BG_SOFT
        style_cell(t_bat.cell(ri, 0), r[0], 8.5, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 1), f"{r[1]}\n({r[2]})", 8.0, True, DARK_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_bat.cell(ri, 2), r[3], 8.0, False, BODY_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_bat.cell(ri, 3), r[4], 8.5, False, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 4), r[5], 8.5, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 5), r[6], 8.0, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 6), r[7], 8.5, True, GREEN, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 7), r[8], 8.0, False, BODY_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 8), r[9], 8.0, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bat.cell(ri, 9), r[10], 9.0, True, RR_PINK if ri <= 3 else DARK_TEXT, bg, PP_ALIGN.CENTER)

    # Bottom Container: High-Ceiling Breakout Radar
    add_box(s4, 0.60, 4.95, 12.13, 2.10, fill=WHITE, border=BORDER_LIGHT)
    add_text(s4, 0.85, 5.08, 6.0, 0.25, "DEVELOPMENTAL SCOUTING RADAR: UNDER-23 DOMESTIC BREAKOUTS", size=9.5, bold=True, color=RR_PINK)
    add_text(s4, 7.50, 5.08, 5.0, 0.25, "Bayesian Sample Calibration Note (N <= 60 Deliveries)", size=8.5, bold=True, color=MUTED_TEXT, align=PP_ALIGN.RIGHT)

    add_text(s4, 0.85, 5.35, 11.6, 0.35,
             "Young prodigies with N <= 60 balls are evaluated under a separate breakout radar. While their raw strike rate lifts (+70 to +84 SR) show generational power, we track them as development assets to prevent low-sample distortions on senior leaderboards.",
             size=8.5, color=BODY_TEXT)

    # Vaibhav Box
    add_box(s4, 0.85, 5.75, 5.70, 1.15, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s4, 1.00, 5.85, 3.5, 0.25, "Vaibhav Sooryavanshi  |  Age 13", size=10.0, bold=True, color=DARK_TEXT)
    add_text(s4, 4.30, 5.85, 2.1, 0.25, "RR ACQUISITION", size=8.5, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)
    add_text(s4, 1.00, 6.10, 5.3, 0.22, "Rajasthan Royals & India U-19  •  55 Leverage Deliveries  •  676 Career Balls", size=8.5, color=MUTED_TEXT)
    add_text(s4, 1.00, 6.35, 5.3, 0.35, "Pressure SR: 234.6  |  SR Lift: +83.78  |  Historic boundary execution under tournament pressure", size=8.5, bold=True, color=DARK_TEXT)

    # Priyansh Box
    add_box(s4, 6.75, 5.75, 5.70, 1.15, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s4, 6.90, 5.85, 3.5, 0.25, "Priyansh Arya  |  Top-Order Striker", size=10.0, bold=True, color=DARK_TEXT)
    add_text(s4, 10.20, 5.85, 2.1, 0.25, "DPL BREAKOUT", size=8.5, bold=True, color=RR_NAVY, align=PP_ALIGN.RIGHT)
    add_text(s4, 6.90, 6.10, 5.3, 0.22, "Punjab Kings & Delhi  •  52 Leverage Deliveries  •  515 Career Balls", size=8.5, color=MUTED_TEXT)
    add_text(s4, 6.90, 6.35, 5.3, 0.35, "Pressure SR: 215.4  |  SR Lift: +70.33  |  Elite powerplay aggression identified in scouting pool", size=8.5, bold=True, color=DARK_TEXT)

    # =========================================================================
    # SLIDE 5: TOP 10 BOWLERS UNDER PRESSURE
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    add_slide_title(s5, "Top 10 Bowlers Under Pressure",
                    "Senior-proven performers evaluated via Volume-Weighted Bayesian Choke Index (100% IPL-Eligible)")

    # Interactive instruction bar
    add_box(s5, 0.60, 1.15, 12.13, 0.32, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s5, 0.75, 1.20, 11.8, 0.22,
             "Interactive Feature: In the live web dashboard, clicking on any bowler row or 'Dossier ->' opens their Hawk-Eye pitch map and length breakdown.",
             size=8.5, bold=True, color=RR_NAVY)

    t_bowl = s5.shapes.add_table(11, 10, Inches(0.60), Inches(1.52), Inches(12.13), Inches(3.35)).table
    for ci, cw in enumerate(b_widths):
        t_bowl.columns[ci].width = Inches(cw)

    bowl_headers = ["#", "Player & Role", "Franchise / State", "Lev. Balls", "Press. Econ", "Exp. Econ", "Econ Diff (Δ)", "Press. Wkts", "90% Rank", "Pressure Score"]
    for ci, h in enumerate(bowl_headers):
        style_cell(t_bowl.cell(0, ci), h, 8.5, True, WHITE, RR_NAVY, PP_ALIGN.LEFT if ci in (1, 2) else PP_ALIGN.CENTER)

    bowlers_data = [
        ("1", "Jasprit Bumrah", "Universal Death & All-Phase Choke", "India, Mumbai Indians", "469", "7.79", "9.18", "-1.39", "26 (+5.8)", "#1 to #5", "28.45"),
        ("2", "Matheesha Pathirana", "Sling-Arm Death Yorker Enforcer", "Chennai Super Kings, Sri Lanka", "290", "9.02", "10.95", "-1.93", "20 (+4.2)", "#1 to #8", "25.80"),
        ("3", "Umran Malik", "Express Middle Overs Striker", "India, KKR, Sunrisers Hyderabad", "111", "7.68", "9.34", "-1.66", "14 (+7.8)", "#1 to #28", "24.75"),
        ("4", "Sunil Narine", "Concealed Release Boundary Denial", "Kolkata Knight Riders, West Indies", "353", "7.60", "9.15", "-1.55", "22 (+6.1)", "#2 to #15", "22.90"),
        ("5", "Josh Hazlewood", "Robotic Line & Hard Length Choke", "Australia, Royal Challengers Bengaluru", "399", "8.14", "8.92", "-0.78", "27 (+6.7)", "#3 to #18", "19.85"),
        ("6", "Mayank Yadav", "155+ km/h Hit-the-Deck Express", "India, Lucknow Super Giants", "49", "6.86", "8.88", "-2.02", "7 (+3.8)", "#1 to #42", "16.60"),
        ("7", "Jacob Duffy", "Powerplay Swing & Death Execution", "New Zealand (RR Priority Target)", "136", "8.07", "9.44", "-1.37", "17 (+8.1)", "#2 to #48", "14.16"),
        ("8", "Shoriful Islam", "Left-Arm Angles & Dipping Slower Balls", "Bangladesh", "213", "7.94", "9.48", "-1.54", "15 (+5.2)", "#1 to #36", "13.95"),
        ("9", "Varun Chakravarthy", "Mystery Spin Overs 14–18 Choke", "India, Kolkata Knight Riders", "242", "7.82", "8.95", "-1.13", "18 (+4.9)", "#3 to #32", "13.50"),
        ("10", "Arshdeep Singh", "Left-Arm Death Yorker Specialist", "India, Punjab Kings", "385", "8.78", "9.82", "-1.04", "25 (+5.5)", "#4 to #45", "12.80"),
    ]
    for ri, r in enumerate(bowlers_data, 1):
        bg = WHITE if ri % 2 == 1 else BG_SOFT
        style_cell(t_bowl.cell(ri, 0), r[0], 8.5, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 1), f"{r[1]}\n({r[2]})", 8.0, True, DARK_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_bowl.cell(ri, 2), r[3], 8.0, False, BODY_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_bowl.cell(ri, 3), r[4], 8.5, False, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 4), r[5], 8.5, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 5), r[6], 8.0, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 6), r[7], 8.5, True, GREEN, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 7), r[8], 8.0, False, BODY_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 8), r[9], 8.0, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bowl.cell(ri, 9), r[10], 9.0, True, RR_NAVY if ri <= 2 else DARK_TEXT, bg, PP_ALIGN.CENTER)

    # Bottom Callout Box
    add_box(s5, 0.60, 4.95, 12.13, 2.10, fill=WHITE, border=BORDER_LIGHT)
    add_text(s5, 0.85, 5.08, 8.0, 0.25, "KEY BOWLING TAKEAWAYS & IPL ROSTER GOVERNANCE", size=9.5, bold=True, color=RR_NAVY)

    add_text(s5, 0.85, 5.35, 11.6, 0.40,
             "• 100% IPL-Eligible Talent: Non-eligible players (including Pakistani cricketers barred under BCCI policy) are excluded from actionable rankings. All ranked players are contractable for IPL franchise operations.",
             size=8.5, color=BODY_TEXT)
    add_text(s5, 0.85, 5.80, 11.6, 0.40,
             "• Jasprit Bumrah (#1) & Matheesha Pathirana (#2): Conceding 7.79 and 9.02 in death overs when baselines exceed 9.18 and 10.95 represents world-leading run suppression. Opponents actively avoid attacking Bumrah, preserving team win probability.",
             size=8.5, color=BODY_TEXT)
    add_text(s5, 0.85, 6.25, 11.6, 0.40,
             "• Jacob Duffy (#7) & Shoriful Islam (#8): Elite high-value targets under purse constraints. Duffy (+1.37 Econ lift) and Shoriful (+1.54 Econ lift) deliver premium death execution at standard base pricing.",
             size=8.5, color=BODY_TEXT)

    # =========================================================================
    # SLIDE 6: INTERACTIVE PLAYER DOSSIERS (NEW FEATURE SHOWCASE SLIDE)
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    add_slide_title(s6, "Interactive Player Dossiers: Delivery-Level Corridor Mapping",
                    "Clicking any player on the live dashboard opens their Hawk-Eye pitch map, 8-sector wagon wheel, and situational breakdown")

    # Left Card: Batting Dossier Feature (Wagon Wheel)
    add_box(s6, 0.60, 1.25, 5.95, 4.05, fill=WHITE, border=BORDER_LIGHT)
    add_text(s6, 0.85, 1.38, 5.45, 0.25, "BATTING PROFILE: 8-SECTOR WAGON WHEEL & CORRIDOR", size=9.5, bold=True, color=RR_PINK)
    add_text(s6, 0.85, 1.62, 5.45, 0.22, "Primary Execution Corridor: Mid-Wicket & Death Arc (28%)", size=8.0, color=MUTED_TEXT)
    if WAGON_WHEEL_PATH.exists():
        s6.shapes.add_picture(str(WAGON_WHEEL_PATH), Inches(0.75), Inches(1.90), width=Inches(5.65))

    # Right Card: Bowling Dossier Feature (Pitch Map)
    add_box(s6, 6.78, 1.25, 5.95, 4.05, fill=WHITE, border=BORDER_LIGHT)
    add_text(s6, 7.03, 1.38, 5.45, 0.25, "BOWLING PROFILE: HAWK-EYE PITCH LENGTH & CONTAINMENT", size=9.5, bold=True, color=RR_NAVY)
    add_text(s6, 7.03, 1.62, 5.45, 0.22, "Primary Execution Corridor: Stump-to-Stump Yorker & Good Length (64%)", size=8.0, color=MUTED_TEXT)
    if PITCH_MAP_PATH.exists():
        s6.shapes.add_picture(str(PITCH_MAP_PATH), Inches(6.93), Inches(1.90), width=Inches(5.65))

    # Bottom Informational Card explaining what clicking a player does
    add_box(s6, 0.60, 5.45, 12.13, 1.65, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s6, 0.85, 5.58, 6.0, 0.25, "GRANULAR SCOUTING COVERAGE ACROSS ALL 342 CANDIDATES", size=9.5, bold=True, color=DARK_TEXT)
    add_text(s6, 7.50, 5.58, 5.0, 0.25, "Live Player Dossier URLs Enabled on Render Dashboard", size=8.5, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)

    add_text(s6, 0.85, 5.88, 11.6, 0.45,
             "• Full Delivery-Level Breakdown: Clicking any candidate row opens their standalone scouting dossier, detailing career strike rate vs. pressure strike rate, true contextual lift, and 1,000-resample bootstrap confidence intervals.\n"
             "• Visual Corridor Mapping: Batters feature 8-sector boundary distribution (6s, 4s, 1s/2s); bowlers feature 5-zone pitch lengths (Yorker, Full Slot, Good Length, Short) mapped to wicket vs. dot-ball execution.",
             size=8.5, color=BODY_TEXT)

    add_text(s6, 0.85, 6.60, 11.6, 0.35,
             "Explore live profiles:  https://rr-dashboard.onrender.com/players/andre_russell.html   |   https://rr-dashboard.onrender.com/players/jasprit_bumrah.html",
             size=8.5, bold=True, color=RR_NAVY)

    # =========================================================================
    # SLIDE 7: PRE-AUCTION TRADE WINDOW & TRADE-OFF STRATEGY
    # =========================================================================
    s7 = prs.slides.add_slide(blank)
    add_slide_title(s7, "Pre-Auction Trade Window & Trade-Off Architecture",
                    "Purse conservation and trade strategies following Rajasthan Royals' 6-player core retention")

    # Retained Core Summary Banner
    add_box(s7, 0.60, 1.25, 12.13, 0.55, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s7, 0.80, 1.32, 7.5, 0.22,
             "Retained Core (6 Players • ₹79.0 Cr): Samson (₹18 Cr), Jaiswal (₹18 Cr), Parag (₹14 Cr), Jurel (₹14 Cr), Hetmyer (₹11 Cr), Sandeep (₹4 Cr)",
             size=8.5, bold=True, color=DARK_TEXT)
    add_text(s7, 8.50, 1.32, 4.0, 0.22,
             "Active Auction Purse: ₹41.0–45.0 Cr", size=8.5, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)

    # 3 Strategic Trade-Off Boxes
    to_boxes = [
        ("TRADE-OFF 1: SPIN CHOKE VS DEATH SEAM",
         "Middle-Spin Enforcer Allocation (₹17.5 Cr)",
         "Rather than overpaying for inflated marquee seamers, allocating ₹17.5 Cr to domestic spin enforcers (Shivam Dube ₹9.5 Cr, Axar Patel ₹8.0 Cr) neutralizes overs 7–15 while reserving ₹11.0 Cr for disciplined pace buys (Jacob Duffy, Josh Hazlewood).",
         AMBER),
        ("TRADE-OFF 2: PRE-AUCTION TRADE ARBITRAGE",
         "Fixed-Price Asset Locking (Donovan Ferreira ₹1.0 Cr)",
         "Executing targeted pre-auction trades (locking Donovan Ferreira at ₹1.0 Cr from Delhi Capitals) secures a Top-10 pressure finisher (+15.08 RAE, 158.2 SR) at base value, completely insulating the purse from multi-crore bidding wars.",
         GREEN),
        ("TRADE-OFF 3: JAIPUR SMS FORTRESS FIT",
         "Boundary Denial Over Flat-Track Power",
         "Sawai Mansingh Stadium has expansive 75m+ boundaries where flat-track power hitters struggle. Prioritizing boundary-suppression seamers (Duffy +1.37 lift, Yash Dayal 8.42 Econ) directly exploits Jaipur's large outfield conditions.",
         RR_NAVY),
    ]
    tox = 0.60
    tow = 3.90
    for htop, hmain, hbody, hcol in to_boxes:
        add_box(s7, tox, 1.95, tow, 2.30, fill=WHITE, border=BORDER_LIGHT)
        add_text(s7, tox + 0.15, 2.08, tow - 0.30, 0.20, htop, size=8.0, bold=True, color=hcol)
        add_text(s7, tox + 0.15, 2.30, tow - 0.30, 0.35, hmain, size=9.5, bold=True, color=DARK_TEXT)
        add_text(s7, tox + 0.15, 2.70, tow - 0.30, 1.45, hbody, size=8.5, color=BODY_TEXT)
        tox += tow + 0.21

    # Evaluation Matrix Table
    add_text(s7, 0.60, 4.40, 6.0, 0.25, "PRE-AUCTION TRADE-OFF EVALUATION MATRIX", size=10.0, bold=True, color=RR_NAVY)

    t_to = s7.shapes.add_table(5, 5, Inches(0.60), Inches(4.70), Inches(12.13), Inches(2.35)).table
    to_widths = [2.00, 1.80, 1.30, 5.43, 1.60]
    for ci, cw in enumerate(to_widths):
        t_to.columns[ci].width = Inches(cw)

    to_headers = ["Strategic Target / Asset", "Acquisition Route", "Target Value", "Tactical Justification", "Purse Impact"]
    for ci, h in enumerate(to_headers):
        style_cell(t_to.cell(0, ci), h, 8.5, True, WHITE, RR_NAVY, PP_ALIGN.LEFT if ci in (0, 3) else PP_ALIGN.CENTER)

    to_data = [
        ("Donovan Ferreira", "Completed Trade (DC -> RR)", "₹1.00 Cr", "Locks in Top-10 pressure batter (+15.08 RAE) at base cost; eliminates need for expensive overseas finisher bidding.", "+₹8.0 Cr Saved"),
        ("Shivam Dube", "Auction Priority 1", "₹9.50 Cr", "Designated middle-overs spin enforcer (162.8 SR); prevents scoring slowdowns between overs 7–15.", "21.1% Purse"),
        ("Jacob Duffy", "Auction Priority 1", "₹6.50 Cr", "Top-5 composite bowler (+14.16 score, 17 pressure wkts); elite powerplay swing and death execution.", "High Value Choke"),
        ("Axar Patel", "Auction Priority 1", "₹8.00 Cr", "Provides batting depth at No. 7 (+7.15 RAE) and 4 tight overs of left-arm orthodox spin calibrated for Jaipur.", "17.8% Purse"),
    ]
    for ri, r in enumerate(to_data, 1):
        bg = WHITE if ri % 2 == 1 else BG_SOFT
        style_cell(t_to.cell(ri, 0), r[0], 8.5, True, DARK_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_to.cell(ri, 1), r[1], 8.5, False, GREEN if "Trade" in r[1] else DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_to.cell(ri, 2), r[2], 8.5, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_to.cell(ri, 3), r[3], 8.0, False, BODY_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_to.cell(ri, 4), r[4], 8.5, True, GREEN if "+" in r[4] else DARK_TEXT, bg, PP_ALIGN.CENTER)

    # =========================================================================
    # SLIDE 8: PRESSURE LIFT QUADRANT SCATTER PLOT
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    add_slide_title(s8, "Pressure Lift Alpha Matrix & Quadrant Classification",
                    "Plotting Bayesian Pressure Rating Score against Contextual Performance Lift (SR / Econ Equivalent)")

    if QUAD_PATH.exists():
        s8.shapes.add_picture(str(QUAD_PATH), Inches(0.60), Inches(1.20), width=Inches(7.30))

    # Right side: 4 Quadrants Summary
    q_x = 8.10
    q_w = 4.63

    add_box(s8, q_x, 1.20, q_w, 1.30, fill=WHITE, border=BORDER_LIGHT)
    add_text(s8, q_x + 0.15, 1.28, q_w - 0.3, 0.20, "QUADRANT I • ELITE PRESSURE MATCH-WINNERS", size=9.0, bold=True, color=GREEN)
    add_text(s8, q_x + 0.15, 1.50, q_w - 0.3, 0.90,
             "• Andre Russell (+26.59 RAE, 165.6 SR, +38.94 Lift)\n• Jasprit Bumrah (28.45 Score, 7.79 Econ Choke)\n• Matheesha Pathirana (25.80 Score, 9.02 Death Econ)\n• Umran Malik (24.75 Score, 14 Wkts, 7.68 Econ)",
             size=8.0, color=DARK_TEXT)

    add_box(s8, q_x, 2.60, q_w, 1.30, fill=WHITE, border=BORDER_LIGHT)
    add_text(s8, q_x + 0.15, 2.68, q_w - 0.3, 0.20, "QUADRANT II • HIGH-CEILING BREAKOUTS", size=9.0, bold=True, color=AMBER)
    add_text(s8, q_x + 0.15, 2.90, q_w - 0.3, 0.90,
             "• Vaibhav Sooryavanshi (234.6 SR under pressure, +83.78 Lift)\n• Priyansh Arya (215.4 SR under pressure, +70.33 Lift)\n• Mayank Yadav (6.86 Econ, 155+ km/h Express Pace)\n• Jacob Duffy (+14.16 Score, +1.37 Econ Lift)",
             size=8.0, color=DARK_TEXT)

    add_box(s8, q_x, 4.00, q_w, 1.30, fill=WHITE, border=BORDER_LIGHT)
    add_text(s8, q_x + 0.15, 4.08, q_w - 0.3, 0.20, "QUADRANT III • SITUATIONAL BASELINE & IMPACT BUYS", size=9.0, bold=True, color=MUTED_TEXT)
    add_text(s8, q_x + 0.15, 4.30, q_w - 0.3, 0.90,
             "• Donovan Ferreira (+15.08 RAE, 158.2 SR, Base Trade Asset)\n• Varun Chakravarthy (13.50 Score, 7.82 Econ Mystery Spin)\n• Arshdeep Singh (12.80 Score, 25 Wkts, Left-Arm Seam)",
             size=8.0, color=DARK_TEXT)

    add_box(s8, q_x, 5.40, q_w, 1.30, fill=WHITE, border=BORDER_LIGHT)
    add_text(s8, q_x + 0.15, 5.48, q_w - 0.3, 0.20, "QUADRANT IV • DISCIPLINED CHOKE SPECIALISTS", size=9.0, bold=True, color=RR_NAVY)
    add_text(s8, q_x + 0.15, 5.70, q_w - 0.3, 0.90,
             "• Heinrich Klaasen (+24.15 RAE, 487 Pressure Balls)\n• Glenn Maxwell (+22.45 RAE, 164.1 SR)\n• Suryakumar Yadav (+21.80 RAE, 682 Pressure Balls)\n• Tim David (+20.11 RAE) & Shivam Dube (+17.90 RAE)",
             size=8.0, color=DARK_TEXT)

    add_box(s8, 0.60, 6.45, 7.30, 0.55, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s8, 0.75, 6.52, 7.00, 0.40,
             "Key Insight: High pressure lift (Y-axis) separates true individual match-winners from players benefiting from dominant top orders or easy low-leverage overs.",
             size=8.5, color=BODY_TEXT)

    # =========================================================================
    # SLIDE 9: RECOMMENDED 2027 PLAYING XI (CAPTAIN RIYAN PARAG)
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    add_slide_title(s9, "Rajasthan Royals — Recommended 2027 Playing XI",
                    "A balanced 11-man lineup calibrated to dominate middle-overs spin and close out death overs under pressure")

    xi_groups = [
        ("TOP-ORDER ANCHORS (OVERS 1–6)", [
            ("1", "Yashasvi Jaiswal", "RETAINED CORE", "Left-Hand Explosive Opener • Powerplay Strike Rate 165+"),
            ("2", "Devon Conway", "AUCTION TARGET", "LHB Top-Order Anchor & Wicketkeeper • Contextual Pressure RAE +11.89"),
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
            ("9", "Josh Hazlewood", "AUCTION TARGET", "Frontline Seam Spearhead • Composite Score +12.27 (27 pressure wkts)"),
            ("10", "Sandeep Sharma", "RETAINED CORE", "Death Yorker & Wide-Line Specialist • Reliable Death Execution"),
            ("11", "Yash Dayal", "AUCTION TARGET", "Left-Arm Seam Specialist • High-Leverage Economy 8.42"),
        ]),
    ]

    coords = [(0.60, 1.25), (6.78, 1.25), (0.60, 3.65), (6.78, 3.65)]
    gw = 5.95

    for idx, (gtitle, gplayers) in enumerate(xi_groups):
        cx, cy = coords[idx]
        ch = 2.25 if idx < 2 else 2.15
        add_box(s9, cx, cy, gw, ch, fill=WHITE, border=BORDER_LIGHT)
        add_text(s9, cx + 0.20, cy + 0.12, gw - 0.40, 0.22, gtitle, size=8.5, bold=True, color=RR_NAVY)

        py = cy + 0.40
        for pnum, pname, ptag, pdesc in gplayers:
            add_box(s9, cx + 0.20, py, gw - 0.40, 0.50, fill=BG_SOFT, border=BORDER_LIGHT)
            add_text(s9, cx + 0.30, py + 0.08, 0.25, 0.30, pnum, size=9.5, bold=True, color=DARK_TEXT)
            add_text(s9, cx + 0.60, py + 0.06, 3.2, 0.20, pname, size=9.5, bold=True, color=DARK_TEXT)
            tag_col = GREEN if "RETAINED" in ptag else RR_PINK
            add_text(s9, cx + 3.80, py + 0.06, 1.9, 0.20, ptag, size=7.5, bold=True, color=tag_col, align=PP_ALIGN.RIGHT)
            add_text(s9, cx + 0.60, py + 0.26, 5.1, 0.20, pdesc, size=7.5, color=MUTED_TEXT)
            py += 0.56

    # Bottom Impact Substitutes Box
    add_box(s9, 0.60, 6.00, 12.13, 1.05, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s9, 0.85, 6.12, 11.6, 0.20, "TACTICAL IMPACT SUBSTITUTES & MATCHUP COVERS:", size=8.5, bold=True, color=RR_NAVY)
    subs = [
        "Jacob Duffy (Pace • Composite Score +14.16)",
        "Axar Patel (Spin All-Rounder • Shrunk RAE +7.15)",
        "Varun Chakravarthy (Mystery Spin • Shrunk RPAE +7.82)",
        "Rajat Patidar (No. 3 Cover • Shrunk RAE +10.64)",
    ]
    sx = 0.85
    for s in subs:
        add_box(s9, sx, 6.42, 2.75, 0.45, fill=WHITE, border=BORDER_LIGHT)
        add_text(s9, sx + 0.10, 6.52, 2.55, 0.25, s, size=7.8, bold=True, color=DARK_TEXT)
        sx += 2.92

    # =========================================================================
    # SLIDE 10: AUCTION PRIORITY TARGETS TABLE
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    add_slide_title(s10, "Auction Priority Targets Evaluation",
                    "Evaluation of calibrated targets across career rate, pressure rate, and pressure lift")

    t_auc = s10.shapes.add_table(11, 6, Inches(0.60), Inches(1.25), Inches(12.13), Inches(5.60)).table
    auc_widths = [0.50, 2.50, 3.43, 1.80, 1.90, 2.00]
    for ci, cw in enumerate(auc_widths):
        t_auc.columns[ci].width = Inches(cw)

    auc_headers = ["#", "Player", "Role in Team", "Career Rate", "Pressure Rate", "Lift (Δ) / Score"]
    for ci, h in enumerate(auc_headers):
        style_cell(t_auc.cell(0, ci), h, 9.0, True, WHITE, RR_NAVY, PP_ALIGN.LEFT if ci in (1, 2) else PP_ALIGN.CENTER)

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
        style_cell(t_auc.cell(ri, 0), r[0], 9.0, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_auc.cell(ri, 1), r[1], 9.0, True, DARK_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_auc.cell(ri, 2), r[2], 8.5, False, BODY_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_auc.cell(ri, 3), r[3], 9.0, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_auc.cell(ri, 4), r[4], 9.0, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_auc.cell(ri, 5), r[5], 9.0, True, GREEN, bg, PP_ALIGN.CENTER)

    # =========================================================================
    # SLIDE 11: AUCTION BUDGET PLAN (₹45 CRORE PURSE)
    # =========================================================================
    s11 = prs.slides.add_slide(blank)
    add_slide_title(s11, "Auction Budget Plan (₹45 Crore Total Purse)",
                    "Disciplined bidding caps to prevent emotional overspending on marquee names")

    # Purse KPI Strip
    p_kpis = [
        ("TOTAL BUDGET", "₹45.0 Cr", "Available Auction Purse", DARK_TEXT),
        ("TARGET ALLOCATIONS", "₹45.0 Cr", "Sum of Target Max Bids", DARK_TEXT),
        ("BUDGET UTILIZATION", "100%", "Completely De-risked Purse", GREEN),
    ]
    px = 0.60
    pw = 3.90
    for plbl, pval, psub, pcol in p_kpis:
        add_box(s11, px, 1.25, pw, 1.10, fill=BG_SOFT, border=BORDER_LIGHT)
        add_text(s11, px + 0.20, 1.35, pw - 0.40, 0.20, plbl, size=8.5, bold=True, color=MUTED_TEXT, align=PP_ALIGN.CENTER)
        add_text(s11, px + 0.20, 1.58, pw - 0.40, 0.40, pval, size=20, bold=True, color=pcol, align=PP_ALIGN.CENTER)
        add_text(s11, px + 0.20, 2.00, pw - 0.40, 0.22, psub, size=8.5, color=BODY_TEXT, align=PP_ALIGN.CENTER)
        px += pw + 0.21

    t_bud = s11.shapes.add_table(7, 5, Inches(0.60), Inches(2.55), Inches(12.13), Inches(4.50)).table
    b_col_widths = [2.20, 1.60, 1.50, 1.30, 5.53]
    for ci, cw in enumerate(b_col_widths):
        t_bud.columns[ci].width = Inches(cw)

    bud_headers = ["Target Player", "Priority", "Max Bid", "% of Purse", "Why Rajasthan Royals Needs Him"]
    for ci, h in enumerate(bud_headers):
        style_cell(t_bud.cell(0, ci), h, 8.5, True, WHITE, RR_NAVY, PP_ALIGN.LEFT if ci in (0, 4) else PP_ALIGN.CENTER)

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
        style_cell(t_bud.cell(ri, 0), r[0], 9.0, True, DARK_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_bud.cell(ri, 1), r[1], 8.0, True, RR_PINK if "1" in r[1] else DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bud.cell(ri, 2), r[2], 9.0, True, DARK_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bud.cell(ri, 3), r[3], 8.5, False, MUTED_TEXT, bg, PP_ALIGN.CENTER)
        style_cell(t_bud.cell(ri, 4), r[4], 8.0, False, BODY_TEXT, bg, PP_ALIGN.LEFT)

    # =========================================================================
    # SLIDE 12: WAR ROOM BIDDING RULES & CONTINGENCY MATRIX
    # =========================================================================
    s12 = prs.slides.add_slide(blank)
    add_slide_title(s12, "War Room Bidding Rules & Contingency Matrix",
                    "Real-time step-down protocols to maintain budget integrity during live auction bidding")

    # Left Column: Bidding Rules & Contingency Triggers
    add_box(s12, 0.60, 1.25, 5.95, 5.85, fill=WHITE, border=BORDER_LIGHT)
    add_text(s12, 0.85, 1.45, 5.45, 0.25, "AUCTION BIDDING RULE (10% CIRCUIT BREAKER)", size=10.0, bold=True, color=RR_NAVY)
    add_text(s12, 0.85, 1.75, 5.45, 0.60,
             "If bidding for any player goes more than 10% above their maximum limit, stop bidding immediately and switch to backup targets to protect the overall team budget.",
             size=8.5, color=BODY_TEXT)

    add_text(s12, 0.85, 2.45, 5.45, 0.25, "CONTINGENCY BIDDING MATRIX (LIVE STEP-DOWNS)", size=10.0, bold=True, color=RR_NAVY)

    triggers = [
        ("If Rinku Singh > ₹11.0 Cr:", "Pivot immediately to Bhanuka Rajapaksa (₹3.5 Cr) and promote Shimron Hetmyer to No. 6, freeing ₹7.5 Cr for the bowling reserve.", RR_PINK),
        ("If Shivam Dube > ₹9.5 Cr:", "Switch to Rajat Patidar (₹7.0 Cr) for spin boundary execution, reallocating ₹2.5 Cr to the overseas pace budget.", RR_NAVY),
        ("If Josh Hazlewood > ₹9.5 Cr:", "Lock Jacob Duffy (₹6.5 Cr) as primary overseas seamer and secure Yash Dayal (₹4.5 Cr) for domestic seam depth.", GREEN),
        ("If Axar Patel > ₹8.0 Cr:", "Pivot to Varun Chakravarthy (₹5.5 Cr) plus a domestic all-rounder backup to secure middle-overs spin choke.", AMBER),
    ]
    ty = 2.80
    for thdr, tbody, tcol in triggers:
        add_box(s12, 0.85, ty, 5.45, 0.88, fill=BG_SOFT, border=BORDER_LIGHT)
        add_box(s12, 0.85, ty, 0.08, 0.88, fill=tcol, border=None)
        add_text(s12, 1.05, ty + 0.08, 5.15, 0.20, thdr, size=8.5, bold=True, color=DARK_TEXT)
        add_text(s12, 1.05, ty + 0.30, 5.15, 0.48, tbody, size=8.0, color=BODY_TEXT)
        ty += 1.00

    # Right Column: Phase Distribution & Principles
    add_box(s12, 6.78, 1.25, 5.95, 5.85, fill=WHITE, border=BORDER_LIGHT)
    add_text(s12, 7.03, 1.45, 5.45, 0.25, "PHASE-BY-PHASE PURSE DISTRIBUTION (₹45.0 CR TOTAL)", size=10.0, bold=True, color=RR_NAVY)

    phases = [
        ("MIDDLE SPIN ATTACK", "₹17.50 Cr", "38.9%", "Shivam Dube (₹9.5 Cr) + Axar Patel (₹8.0 Cr)"),
        ("DEATH FINISHING", "₹11.00 Cr", "24.4%", "Rinku Singh (₹11.0 Cr - Priority 1)"),
        ("PACE SPEARHEADS", "₹11.00 Cr", "24.4%", "Jacob Duffy (₹6.5 Cr) + Romario Shepherd (₹4.5 Cr)"),
        ("MYSTERY SPIN CHOKE", "₹5.50 Cr", "12.2%", "Varun Chakravarthy (₹5.5 Cr - Priority 2)"),
    ]
    pyx = 7.03
    pyy = 1.80
    for ptitle, pval, ppct, pdesc in phases:
        add_box(s12, pyx, pyy, 2.62, 0.95, fill=BG_SOFT, border=BORDER_LIGHT)
        add_text(s12, pyx + 0.12, pyy + 0.08, 2.38, 0.20, ptitle, size=7.5, bold=True, color=MUTED_TEXT)
        add_text(s12, pyx + 0.12, pyy + 0.28, 1.50, 0.30, pval, size=13.0, bold=True, color=DARK_TEXT)
        add_text(s12, pyx + 1.62, pyy + 0.32, 0.88, 0.22, ppct, size=8.5, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)
        add_text(s12, pyx + 0.12, pyy + 0.62, 2.38, 0.25, pdesc, size=7.0, color=BODY_TEXT)
        if pyx == 7.03:
            pyx = 9.86
        else:
            pyx = 7.03
            pyy += 1.08

    add_text(s12, 7.03, 4.10, 5.45, 0.25, "WAR ROOM OPERATIONAL PRINCIPLES", size=10.0, bold=True, color=RR_NAVY)
    principles = [
        ("No Emotional Marquee Bidding:", "Resist brand-driven inflation on famous names whose clutch win differential is negative."),
        ("Jaipur SMS Fortress Fit:", "Prioritize players suited to 75m+ boundaries and middle-overs spin grip over flat-track sluggers."),
        ("Strict 2+2 Overseas Structure:", "Exactly 2 overseas players in the Starting XI (Conway, Hazlewood) and 2 impact covers (Duffy, Hetmyer)."),
        ("10% Circuit Breaker:", "The instant any target exceeds 10% above max valuation, immediately execute the step-down contingency."),
    ]
    pry = 4.45
    for prtitle, prbody in principles:
        add_text(s12, 7.03, pry, 5.45, 0.20, f"• {prtitle}", size=8.5, bold=True, color=DARK_TEXT)
        add_text(s12, 7.20, pry + 0.20, 5.28, 0.35, prbody, size=8.0, color=BODY_TEXT)
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
        add_box(s13, 0.60, ty, 0.08, 1.15, fill=tcol, border=None)
        add_text(s13, 0.85, ty + 0.12, 11.5, 0.25, tnum, size=10.5, bold=True, color=DARK_TEXT)
        add_text(s13, 0.85, ty + 0.40, 11.5, 0.65, tbody, size=8.5, color=BODY_TEXT)
        ty += 1.25

    # Dedicated Production Resources Container (URLs, no footer bar)
    add_box(s13, 0.60, 6.30, 5.95, 0.95, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s13, 0.80, 6.38, 5.5, 0.20, "LIVE WEB DASHBOARD & DOSSIER SUITE:", size=8.5, bold=True, color=RR_NAVY)
    add_text(s13, 0.80, 6.62, 5.5, 0.25, "https://rr-dashboard.onrender.com/", size=10.5, bold=True, color=RR_PINK)
    add_text(s13, 0.80, 6.90, 5.5, 0.25, "Full 342-player dossiers, interactive wagon wheels & live war room", size=7.5, color=MUTED_TEXT)

    add_box(s13, 6.78, 6.30, 5.95, 0.95, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s13, 6.98, 6.38, 5.5, 0.20, "OPEN-SOURCE CODEBASE & REPLICATION:", size=8.5, bold=True, color=RR_NAVY)
    add_text(s13, 6.98, 6.62, 5.5, 0.25, "https://github.com/Ketanrawat2004/RR-Dashboard", size=10.5, bold=True, color=DARK_TEXT)
    add_text(s13, 6.98, 6.90, 5.5, 0.25, "Complete pipeline scripts, bootstrap models & automated documentation", size=7.5, color=MUTED_TEXT)

    # Save outputs to both main and pressure_output copy
    prs.save(str(OUT_MAIN))
    print(f"Saved PPTX to: {OUT_MAIN}")
    prs.save(str(OUT_COPY))
    print(f"Saved PPTX copy to: {OUT_COPY}")

if __name__ == "__main__":
    build_deck()
