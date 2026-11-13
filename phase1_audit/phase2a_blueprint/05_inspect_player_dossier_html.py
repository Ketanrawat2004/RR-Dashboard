import os
import re

ROOT = r"C:\RR NEW"

def main():
    p_path = os.path.join(ROOT, "players", "shivam_dube.html")
    with open(p_path, "r", encoding="utf-8") as f:
        html = f.read()

    print(f"=== INSPECTING players/shivam_dube.html ({len(html):,} chars) ===")
    
    # Check title
    title = re.search(r'<title>([^<]+)<\/title>', html)
    print(f"Title: {title.group(1) if title else 'None'}")
    
    # Check headings
    h1s = re.findall(r'<h[1-3][^>]*>([\s\S]*?)<\/h[1-3]>', html)
    print(f"Headings sample: {[re.sub(r'<[^>]+>', '', h).strip() for h in h1s[:10]]}")
    
    # Check images / charts embedded
    imgs = re.findall(r'<img\b[^>]*src=["\']([^"\']+)["\']', html)
    print(f"Images count: {len(imgs)}")
    for i, img in enumerate(imgs[:5]):
        if img.startswith("data:"):
            print(f"  Img {i+1}: data URI ({len(img)} chars)")
        else:
            print(f"  Img {i+1}: {img}")
            
    # Check links
    links = re.findall(r'href=["\']([^"\']+)["\']', html)
    print(f"Links count: {len(links)}")
    for l in set(links):
        print(f"  Link: {l}")
        
    # Check scripts
    scripts = re.findall(r'<script\b[^>]*>([\s\S]*?)<\/script>', html)
    print(f"Inline scripts in player page: {len(scripts)}")
    for s in scripts:
        print(f"  Script: {len(s)} chars")

if __name__ == "__main__":
    main()

