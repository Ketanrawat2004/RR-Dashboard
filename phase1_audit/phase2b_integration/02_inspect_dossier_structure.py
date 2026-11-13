import os
import re

ROOT = r"C:\RR NEW"

def main():
    p = os.path.join(ROOT, "players", "heinrich_klaasen.html")
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()

    print(f"File length: {len(html)} chars")
    title = re.search(r'<title>(.*?)</title>', html)
    print(f"Title: {title.group(1) if title else 'None'}")

    # Check structural layout
    div_classes = re.findall(r'<div\b[^>]*class=["\']([^"\']+)["\']', html)
    print(f"Div classes sample (first 25):")
    for dc in div_classes[:25]:
        print(f"  - {dc}")

    # Check how wagon wheel / charts are rendered
    # Look for chart, svg, canvas, img
    canvas_count = len(re.findall(r'<canvas', html))
    svg_count = len(re.findall(r'<svg', html))
    img_count = len(re.findall(r'<img', html))
    print(f"\nVisual elements: canvas={canvas_count}, svg={svg_count}, img={img_count}")

    # Print first 2000 chars of body
    body_match = re.search(r'<body[^>]*>([\s\S]*?)<\/body>', html)
    if body_match:
        body = body_match.group(1)
        # remove base64
        body_clean = re.sub(r'data:image/[^;]+;base64,[^"\']+', '[BASE64_IMAGE]', body)
        print("\n--- BODY PREVIEW (First 2500 chars) ---")
        print(body_clean[:2500])

if __name__ == "__main__":
    main()

