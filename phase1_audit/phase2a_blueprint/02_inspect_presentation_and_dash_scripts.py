import os
import re

ROOT = r"C:\RR NEW"

def inspect_file(filename):
    path = os.path.join(ROOT, filename)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()
    
    print(f"\n{'='*70}\nINSPECTING {filename} ({len(code):,} chars, {len(code.splitlines())} lines)\n{'='*70}")
    
    # Check imports
    imports = [l.strip() for l in code.splitlines() if l.strip().startswith("import ") or l.strip().startswith("from ")]
    print(f"Imports ({len(imports)}): {imports[:10]}")
    
    # Check file reading
    file_reads = []
    for l in code.splitlines():
        if any(term in l for term in ["open(", "read_csv", "load(", "read_json", ".pkl"]):
            file_reads.append(l.strip())
    print(f"File reading operations ({len(file_reads)}):")
    for fr in file_reads:
        print(f"  {fr}")
        
    # Check mentions of players, tables, scores, metrics
    print("Key metrics / terms mentioned:")
    terms = ["CPPI", "RAE", "RPAE", "WAE", "win_rate", "winrate", "bayes", "players_db", "Shivam Dube", "Russell", "Bumrah", "Umran", "table-batters", "table-bowlers"]
    for t in terms:
        cnt = len(re.findall(re.escape(t), code, re.IGNORECASE))
        if cnt > 0:
            print(f"  '{t}': {cnt} occurrences")

def main():
    inspect_file("build_submission_pdf.py")
    inspect_file("build_submission_pptx.py")
    inspect_file("build_clean_submission_pptx.py")
    inspect_file("clean_powerbi_dashboard.py")
    inspect_file("fix_dashboard_and_wagon.py")

if __name__ == "__main__":
    main()

