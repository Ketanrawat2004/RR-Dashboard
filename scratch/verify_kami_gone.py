import glob, re

print("=== CHECKING FOR 'kami' OUTSIDE BASE64 IN ALL FILES ===")
for fp in glob.glob("*.html") + glob.glob("players/*.html") + glob.glob("*.py") + glob.glob("pressure_output/*.md"):
    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
        c = f.read()
    c_clean = re.sub(r'data:image/[^"\'\s>]+', '[B64]', c)
    for m in re.finditer(r'kami', c_clean, re.IGNORECASE):
        idx = m.start()
        print(f"STILL FOUND in {fp}:", c_clean[max(0, idx-30):idx+50])

print("=== CHECKING JASPRIT BUMRAH AUCTION SECTION ===")
with open("players/jasprit_bumrah.html", "r", encoding="utf-8") as f:
    b = f.read()
idx = b.find("EXCLUSION AUDIT")
if idx != -1:
    print(b[idx-20:idx+250])

print("=== CHECKING TACTICAL GRID ALIGNMENT IN rr_war_room_terminal.html ===")
with open("rr_war_room_terminal.html", "r", encoding="utf-8") as f:
    r = f.read()
idx2 = r.find(".tactical-grid {")
print(r[idx2:idx2+180])

