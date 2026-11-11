with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

old_doc_grid = """        .doc-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}"""

new_doc_grid = """        .data-section {{
            margin-bottom: 28px;
        }}

        .doc-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 28px;
            margin-bottom: 24px;
        }}"""

assert old_doc_grid in text, "old_doc_grid not found!"
text = text.replace(old_doc_grid, new_doc_grid, 1)

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(text)

print("✓ Successfully updated .doc-grid and added .data-section spacing!")

