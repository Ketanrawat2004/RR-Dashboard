import re

# 1. Update fix_dashboard_and_wagon.py to remove 'Kami'
with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    py_text = f.read()

# Replace Kami / Shortcoming
py_text_new = re.sub(r'\(Kami\s*/\s*Shortcoming\)', '(Strategic Assessment)', py_text)
py_text_new = re.sub(r'Kami\s*/\s*Shortcoming', 'Strategic Assessment', py_text_new)
py_text_new = re.sub(r'Kami', 'Shortcoming', py_text_new) # Any remaining Kami

# Ensure .tactical-grid has align-items: start
py_text_new = py_text_new.replace(
    """.tactical-grid {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 24px;
            margin-bottom: 24px;
        }""",
    """.tactical-grid {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 24px;
            margin-bottom: 24px;
            align-items: start;
        }"""
)

with open('fix_dashboard_and_wagon.py', 'w', encoding='utf-8') as f:
    f.write(py_text_new)

print("Updated fix_dashboard_and_wagon.py successfully!")

