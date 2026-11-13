import os
import re

ROOT = r"C:\RR NEW"

def main():
    with open(os.path.join(ROOT, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()

    m = re.search(r'(<table[^>]*id=["\']table-superstars["\'][\s\S]*?<\/table>)', html)
    if m:
        clean = re.sub(r'data:image/[^;]+;base64,[^"\']+', '[BASE64]', m.group(1))
        print("=== TABLE-SUPERSTARS ===")
        print(clean)

if __name__ == "__main__":
    main()

