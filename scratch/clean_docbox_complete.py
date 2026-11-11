with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

idx1 = text.find('.doc-box {{')
snippet_idx = text.find('.code-snippet {{', idx1)
end_snippet_idx = text.find('}}', snippet_idx) + 2

clean_docbox_css = """.doc-box {{
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 22px 24px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        }}

        .doc-heading {{
            font-size: 14px;
            font-weight: 800;
            color: #111827;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 12px;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 8px;
        }}

        .doc-box p {{
            font-size: 12.5px;
            color: #374151;
            line-height: 1.6;
        }}

        .doc-box p strong {{
            color: #111827;
            font-weight: 700;
        }}

        .code-snippet {{
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-left: 3px solid #EB1A8D;
            border-radius: 6px;
            padding: 10px 14px;
            font-family: ui-monospace, Menlo, Consolas, monospace;
            font-size: 12px;
            color: #111827;
            font-weight: 600;
            margin-top: 10px;
            margin-bottom: 10px;
        }}"""

text = text[:idx1] + clean_docbox_css + text[end_snippet_idx:]

# Also remove any duplicate .doc-box or .doc-heading rules at the end of fix_dashboard_and_wagon.py
text = text.replace('.doc-heading {\n            color: var(--rr-navy) !important;', '.doc-heading {\n            color: #111827 !important;')
text = text.replace('.doc-heading {\n            color: #111827 !important;\n            font-size: 14px;', '/* doc-heading removed duplicate */')

# Make sure NO text anywhere uses blue colors
text = text.replace('color: var(--rr-navy);', 'color: #111827;')
text = text.replace('color:var(--rr-navy);', 'color:#111827;')
text = text.replace('color: #001D48;', 'color: #111827;')
text = text.replace('color: #0284C7;', 'color: #111827;')
text = text.replace('.q-tag-blue { color: #0284C7; }', '.q-tag-blue { color: #111827; }')
text = text.replace('.q-tag-navy { color: #001D48; }', '.q-tag-navy { color: #111827; }')

# In tactical grid and takeaways:
text = text.replace('color:var(--text-main);', 'color:#374151;')
text = text.replace('color: var(--text-main);', 'color: #374151;')

# In HTML doc-box definitions: remove any inline dark colors
text = text.replace('style="font-size:12.5px;color:#CBD5E1;margin-bottom:8px;"', 'style="font-size:12.5px;color:#374151;margin-bottom:8px;"')
text = text.replace('style="font-size:12.5px;color:#CBD5E1;line-height:1.6;"', 'style="font-size:12.5px;color:#374151;line-height:1.6;"')
text = text.replace('style="color:#FFFFFF;"', 'style="color:#111827;"')
text = text.replace('style="font-size:12px;color:#94A3B8;line-height:1.5;"', 'style="font-size:12px;color:#4B5563;line-height:1.5;"')

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Cleaned up doc-box and removed all blue text!")

