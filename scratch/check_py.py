with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Searching in fix_dashboard_and_wagon.py:")
for phrase in [
    "True Clutch Lift",
    "Pressure Lift Quadrants Matrix",
    "Recommended 2027 Playing XI",
    "QUANTITATIVE MODEL FORMULATION",
    "Tactical Playing-XI Blueprint",
    "Auction Bidding Rule",
    "CAREER MATCHES",
    "Dataset Matches",
    "KEY CAPABILITY"
]:
    matches = len(re.findall(re.escape(phrase), text, re.IGNORECASE))
    print(f"'{phrase}': {matches} matches")

