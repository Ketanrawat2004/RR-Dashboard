with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
audit_table = re.search(r'<div id="section-superstars".*?</table>', text, re.DOTALL)
if audit_table:
    print("Found section-superstars table! Length:", len(audit_table.group(0)))
    print(audit_table.group(0)[:800])
else:
    print("Not found!")

