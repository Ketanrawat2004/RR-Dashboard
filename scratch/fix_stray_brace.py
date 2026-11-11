with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

bad_snippet = """        /* doc-heading removed duplicate */
            font-weight: 800;
            margin-bottom: 8px;
        }"""

text = text.replace(bad_snippet, "")

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Removed leftover lines in fix_dashboard_and_wagon.py")

