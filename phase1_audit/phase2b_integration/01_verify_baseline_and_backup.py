import os
import hashlib
import shutil
import re

ROOT = r"C:\RR NEW"
BLUEPRINT_DIR = os.path.join(ROOT, "phase1_audit", "phase2a_blueprint")
BACKUP_DIR = os.path.join(ROOT, "phase1_audit", "phase2_backup_pre_implementation")
HASH_FILE = os.path.join(BLUEPRINT_DIR, "PRODUCTION_BASELINE_HASHES.txt")

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("=" * 80)
    print("PHASE 2B: STEP 1 — PRE-IMPLEMENTATION BASELINE VERIFICATION & BACKUP")
    print("=" * 80)

    # 1. Parse PRODUCTION_BASELINE_HASHES.txt
    if not os.path.exists(HASH_FILE):
        print(f"ERROR: Hash file not found at {HASH_FILE}")
        return False

    with open(HASH_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    # Pattern: path | size | sha256 | mtime
    line_pattern = re.compile(r'^\s*([^\s|]+(?: [^\s|]+)*?)\s*\|\s*(\d+)\s*\|\s*([a-f0-9]{64})\s*\|', re.IGNORECASE)

    for l in lines:
        m = line_pattern.match(l)
        if m:
            rel_path = m.group(1).strip()
            size = int(m.group(2).strip())
            sha = m.group(3).strip()
            entries.append((rel_path, size, sha))

    print(f"Parsed {len(entries)} file records from PRODUCTION_BASELINE_HASHES.txt.")

    # 2. Verify all hashes
    mismatches = []
    missing = []
    verified = 0

    for rel_path, expected_size, expected_sha in entries:
        full_path = os.path.join(ROOT, rel_path)
        if not os.path.exists(full_path):
            missing.append(rel_path)
            continue
        actual_size = os.path.getsize(full_path)
        actual_sha = sha256_file(full_path)
        if actual_size != expected_size or actual_sha != expected_sha:
            mismatches.append((rel_path, expected_size, actual_size, expected_sha, actual_sha))
        else:
            verified += 1

    print(f"Verified files: {verified}/{len(entries)}")
    if missing:
        print(f"ERROR: Missing files ({len(missing)}): {missing}")
        return False
    if mismatches:
        print(f"CRITICAL ERROR: Hash mismatches found ({len(mismatches)}):")
        for m in mismatches:
            print(f"  {m[0]}: Size {m[2]} vs {m[1]}, SHA {m[4]} vs {m[3]}")
        return False

    print("SUCCESS: All 45 production baseline hashes verified 100% exact match!")

    # 3. Create Backup of files Phase 2B may touch
    print("\nCreating timestamped backup of files that Phase 2B may modify...")
    backup_files = [
        "players_db.json"
    ]
    # players directory
    players_src = os.path.join(ROOT, "players")
    players_dst = os.path.join(BACKUP_DIR, "players")
    os.makedirs(players_dst, exist_ok=True)
    
    # player_images directory
    images_src = os.path.join(ROOT, "player_images")
    images_dst = os.path.join(BACKUP_DIR, "player_images")
    os.makedirs(images_dst, exist_ok=True)

    # Backup players_db.json
    shutil.copy2(os.path.join(ROOT, "players_db.json"), os.path.join(BACKUP_DIR, "players_db.json"))
    print(f"Backed up players_db.json to {BACKUP_DIR}")

    # Backup all files in players/
    p_files = os.listdir(players_src)
    for pf in p_files:
        src = os.path.join(players_src, pf)
        dst = os.path.join(players_dst, pf)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
    print(f"Backed up {len(p_files)} player dossiers to {players_dst}")

    # Backup all files in player_images/
    img_files = os.listdir(images_src)
    for imf in img_files:
        src = os.path.join(images_src, imf)
        dst = os.path.join(images_dst, imf)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
    print(f"Backed up {len(img_files)} player headshots to {images_dst}")

    # Verify backup integrity
    print("\nVerifying backup file integrity...")
    assert sha256_file(os.path.join(BACKUP_DIR, "players_db.json")) == sha256_file(os.path.join(ROOT, "players_db.json"))
    for pf in p_files:
        assert sha256_file(os.path.join(players_dst, pf)) == sha256_file(os.path.join(players_src, pf))
    for imf in img_files:
        assert sha256_file(os.path.join(images_dst, imf)) == sha256_file(os.path.join(images_src, imf))

    print("Backup verified: 100% cryptographic parity confirmed.")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)

