import re

with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update :root definition in fix_dashboard_and_wagon.py to turn text colors to clean black/dark charcoal
text = re.sub(r'--rr-navy:\s*#001D48;', '--rr-navy: #111827;', text)
text = re.sub(r'--rr-navy-light:\s*#0A2540;', '--rr-navy-light: #1F2937;', text)

# 2. Fix the original .doc-box and .doc-heading rules around line 1833
doc_box_old = """        .doc-box {
            position: relative;
            overflow: hidden;
            background: #00122e;
            border: 1px solid rgba(235, 26, 141, 0.35);
            border-radius: 10px;
            padding: 22px 24px;
            box-shadow: 0 4px 18px rgba(0, 18, 46, 0.25);
        }

        /* Low Opacity RR Wallpaper Background Layer */
        .doc-box::before {
            content: "";
            position: absolute;
            inset: 0;
            background-image: url('{banner_bg_b64}');
            background-size: cover;
            background-position: center right;
            background-repeat: no-repeat;
            opacity: 0.18;
            pointer-events: none;
            z-index: 1;
        }

        /* Rich Dark Gradient Overlay (Deep Navy to Black) */
        .doc-box::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(125deg, rgba(0, 16, 42, 0.94) 0%, rgba(0, 22, 54, 0.88) 50%, rgba(10, 12, 22, 0.95) 100%);
            pointer-events: none;
            z-index: 2;
        }

        /* Elevate all content above overlay for high visibility & crisp contrast */
        .doc-box > * {
            position: relative;
            z-index: 3;
        }

        .doc-heading {
            font-size: 13.5px;
            font-weight: 800;
            color: #FFFFFF;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.15);
            padding-bottom: 8px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
        }

        .doc-box p {
            font-size: 12.5px;
            color: #CBD5E1 !important;
            line-height: 1.6;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
        }

        .doc-box p strong {
            color: #FFFFFF !important;
            font-weight: 700;
        }

        .code-snippet {
            background: rgba(0, 15, 38, 0.75);
            border: 1px solid rgba(235, 26, 141, 0.4);
            border-left: 3px solid #EB1A8D;
            border-radius: 6px;
            padding: 10px 14px;
            font-family: ui-monospace, Menlo, Consolas, monospace;
            font-size: 12px;
            color: #38BDF8;
            font-weight: 600;
            margin-top: 10px;
            margin-bottom: 10px;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5);
        }"""

doc_box_new = """        .doc-box {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px;
            padding: 22px 24px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
        }

        .doc-box::before, .doc-box::after {
            display: none !important;
        }

        .doc-box > * {
            position: relative;
            z-index: 1;
        }

        .doc-heading {
            font-size: 14px;
            font-weight: 800;
            color: #111827 !important;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 12px;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 8px;
            text-shadow: none !important;
        }

        .doc-box p {
            font-size: 12.5px;
            color: #374151 !important;
            line-height: 1.6;
            text-shadow: none !important;
        }

        .doc-box p strong {
            color: #111827 !important;
            font-weight: 700;
        }

        .code-snippet {
            background: #F8FAFC !important;
            border: 1px solid #CBD5E1 !important;
            border-left: 3px solid #EB1A8D !important;
            border-radius: 6px;
            padding: 10px 14px;
            font-family: ui-monospace, Menlo, Consolas, monospace;
            font-size: 12px;
            color: #111827 !important;
            font-weight: 600;
            margin-top: 10px;
            margin-bottom: 10px;
            box-shadow: none !important;
        }"""

# In the python f-string, double braces were used for literal braces. Let's handle both single and double brace versions
if ".doc-box {{" in text:
    # replace double brace version
    doc_box_old_db = doc_box_old.replace("{", "{{").replace("}", "}}")
    doc_box_new_db = doc_box_new.replace("{", "{{").replace("}", "}}")
    text = text.replace(doc_box_old_db, doc_box_new_db)
    print("Replaced double-brace doc-box!")
else:
    text = text.replace(doc_box_old, doc_box_new)
    print("Replaced single-brace doc-box!")

# 3. Clean all blue text in the Strategic Takeaways and Quadrants
text = text.replace('color:var(--rr-navy);', 'color:#111827;')
text = text.replace('color: var(--rr-navy);', 'color: #111827;')
text = text.replace('color: #001D48;', 'color: #111827;')
text = text.replace('color: #0284C7;', 'color: #111827;')

# 4. In Quadrant Tags and Borders
text = text.replace('.q-tag-blue { color: #0284C7; }', '.q-tag-blue { color: #111827; }')
text = text.replace('.q-tag-navy { color: #001D48; }', '.q-tag-navy { color: #111827; }')
text = text.replace('.q-box-2 { border-left: 4px solid #0284C7; }', '.q-box-2 { border-left: 4px solid #64748B; }')
text = text.replace('.q-box-4 { border-left: 4px solid #001D48; }', '.q-box-4 { border-left: 4px solid #111827; }')

# 5. In SVG Scatter Chart: replace navy text/dots with deep charcoal
text = text.replace('fill="#001D48"', 'fill="#111827"')

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated fix_dashboard_and_wagon.py to completely eliminate blue text!")

