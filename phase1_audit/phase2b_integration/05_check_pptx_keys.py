import os
import re

ROOT = r"C:\RR NEW"

def main():
    p = os.path.join(ROOT, "build_clean_submission_pptx.py")
    with open(p, "r", encoding="utf-8") as f:
        code = f.read()

    # Search for all dict accesses: db[...] or p[...] or p.get(...)
    matches = re.findall(r'\[["\']([a-zA-Z0-9_]+)["\']\]', code)
    gets = re.findall(r'\.get\(["\']([a-zA-Z0-9_]+)["\']', code)
    all_keys = set(matches + gets)
    print(f"Keys accessed in build_clean_submission_pptx.py ({len(all_keys)}):")
    for k in sorted(all_keys):
        print(f"  - {k}")

if __name__ == "__main__":
    main()

