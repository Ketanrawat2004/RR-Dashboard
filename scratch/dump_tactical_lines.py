with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

import re
out = []
for i in range(2569, min(2950, len(lines))):
    l = lines[i]
    if 'data:image/png;base64' in l:
        out.append(f"{i+1}: [BASE64_IMAGE_LINE]\n")
    else:
        out.append(f"{i+1}: {l}")

with open('scratch/tactical_lines.txt', 'w', encoding='utf-8') as f:
    f.writelines(out)

print(f"Written {len(out)} lines to scratch/tactical_lines.txt")

