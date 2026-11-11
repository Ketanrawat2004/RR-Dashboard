with open("build_submission_pdf.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'Paragraph\("(\d+)",\s*table_cell_center\),\s*Paragraph\("<b>([^<]+)</b>', text)
print("PDF Table entries found:", len(matches))
for r, n in matches:
    print(f"  Rank {r}: {n}")

