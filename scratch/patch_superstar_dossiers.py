import re
from superstar_dossiers import SUPERSTAR_ROLE_INFO

with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    code = f.read()

# Generate the python string for the 5 superstars
lines = []
lines.append('ROLE_CAPABILITY_MAP = {')
for k, data in SUPERSTAR_ROLE_INFO.items():
    lines.append(f'    "{k}": {{')
    lines.append(f'        "role": {repr(data["role"])},')
    lines.append(f'        "specialty": {repr(data["specialty"])},')
    lines.append(f'        "style": {repr(data["style"])},')
    lines.append(f'        "technical_strength": {repr(data["technical_strength"])},')
    lines.append(f'        "peer_comparison": {repr(data["peer_comparison"])},')
    lines.append(f'        "jaipur_fit": {repr(data["jaipur_fit"])},')
    lines.append(f'        "auction_valuation": {repr(data["auction_valuation"])}')
    lines.append('    },')

replacement_text = "\n".join(lines)

# Target pattern: from ROLE_CAPABILITY_MAP = { to "rajat_patidar":
pattern = r'ROLE_CAPABILITY_MAP = \{.*?(?="rajat_patidar":)'
match = re.search(pattern, code, re.DOTALL)
if not match:
    print("ERROR: Pattern not matched!")
else:
    print(f"Matched from {match.start()} to {match.end()}!")
    new_code = code[:match.start()] + replacement_text + "\n\n    " + code[match.end():]
    with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
        f.write(new_code)
    print("SUCCESS: Updated fix_dashboard_and_wagon.py with full superstar capability dossiers!")

