import os
import re

ROOT = r"C:\RR NEW"

def main():
    with open(os.path.join(ROOT, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()

    # Find section-batters and section-bowlers
    sb_match = re.search(r'(<div[^>]*id=["\']section-batters["\'][\s\S]*?<\/table>\s*<\/div>)', html, re.IGNORECASE)
    if sb_match:
        content = sb_match.group(1)
        # clean base64 images for printing
        clean = re.sub(r'data:image/[^;]+;base64,[^"\']+', '[BASE64]', content)
        print("=== SECTION-BATTERS PREVIEW ===")
        print(clean[:1500])
        print("...\n" + clean[-500:])

    sbw_match = re.search(r'(<div[^>]*id=["\']section-bowlers["\'][\s\S]*?<\/table>\s*<\/div>)', html, re.IGNORECASE)
    if sbw_match:
        content = sbw_match.group(1)
        clean = re.sub(r'data:image/[^;]+;base64,[^"\']+', '[BASE64]', content)
        print("\n=== SECTION-BOWLERS PREVIEW ===")
        print(clean[:1500])
        print("...\n" + clean[-500:])

if __name__ == "__main__":
    main()

