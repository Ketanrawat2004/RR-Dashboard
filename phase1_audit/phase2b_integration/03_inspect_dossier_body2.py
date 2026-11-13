import os
import re

ROOT = r"C:\RR NEW"

def main():
    p = os.path.join(ROOT, "players", "heinrich_klaasen.html")
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()

    body_match = re.search(r'<body[^>]*>([\s\S]*?)<\/body>', html)
    if body_match:
        body = body_match.group(1)
        body_clean = re.sub(r'data:image/[^;]+;base64,[^"\']+', '[BASE64_IMAGE]', body)
        print("--- BODY PREVIEW (Chars 2500 - 6500) ---")
        print(body_clean[2500:6500])

if __name__ == "__main__":
    main()

