import re

for fp in ['players/romario_shepherd.html', 'players/sediqullah_atal.html', 'players/shivam_dube.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()
    # clean base64
    text_clean = re.sub(r'data:image/[^"\'\s>]+', '[B64]', text)
    for m in re.finditer(r'kami', text_clean, re.IGNORECASE):
        idx = m.start()
        print(f"[{fp}]: {text_clean[max(0, idx-40):min(len(text_clean), idx+40)].replace(chr(10), ' ')}")

