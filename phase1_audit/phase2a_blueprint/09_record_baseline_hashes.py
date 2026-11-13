import os
import hashlib
from datetime import datetime

ROOT = r"C:\RR NEW"
BLUEPRINT_DIR = os.path.join(ROOT, "phase1_audit", "phase2a_blueprint")

def get_file_info(filepath):
    if not os.path.exists(filepath):
        return None
    size = os.path.getsize(filepath)
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return {
        "path": filepath,
        "size": size,
        "sha256": h.hexdigest(),
        "mtime": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
    }

def main():
    target_files = [
        # Web core
        "index.html",
        "rr_pressure_dashboard.html",
        "rr_war_room_terminal.html",
        "players_db.json",
        
        # Generation scripts
        "fix_dashboard_and_wagon.py",
        "clean_powerbi_dashboard.py",
        "build_player_pages_and_dashboard.py",
        "generate_powerbi_wagon_dashboard.py",
        "build_plain_english_dashboard.py",
        
        # Presentation scripts & deliverables
        "build_submission_pdf.py",
        "build_submission_pptx.py",
        "build_clean_submission_pptx.py",
        "RR_SupeRR_Selector_Season2_Report_Ketan_Rawat.pdf",
        "RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx",
        
        # Original official CSV datasets (preservation reference)
        "ball_by_ball.csv",
        "matches.csv",
        "competitions.csv",
        "teams.csv",
        "playing_eleven.csv",
        "competition_team_player_mapping.csv"
    ]
    
    # Also collect all 25 player dossier files
    players_dir = os.path.join(ROOT, "players")
    player_files = sorted(os.listdir(players_dir))
    
    lines = []
    lines.append("=" * 100)
    lines.append("PHASE 2A PRODUCTION BASELINE CRYPTOGRAPHIC HASH REGISTER")
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append("Repository: C:\\RR NEW")
    lines.append("Strict Constraint: READ-ONLY BASELINE CAPTURE BEFORE PHASE 2 IMPLEMENTATION")
    lines.append("=" * 100)
    lines.append("")
    lines.append(f"{'Category / Relative Path':<45} | {'Size (Bytes)':<12} | {'SHA-256 Checksum':<64} | {'Last Modified'}")
    lines.append("-" * 150)
    
    lines.append("\n[CORE PRODUCTION WEB FILES & DATABASES]")
    for tf in target_files[:4]:
        p = os.path.join(ROOT, tf)
        info = get_file_info(p)
        if info:
            lines.append(f"{tf:<45} | {info['size']:<12} | {info['sha256']} | {info['mtime']}")

    lines.append("\n[PRODUCTION BUILD & GENERATION SCRIPTS]")
    for tf in target_files[4:9]:
        p = os.path.join(ROOT, tf)
        info = get_file_info(p)
        if info:
            lines.append(f"{tf:<45} | {info['size']:<12} | {info['sha256']} | {info['mtime']}")

    lines.append("\n[PRESENTATION SCRIPTS & OFFICIAL SUBMISSION ARTIFACTS]")
    for tf in target_files[9:14]:
        p = os.path.join(ROOT, tf)
        info = get_file_info(p)
        if info:
            lines.append(f"{tf:<45} | {info['size']:<12} | {info['sha256']} | {info['mtime']}")

    lines.append("\n[ORIGINAL OFFICIAL DATASETS (PRESERVATION BASELINE)]")
    for tf in target_files[14:]:
        p = os.path.join(ROOT, tf)
        info = get_file_info(p)
        if info:
            lines.append(f"{tf:<45} | {info['size']:<12} | {info['sha256']} | {info['mtime']}")

    lines.append("\n[STANDALONE PLAYER DOSSIER PAGES (PLAYERS/ DIRECTORY)]")
    for pf in player_files:
        if pf.endswith(".html"):
            p = os.path.join(players_dir, pf)
            rel = os.path.join("players", pf)
            info = get_file_info(p)
            if info:
                lines.append(f"{rel:<45} | {info['size']:<12} | {info['sha256']} | {info['mtime']}")

    out_path = os.path.join(BLUEPRINT_DIR, "PRODUCTION_BASELINE_HASHES.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"Recorded baseline hashes for {len(target_files) + len(player_files)} files.")
    print(f"Saved to {out_path}")

if __name__ == "__main__":
    main()

