import re, glob

print("=== 1. SEARCHING FOR 'kami' OUTSIDE BASE64 ===")
files_to_check = glob.glob("*.py") + glob.glob("*.html") + glob.glob("players/*.html") + glob.glob("pressure_output/*.md")
for fp in files_to_check:
    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
        c = f.read()
    # strip base64 strings
    c_clean = re.sub(r'data:image/[^"\'\s>]+', '[B64]', c)
    for m in re.finditer(r'kami', c_clean, re.IGNORECASE):
        idx = m.start()
        snippet = c_clean[max(0, idx-60):min(len(c_clean), idx+80)].replace('\n', ' ')
        print(f"[{fp}]: {snippet}")

print("\n=== 2. INSPECTING PLAYING XI TABLE & SPACE BELOW IT IN index.html ===")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

idx_table = html.find("NORMAL WIN%")
if idx_table != -1:
    # find the containing section or card
    print(html[idx_table-200:idx_table+4500])
else:
    print("NORMAL WIN% not found in index.html")

