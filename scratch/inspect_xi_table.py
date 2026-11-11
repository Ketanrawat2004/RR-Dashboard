with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find("Accurate Swing & Seam")
if idx == -1:
    idx = html.find("Top-Order Anchor & Wicketkeeper")

print("=== TABLE CONTEXT IN index.html ===")
# Print from 1000 chars before to 3500 chars after
print(html[max(0, idx-1500):min(len(html), idx+2500)])

