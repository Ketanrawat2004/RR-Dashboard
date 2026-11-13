import os
import hashlib

files = [
    "ball_by_ball.csv", "matches.csv", "competitions.csv", "teams.csv",
    "playing_eleven.csv", "competition_team_player_mapping.csv",
    "build_clean_submission_pptx.py", "build_submission_pdf.py"
]

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

for f in files:
    print(f"{f}: {sha256_file(f)}")

