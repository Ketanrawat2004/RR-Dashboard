import os
import re

ROOT = r"C:\RR NEW"

def main():
    p = os.path.join(ROOT, "players", "heinrich_klaasen.html")
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract head including styles
    head_match = re.search(r'(<head[\s\S]*?<\/head>)', html, re.IGNORECASE)
    print("Head length:", len(head_match.group(1)) if head_match else 0)

    # Extract CSS
    style_match = re.search(r'<style>([\s\S]*?)<\/style>', html)
    if style_match:
        css = style_match.group(1)
        print("CSS length:", len(css))
        print("CSS preview (first 500 chars):")
        print(css[:500])

    # Check footer in heinrich_klaasen.html
    footer_match = re.search(r'(<footer[\s\S]*?<\/footer>)', html)
    if footer_match:
        print("Footer length:", len(footer_match.group(1)))

if __name__ == "__main__":
    main()

