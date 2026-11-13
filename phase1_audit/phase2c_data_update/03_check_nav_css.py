import os
import re

ROOT = r"C:\RR NEW"

def main():
    with open(os.path.join(ROOT, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()

    # Find nav-tab-btn css
    styles = re.findall(r'(\.nav-tab-btn[^{]*\{[^}]*\})', html)
    print("Nav tab styles:")
    for s in styles:
        print(s)

    # Find the nav tab HTML
    nav_match = re.search(r'(<div\b[^>]*class=["\'][^"\']*nav-[^"\']*["\'][\s\S]*?<\/div>)', html)
    if nav_match:
        print("\nNav markup:")
        print(nav_match.group(1)[:500])

if __name__ == "__main__":
    main()

