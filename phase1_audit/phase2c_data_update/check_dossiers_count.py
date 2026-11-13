import os
import re

with open("phase1_audit/phase2c_data_update/BEFORE_IMPLEMENTATION_HASHES.txt", "r") as f:
    print(f.read())

dossiers = os.listdir("players")
print(f"Total files in players/: {len(dossiers)}")

