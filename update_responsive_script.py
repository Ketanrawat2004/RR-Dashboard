import re

with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update graphic_flex in player pages
old_graphic_wrap = '''        <div style="display:flex;gap:24px;align-items:center;flex-wrap:wrap;">
            <div style="flex:1;min-width:300px;text-align:center;">
                {graphic_visual}
            </div>
            {phase_panel}
        </div>'''

new_graphic_wrap = '''        <div class="graphic-flex">
            <div class="graphic-col-visual">
                {graphic_visual}
            </div>
            {phase_panel}
        </div>'''

if old_graphic_wrap in content:
    content = content.replace(old_graphic_wrap, new_graphic_wrap)
    print("Replaced graphic wrapper in player pages.")

# 2. Update phase_panel to use graphic-col-data
content = content.replace('<div style="flex:1.1;min-width:280px;">', '<div class="graphic-col-data">')
print("Replaced phase_panel div with graphic-col-data.")

# 3. Add table-scroll-wrapper around matrix-table
old_matrix = '''        <!-- 3. Leverage Level Performance Matrix -->
        <div class="panel-box">
            <div class="panel-header-box">
                <span class="pill-header">LEVERAGE LEVEL PERFORMANCE MATRIX</span>
            </div>
            <table class="matrix-table">'''

new_matrix = '''        <!-- 3. Leverage Level Performance Matrix -->
        <div class="panel-box">
            <div class="panel-header-box">
                <span class="pill-header">LEVERAGE LEVEL PERFORMANCE MATRIX</span>
            </div>
            <div class="table-scroll-wrapper">
                <table class="matrix-table">'''

if old_matrix in content:
    content = content.replace(old_matrix, new_matrix)
    old_matrix_end = '            </table>\n            <div style="font-size:11px;color:var(--text-muted);text-align:center;margin-top:6px;">Win conversion matrix across acute match margin categories</div>'
    new_matrix_end = '            </table>\n            </div>\n            <div style="font-size:11px;color:var(--text-muted);text-align:center;margin-top:6px;">Win conversion matrix across acute match margin categories</div>'
    content = content.replace(old_matrix_end, new_matrix_end)
    print("Wrapped matrix table in table-scroll-wrapper.")

# 4. Add mobile swipe hint above main table
old_table_block = '''    <div class="table-container">
        <table id="playersTable">'''

new_table_block = '''    <div class="mobile-table-hint">
        &larr; Swipe horizontally to inspect all 9 performance metrics &rarr;
    </div>
    <div class="table-container">
        <table id="playersTable">'''

if old_table_block in content:
    content = content.replace(old_table_block, new_table_block)
    print("Added mobile swipe hint above players table.")

# 5. Replace player HTML CSS media queries with rich responsive styling
old_player_css = '''        @media (max-width: 768px) {
            .metric-grid { grid-template-columns: repeat(2, 1fr); }
            .bar-item { flex-direction: column; align-items: flex-start; gap: 4px; }
            .bar-track { width: 100%; margin: 4px 0; }
            .bar-label { width: 100%; }
        }'''

