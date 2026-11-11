with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# check where batters_data and bowlers_data are defined
print("batters_data present:", "batters_data" in text)
print("bowlers_data present:", "bowlers_data" in text)
print("superstars_audit present:", "superstars_audit" in text)

