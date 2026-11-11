import csv, json, os, re

with open("pressure_output/SUBMISSION_top10_batters.csv", encoding="utf-8") as f:
    csv_bat = [r["Player_Name"] for r in csv.DictReader(f)]
with open("pressure_output/SUBMISSION_top10_bowlers.csv", encoding="utf-8") as f:
    csv_bowl = [r["Player_Name"] for r in csv.DictReader(f)]

with open("players_db.json", encoding="utf-8") as f:
    db = json.load(f)
db_bat = [p["name"] for p in sorted([x for x in db if x["category"] == "Batter"], key=lambda x: x["rank"])]
db_bowl = [p["name"] for p in sorted([x for x in db if x["category"] == "Bowler"], key=lambda x: x["rank"])]

print("CSV == JSON Batters:", csv_bat == db_bat, len(csv_bat))
print("CSV == JSON Bowlers:", csv_bowl == db_bowl, len(csv_bowl))

targets = [
    "index.html",
    "rr_war_room_terminal.html",
    "rr_pressure_dashboard.html",
    "players/jasprit_bumrah.html",
    "players/shivam_dube.html",
    "pressure_output/methodology_report.md",
]

for t in targets:
    txt = open(t, encoding="utf-8").read()
    txt_nob64 = re.sub(r'data:image/[^"]+', '', txt)
    has_174_hp = bool(re.search(r"\b174\b(?!\.6)", txt_nob64))
    has_180_hp = bool(re.search(r"\b180\s*(High-Pressure|fixtures|matches)", txt_nob64))
    has_178 = bool(re.search(r"\b178\b", txt_nob64))
    has_kami = "kami" in txt_nob64.lower()
    has_old_weights = "WR_base + 0.20" in txt_nob64 or "(20%), Baseline Win Rate (15%)" in txt_nob64
    has_all_bat = all(n in txt_nob64 for n in csv_bat) if "players/" not in t else True
    has_all_bowl = all(n in txt_nob64 for n in csv_bowl) if "players/" not in t else True
    has_cert_add = "Season 1 Certificate (Additional Top 20)" in txt_nob64 if t.endswith(".html") else True
    has_view_cert = "View Certificate" in txt_nob64 if t.endswith(".html") else False
    print(f"{t}: has_178={has_178}, stale_174={has_174_hp}, stale_180_hp={has_180_hp}, stale_weights={has_old_weights}, kami={has_kami}, all_20={has_all_bat and has_all_bowl}, cert_add={has_cert_add}, view_cert={has_view_cert}")

for art in [
    "RR_SupeRR_Selector_Season2_Report_Ketan_Rawat.pdf",
    "RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx",
    "pressure_output/RR_SupeRR_Selector_Season2_Report_Ketan_Rawat.pdf",
    "pressure_output/RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx",
    "pressure_output/methodology_report.md",
    "pressure_output/SUBMISSION_top10_batters.csv",
    "pressure_output/SUBMISSION_top10_bowlers.csv",
]:
    print(f"FILE {art}: exists={os.path.exists(art)}, size={os.path.getsize(art) if os.path.exists(art) else 0} bytes")