# Note: in python f-string, braces are doubled {{ and }}
new_player_css = '''        /* Responsive Layout Classes */
        .graphic-flex {{
            display: flex;
            gap: 24px;
            align-items: center;
            flex-wrap: wrap;
        }}
        .graphic-col-visual {{
            flex: 1;
            min-width: 280px;
            text-align: center;
            width: 100%;
        }}
        .graphic-col-data {{
            flex: 1.1;
            min-width: 260px;
            width: 100%;
        }}

        /* Top Nav */
        .top-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .cand-nav {{
            display: flex;
            gap: 10px;
        }}
        .cand-nav a {{
            color: var(--rr-navy);
            text-decoration: none;
            font-size: 12.5px;
            font-weight: 600;
            padding: 8px 14px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: #FFFFFF;
            transition: all 0.15s ease;
        }}
        .cand-nav a:hover {{
            background: #F1F5F9;
            border-color: var(--rr-navy);
        }}

        /* Tablet Responsive (<= 1024px) */
        @media (max-width: 1024px) {{
            body {{
                padding: 16px;
            }}
            .metric-grid {{
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
            }}
        }}

        /* Mobile Responsive (<= 768px) */
        @media (max-width: 768px) {{
            body {{
                padding: 10px 8px;
            }}
            .container {{
                padding: 0 4px;
            }}
            .top-nav {{
                flex-direction: column;
                align-items: stretch;
                gap: 10px;
                margin-bottom: 14px;
            }}
            .nav-back {{
                width: 100%;
                text-align: center;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 40px;
                margin-bottom: 0;
            }}
            .cand-nav {{
                width: 100%;
                justify-content: space-between;
                gap: 8px;
            }}
            .cand-nav a {{
                flex: 1;
                text-align: center;
                min-height: 38px;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 6px 8px;
                font-size: 11.5px;
            }}
            .profile-card {{
                flex-direction: column;
                align-items: center;
                text-align: center;
                padding: 18px 14px;
                gap: 14px;
            }}
            .profile-img {{
                width: 96px;
                height: 96px;
                margin: 0 auto;
            }}
            .profile-info {{
                min-width: 0;
                width: 100%;
                text-align: center;
            }}
            .player-name {{
                font-size: 22px;
            }}
            .player-teams {{
                font-size: 12px;
            }}
            .rating-box {{
                width: 100%;
                max-width: 240px;
                margin: 0 auto;
                padding: 12px;
            }}
            .rating-val {{
                font-size: 28px;
            }}
            .metric-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 8px;
                margin-bottom: 14px;
            }}
            .metric-card {{
                padding: 10px 8px;
            }}
            .metric-val {{
                font-size: 18px;
            }}
            .metric-lbl {{
                font-size: 10px;
            }}
            .metric-sub {{
                font-size: 9px;
            }}
            .section-card {{
                padding: 16px 14px;
                margin-bottom: 14px;
            }}
            .section-header {{
                font-size: 13px;
                margin-bottom: 8px;
            }}
            .section-content {{
                font-size: 12.5px;
            }}
            .graphic-flex {{
                flex-direction: column;
                gap: 16px;
            }}
            .graphic-col-visual {{
                min-width: 0;
                width: 100%;
            }}
            .graphic-col-data {{
                min-width: 0;
                width: 100%;
                margin-top: 8px;
            }}
            .bar-item {{
                flex-direction: column;
                align-items: stretch;
                gap: 4px;
                margin-bottom: 12px;
            }}
            .bar-label {{
                width: 100%;
                font-size: 12px;
            }}
            .bar-track {{
                width: 100%;
                margin: 4px 0;
                height: 10px;
            }}
            .bar-value {{
                width: 100%;
                text-align: right;
                font-size: 12.5px;
            }}
            .bottom-nav {{
                flex-direction: column;
                gap: 10px;
                align-items: stretch;
                margin-top: 20px;
                padding-top: 14px;
            }}
            .bottom-nav a {{
                width: 100%;
                text-align: center;
                min-height: 42px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
        }}

        /* Extra Small Mobile (<= 420px) */
        @media (max-width: 420px) {{
            body {{
                padding: 6px 4px;
            }}
            .profile-card {{
                padding: 14px 10px;
            }}
            .player-name {{
                font-size: 20px;
            }}
            .metric-grid {{
                grid-template-columns: 1fr;
                gap: 6px;
            }}
            .metric-card {{
                padding: 8px 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                text-align: left;
            }}
            .metric-val {{
                font-size: 17px;
                order: 2;
            }}
            .metric-lbl {{
                margin-top: 0;
            }}
        }}'''

