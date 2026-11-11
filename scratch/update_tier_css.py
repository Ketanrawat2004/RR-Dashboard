with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace .tier-badge CSS rule with white-space: nowrap
old_rule = """.tier-badge {
            display: inline-block;
            font-size: 10px;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }"""

new_rule = """.tier-badge {
            display: inline-block;
            font-size: 10.5px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            white-space: nowrap;
        }"""

text = text.replace(old_rule, new_rule)

# Also check for any other .tier-badge definition
text = text.replace("letter-spacing: 0.5px;\n        }", "letter-spacing: 0.5px;\n            white-space: nowrap;\n        }")

with open('fix_dashboard_and_wagon.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated .tier-badge CSS with white-space: nowrap")

