import os

with open("phase1_audit/phase2a_blueprint/PHASE2A_BLUEPRINT.md", "r", encoding="utf-8") as f:
    text = f.read()

for line in text.split("\n"):
    if "dossier" in line.lower() or "404" in line.lower() or "action-link" in line.lower():
        print(line[:120])

