import json
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

BASE_DIR = Path(r"C:\Rajasthan Royals")
SCRATCH = BASE_DIR / "scratch"
LOGO_PATH = SCRATCH / "rr_corner_logo.png"
DONUT_PATH = SCRATCH / "ppt_chart_donut.png"
QUAD_PATH = SCRATCH / "ppt_chart_quadrants.png"
OUT_MAIN = BASE_DIR / "RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx"
OUT_COPY = BASE_DIR / "pressure_output" / "RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx"

# Minimal Light Palette
WHITE = RGBColor(255, 255, 255)
BG_SOFT = RGBColor(248, 250, 252)
BG_PINK_TINT = RGBColor(253, 242, 248)
BG_GREEN_TINT = RGBColor(240, 253, 244)
BG_AMBER_TINT = RGBColor(255, 251, 235)
BORDER = RGBColor(203, 213, 225)
BORDER_LIGHT = RGBColor(226, 232, 240)
DARK_TEXT = RGBColor(17, 24, 39)
BODY_TEXT = RGBColor(55, 65, 81)
MUTED_TEXT = RGBColor(100, 116, 139)
RR_NAVY = RGBColor(0, 29, 72)
RR_PINK = RGBColor(217, 27, 122)
GREEN = RGBColor(4, 120, 87)
RED = RGBColor(185, 28, 28)
AMBER = RGBColor(180, 83, 9)

FONT_MAIN = "Calibri"

with open(BASE_DIR / "players_db.json", encoding="utf-8") as f:
    db = json.load(f)

batters = sorted([p for p in db if p["category"] == "Batter"], key=lambda x: x["rank"])
bowlers = sorted([p for p in db if p["category"] == "Bowler"], key=lambda x: x["rank"])


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


def style_cell(cell, text, font_size=9.5, bold=False, color=BODY_TEXT, fill=None, align=PP_ALIGN.LEFT, margins=(0.06, 0.06, 0.04, 0.04)):
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
    # RR logo cleanly placed in top-right corner of every slide (aspect ~ 348:544 = 0.64)
    if LOGO_PATH.exists():
        slide.shapes.add_picture(str(LOGO_PATH), Inches(12.35), Inches(0.26), height=Inches(0.76))


def add_slide_title(slide, title, subtitle=None):
    add_corner_logo(slide)
    tb = slide.shapes.add_textbox(Inches(0.60), Inches(0.32), Inches(11.4), Inches(0.75))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_MAIN
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(11.5)
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