# Replace in player template CSS
content = re.sub(
    r'\s+@media \(max-width: 768px\) \{\{\s+\.metric-grid \{\{ grid-template-columns: repeat\(2, 1fr\); \}\}\s+\.bar-item \{\{ flex-direction: column; align-items: flex-start; gap: 4px; \}\}\s+\.bar-track \{\{ width: 100%; margin: 4px 0; \}\}\s+\.bar-label \{\{ width: 100%; \}\}\s+\}\}',
    '\n' + new_player_css,
    content
)
print("Updated player template responsive CSS.")

# 6. Add top navigation to player template
old_nav_back = '<a href="../index.html" class="nav-back">&larr; Back to Performance Dashboard</a>'
new_top_nav = '''    <div class="top-nav">
        <a href="../index.html" class="nav-back">&larr; Back to Performance Dashboard</a>
        <div class="cand-nav">
            <a href="{prev_p['key']}.html">&larr; Previous ({prev_p['name']})</a>
            <a href="{next_p['key']}.html">Next ({next_p['name']}) &rarr;</a>
        </div>
    </div>'''

if old_nav_back in content:
    content = content.replace(old_nav_back, new_top_nav)
    print("Added dual candidate navigation to top of player dossier.")

# 7. Update dashboard template CSS media queries with rich responsive styling
new_dashboard_css = '''        /* Table Scroll Wrapper */
        .table-scroll-wrapper {{
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            width: 100%;
        }}
        .mobile-table-hint {{
            display: none;
            font-size: 11.5px;
            color: var(--text-muted);
            margin-bottom: 6px;
            text-align: right;
            font-weight: 600;
        }}

        /* ==========================================================
           COMPREHENSIVE RESPONSIVE DESIGN (LAPTOP, TABLET & MOBILE)
           ========================================================== */

        /* 1. Laptops & Small Desktops (1025px - 1200px) */
        @media (max-width: 1200px) {{
            body {{
                padding: 16px;
            }}
            .kpi-strip {{
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
            }}
            .analytics-row-3col {{
                grid-template-columns: 1fr 1fr;
                gap: 16px;
            }}
            .analytics-row-3col > .panel-box:nth-child(3) {{
                grid-column: 1 / -1;
            }}
        }}

        /* 2. Tablets (769px - 1024px) */
        @media (max-width: 1024px) {{
            .executive-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 14px;
                padding: 16px 20px;
            }}
            .header-meta {{
                text-align: left;
                width: 100%;
                border-top: 1px solid #F1F5F9;
                padding-top: 10px;
            }}
            .kpi-strip {{
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
            }}
            .analytics-row-3col {{
                grid-template-columns: 1fr 1fr;
                gap: 16px;
            }}
            .analytics-row-3col > .panel-box:nth-child(3) {{
                grid-column: 1 / -1;
            }}
            .slicer-card {{
                padding: 14px 18px;
                gap: 14px;
            }}
            .doc-grid {{
                grid-template-columns: 1fr;
                gap: 16px;
            }}
        }}

        /* 3. Mobile & Small Tablets (521px - 768px) */
        @media (max-width: 768px) {{
            body {{
                padding: 10px 8px;
            }}
            .executive-header {{
                padding: 14px 16px;
                gap: 12px;
                border-radius: 6px;
            }}
            .header-titles h1 {{
                font-size: 18px;
            }}
            .header-titles p {{
                font-size: 11.5px;
            }}
            .rr-logo {{
                width: 48px;
                height: 48px;
            }}
            .kpi-strip {{
                grid-template-columns: repeat(2, 1fr);
                gap: 8px;
                margin-bottom: 16px;
            }}
            .kpi-item {{
                padding: 12px 14px;
            }}
            .kpi-num {{
                font-size: 22px;
            }}
            .analytics-row-3col {{
                grid-template-columns: 1fr;
                gap: 14px;
                margin-bottom: 18px;
            }}
            .analytics-row-3col > .panel-box:nth-child(3) {{
                grid-column: 1;
            }}
            .panel-box {{
                padding: 16px;
            }}
            .donut-container {{
                flex-direction: column;
                text-align: center;
                gap: 12px;
            }}
            .donut-legend {{
                text-align: left;
                display: inline-block;
                margin: 0 auto;
            }}
            .slicer-card {{
                flex-direction: column;
                align-items: stretch;
                padding: 14px;
                gap: 12px;
            }}
            .slicer-group {{
                flex-direction: column;
                align-items: stretch;
                width: 100%;
                gap: 10px;
            }}
            .slicer-item {{
                display: flex;
                flex-direction: column;
                gap: 4px;
                width: 100%;
            }}
            .slicer-select {{
                width: 100%;
                height: 40px;
                font-size: 13px;
            }}
            .search-field {{
                width: 100%;
                height: 40px;
                font-size: 13px;
            }}
            .nav-tabs {{
                gap: 6px;
                padding-bottom: 6px;
            }}
            .nav-tab-btn {{
                padding: 8px 14px;
                font-size: 12px;
                min-height: 38px;
            }}
            .mobile-table-hint {{
                display: block;
            }}
            .table-container {{
                margin-bottom: 18px;
                border-radius: 6px;
            }}
            .doc-grid {{
                grid-template-columns: 1fr;
                gap: 14px;
                margin-bottom: 24px;
            }}
            .code-snippet {{
                font-size: 11px;
                overflow-x: auto;
                padding: 10px;
            }}
        }}

        /* 4. Extra Small Mobile Phones (<= 520px) */
        @media (max-width: 520px) {{
            body {{
                padding: 6px 4px;
            }}
            .dashboard-container {{
                padding: 0 4px;
            }}
            .executive-header {{
                padding: 12px;
            }}
            .brand-section {{
                gap: 10px;
            }}
            .rr-logo {{
                width: 40px;
                height: 40px;
            }}
            .header-titles h1 {{
                font-size: 16px;
            }}
            .header-titles p {{
                font-size: 11px;
            }}
            .header-meta strong {{
                font-size: 11.5px;
            }}
            .header-meta span {{
                font-size: 10.5px;
            }}
            .kpi-strip {{
                grid-template-columns: 1fr;
                gap: 8px;
            }}
            .kpi-item {{
                padding: 10px 12px;
            }}
            .kpi-num {{
                font-size: 20px;
            }}
            .pill-header {{
                font-size: 10px;
                padding: 5px 12px;
            }}
            .panel-box {{
                padding: 14px 10px;
            }}
            .diff-row-header {{
                font-size: 11.5px;
            }}
        }}'''

