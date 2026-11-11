import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = Path(r"C:\Rajasthan Royals")
OUTPUT_DIR = BASE_DIR / "pressure_output"
PDF_PATH = BASE_DIR / "RR_SupeRR_Selector_Season2_Report_Ketan_Rawat.pdf"
CHART2_PATH = OUTPUT_DIR / "chart_02_pressure_lift_quadrants.png"

# RR Brand Colors
RR_PINK = colors.HexColor("#E91E8C")
RR_BLUE = colors.HexColor("#0F1F38")
RR_NAVY = colors.HexColor("#0A1424")
RR_GOLD = colors.HexColor("#FFD700")
RR_CYAN = colors.HexColor("#00B0FF")
DARK_GRAY = colors.HexColor("#1E293B")
LIGHT_GRAY = colors.HexColor("#F8FAFC")
BORDER_COLOR = colors.HexColor("#CBD5E1")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(RR_PINK)
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 812, "RAJASTHAN ROYALS WAR ROOM")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(185, 812, "|  SupeRR Selector Season 2 — Pressure Performance Analytics")
            self.setStrokeColor(RR_PINK)
            self.setLineWidth(0.8)
            self.line(40, 806, 555, 806)
        
        # Footer
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(40, 38, 555, 38)
        
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(RR_BLUE)
        self.drawString(40, 26, "ANALYST: KETAN RAWAT (NIT JAMSHEDPUR)")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(240, 26, "Confidential — Prepared for Rajasthan Royals War Room")
        self.drawRightString(555, 26, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def generate_pdf():
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=38,
        rightMargin=38,
        topMargin=36,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=23,
        textColor=RR_PINK,
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=RR_GOLD,
        spaceAfter=5
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14.5,
        textColor=RR_BLUE,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=RR_PINK,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=10,
        firstLineIndent=-7,
        spaceAfter=1.8
    )

    table_header_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_cell_bold = ParagraphStyle(
        'TDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_cell_center = ParagraphStyle(
        'TDCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.5,
        alignment=1
    )

    story = []

    # ═══════════════════════════════════════════════════════════
    # PAGE 1: COVER, EXECUTIVE SUMMARY, MLI & CPPI FORMULATION
    # ═══════════════════════════════════════════════════════════
    story.append(Paragraph("RAJASTHAN ROYALS WAR ROOM", title_style))
    story.append(Paragraph("SupeRR Selector Season 2 — Round 1 Master Submission", subtitle_style))
    story.append(Paragraph(
        "<b>Challenge:</b> Identifying the Most Reliable Players Under Pressure &nbsp;|&nbsp; "
        "<b>Analyst:</b> Ketan Rawat (B.Tech ECE, NIT Jamshedpur) &nbsp;|&nbsp; "
        "<b>Scope:</b> 883 Matches (IPL 2022–2026 + T20Is)",
        ParagraphStyle('Meta', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=colors.HexColor("#475569"))
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=RR_PINK, spaceBefore=4, spaceAfter=6))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary & The Core Problem", h1_style))
    story.append(Paragraph(
        "In modern franchise T20 cricket, silverware is decided in moments of acute leverage: defending 12 runs off the final over of an IPL Qualifier, pacing a tense chase at 10.5 RRR with 4 wickets down, or dismantling bowling attacks under scoreboard pressure. Traditional raw aggregates (runs, wickets, strike rates) fail because they suffer from <b>reputational and context bias</b> — 50 runs scored in a low-stakes dead rubber are weighted identically to 50 runs scored in an IPL Final.",
        body_style
    ))
    story.append(Paragraph(
        "To solve this, our analytical cell constructed the <b>Composite Pressure Performance Index (CPPI)</b>, calibrated across <b>883 matches</b> (IPL 2022–2026 and T20Is 2022–2026). The system isolates <b>178 High-Pressure (HP) fixtures</b> (20.2% highest leverage games) using a four-dimensional Match Leverage Index, applies <b>Empirical Bayes shrinkage</b> to handle sample variability, computes a player's <b>True Pressure Lift (&Delta;)</b> to identify who genuinely elevates under stress, and enforces an <b>IPL Auction Regulatory Realism Filter</b> to ensure all targets are 100% eligible for Rajasthan Royals' IPL 2027 auction.",
        body_style
    ))

    # 2. Match Leverage Index
    story.append(Paragraph("2. Defining Pressure: The Match Leverage Index (MLI)", h1_style))
    story.append(Paragraph(
        "Pressure is defined along four orthogonal axes representing match stakes, contest closeness, elimination jeopardy, and external disruptions:",
        body_style
    ))

    mli_data = [
        [Paragraph("Axis", table_header_style), Paragraph("Dimension", table_header_style), Paragraph("Weight", table_header_style), Paragraph("Operational Scoring Logic & Tactical Rationale", table_header_style)],
        [Paragraph("<b>Axis 1</b>", table_cell_center), Paragraph("Stage Stakes", table_cell_bold), Paragraph("0–40 pts", table_cell_center), Paragraph("<b>Final:</b> 40 | <b>Semi-Final:</b> 35 | <b>Qualifier/Eliminator:</b> 30 | <b>Super 4:</b> 20 | <b>League:</b> 5. Single-elimination matches carry extreme psychological weight and zero margin for error.", table_cell_style)],
        [Paragraph("<b>Axis 2</b>", table_cell_center), Paragraph("Contest Closeness", table_cell_bold), Paragraph("0–40 pts", table_cell_center), Paragraph("<b>Super Over/Tie:</b> 40 | <b>Margin &le;5 runs or 1 wkt:</b> 38 | <b>Margin &le;10 runs or 2 wkts:</b> 32 | <b>Margin &le;15 runs or 3 wkts:</b> 26. Tense finishes mean every single delivery shifts win probability exponentially.", table_cell_style)],
        [Paragraph("<b>Axis 3</b>", table_cell_center), Paragraph("Elimination Stakes", table_cell_bold), Paragraph("0–20 pts", table_cell_center), Paragraph("<b>Knockout Flag = +20 pts.</b> Binary consequence games trigger heightened physiological stress, separating clutch composure from reputational inflation.", table_cell_style)],
        [Paragraph("<b>Axis 4</b>", table_cell_center), Paragraph("Target Disruption", table_cell_bold), Paragraph("0–5 pts", table_cell_center), Paragraph("<b>DLS / Revised Target = +5 pts.</b> Sudden over reductions and accelerated target recalculations introduce tactical chaos and condensed decision windows.", table_cell_style)],
    ]
    t_mli = Table(mli_data, colWidths=[42, 85, 52, 340])
    t_mli.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RR_BLUE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_mli)
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>High-Pressure Classification:</b> Any match with <b>MLI &ge; 30 points</b> is classified as High Pressure (178 matches / 20.2% of dataset).", bullet_style))

    # 3. CPPI Formulation
    story.append(Paragraph("3. Calibrated Composite Pressure Performance Index (CPPI)", h1_style))
    story.append(Paragraph(
        "<b>Calibrated CPPI Master Equation:</b><br/>"
        "<code>CPPI = [ 0.35 &times; Bayes_HP_WR + 0.25 &times; Lift_norm + 0.20 &times; Bayes_KO_WR + 0.10 &times; MOM_HP + 0.10 &times; Base_WR ] &times; Credibility(n_HP)</code>",
        ParagraphStyle('Formula', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=RR_BLUE, backColor=LIGHT_GRAY, borderPadding=4, spaceAfter=4)
    ))
    story.append(Paragraph("• <b>Bayesian Win Rate (35%):</b> Regularizes high-pressure win rates using career baseline as conjugate prior with pseudo-weight M = 5.0 matches.", bullet_style))
    story.append(Paragraph("• <b>True Clutch Elevation Lift &Delta; (25%, calibrated from 15%):</b> <code>(HP_WR &minus; Base_WR)</code>. Strongly rewards players who elevate their win rate above baseline under stress, preventing unearned reputation riding on powerhouse teams.", bullet_style))
    story.append(Paragraph("• <b>Bayesian Knockout Win Rate (20%):</b> Direct empirical measure of performance in sudden-death knockout matches.", bullet_style))
    story.append(Paragraph("• <b>Clutch MOM Density (10%, calibrated from 20%):</b> Player of the Match awards in HP fixtures; dampened to prevent small-sample media award bias.", bullet_style))
    story.append(Paragraph("• <b>Sample Credibility & Regulatory Filter:</b> Sigmoid curve saturating at ~15 HP matches: <code>0.85 + 0.15 / [1 + exp(-0.25 &times; (n_HP &minus; 8))]</code>. Excludes Pakistani players per BCCI IPL auction bylaws, ensuring 100% executable targets for Rajasthan Royals.", bullet_style))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # PAGE 2: OFFICIAL PLAYER RANKINGS (TOP 10 BATTERS & BOWLERS)
    # ═══════════════════════════════════════════════════════════
    story.append(Paragraph("4. Official Player Rankings (Unstop Submission Dropdowns)", h1_style))
    story.append(Paragraph(
        "Eligible players met a rigorous sample-size threshold: minimum <b>12 total matches</b> and minimum <b>8 high-pressure matches</b>. Role classification was strictly enforced using empirical batting orders (Batters &le; 6.3 avg order / WK; Bowlers &ge; 8.2 avg order) to guarantee zero positional cross-contamination, filtered for 100% IPL Auction Eligibility.",
        body_style
    ))

    story.append(Paragraph("TOP 10 BATTERS UNDER PRESSURE (CALIBRATED IPL AUCTION TARGETS)", h2_style))
    batters_table = [
        [Paragraph("Rank", table_header_style), Paragraph("Player Name", table_header_style), Paragraph("Teams / Franchise", table_header_style), Paragraph("HP M", table_header_style), Paragraph("HP WR", table_header_style), Paragraph("Pressure Lift (&Delta;)", table_header_style), Paragraph("HP MOM", table_header_style), Paragraph("KO WR", table_header_style), Paragraph("CPPI", table_header_style)],
        [Paragraph("<b>1</b>", table_cell_center), Paragraph("<b>Shivam Dube</b>", table_cell_bold), Paragraph("Chennai Super Kings, India", table_cell_style), Paragraph("18", table_cell_center), Paragraph("66.7%", table_cell_center), Paragraph("<font color='#00C853'><b>+12.4%</b></font>", table_cell_center), Paragraph("1", table_cell_center), Paragraph("<b>100.0%</b>", table_cell_center), Paragraph("<b>66.81</b>", table_cell_center)],
        [Paragraph("<b>2</b>", table_cell_center), Paragraph("<b>Rinku Singh</b>", table_cell_bold), Paragraph("India, Kolkata Knight Riders", table_cell_style), Paragraph("26", table_cell_center), Paragraph("69.2%", table_cell_center), Paragraph("<font color='#00C853'><b>+5.4%</b></font>", table_cell_center), Paragraph("1", table_cell_center), Paragraph("<b>100.0%</b>", table_cell_center), Paragraph("<b>66.26</b>", table_cell_center)],
        [Paragraph("<b>3</b>", table_cell_center), Paragraph("<b>Axar Patel</b>", table_cell_bold), Paragraph("Delhi Capitals, India", table_cell_style), Paragraph("28", table_cell_center), Paragraph("64.3%", table_cell_center), Paragraph("<font color='#00C853'><b>+7.8%</b></font>", table_cell_center), Paragraph("2", table_cell_center), Paragraph("<b>100.0%</b>", table_cell_center), Paragraph("<b>65.82</b>", table_cell_center)],
        [Paragraph("<b>4</b>", table_cell_center), Paragraph("<b>Rajat Patidar</b>", table_cell_bold), Paragraph("Royal Challengers Bengaluru", table_cell_style), Paragraph("14", table_cell_center), Paragraph("71.4%", table_cell_center), Paragraph("<font color='#00C853'><b>+11.1%</b></font>", table_cell_center), Paragraph("2", table_cell_center), Paragraph("71.4%", table_cell_center), Paragraph("<b>64.26</b>", table_cell_center)],
        [Paragraph("<b>5</b>", table_cell_center), Paragraph("<b>Ruturaj Gaikwad</b>", table_cell_bold), Paragraph("Chennai Super Kings, India", table_cell_style), Paragraph("14", table_cell_center), Paragraph("57.1%", table_cell_center), Paragraph("<font color='#00C853'>+6.5%</font>", table_cell_center), Paragraph("2", table_cell_center), Paragraph("<b>100.0%</b>", table_cell_center), Paragraph("<b>62.41</b>", table_cell_center)],
        [Paragraph("<b>6</b>", table_cell_center), Paragraph("<b>Devon Conway</b>", table_cell_bold), Paragraph("Chennai Super Kings, New Zealand", table_cell_style), Paragraph("14", table_cell_center), Paragraph("64.3%", table_cell_center), Paragraph("<font color='#00C853'><b>+18.1%</b></font>", table_cell_center), Paragraph("2", table_cell_center), Paragraph("66.7%", table_cell_center), Paragraph("<b>61.97</b>", table_cell_center)],
        [Paragraph("<b>7</b>", table_cell_center), Paragraph("<b>Virat Kohli</b>", table_cell_bold), Paragraph("India, Royal Challengers Bengaluru", table_cell_style), Paragraph("20", table_cell_center), Paragraph("70.0%", table_cell_center), Paragraph("<font color='#00C853'>+7.6%</font>", table_cell_center), Paragraph("1", table_cell_center), Paragraph("71.4%", table_cell_center), Paragraph("<b>61.47</b>", table_cell_center)],
        [Paragraph("<b>8</b>", table_cell_center), Paragraph("<b>Bhanuka Rajapaksa</b>", table_cell_bold), Paragraph("Punjab Kings, Sri Lanka", table_cell_style), Paragraph("9", table_cell_center), Paragraph("66.7%", table_cell_center), Paragraph("<font color='#00C853'><b>+10.4%</b></font>", table_cell_center), Paragraph("1", table_cell_center), Paragraph("<b>100.0%</b>", table_cell_center), Paragraph("<b>59.88</b>", table_cell_center)],
        [Paragraph("<b>9</b>", table_cell_center), Paragraph("<b>Shreyas Iyer</b>", table_cell_bold), Paragraph("India, Kolkata Knight Riders", table_cell_style), Paragraph("18", table_cell_center), Paragraph("55.6%", table_cell_center), Paragraph("<font color='#00C853'>+1.1%</font>", table_cell_center), Paragraph("3", table_cell_center), Paragraph("60.0%", table_cell_center), Paragraph("<b>54.18</b>", table_cell_center)],
        [Paragraph("<b>10</b>", table_cell_center), Paragraph("<b>Sediqullah Atal</b>", table_cell_bold), Paragraph("Afghanistan, Delhi Capitals", table_cell_style), Paragraph("8", table_cell_center), Paragraph("50.0%", table_cell_center), Paragraph("<font color='#D50000'>-7.9%</font>", table_cell_center), Paragraph("2", table_cell_center), Paragraph("66.7%", table_cell_center), Paragraph("<b>50.07</b>", table_cell_center)],
    ]
    t_bat = Table(batters_table, colWidths=[36, 92, 125, 30, 42, 60, 40, 44, 45])
    t_bat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RR_PINK),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(t_bat)
    story.append(Spacer(1, 4))

    story.append(Paragraph("TOP 10 BOWLERS UNDER PRESSURE (CALIBRATED IPL AUCTION TARGETS)", h2_style))
    bowlers_table = [
        [Paragraph("Rank", table_header_style), Paragraph("Player Name", table_header_style), Paragraph("Teams / Franchise", table_header_style), Paragraph("HP M", table_header_style), Paragraph("HP WR", table_header_style), Paragraph("Pressure Lift (&Delta;)", table_header_style), Paragraph("HP MOM", table_header_style), Paragraph("KO WR", table_header_style), Paragraph("CPPI", table_header_style)],
        [Paragraph("<b>1</b>", table_cell_center), Paragraph("<b>Jacob Duffy</b>", table_cell_bold), Paragraph("New Zealand, Royal Challengers Bengaluru", table_cell_style), Paragraph("8", table_cell_center), Paragraph("75.0%", table_cell_center), Paragraph("<font color='#00C853'><b>+20.5%</b></font>", table_cell_center), Paragraph("1", table_cell_center), Paragraph("<b>100.0%</b>", table_cell_center), Paragraph("<b>68.83</b>", table_cell_center)],
        [Paragraph("<b>2</b>", table_cell_center), Paragraph("<b>Josh Hazlewood</b>", table_cell_bold), Paragraph("Australia, Royal Challengers Bengaluru", table_cell_style), Paragraph("14", table_cell_center), Paragraph("78.6%", table_cell_center), Paragraph("<font color='#00C853'><b>+14.9%</b></font>", table_cell_center), Paragraph("1", table_cell_center), Paragraph("83.3%", table_cell_center), Paragraph("<b>68.59</b>", table_cell_center)],
        [Paragraph("<b>3</b>", table_cell_center), Paragraph("<b>Yash Dayal</b>", table_cell_bold), Paragraph("Gujarat Titans, India, RCB", table_cell_style), Paragraph("10", table_cell_center), Paragraph("80.0%", table_cell_center), Paragraph("<font color='#00C853'><b>+10.2%</b></font>", table_cell_center), Paragraph("0", table_cell_center), Paragraph("80.0%", table_cell_center), Paragraph("<b>63.09</b>", table_cell_center)],
        [Paragraph("<b>4</b>", table_cell_center), Paragraph("<b>Mitchell Starc</b>", table_cell_bold), Paragraph("Australia, KKR, Delhi Capitals", table_cell_style), Paragraph("10", table_cell_center), Paragraph("60.0%", table_cell_center), Paragraph("<font color='#D50000'>-8.3%</font>", table_cell_center), Paragraph("3", table_cell_center), Paragraph("<b>100.0%</b>", table_cell_center), Paragraph("<b>62.80</b>", table_cell_center)],
        [Paragraph("<b>5</b>", table_cell_center), Paragraph("<b>Varun Chakravarthy</b>", table_cell_bold), Paragraph("India, Kolkata Knight Riders", table_cell_style), Paragraph("21", table_cell_center), Paragraph("61.9%", table_cell_center), Paragraph("<font color='#00C853'>+3.3%</font>", table_cell_center), Paragraph("1", table_cell_center), Paragraph("<b>100.0%</b>", table_cell_center), Paragraph("<b>62.38</b>", table_cell_center)],
        [Paragraph("<b>6</b>", table_cell_center), Paragraph("<b>Romario Shepherd</b>", table_cell_bold), Paragraph("LSG, Mumbai Indians, West Indies", table_cell_style), Paragraph("25", table_cell_center), Paragraph("56.0%", table_cell_center), Paragraph("<font color='#00C853'>+7.0%</font>", table_cell_center), Paragraph("2", table_cell_center), Paragraph("<b>100.0%</b>", table_cell_center), Paragraph("<b>62.00</b>", table_cell_center)],
        [Paragraph("<b>7</b>", table_cell_center), Paragraph("<b>Suyash Sharma</b>", table_cell_bold), Paragraph("India A, Kolkata Knight Riders", table_cell_style), Paragraph("11", table_cell_center), Paragraph("72.7%", table_cell_center), Paragraph("<font color='#00C853'>+7.6%</font>", table_cell_center), Paragraph("1", table_cell_center), Paragraph("66.7%", table_cell_center), Paragraph("<b>60.07</b>", table_cell_center)],
        [Paragraph("<b>8</b>", table_cell_center), Paragraph("<b>Bhuvneshwar Kumar</b>", table_cell_bold), Paragraph("India, SRH, Royal Challengers Bengaluru", table_cell_style), Paragraph("25", table_cell_center), Paragraph("60.0%", table_cell_center), Paragraph("<font color='#00C853'>+2.7%</font>", table_cell_center), Paragraph("2", table_cell_center), Paragraph("71.4%", table_cell_center), Paragraph("<b>56.86</b>", table_cell_center)],
        [Paragraph("<b>9</b>", table_cell_center), Paragraph("<b>Arshdeep Singh</b>", table_cell_bold), Paragraph("India, Punjab Kings", table_cell_style), Paragraph("25", table_cell_center), Paragraph("68.0%", table_cell_center), Paragraph("<font color='#00C853'><b>+11.1%</b></font>", table_cell_center), Paragraph("2", table_cell_center), Paragraph("33.3%", table_cell_center), Paragraph("<b>55.26</b>", table_cell_center)],
        [Paragraph("<b>10</b>", table_cell_center), Paragraph("<b>Lockie Ferguson</b>", table_cell_bold), Paragraph("GT, KKR, New Zealand, RCB", table_cell_style), Paragraph("9", table_cell_center), Paragraph("55.6%", table_cell_center), Paragraph("<font color='#00C853'>+6.5%</font>", table_cell_center), Paragraph("2", table_cell_center), Paragraph("50.0%", table_cell_center), Paragraph("<b>52.00</b>", table_cell_center)],
    ]
    t_bowl = Table(bowlers_table, colWidths=[36, 92, 125, 30, 42, 60, 40, 44, 45])
    t_bowl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RR_BLUE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(t_bowl)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Key Tactical Highlights:</b>", h2_style))
    story.append(Paragraph("• <b>Shivam Dube (#1 Batter, 66.81 CPPI):</b> +12.4% Pressure Lift, 100% Knockout Win Rate. Destroys spin over long Sawai Mansingh Stadium boundaries.", bullet_style))
    story.append(Paragraph("• <b>Rinku Singh (#2 Batter, 66.26 CPPI):</b> 26 pressure fixtures (largest sample in dataset). 100% Knockout Win Rate; ice-in-the-veins 20th over composure.", bullet_style))
    story.append(Paragraph("• <b>Jacob Duffy (#1 Bowler, 68.83 CPPI):</b> Highest Pressure Lift in dataset (+20.5%!). Extreme high-value overseas pace steal under purse constraints.", bullet_style))
    story.append(Paragraph("• <b>Josh Hazlewood (#2 Bowler, 68.59 CPPI):</b> 78.6% HP win rate (+14.9% lift). Robotic stump-to-stump accuracy eliminates death boundary releases.", bullet_style))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # PAGE 3: VISUAL QUADRANTS & RAJASTHAN ROYALS SQUAD FIT
    # ═══════════════════════════════════════════════════════════
    story.append(Paragraph("5. Visual Empirical Analysis: The Pressure Lift Alpha Matrix", h1_style))
    story.append(Paragraph(
        "To visually isolate authentic pressure match-winners from players riding on dominant team baselines, we plot High-Pressure Win Rate against True Pressure Lift (&Delta;):",
        body_style
    ))

    # Embed Chart 2
    if CHART2_PATH.exists():
        img = Image(str(CHART2_PATH), width=515, height=210)
        story.append(img)
        story.append(Spacer(1, 4))

    story.append(Paragraph("6. Tactical Squad Integration Strategy for Rajasthan Royals (IPL 2027)", h1_style))
    story.append(Paragraph(
        "Following our strategic philosophy from Season 1, we map our top pressure performers directly into Rajasthan Royals' structural squad gaps:",
        body_style
    ))

    story.append(Paragraph("A. Middle-Overs Spin Enforcers & Finishing Composure", h2_style))
    story.append(Paragraph(
        "• <b>Shivam Dube & Rajat Patidar (Middle-Overs Spin Destroyers):</b> Solves RR's chronic vulnerability in overs 7–15 against quality wrist-spin at Sawai Mansingh Stadium (Jaipur). Dube's +12.4% Lift and Patidar's +11.1% Lift eliminate batting slowdowns and relieve pressure from Sanju Samson and Riyan Parag.<br/>"
        "• <b>Rinku Singh (Designated Elite Finisher #6/#7):</b> With a 100% Knockout Win Rate across 26 high-pressure fixtures, Rinku provides the ultimate safety net. Pairing Rinku with Dhruv Jurel and Shimron Hetmyer creates the most intimidating 16–20 death-overs finishing core in the IPL.",
        body_style
    ))

    story.append(Paragraph("B. High-Stakes Death Bowling & Powerplay Control", h2_style))
    story.append(Paragraph(
        "• <b>Josh Hazlewood (Frontline Overseas Powerplay & Death Anchor):</b> Hazlewood's 78.6% High-Pressure win rate (+14.9% lift) provides the robotic stump-to-stump accuracy RR needs when defending totals at Jaipur, drastically reducing pressure on Sandeep Sharma.<br/>"
        "• <b>Jacob Duffy & Mitchell Starc (Overseas Value Steal & Knockout Spearhead):</b> Duffy provides the highest empirical lift (+20.5%) at auction base price; Starc brings unmatched big-match knockout pedigree (100% KO WR, 3 HP POTMs).<br/>"
        "• <b>Yash Dayal & Arshdeep Singh (Indian Left-Arm Death Specialism):</b> Slanted left-arm angle across right-handers in overs 18–20 has been a persistent tactical gap for RR. Dayal's 80.0% HP win rate (+10.2% lift) and Arshdeep's +11.1% Lift give RR world-class Indian pace depth.<br/>"
        "• <b>Varun Chakravarthy & Suyash Sharma (Mystery Spin Choke):</b> Elite wicket-taking mystery spin to complement Ravi Bishnoi, strangling scoring in the middle overs.",
        body_style
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # PAGE 4: STARTING XI BLUEPRINT, AUCTION PURSE & AUDIT
    # ═══════════════════════════════════════════════════════════
    story.append(Paragraph("7. Rajasthan Royals IPL 2027 Tactical Starting XI Blueprint", h1_style))
    
    xi_data = [
        [Paragraph("Pos", table_header_style), Paragraph("Player Name", table_header_style), Paragraph("Squad Role & Status", table_header_style), Paragraph("Key Pressure Metric", table_header_style), Paragraph("Tactical Deployment at SMS Jaipur", table_header_style)],
        [Paragraph("<b>1</b>", table_cell_center), Paragraph("<b>Yashasvi Jaiswal</b>", table_cell_bold), Paragraph("LH Aggressive Opener (Retained)", table_cell_style), Paragraph("SR: 165+ | Retained", table_cell_center), Paragraph("Powerplay boundary blitzkrieg; disrupts defensive field sets early.", table_cell_style)],
        [Paragraph("<b>2</b>", table_cell_center), Paragraph("<b>Devon Conway</b>", table_cell_bold), Paragraph("LHB Anchor & WK (Target #6)", table_cell_style), Paragraph("CPPI 61.97 | +18.1% Lift", table_cell_center), Paragraph("Controlled chase pacing; elite strike-rotation against swinging ball.", table_cell_style)],
        [Paragraph("<b>3</b>", table_cell_center), Paragraph("<b>Sanju Samson (C)</b>", table_cell_bold), Paragraph("Captain & Keeper (Retained)", table_cell_style), Paragraph("Core Leader | Retained", table_cell_center), Paragraph("Attacks pace in PP; anchors transition into middle overs.", table_cell_style)],
        [Paragraph("<b>4</b>", table_cell_center), Paragraph("<b>Shivam Dube</b>", table_cell_bold), Paragraph("Middle Spin Enforcer (Target #1)", table_cell_style), Paragraph("CPPI 66.81 | +12.4% Lift", table_cell_center), Paragraph("Demolishes wrist-spin into top tier over 75m Jaipur boundaries.", table_cell_style)],
        [Paragraph("<b>5</b>", table_cell_center), Paragraph("<b>Riyan Parag</b>", table_cell_bold), Paragraph("Middle Striker & Seam (Retained)", table_cell_style), Paragraph("Core Hitter | Retained", table_cell_center), Paragraph("Attacks lengths; secondary 2 overs of seam in middle phase.", table_cell_style)],
        [Paragraph("<b>6</b>", table_cell_center), Paragraph("<b>Dhruv Jurel (WK)</b>", table_cell_bold), Paragraph("Designated Finisher (Retained)", table_cell_style), Paragraph("Death Specialist | Retained", table_cell_center), Paragraph("360-degree boundary scoop and ramp execution in overs 16–20.", table_cell_style)],
        [Paragraph("<b>7</b>", table_cell_center), Paragraph("<b>Rinku Singh</b>", table_cell_bold), Paragraph("Elite Finisher (Target #2)", table_cell_style), Paragraph("CPPI 66.26 | 100% KO WR", table_cell_center), Paragraph("Ice-in-veins composure; guaranteed 20th over execution.", table_cell_style)],
        [Paragraph("<b>8</b>", table_cell_center), Paragraph("<b>Shimron Hetmyer</b>", table_cell_bold), Paragraph("Overseas Finisher (Retained)", table_cell_style), Paragraph("Power Finisher | Retained", table_cell_center), Paragraph("Explosive death boundary hitting; intimidates opposing death bowlers.", table_cell_style)],
        [Paragraph("<b>9</b>", table_cell_center), Paragraph("<b>Josh Hazlewood</b>", table_cell_bold), Paragraph("Overseas Spearhead (Target #2)", table_cell_style), Paragraph("CPPI 68.59 | 78.6% HP WR", table_cell_center), Paragraph("Robotic hard-length discipline; shuts down powerplay & death.", table_cell_style)],
        [Paragraph("<b>10</b>", table_cell_center), Paragraph("<b>Sandeep Sharma</b>", table_cell_bold), Paragraph("Death Yorker Specialist (Retained)", table_cell_style), Paragraph("Death Master | Retained", table_cell_center), Paragraph("Pinpoint wide yorkers and knuckle balls in high-pressure 19th over.", table_cell_style)],
        [Paragraph("<b>11</b>", table_cell_center), Paragraph("<b>Yash Dayal</b>", table_cell_bold), Paragraph("Left-Arm Seamer (Target #3)", table_cell_style), Paragraph("CPPI 63.09 | 80.0% HP WR", table_cell_center), Paragraph("Slanted angle across right-handers; wide yorker death control.", table_cell_style)],
    ]
    t_xi = Table(xi_data, colWidths=[32, 88, 120, 95, 180])
    t_xi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RR_BLUE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_xi)
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Tactical Impact Subs & Rotation Bench:</b> ★ Jacob Duffy (Overseas Pace Steal, CPPI 68.83) &nbsp;|&nbsp; ★ Axar Patel (Spin All-Rounder, CPPI 65.82) &nbsp;|&nbsp; ★ Varun Chakravarthy (Mystery Spin, CPPI 62.38) &nbsp;|&nbsp; ★ Rajat Patidar (Spin Enforcer, CPPI 64.26).", ParagraphStyle('SubBench', fontName='Helvetica', fontSize=6.8, leading=8.5, textColor=colors.HexColor("#475569"))))
    story.append(Spacer(1, 3))

    # 8. Auction Purse Allocation & Bid Ceilings
    story.append(Paragraph("8. Auction Valuation Model & Purse Allocation (INR 45 Cr War Chest)", h1_style))
    auc_data = [
        [Paragraph("Role / Target Tier", table_header_style), Paragraph("Primary Target", table_header_style), Paragraph("Backup Pivot", table_header_style), Paragraph("Target Price", table_header_style), Paragraph("Max Bid Ceiling", table_header_style), Paragraph("Purse Optimization Rationale", table_header_style)],
        [Paragraph("Middle Spin Enforcer", table_cell_bold), Paragraph("Shivam Dube (#1)", table_cell_style), Paragraph("Rajat Patidar (#4)", table_cell_style), Paragraph("INR 10.0–11.5 Cr", table_cell_center), Paragraph("INR 13.5 Cr", table_cell_center), Paragraph("Eliminates middle-overs slowdown; 100% KO Win Rate.", table_cell_style)],
        [Paragraph("Overseas Pace Anchor", table_cell_bold), Paragraph("Josh Hazlewood (#2)", table_cell_style), Paragraph("Jacob Duffy (#1 Value)", table_cell_style), Paragraph("INR 8.5–9.5 Cr", table_cell_center), Paragraph("INR 11.0 Cr", table_cell_center), Paragraph("Stump-to-stump accuracy; controls true-bounce Jaipur pitch.", table_cell_style)],
        [Paragraph("Indian Left-Arm Seam", table_cell_bold), Paragraph("Yash Dayal (#3)", table_cell_style), Paragraph("Arshdeep Singh (#9)", table_cell_style), Paragraph("INR 6.0–7.5 Cr", table_cell_center), Paragraph("INR 8.5 Cr", table_cell_center), Paragraph("Angle across right-handers + wide yorkers in overs 18–20.", table_cell_style)],
        [Paragraph("Death Finishing Core", table_cell_bold), Paragraph("Rinku Singh (#2)", table_cell_style), Paragraph("Axar Patel (#3 All-Rd)", table_cell_style), Paragraph("INR 8.5–10.0 Cr", table_cell_center), Paragraph("INR 11.5 Cr", table_cell_center), Paragraph("Unblemished knockout record; 20th over ice-in-the-veins.", table_cell_style)],
        [Paragraph("Mystery Spin Weapon", table_cell_bold), Paragraph("Varun Chakravarthy (#5)", table_cell_style), Paragraph("Suyash Sharma (#7)", table_cell_style), Paragraph("INR 6.5–7.5 Cr", table_cell_center), Paragraph("INR 8.5 Cr", table_cell_center), Paragraph("Unreadable middle choke; creates immediate wicket threat.", table_cell_style)],
        [Paragraph("High-Value Steal", table_cell_bold), Paragraph("Jacob Duffy (#1)", table_cell_style), Paragraph("Bhanuka Rajapaksa (#8)", table_cell_style), Paragraph("INR 1.5–2.5 Cr", table_cell_center), Paragraph("INR 3.5 Cr", table_cell_center), Paragraph("Peak empirical Lift (+20.5%) at minimum purse drain.", table_cell_style)],
    ]
    t_auc = Table(auc_data, colWidths=[92, 88, 88, 72, 65, 110])
    t_auc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RR_PINK),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_auc)
    story.append(Spacer(1, 3))

    # 9. Model Verification, Limitations & Sign-off
    story.append(Paragraph("9. Audit, Reliability, Limitations & War Room Sign-Off", h1_style))
    story.append(Paragraph(
        "• <b>100% Ground Truth Reconciliation:</b> Every player's matches, win rates, and lift were audited against all 28,381 playing-XI rows with zero discrepancies.<br/>"
        "• <b>Model Sensitivity & Calibration:</b> Elevating True Clutch Elevation (&Delta;) to 25% and damping subjective POTMs to 10% reduced award bias (Sediqullah Atal #10; Starc #4), establishing positive-lift dominance.<br/>"
        "• <b>Reliability & Limitations:</b> (1) Match-level win rates carry residual team-strength confounding despite Lift (&Delta;) and Bayesian shrinkage (prior M = 5.0). (2) Fringe qualifiers near the 8-HP-match floor (Duffy 8, Atal 8, Rajapaksa 9, Ferguson 9) retain wider confidence intervals despite the sigmoid credibility damper. (3) Pool combines IPL (Impact-Sub tactical rules) and T20I fixtures; role-level ball-by-ball matchup validation was overlaid during Jaipur XI selection.<br/>"
        "• <b>Interactive War Room Terminal:</b> Hosted live in <code>index.html</code> and <code>rr_war_room_terminal.html</code> with player dossiers, wagon wheels, and pitch maps.",
        body_style
    ))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1, color=RR_PINK, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "<b>War Room Analyst:</b> Ketan Rawat (B.Tech ECE, NIT Jamshedpur) &nbsp;|&nbsp; "
        "<b>Status:</b> Calibrated, Fully Audited & Ready for Official Unstop Submission.",
        ParagraphStyle('FooterSign', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=RR_BLUE)
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✓ Master Submission PDF Generated: {PDF_PATH}")

if __name__ == "__main__":
    generate_pdf()