def add_text(slide, left, top, width, height, text, size=10.5, bold=False, color=BODY_TEXT, align=PP_ALIGN.LEFT, font_name=FONT_MAIN):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.font.name = font_name
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    return tb


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 1: BEGINNING / COVER SLIDE (NO HEADER, NO FOOTER, RR LOGO IN CORNER)
    # ═══════════════════════════════════════════════════════════════
    s1 = prs.slides.add_slide(blank)
    add_corner_logo(s1)

    add_text(s1, 0.90, 1.55, 10.5, 0.35, "Rajasthan Royals  |  SupeRR Selector Season 2 (Round 1)", size=13, bold=True, color=RR_PINK)
    add_text(s1, 0.90, 2.05, 11.2, 1.35, "Identifying the Most Reliable Players\nUnder Match Pressure", size=38, bold=True, color=DARK_TEXT)
    add_text(s1, 0.90, 3.65, 10.8, 0.75,
             "Measuring Match Leverage, True Pressure Lift, and Building a Balanced IPL 2027 Auction Plan for Sawai Mansingh Stadium, Jaipur",
             size=15, color=BODY_TEXT)

    # Simple hairline separator
    add_box(s1, 0.90, 4.65, 3.2, 0.03, fill=RR_NAVY, border=None)

    # Clean key stats & author in body (not a footer)
    add_text(s1, 0.90, 4.95, 10.8, 0.40,
             "Dataset Scope: 883 IPL & T20I Matches (2022–2026)  |  1,217 Players Evaluated  |  178 High-Pressure Fixtures (20.2%)",
             size=12, bold=True, color=RR_NAVY)
    add_text(s1, 0.90, 5.45, 10.8, 0.35,
             "Submitted by: Ketan Rawat (B.Tech ECE, NIT Jamshedpur)",
             size=12, color=MUTED_TEXT)

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 2: DATASET OVERVIEW & PERFORMANCE BY MARGIN (IMAGES #1 & #2)
    # ═══════════════════════════════════════════════════════════════
    s2 = prs.slides.add_slide(blank)
    add_slide_title(s2, "Dataset Scope & High-Pressure Sample Overview",
                    "Summary of 883 IPL and T20I fixtures (2022–2026) filtered by Match Leverage Index (MLI >= 30)")

    kpis = [
        ("MATCHES EVALUATED", "883", "IPL & T20I (2022–2026)", DARK_TEXT),
        ("HIGH-PRESSURE SAMPLE", "178", "20.2% of total dataset", DARK_TEXT),
        ("PLAYER POOL", "1,217", "28,381 playing-XI records", DARK_TEXT),
        ("TOP RANKED BATTER", "66.81", "Shivam Dube (+12.4% Lift)", RR_PINK),
        ("TOP RANKED BOWLER", "68.83", "Jacob Duffy (+20.5% Lift)", RR_NAVY),
        ("HIGHEST WIN LIFT", "+20.5%", "Jacob Duffy (75.0% HP WR)", GREEN),
    ]
    kx = 0.60
    kw = 1.92
    for lbl, num, sub, ncol in kpis:
        add_box(s2, kx, 1.32, kw, 1.25, fill=BG_SOFT, border=BORDER_LIGHT)
        add_text(s2, kx + 0.12, 1.44, kw - 0.24, 0.25, lbl, size=8.5, bold=True, color=MUTED_TEXT, align=PP_ALIGN.CENTER)
        add_text(s2, kx + 0.12, 1.72, kw - 0.24, 0.42, num, size=21, bold=True, color=ncol, align=PP_ALIGN.CENTER)
        add_text(s2, kx + 0.12, 2.18, kw - 0.24, 0.28, sub, size=8.5, color=BODY_TEXT, align=PP_ALIGN.CENTER)
        kx += kw + 0.12

    # Bottom 3 Panels matching Image #2
    # Panel 1: Fixture Distribution Donut
    add_box(s2, 0.60, 2.82, 3.85, 4.10, fill=WHITE, border=BORDER_LIGHT)
    add_text(s2, 0.80, 2.98, 3.45, 0.30, "HIGH-PRESSURE FIXTURE BREAKDOWN", size=10.5, bold=True, color=RR_NAVY)
    s2.shapes.add_picture(str(DONUT_PATH), Inches(1.42), Inches(3.38), width=Inches(2.20))
    dist_rows = [
        ("Defend <= 15 runs", "118 (66%)", RR_PINK),
        ("Playoff / Knockout", "35 (20%)", RR_NAVY),
        ("Chase <= 2 wkts / Tie", "25 (14%)", GREEN),
    ]
    dy = 5.72
    for dlabel, dval, dcol in dist_rows:
        add_box(s2, 0.85, dy + 0.05, 0.14, 0.14, fill=dcol, border=None)
        add_text(s2, 1.08, dy, 2.0, 0.25, dlabel, size=10, color=BODY_TEXT)
        add_text(s2, 3.15, dy, 1.1, 0.25, dval, size=10, bold=True, color=DARK_TEXT, align=PP_ALIGN.RIGHT)
        dy += 0.33

    # Panel 2: Top Win-Rate Gains Under Pressure
    add_box(s2, 4.65, 2.82, 3.85, 4.10, fill=WHITE, border=BORDER_LIGHT)
    add_text(s2, 4.85, 2.98, 3.45, 0.30, "TOP PRESSURE WIN-RATE GAINS (LIFT)", size=10.5, bold=True, color=RR_NAVY)
    add_text(s2, 4.85, 3.28, 3.45, 0.28, "Change in team win rate vs career baseline:", size=9.5, color=MUTED_TEXT)
    gains = [
        ("1. Jacob Duffy", "+20.5%", 20.5),
        ("2. Devon Conway", "+18.1%", 18.1),
        ("3. Josh Hazlewood", "+14.9%", 14.9),
        ("4. Shivam Dube", "+12.4%", 12.4),
        ("5. R. Patidar / Arshdeep", "+11.1%", 11.1),
    ]
    gy = 3.72
    for gname, gval, gpct in gains:
        add_text(s2, 4.85, gy, 2.35, 0.25, gname, size=10, bold=True, color=DARK_TEXT)
        add_text(s2, 7.25, gy, 1.05, 0.25, gval, size=10, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)
        add_box(s2, 4.85, gy + 0.28, 3.45, 0.10, fill=BORDER_LIGHT, border=None)
        add_box(s2, 4.85, gy + 0.28, 3.45 * (gpct / 21.5), 0.10, fill=GREEN, border=None)
        gy += 0.60

    # Panel 3: Margin Performance Matrix
    add_box(s2, 8.70, 2.82, 4.03, 4.10, fill=WHITE, border=BORDER_LIGHT)
    add_text(s2, 8.90, 2.98, 3.63, 0.30, "WIN CONVERSION BY MARGIN TIER", size=10.5, bold=True, color=RR_NAVY)
    add_text(s2, 8.90, 3.28, 3.63, 0.38, "Comparison across close run margins and playoffs:", size=9.5, color=MUTED_TEXT)
    t_mat = s2.shapes.add_table(4, 5, Inches(8.88), Inches(3.85), Inches(3.68), Inches(2.10)).table
    mat_widths = [1.28, 0.60, 0.60, 0.60, 0.60]
    for ci, cw in enumerate(mat_widths):
        t_mat.columns[ci].width = Inches(cw)
    m_headers = ["Group", "<=6 R", "7-12 R", "13-15 R", "Playoff"]
    for ci, h in enumerate(m_headers):
        style_cell(t_mat.cell(0, ci), h, 9, True, WHITE, RR_NAVY, PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER)
    m_rows = [
        ("Top 10 Batters", "68.4%", "71.2%", "64.5%", "72.0%", GREEN),
        ("Top 10 Bowlers", "66.7%", "63.8%", "69.1%", "74.2%", GREEN),
        ("Peer Baseline", "44.2%", "48.1%", "49.6%", "41.8%", RED),
    ]
    for ri, row in enumerate(m_rows, 1):
        style_cell(t_mat.cell(ri, 0), row[0], 9, True, DARK_TEXT, BG_SOFT if ri == 3 else WHITE, PP_ALIGN.LEFT)
        for ci in range(1, 5):
            style_cell(t_mat.cell(ri, ci), row[ci], 9, True, row[5], BG_SOFT if ri == 3 else WHITE, PP_ALIGN.CENTER)
    add_text(s2, 8.90, 6.22, 3.63, 0.50,
             "Selected top-10 players win roughly 20–30 percentage points more tight matches than the broader peer group.",
             size=9.5, color=BODY_TEXT)

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 3: METHODOLOGY — PRESSURE DEFINITION & CPPI FORMULA (IMAGE #3)
    # ═══════════════════════════════════════════════════════════════
    s3 = prs.slides.add_slide(blank)
    add_slide_title(s3, "How Pressure Is Defined and Scored",
                    "Transparent rules separating high-stakes games from routine fixtures and controlling small-sample noise")

    # Left Card: Defining High-Pressure Matches
    add_box(s3, 0.60, 1.32, 5.95, 5.65, fill=WHITE, border=BORDER)
    add_text(s3, 0.85, 1.50, 5.45, 0.35, "1. Match Leverage Index (MLI >= 30 Points)", size=13, bold=True, color=RR_NAVY)
    add_text(s3, 0.85, 1.85, 5.45, 0.45,
             "Each match is scored on a 0–100 point scale across four objective game-context signals. Matches scoring 30+ qualify (178 of 883 matches, 20.2%).",
             size=10.5, color=BODY_TEXT)

    t_mli = s3.shapes.add_table(5, 3, Inches(0.85), Inches(2.42), Inches(5.45), Inches(2.55)).table
    for ci, cw in enumerate([1.45, 0.85, 3.15]):
        t_mli.columns[ci].width = Inches(cw)
    for ci, h in enumerate(["Factor", "Points", "Scoring Thresholds"]):
        style_cell(t_mli.cell(0, ci), h, 9.5, True, WHITE, RR_NAVY, PP_ALIGN.CENTER if ci == 1 else PP_ALIGN.LEFT)
    mli_rows = [
        ("Stage Stakes", "0–40", "Final 40 | Semi-Final 35 | Qualifier/Eliminator 30 | Super 4 20 | League 5"),
        ("Match Closeness", "0–40", "Super Over / Tie 40 | Margin <=5 runs or 1 wkt 38 | <=10r or 2w 32 | <=15r 26"),
        ("Knockout Jeopardy", "0–20", "+20 points if defeat causes immediate elimination"),
        ("Target Disruption", "0–5", "+5 points for DLS / rain-revised chases"),
    ]
    for ri, r in enumerate(mli_rows, 1):
        bg = BG_SOFT if ri % 2 == 0 else WHITE
        style_cell(t_mli.cell(ri, 0), r[0], 9.5, True, DARK_TEXT, bg, PP_ALIGN.LEFT)
        style_cell(t_mli.cell(ri, 1), r[1], 9.5, True, RR_NAVY, bg, PP_ALIGN.CENTER)
        style_cell(t_mli.cell(ri, 2), r[2], 9.2, False, BODY_TEXT, bg, PP_ALIGN.LEFT)

    add_text(s3, 0.85, 5.20, 5.45, 0.28, "Player Eligibility & Fair Comparison Filters", size=11.5, bold=True, color=DARK_TEXT)
    add_text(s3, 0.85, 5.52, 5.45, 1.30,
             "- Sample floor: minimum 12 total matches and 8 high-pressure matches.\n"
             "- Role separation: Batters (<= 6.3 avg batting position / WK) and Bowlers (>= 8.2 avg position) evaluated in separate lists.\n"
             "- Auction realism: BCCI IPL auction eligibility rules applied before ranking.",
             size=10, color=BODY_TEXT)

    # Right Card: CPPI Formula
    add_box(s3, 6.78, 1.32, 5.95, 5.65, fill=WHITE, border=BORDER)
    add_text(s3, 7.03, 1.50, 5.45, 0.35, "2. Calibrated Scoring Model (CPPI)", size=13, bold=True, color=RR_NAVY)
    add_text(s3, 7.03, 1.85, 5.45, 0.45,
             "Scores balance win conversion under pressure against career baseline lift and sample volume:",
             size=10.5, color=BODY_TEXT)

    add_box(s3, 7.03, 2.38, 5.45, 0.78, fill=BG_SOFT, border=BORDER)
    add_text(s3, 7.15, 2.48, 5.21, 0.58,
             "CPPI = [ 0.35 x Bayes_HP_WR + 0.25 x Lift_norm + 0.20 x Bayes_KO_WR + 0.10 x MOM_HP + 0.10 x Base_WR ] x Credibility(n_HP)",
             size=9.5, bold=True, color=RR_NAVY, align=PP_ALIGN.CENTER, font_name="Consolas")

    weights = [
        ("Bayesian HP Win Rate (35%):", "Regularizes pressure win rate toward career baseline using prior weight M = 5.0 matches."),
        ("Normalized Pressure Lift (25%):", "Measures HP Win Rate minus Career Baseline Win Rate (Delta), scaled around 50 pts."),
        ("Bayesian Knockout Win Rate (20%):", "Direct win rate in sudden-death playoff and World Cup knockouts, shrunk by baseline."),
        ("HP Player of the Match Rate (10%):", "Damped from 20% to stop small-sample award spikes from distorting the top 10."),
        ("Career Baseline Win Rate (10%):", "Anchors overall match reliability across the full 2022–2026 sample."),
        ("Credibility Multiplier:", "0.85 + 0.15 / [1 + exp(-0.25 x (n_HP - 8))], reducing scores when HP sample is 8–12 matches."),
    ]
    wy = 3.35
    for wt, wd in weights:
        add_text(s3, 7.03, wy, 5.45, 0.25, wt, size=10, bold=True, color=DARK_TEXT)
        add_text(s3, 7.03, wy + 0.22, 5.45, 0.30, wd, size=9.5, color=BODY_TEXT)
        wy += 0.58

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 4: TOP 10 BATTERS UNDER PRESSURE (IMAGE #4)
    # ═══════════════════════════════════════════════════════════════
    s4 = prs.slides.add_slide(blank)
    add_slide_title(s4, "Top 10 Batters Under Pressure (Official Ranking)",
                    "Calibrated CPPI order matching Unstop Component 01 submission dropdowns")

    t_bat = s4.shapes.add_table(11, 10, Inches(0.60), Inches(1.26), Inches(12.13), Inches(4.50)).table
    bat_w = [0.50, 1.62, 2.55, 2.95, 0.65, 0.78, 0.78, 0.80, 0.72, 0.78]
    for ci, cw in enumerate(bat_w):
        t_bat.columns[ci].width = Inches(cw)
    b_headers = ["Rank", "Player", "Tactical Role", "Franchise / Teams", "HP M", "HP WR", "Base WR", "Win Diff", "KO WR", "CPPI"]
    for ci, h in enumerate(b_headers):
        al = PP_ALIGN.LEFT if ci in (1, 2, 3) else PP_ALIGN.CENTER
        style_cell(t_bat.cell(0, ci), h, 8.8, True, WHITE, RR_NAVY, al, margins=(0.05, 0.05, 0.03, 0.03))

    for ri, p in enumerate(batters, 1):
        bg = BG_PINK_TINT if ri == 1 else (BG_SOFT if ri % 2 == 0 else WHITE)
        lift_str = f"{p['lift']:+.1f}%"
        lcol = GREEN if p["lift"] > 0 else RED
        vals = [
            f"{p['rank']}",
            p["name"],
            p["tactical_role"],
            p["teams"],
            f"{p['hp_m']}",
            f"{p['hp_wr']:.1f}%",
            f"{p['base_wr']:.1f}%",
            lift_str,
            f"{p['ko_wr']:.1f}%",
            f"{p['cppi']:.2f}",
        ]
        for ci, v in enumerate(vals):
            al = PP_ALIGN.LEFT if ci in (1, 2, 3) else PP_ALIGN.CENTER
            is_b = ci in (0, 1, 7, 9)
            col = lcol if ci == 7 else (DARK_TEXT if ci in (0, 1, 5, 9) else BODY_TEXT)
            style_cell(t_bat.cell(ri, ci), v, 8.5, is_b, col, bg, al, margins=(0.05, 0.05, 0.025, 0.025))

    add_text(s4, 0.60, 6.56, 12.13, 0.45,
             "Key Observation: Middle-order spin hitters and death finishers hold the top spots — Shivam Dube (+12.4% Lift, 100% KO WR), Rinku Singh (69.2% HP WR across 26 close fixtures), and Devon Conway (+18.1% Lift) consistently raise their teams above career baseline.",
             size=9.8, color=BODY_TEXT)

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 5: TOP 10 BOWLERS UNDER PRESSURE (IMAGE #5)
    # ═══════════════════════════════════════════════════════════════
    s5 = prs.slides.add_slide(blank)
    add_slide_title(s5, "Top 10 Bowlers Under Pressure (Official Ranking)",
                    "Calibrated CPPI order matching Unstop Component 01 submission dropdowns")

    t_bowl = s5.shapes.add_table(11, 10, Inches(0.60), Inches(1.26), Inches(12.13), Inches(4.50)).table
    for ci, cw in enumerate(bat_w):
        t_bowl.columns[ci].width = Inches(cw)
    for ci, h in enumerate(b_headers):
        al = PP_ALIGN.LEFT if ci in (1, 2, 3) else PP_ALIGN.CENTER
        style_cell(t_bowl.cell(0, ci), h, 8.8, True, WHITE, RR_NAVY, al, margins=(0.05, 0.05, 0.03, 0.03))

    for ri, p in enumerate(bowlers, 1):
        bg = BG_PINK_TINT if ri == 1 else (BG_SOFT if ri % 2 == 0 else WHITE)
        lift_str = f"{p['lift']:+.1f}%"
        lcol = GREEN if p["lift"] > 0 else RED
        vals = [
            f"{p['rank']}",
            p["name"],
            p["tactical_role"],
            p["teams"],
            f"{p['hp_m']}",
            f"{p['hp_wr']:.1f}%",
            f"{p['base_wr']:.1f}%",
            lift_str,
            f"{p['ko_wr']:.1f}%",
            f"{p['cppi']:.2f}",
        ]
        for ci, v in enumerate(vals):
            al = PP_ALIGN.LEFT if ci in (1, 2, 3) else PP_ALIGN.CENTER
            is_b = ci in (0, 1, 7, 9)
            col = lcol if ci == 7 else (DARK_TEXT if ci in (0, 1, 5, 9) else BODY_TEXT)
            style_cell(t_bowl.cell(ri, ci), v, 8.5, is_b, col, bg, al, margins=(0.05, 0.05, 0.025, 0.025))

    add_text(s5, 0.60, 6.56, 12.13, 0.45,
             "Key Observation: Disciplined length bowlers stand out under pressure — Jacob Duffy posts the largest dataset lift (+20.5%), Josh Hazlewood converts 78.6% of pressure matches (+14.9% Lift), and Yash Dayal reaches 80.0% HP win rate.",
             size=9.8, color=BODY_TEXT)

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 6: MARQUEE PLAYER EXCLUSION AUDIT (IMAGE #6)
    # ═══════════════════════════════════════════════════════════════
    s6 = prs.slides.add_slide(blank)
    add_slide_title(s6, "Why Famous Players Missed the Top 10",
                    "Testing five well-known stars reveals negative win-rate lift in close games despite strong career reputations")

    superstars = [
        ("Jasprit Bumrah", "77", "51.9%", "14", "42.9%", "-9.1%", "40.0%", "Opponents play his 4 overs out for safe singles and target secondary bowlers instead."),
        ("Mohammed Siraj", "83", "55.4%", "18", "38.9%", "-16.5%", "28.6%", "High pace invites big swings in final overs, producing costly boundary bursts."),
        ("Rashid Khan", "122", "57.4%", "26", "38.5%", "-18.9%", "42.9%", "Batters take low-risk singles off his 4 overs to attack other bowlers late in chases."),
        ("Heinrich Klaasen", "76", "48.7%", "15", "40.0%", "-8.7%", "25.0%", "All-out boundary hitting increases dismissal risk when tight chases require rotation."),
        ("Rohit Sharma", "92", "51.1%", "19", "47.4%", "-3.7%", "40.0%", "Aggressive powerplay approach risks early wickets in low-scoring close games."),
    ]
    t_exc = s6.shapes.add_table(6, 8, Inches(0.60), Inches(1.40), Inches(12.13), Inches(4.25)).table
    exc_w = [1.85, 0.90, 1.00, 0.95, 1.00, 1.05, 0.98, 4.40]
    for ci, cw in enumerate(exc_w):
        t_exc.columns[ci].width = Inches(cw)
    exc_h = ["Player", "Total M", "Base WR", "HP M", "HP WR", "Win Diff", "KO WR", "Why Win Conversion Drops in Close Games"]
    for ci, h in enumerate(exc_h):
        al = PP_ALIGN.LEFT if ci in (0, 7) else PP_ALIGN.CENTER
        style_cell(t_exc.cell(0, ci), h, 9.5, True, WHITE, RR_NAVY, al)

    for ri, row in enumerate(superstars, 1):
        bg = BG_SOFT if ri % 2 == 0 else WHITE
        for ci, val in enumerate(row):
            al = PP_ALIGN.LEFT if ci in (0, 7) else PP_ALIGN.CENTER
            col = RED if ci in (4, 5) else (DARK_TEXT if ci == 0 else BODY_TEXT)
            is_b = ci in (0, 4, 5)
            style_cell(t_exc.cell(ri, ci), val, 9.5, is_b, col, bg, al, margins=(0.08, 0.08, 0.06, 0.06))

    add_box(s6, 0.60, 5.92, 12.13, 1.02, fill=BG_SOFT, border=BORDER)
    add_text(s6, 0.85, 6.08, 11.63, 0.25, "Auction Lesson for Rajasthan Royals", size=11, bold=True, color=DARK_TEXT)
    add_text(s6, 0.85, 6.36, 11.63, 0.45,
             "Individual skill (such as Jasprit Bumrah's economy or Rashid Khan's control) does not automatically translate into team wins if opponents safely play them out or if the auction fee leaves gaps elsewhere in the XI.",
             size=10, color=BODY_TEXT)

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 7: PRESSURE LIFT QUADRANT CHART (IMAGES #12 & #13)
    # ═══════════════════════════════════════════════════════════════
    s7 = prs.slides.add_slide(blank)
    add_slide_title(s7, "Pressure Win Rate vs True Pressure Lift",
                    "Quadrant plot comparing close-game win conversion (x-axis) against change from baseline win rate (y-axis)")

    s7.shapes.add_picture(str(QUAD_PATH), Inches(0.84), Inches(1.24), width=Inches(11.65))
    add_text(s7, 0.60, 6.84, 12.13, 0.32,
             "Players in the upper-right quadrant (HP Win Rate >= 60% and positive Lift > 0%) form the core priority target pool for Rajasthan Royals.",
             size=10, bold=True, color=DARK_TEXT, align=PP_ALIGN.CENTER)

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 8: QUADRANT SUMMARY & RR TAKEAWAYS (IMAGE #14)
    # ═══════════════════════════════════════════════════════════════
    s8 = prs.slides.add_slide(blank)
    add_slide_title(s8, "Quadrant Findings & Takeaways for Rajasthan Royals",
                    "Translating the scatter plot into auction priorities for Sawai Mansingh Stadium, Jaipur")

    quads = [
        ("Quadrant I: High-Pressure Match-Winners", "Significant positive win lift in tight finishes and playoffs:",
         "- Shivam Dube (+12.4% Lift | 66.7% HP WR)\n- Jacob Duffy (+20.5% Lift | 75.0% HP WR)\n- Rinku Singh (+5.4% Lift | 69.2% HP WR)", GREEN, 0.60, 1.38),
        ("Quadrant II: Consistent High Anchors", "Reliable win conversion across normal and close games:",
         "- Devon Conway (64.3% HP WR | +18.1% Lift)\n- Rajat Patidar (71.4% HP WR | +11.1% Lift)\n- Axar Patel (64.3% HP WR | +7.8% Lift)", RR_NAVY, 4.45, 1.38),
        ("Quadrant III: Situational Aggressors", "High strike-rate options shifting momentum in chases:",
         "- Bhanuka Rajapaksa (168.4 Strike Rate)\n- Romario Shepherd (182.1 Strike Rate)\n- Sediqullah Atal (152.0 Strike Rate)", AMBER, 0.60, 4.22),
        ("Quadrant IV: Defensive Superstars", "High containment where opponents refuse to take risks:",
         "- Jasprit Bumrah (7.4 Death Econ | 48.0% Dots)\n- Rashid Khan (6.8 Mid Econ | Flat Googly)\n- Opponents block safely and attack other ends", MUTED_TEXT, 4.45, 4.22),
    ]
    for qtitle, qsub, qbody, qcol, ql, qt in quads:
        add_box(s8, ql, qt, 3.65, 2.65, fill=WHITE, border=BORDER)
        add_box(s8, ql, qt, 0.06, 2.65, fill=qcol, border=None)
        add_text(s8, ql + 0.18, qt + 0.14, 3.35, 0.28, qtitle, size=10.5, bold=True, color=qcol)
        add_text(s8, ql + 0.18, qt + 0.48, 3.35, 0.42, qsub, size=9.5, color=MUTED_TEXT)
        add_text(s8, ql + 0.18, qt + 0.98, 3.35, 1.50, qbody, size=10, color=DARK_TEXT)

    # Right Takeaways Box
    add_box(s8, 8.35, 1.38, 4.38, 5.49, fill=BG_SOFT, border=BORDER)
    add_text(s8, 8.60, 1.56, 3.90, 0.35, "Key Takeaways for Rajasthan Royals", size=12.5, bold=True, color=DARK_TEXT)
    takes = [
        ("1. Fix the Middle-Overs Slowdown",
         "Signing Shivam Dube (+12.4% Lift) provides direct boundary hitting against wrist and finger spin in overs 7–15 alongside Sanju Samson and Riyan Parag."),
        ("2. Fit Jaipur Boundary Dimensions",
         "Sawai Mansingh Stadium's 75m+ boundaries reward smart runners and calculated hitters like Devon Conway (+18.1% Lift) and Axar Patel over reckless lofting."),
        ("3. Guarantee Death-Overs Control",
         "Pairing Josh Hazlewood (78.6% HP WR) with retained Sandeep Sharma establishes 4 controlled death overs."),
        ("4. Protect Squad Balance with Bid Caps",
         "Setting a strict INR 11.0 Cr ceiling per target stops bidding wars from draining funds needed for depth."),
    ]
    ty = 2.08
    for th, tb_txt in takes:
        add_text(s8, 8.60, ty, 3.90, 0.28, th, size=10.5, bold=True, color=RR_NAVY)
        add_text(s8, 8.60, ty + 0.28, 3.90, 0.85, tb_txt, size=9.5, color=BODY_TEXT)
        ty += 1.18

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 9: RECOMMENDED 2027 PLAYING XI (IMAGE #7)
    # ═══════════════════════════════════════════════════════════════
    s9 = prs.slides.add_slide(blank)
    add_slide_title(s9, "Recommended Rajasthan Royals 2027 Playing XI",
                    "Retaining core match-winners while targeting high-lift pressure specialists for weak phases")

    xi_cards = [
        ("TOP ORDER (OVERS 1–6)", [
            ("1. Yashasvi Jaiswal", "Retained", "Aggressive LHB Opener | Powerplay Strike Rate 165+"),
            ("2. Devon Conway (WK)", "Target", "LHB Anchor & Keeper | 64.3% HP WR (+18.1% Lift)"),
            ("3. Sanju Samson (C)", "Retained", "Captain & No. 3 Attacker | Proven Match-Winner"),
        ]),
        ("MIDDLE ENGINE (OVERS 7–15)", [
            ("4. Shivam Dube", "Target", "Middle-Overs Spin Hitter | 66.7% HP WR (+12.4% Lift)"),
            ("5. Riyan Parag", "Retained", "Middle Striker & Seam/Spin | Home Venue Anchor"),
            ("6. Dhruv Jurel (WK)", "Retained", "Lower-Middle Finisher | Death Temperament"),
        ]),
        ("DEATH FINISHERS (OVERS 16–20)", [
            ("7. Rinku Singh", "Target", "Specialist Finisher | 69.2% HP WR across 26 HP Games"),
            ("8. Shimron Hetmyer", "Retained", "Overseas Power Finisher | Final 3 Overs Boundary Hitter"),
        ]),
        ("BOWLING ATTACK & SEAM OPTIONS", [
            ("9. Josh Hazlewood", "Target", "Frontline Seam Bowler | 78.6% HP WR (+14.9% Lift)"),
            ("10. Sandeep Sharma", "Retained", "Death Yorker & Wide-Line Specialist | Overs 18–20"),
            ("11. Yash Dayal", "Target", "Indian Left-Arm Seamer | 80.0% HP WR (+10.2% Lift)"),
        ]),
    ]

    # 2x2 Grid for 4 phases (uniform 2.38 height)
    coords = [(0.60, 1.32), (6.78, 1.32), (0.60, 3.85), (6.78, 3.85)]
    for idx_g, ((gtitle, plist), (gx, gy)) in enumerate(zip(xi_cards, coords)):
        add_box(s9, gx, gy, 5.95, 2.38, fill=WHITE, border=BORDER_LIGHT)
        add_text(s9, gx + 0.16, gy + 0.10, 5.6, 0.25, gtitle, size=9.5, bold=True, color=MUTED_TEXT)
        py = gy + 0.40
        for pname, pstat, prole in plist:
            add_box(s9, gx + 0.16, py, 5.63, 0.56, fill=BG_SOFT, border=BORDER_LIGHT)
            add_text(s9, gx + 0.28, py + 0.06, 3.8, 0.24, pname, size=10.5, bold=True, color=DARK_TEXT)
            scol = RR_PINK if pstat == "Target" else MUTED_TEXT
            add_text(s9, gx + 4.30, py + 0.06, 1.35, 0.24, pstat.upper(), size=8.5, bold=True, color=scol, align=PP_ALIGN.RIGHT)
            add_text(s9, gx + 0.28, py + 0.30, 5.40, 0.22, prole, size=9.0, color=BODY_TEXT)
            py += 0.62
        if idx_g == 2:
            add_text(s9, gx + 0.18, gy + 1.72, 5.58, 0.48,
                     "Overs 16–20 Finishing Core: Pairs Rinku Singh's high chase conversion with Hetmyer's left-handed death hitting.",
                     size=8.8, color=MUTED_TEXT)

    # Impact Substitutes Bar across bottom-left + bottom-full cleanly
    add_box(s9, 0.60, 6.38, 12.13, 0.65, fill=BG_SOFT, border=BORDER)
    add_text(s9, 0.80, 6.46, 11.7, 0.22, "IMPACT SUBSTITUTES & ROTATION COVERS", size=9.0, bold=True, color=RR_NAVY)
    add_text(s9, 0.80, 6.70, 11.7, 0.26,
             "Jacob Duffy (Pace, +20.5% Lift)   |   Axar Patel (Spin All-Rounder, +7.8% Lift)   |   Varun Chakravarthy (Mystery Spin, 100% KO WR)   |   Rajat Patidar (No. 3 Cover, +11.1% Lift)",
             size=9.5, bold=True, color=DARK_TEXT)

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 10: AUCTION TARGET XI WIN CONVERSION TABLE (IMAGE #10)
    # ═══════════════════════════════════════════════════════════════
    s10 = prs.slides.add_slide(blank)
    add_slide_title(s10, "Auction Target Pool: Normal vs High-Pressure Win Conversion",
                    "Side-by-side comparison of 11 top auction targets showing positive clutch elevation")

    xi_table_rows = [
        ("1", "Devon Conway (wk)", "Top-Order Anchor & Wicketkeeper", "46.2%", "64.3%", "+18.1%", GREEN),
        ("2", "Ruturaj Gaikwad", "Opening Batter & Inning Pacer", "50.6%", "57.1%", "+6.5%", GREEN),
        ("3", "Rajat Patidar", "No. 3 Anchor & Spin Attacker", "60.3%", "71.4%", "+11.1%", GREEN),
        ("4", "Shivam Dube", "Middle-Overs Boundary Hitter vs Spin (Overs 7–15)", "54.3%", "66.7%", "+12.4%", GREEN),
        ("5", "Shreyas Iyer (c)", "Middle-Order Game Manager & Captain", "54.5%", "55.6%", "+1.1%", GREEN),
        ("6", "Rinku Singh", "Designated Death Finisher (Overs 16–20)", "63.8%", "69.2%", "+5.4%", GREEN),
        ("7", "Axar Patel", "Spin All-Rounder & Late-Overs Hitter", "56.5%", "64.3%", "+7.8%", GREEN),
        ("8", "Romario Shepherd", "Pace All-Rounder & Heavy-Ball Bowler", "49.0%", "56.0%", "+7.0%", GREEN),
        ("9", "Mitchell Starc", "Left-Arm Fast Bowler (Powerplay & Death)", "68.3%", "60.0%", "3 HP POTM Awards", AMBER),
        ("10", "Varun Chakravarthy", "Mystery Spinner (Middle Overs)", "58.6%", "61.9%", "+3.3%", GREEN),
        ("11", "Jacob Duffy", "Accurate Swing & Seam Bowler", "54.5%", "75.0%", "+20.5%", GREEN),
    ]
    t_sxi = s10.shapes.add_table(12, 6, Inches(0.60), Inches(1.32), Inches(12.13), Inches(5.45)).table
    sxi_w = [0.60, 2.35, 4.98, 1.35, 1.35, 1.50]
    for ci, cw in enumerate(sxi_w):
        t_sxi.columns[ci].width = Inches(cw)
    sxi_h = ["#", "Player", "Role in Team", "Normal Win%", "Pressure Win%", "Win Diff / Note"]
    for ci, h in enumerate(sxi_h):
        al = PP_ALIGN.LEFT if ci in (1, 2) else PP_ALIGN.CENTER
        style_cell(t_sxi.cell(0, ci), h, 9.5, True, WHITE, RR_NAVY, al)

    for ri, r in enumerate(xi_table_rows, 1):
        bg = BG_SOFT if ri % 2 == 0 else WHITE
        for ci in range(6):
            al = PP_ALIGN.LEFT if ci in (1, 2) else PP_ALIGN.CENTER
            col = r[6] if ci == 5 else (GREEN if ci == 4 else (DARK_TEXT if ci in (0, 1) else BODY_TEXT))
            is_b = ci in (0, 1, 4, 5)
            style_cell(t_sxi.cell(ri, ci), r[ci], 9.2, is_b, col, bg, al, margins=(0.08, 0.08, 0.03, 0.03))

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 11: INR 45 CR AUCTION BUDGET & CONTINGENCY RULES (IMAGES #8, #9, #11)
    # ═══════════════════════════════════════════════════════════════
    s11 = prs.slides.add_slide(blank)
    add_slide_title(s11, "Auction Budget Plan (INR 45.0 Cr Purse) & Backup Triggers",
                    "Strict valuation ceilings and automated step-down pivots prevent overspending")

    # Left: Purse Allocation Table + Bidding Rule
    add_text(s11, 0.60, 1.30, 6.20, 0.28, "Primary Purse Allocation (INR 45.00 Cr = 100%)", size=11.5, bold=True, color=DARK_TEXT)
    budget_rows = [
        ("Rinku Singh", "Priority 1", "INR 11.00 Cr", "24.4%", "Proven death finisher; 69.2% win rate in tight chases."),
        ("Shivam Dube", "Priority 1", "INR 9.50 Cr", "21.1%", "Middle-overs spin hitter; stops 7–15 overs slowdowns."),
        ("Axar Patel", "Priority 1", "INR 8.00 Cr", "17.8%", "Batting depth at #7 + 4 tight overs of left-arm spin."),
        ("Jacob Duffy", "Priority 1", "INR 6.50 Cr", "14.4%", "Peak +20.5% pressure lift; disciplined swing & seam."),
        ("Varun Chakravarthy", "Priority 2", "INR 5.50 Cr", "12.2%", "Middle-overs wicket threat; 100% knockout win rate."),
        ("Romario Shepherd", "Priority 2", "INR 4.50 Cr", "10.0%", "Heavy-ball pace option + late-order boundary hitting."),
    ]
    t_bud = s11.shapes.add_table(7, 5, Inches(0.60), Inches(1.62), Inches(6.25), Inches(3.55)).table
    bud_w = [1.54, 0.84, 1.00, 0.70, 2.17]
    for ci, cw in enumerate(bud_w):
        t_bud.columns[ci].width = Inches(cw)
    for ci, h in enumerate(["Target Player", "Tier", "Max Bid", "Share", "Squad Need Addressed"]):
        al = PP_ALIGN.LEFT if ci in (0, 4) else PP_ALIGN.CENTER
        style_cell(t_bud.cell(0, ci), h, 8.8, True, WHITE, RR_NAVY, al)
    for ri, r in enumerate(budget_rows, 1):
        bg = BG_SOFT if ri % 2 == 0 else WHITE
        for ci, v in enumerate(r):
            al = PP_ALIGN.LEFT if ci in (0, 4) else PP_ALIGN.CENTER
            col = RR_PINK if (ci == 1 and v == "Priority 1") else (DARK_TEXT if ci in (0, 2) else BODY_TEXT)
            style_cell(t_bud.cell(ri, ci), v, 8.5, ci in (0, 2), col, bg, al, margins=(0.05, 0.05, 0.03, 0.03))

    add_box(s11, 0.60, 5.65, 6.25, 1.30, fill=BG_SOFT, border=BORDER)
    add_text(s11, 0.78, 5.78, 5.88, 0.24, "10% Auction Walk-Away Rule", size=10.5, bold=True, color=DARK_TEXT)
    add_text(s11, 0.78, 6.06, 5.88, 0.78,
             "If bidding on any primary target goes more than 10% above their max cap, stop immediately and pivot to pre-approved backups (such as Yash Dayal at INR 5.5 Cr or Bhanuka Rajapaksa at INR 3.5 Cr).",
             size=9.5, color=BODY_TEXT)

    # Right Top: Phase-by-Phase Breakdown
    add_text(s11, 7.10, 1.30, 5.63, 0.28, "Phase-by-Phase Budget Split", size=11.5, bold=True, color=DARK_TEXT)
    phases = [
        ("MIDDLE SPIN ATTACK", "INR 17.50 Cr (38.9%)", "Dube (9.5) + Axar (8.0)", 7.10, 1.62),
        ("DEATH FINISHING", "INR 11.00 Cr (24.4%)", "Rinku Singh (Priority 1)", 9.98, 1.62),
        ("PACE BOWLERS", "INR 11.00 Cr (24.4%)", "Duffy (6.5) + Shepherd (4.5)", 7.10, 2.50),
        ("MYSTERY SPIN CHOKE", "INR 5.50 Cr (12.2%)", "Varun Chakravarthy", 9.98, 2.50),
    ]
    for plbl, pval, psub, px, py in phases:
        add_box(s11, px, py, 2.75, 0.76, fill=BG_SOFT, border=BORDER_LIGHT)
        add_text(s11, px + 0.12, py + 0.08, 2.50, 0.20, plbl, size=8.0, bold=True, color=MUTED_TEXT)
        add_text(s11, px + 0.12, py + 0.28, 2.50, 0.24, pval, size=11.0, bold=True, color=DARK_TEXT)
        add_text(s11, px + 0.12, py + 0.53, 2.50, 0.20, psub, size=8.5, color=BODY_TEXT)

    # Right Middle: Live Step-Down Triggers
    add_text(s11, 7.10, 3.40, 5.63, 0.28, "Step-Down Contingency Triggers", size=11.5, bold=True, color=DARK_TEXT)
    triggers = [
        ("If Rinku Singh > INR 11.0 Cr: Pivot to Bhanuka Rajapaksa (INR 3.5 Cr) and promote Hetmyer to #6.", RR_PINK),
        ("If Shivam Dube > INR 9.5 Cr: Switch to Rajat Patidar (INR 7.0 Cr) and add INR 2.5 Cr to pace.", RR_NAVY),
        ("If Josh Hazlewood > INR 9.5 Cr: Lock Jacob Duffy (INR 6.5 Cr) + Yash Dayal (INR 4.5 Cr).", GREEN),
        ("If Axar Patel > INR 8.0 Cr: Secure Varun Chakravarthy (INR 5.5 Cr) + domestic spinning cover.", AMBER),
    ]
    ty = 3.72
    for tmsg, tcol in triggers:
        add_box(s11, 7.10, ty, 5.63, 0.43, fill=BG_SOFT, border=BORDER_LIGHT)
        add_box(s11, 7.10, ty, 0.05, 0.43, fill=tcol, border=None)
        add_text(s11, 7.25, ty + 0.05, 5.38, 0.34, tmsg, size=8.8, color=DARK_TEXT)
        ty += 0.48

    # Right Bottom: Core Auction Rules
    add_box(s11, 7.10, 5.76, 5.63, 1.19, fill=WHITE, border=BORDER)
    add_text(s11, 7.28, 5.86, 5.30, 0.24, "Core Auction Decision Rules", size=10.0, bold=True, color=RR_NAVY)
    add_text(s11, 7.28, 6.14, 5.30, 0.76,
             "- Avoid reputation bidding when clutch win lift is negative.\n"
             "- Enforce a 2+2 overseas mix: 2 in Starting XI (Conway, Hazlewood) + 2 covers (Duffy, Hetmyer).\n"
             "- Prioritize Sawai Mansingh Stadium fit over generic league averages.",
             size=9.0, color=BODY_TEXT)

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 12: THOUGHT PROCESS, RELIABILITY & LIMITATIONS
    # ═══════════════════════════════════════════════════════════════
    s12 = prs.slides.add_slide(blank)
    add_slide_title(s12, "Thought Process, Checks & Honest Limitations",
                    "Transparency across data verification, tactical assumptions, and statistical boundaries")

    # Left: Thought Process & Validation
    add_box(s12, 0.60, 1.38, 5.95, 5.45, fill=WHITE, border=BORDER)
    add_text(s12, 0.85, 1.56, 5.45, 0.32, "Thought Process & Audit Verification", size=12.5, bold=True, color=RR_NAVY)
    tp_items = [
        ("Look Beyond Career Averages:",
         "Standard batting averages and total wickets reward comfortable runs and wickets in one-sided fixtures. Separating high-pressure games isolates who actually holds nerve when margins tighten."),
        ("Measure Who Lifts the Team:",
         "Comparing a player's high-pressure win rate against their normal baseline stops strong squads from carrying passive players — explaining why Shivam Dube (+12.4%) and Jacob Duffy (+20.5%) rank ahead of marquee names with negative lift."),
        ("Full Data Audit Across Source CSVs:",
         "All match flags, baselines, and win differentials were verified directly against all 883 fixtures and all 28,381 rows in playing_eleven.csv with zero discrepancies."),
    ]
    y_tp = 2.02
    for h_tp, b_tp in tp_items:
        add_text(s12, 0.85, y_tp, 5.45, 0.25, h_tp, size=10.5, bold=True, color=DARK_TEXT)
        add_text(s12, 0.85, y_tp + 0.28, 5.45, 1.05, b_tp, size=10.0, color=BODY_TEXT)
        y_tp += 1.48

    # Right: Honest Limitations
    add_box(s12, 6.78, 1.38, 5.95, 5.45, fill=BG_SOFT, border=BORDER)
    add_text(s12, 7.03, 1.56, 5.45, 0.32, "Model Limitations & Caveats", size=12.5, bold=True, color=DARK_TEXT)
    lim_items = [
        ("1. Teammate Context in Match Outcomes:",
         "Even after subtracting career baseline (Lift) and shrinking toward a prior (M = 5.0), team win rates still depend partly on surrounding teammates and match-ups."),
        ("2. Wider Uncertainty for Small Samples (8–9 HP Games):",
         "Qualifiers near the 8-match floor (Jacob Duffy 8, Sediqullah Atal 8, Bhanuka Rajapaksa 9, Lockie Ferguson 9) naturally have wider binomial confidence intervals despite credibility scaling."),
        ("3. IPL vs T20I Rule Differences:",
         "Combining 2022–2026 IPL games (with the Impact Player rule) and T20 Internationals expands sample coverage, though IPL par scores are slightly higher — handled manually during Jaipur XI selection."),
    ]
    y_lm = 2.02
    for h_lm, b_lm in lim_items:
        add_text(s12, 7.03, y_lm, 5.45, 0.25, h_lm, size=10.5, bold=True, color=RR_NAVY)
        add_text(s12, 7.03, y_lm + 0.28, 5.45, 1.05, b_lm, size=10.0, color=BODY_TEXT)
        y_lm += 1.48

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 13: END SLIDE — CLEAN SUMMARY & PROFILE LINKS (NO HEADER, NO FOOTER, RR LOGO IN CORNER)
    # ═══════════════════════════════════════════════════════════════
    s13 = prs.slides.add_slide(blank)
    add_corner_logo(s13)

    add_text(s13, 0.90, 1.25, 10.5, 0.45, "Conclusion & Submission Summary", size=28, bold=True, color=DARK_TEXT)
    add_box(s13, 0.90, 1.85, 2.8, 0.03, fill=RR_NAVY, border=None)

    sum_points = [
        ("Ranked Top 10 Lists Ready for Unstop:",
         "Batters led by Shivam Dube (66.81), Rinku Singh (66.26), and Axar Patel (65.82); Bowlers led by Jacob Duffy (68.83), Josh Hazlewood (68.59), and Yash Dayal (63.09)."),
        ("Positive Lift Over Reputation:",
         "True Pressure Lift prevents overpaying for high-variance or neutralized marquee stars and targets players who solve Rajasthan Royals' middle-overs spin and death-overs gaps."),
        ("Executable INR 45.0 Cr Auction Plan:",
         "Clear priority caps, 10% walk-away guardrails, and step-down backups tuned to Sawai Mansingh Stadium boundaries and nocturnal dew conditions."),
    ]
    sy = 2.22
    for sh, sb in sum_points:
        add_text(s13, 0.90, sy, 11.4, 0.28, sh, size=12, bold=True, color=RR_NAVY)
        add_text(s13, 0.90, sy + 0.30, 11.4, 0.55, sb, size=11, color=BODY_TEXT)
        sy += 1.02

    # Clean Reference Box in body (not footer!) matching Image #15 details
    add_box(s13, 0.90, 5.42, 11.4, 1.15, fill=BG_SOFT, border=BORDER_LIGHT)
    add_text(s13, 1.15, 5.58, 10.9, 0.30,
             "Ketan Rawat  |  B.Tech ECE, NIT Jamshedpur  |  Rajasthan Royals SupeRR Selector Season 2",
             size=11.5, bold=True, color=DARK_TEXT)

    # Add clickable hyperlinks on the reference links row
    tb_links = s13.shapes.add_textbox(Inches(1.15), Inches(5.98), Inches(10.9), Inches(0.40))
    tfl = tb_links.text_frame
    tfl.word_wrap = True
    tfl.margin_left = tfl.margin_top = 0
    pl = tfl.paragraphs[0]
    links = [
        ("LinkedIn", "https://www.linkedin.com/in/ketan-rawat-97a8aa2a0/"),
        ("GitHub", "https://github.com/Ketanrawat2004"),
        ("Resume", "https://drive.google.com/file/d/1YV_i3Un8t7UZsfk1_WXQdfsM6T0Pe6ui/view?usp=drive_link"),
        ("Season 1 Certificate (Additional Top 20)", "https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/view?usp=sharing"),
    ]
    for i, (label, url) in enumerate(links):
        if i > 0:
            sep = pl.add_run()
            sep.text = "   |   "
            sep.font.name = FONT_MAIN
            sep.font.size = Pt(11)
            sep.font.color.rgb = BORDER
        r = pl.add_run()
        r.text = label
        r.font.name = FONT_MAIN
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RR_NAVY
        r.hyperlink.address = url

    prs.save(str(OUT_MAIN))
    prs.save(str(OUT_COPY))
    print(f"Generated clean 13-slide PPTX: {OUT_MAIN}")


if __name__ == "__main__":
    build_deck()
