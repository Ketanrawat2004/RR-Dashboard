with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
target = 'id="section-tactical-xi"'
idx = text.find(target)
if idx != -1:
    # replace all base64 images everywhere
    sub = text[idx:]
    # find where the section ends
    end_tag = '<!-- Analytics Audit Tab Script'
    end_idx = sub.find(end_tag)
    if end_idx != -1:
        sub = sub[:end_idx]
    sub = re.sub(r'data:image/png;base64,[A-Za-z0-9+/=]+', '[BASE64_IMAGE]', sub)
    print("Full tactical section content (without base64):")
    print(sub)
else:
    print("Not found")
