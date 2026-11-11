with open("build_submission_pdf.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'#1.*|Rank 1.*', text)
for m in matches[:10]:
    print("PDF script:", m)

with open("build_submission_pptx.py", "r", encoding="utf-8") as f:
    text_ppt = f.read()

matches_ppt = re.findall(r'#1.*|Rank 1.*', text_ppt)
for m in matches_ppt[:10]:
    print("PPT script:", m)

