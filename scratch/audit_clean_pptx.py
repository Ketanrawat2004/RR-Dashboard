import csv
from pptx import Presentation

prs = Presentation(r"C:\Rajasthan Royals\RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx")
print(f"Total slides: {len(prs.slides)}")

banned_words = [
    "delve", "unleash", "synergy", "tapestry", "beacon", "fortress", "cutting-edge",
    "holistic", "seamless", "war room", "supercharge", "paramount", "unlock", "kami",
    "dna", "spearhead", "blitzkrieg", "masterpiece"
]
# Note: check "spearhead" carefully! Look if we wrote "Spearhead" in Slides 9 or 11 ("PACE SPEARHEADS", "Frontline Seam Spearhead") -> let's replace even slightly dramatic words like "Spearhead" with "Pace Bowlers" / "Lead Seamer"!

ai_symbols = ["★", "✓", "🚀", "⚡", "🔍", "📊", "💡", "🎯", "🔥", "🏆", "🏏"]

with open("pressure_output/SUBMISSION_top10_batters.csv", encoding="utf-8") as f:
    csv_bat = [r["Player_Name"] for r in csv.DictReader(f)]
with open("pressure_output/SUBMISSION_top10_bowlers.csv", encoding="utf-8") as f:
    csv_bowl = [r["Player_Name"] for r in csv.DictReader(f)]

for si, slide in enumerate(prs.slides, 1):
    pics = [s for s in slide.shapes if s.shape_type == 13]
    has_corner_logo = any(round(s.left / 914400, 2) >= 12.0 and round(s.top / 914400, 2) <= 0.5 for s in pics)
    fonts_used = set()
    hits = []
    max_bottom = 0.0
    for s in slide.shapes:
        bot = (s.top + s.height) / 914400
        if bot > max_bottom:
            max_bottom = bot
        if s.has_text_frame:
            for p in s.text_frame.paragraphs:
                txt = p.text
                if p.font.name:
                    fonts_used.add(p.font.name)
                for r in p.runs:
                    if r.font.name:
                        fonts_used.add(r.font.name)
                low = txt.lower()
                for bw in banned_words:
                    if bw in low:
                        hits.append(f"word:{bw} in '{txt[:40]}'")
                for sym in ai_symbols:
                    if sym in txt:
                        hits.append(f"sym:{sym}")
        if s.has_table:
            tbl = s.table
            for r in tbl.rows:
                for c in r.cells:
                    for p in c.text_frame.paragraphs:
                        if p.font.name:
                            fonts_used.add(p.font.name)
                        low = p.text.lower()
                        for bw in banned_words:
                            if bw in low:
                                hits.append(f"tbl_word:{bw} in '{p.text[:40]}'")
                        for sym in ai_symbols:
                            if sym in p.text:
                                hits.append(f"tbl_sym:{sym}")

    # Verify batters table on Slide 4 & bowlers table on Slide 5
    extra = ""
    if si == 4:
        tbls = [s.table for s in slide.shapes if s.has_table]
        names = [tbls[0].cell(r, 1).text for r in range(1, 11)]
        extra = f" | BattersMatch={names == csv_bat}"
    elif si == 5:
        tbls = [s.table for s in slide.shapes if s.has_table]
        names = [tbls[0].cell(r, 1).text for r in range(1, 11)]
        extra = f" | BowlersMatch={names == csv_bowl}"

    print(f"Slide {si:2d}: corner_logo={has_corner_logo}, fonts={sorted(fonts_used)}, max_bottom={max_bottom:.2f}\", hits={hits}{extra}")

