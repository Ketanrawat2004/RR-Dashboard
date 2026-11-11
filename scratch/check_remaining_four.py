for p_name in ['mohammed_siraj', 'rashid_khan', 'heinrich_klaasen', 'rohit_sharma']:
    with open(f"players/{p_name}.html", "r", encoding="utf-8") as f:
        text = f.read()
    import re
    sections = re.findall(r'<div class="section-card">\s*<div class="section-header">([0-9]\.[^<]+)</div>\s*<div class="section-content">(.*?)</div>\s*</div>', text, re.DOTALL)
    print(f"=== {p_name}.html ===")
    for h, c in sections:
        print(f"  {h}: {c.strip()[:60]}...")

