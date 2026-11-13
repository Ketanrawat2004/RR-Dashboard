import os
import hashlib
import subprocess

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit", "phase2c_data_update")
SHOTS_DIR = os.path.join(AUDIT_DIR, "screenshots")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("=" * 80)
    print("PHASE 2C: STEP 1 — CAPTURE BEFORE STATE & RECORD PRODUCTION HASHES")
    print("=" * 80)

    # 1. Record hashes before implementation
    html_files = ["index.html", "rr_pressure_dashboard.html", "rr_war_room_terminal.html", "players_db.json"]
    lines = []
    lines.append("PHASE 2C BEFORE IMPLEMENTATION PRODUCTION HASHES")
    lines.append("-" * 80)
    for hf in html_files:
        p = os.path.join(ROOT, hf)
        size = os.path.getsize(p)
        sha = sha256_file(p)
        info = f"{hf:<28} | Size: {size:>10,} B | SHA256: {sha}"
        lines.append(info)
        print(info)

    out_hash = os.path.join(AUDIT_DIR, "BEFORE_IMPLEMENTATION_HASHES.txt")
    with open(out_hash, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nSaved before-hashes to {out_hash}")

    # 2. Capture screenshot of existing index.html
    html_url = "file:///" + os.path.abspath(os.path.join(ROOT, "index.html")).replace("\\", "/")
    shot_path = os.path.join(SHOTS_DIR, "01_before_index_batters.png")

    if os.path.exists(EDGE_PATH):
        print(f"\nCapturing before screenshot using Microsoft Edge...")
        cmd = [
            EDGE_PATH,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size=1400,1200",
            f"--screenshot={shot_path}",
            html_url
        ]
        res = subprocess.run(cmd, capture_output=True)
        if os.path.exists(shot_path):
            print(f"Captured screenshot: {shot_path} ({os.path.getsize(shot_path):,} bytes)")
        else:
            print(f"Screenshot capture failed: {res.stderr.decode('utf-8', errors='ignore')}")

if __name__ == "__main__":
    main()