# Replace dashboard media queries
dashboard_css_pattern = r'\s+@media \(max-width: 1024px\) \{\{\s+\.kpi-strip \{\{ grid-template-columns: repeat\(3, 1fr\); \}\}\s+\.analytics-row-3col \{\{ grid-template-columns: 1fr; \}\}\s+\.doc-grid \{\{ grid-template-columns: 1fr; \}\}\s+\}\}\s+@media \(max-width: 768px\) \{\{\s+body \{\{ padding: 12px; \}\}\s+\.kpi-strip \{\{ grid-template-columns: repeat\(2, 1fr\); \}\}\s+\.slicer-card \{\{ flex-direction: column; align-items: stretch; \}\}\s+\.search-field \{\{ width: 100%; \}\}\s+\}\}'

content = re.sub(dashboard_css_pattern, '\n' + new_dashboard_css, content)
print("Updated dashboard template responsive CSS.")

# 8. Ensure table min-width 820px in dashboard CSS
content = content.replace('table {{\n            width: 100%;\n            border-collapse: collapse;\n        }}',
                          'table {{\n            width: 100%;\n            min-width: 820px;\n            border-collapse: collapse;\n        }}')
print("Ensured min-width: 820px on data table.")

# Save updated fix_dashboard_and_wagon.py
with open('fix_dashboard_and_wagon.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully wrote updated fix_dashboard_and_wagon.py!")

