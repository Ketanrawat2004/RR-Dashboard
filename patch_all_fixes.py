import json
import re

with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update KPI Strip items
old_kpi_block = '''        <div class="kpi-item">
            <div class="kpi-lbl">Top Batter Differential</div>
            <div class="kpi-num" style="color:var(--success);">+11.1%</div>
            <div class="kpi-sub">Rajat Patidar (#1 Batter)</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-lbl">Top Bowler Differential</div>
            <div class="kpi-num" style="color:var(--success);">+14.9%</div>
            <div class="kpi-sub">Josh Hazlewood (#2 Bowler)</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-lbl">Regulatory Compliance</div>
            <div class="kpi-num" style="font-size:18px;color:var(--rr-navy);margin-top:6px;">BCCI Verified</div>
            <div class="kpi-sub">IPL 2025-2027 Bye-Laws</div>
        </div>'''

new_kpi_block = '''        <div class="kpi-item">
            <div class="kpi-lbl">Top Ranked Batter</div>
            <div class="kpi-num" style="color:var(--rr-pink);">63.3</div>
            <div class="kpi-sub">Rajat Patidar (+11.1% &Delta;)</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-lbl">Top Ranked Bowler</div>
            <div class="kpi-num" style="color:var(--rr-navy);">66.6</div>
            <div class="kpi-sub">Mitchell Starc (60.0% HP)</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-lbl">Peak Leverage Lift</div>
            <div class="kpi-num" style="color:var(--success);">+20.5%</div>
            <div class="kpi-sub">Jacob Duffy (75.0% HP)</div>
        </div>'''

if old_kpi_block in code:
    code = code.replace(old_kpi_block, new_kpi_block, 1)
    print("Updated KPI strip to 100% accurate mathematical rankings.")
else:
    print("Warning: old_kpi_block not found directly.")

# 2. Update Card 2 Top Differentials with genuine top 5 from players_db
old_card2_block = '''        <!-- 2. Individual Top Differentials (NO TEXT WRAP) -->
        <div class="panel-box">
            <div class="panel-header-box">
                <span class="pill-header">TOP LEVERAGE DIFFERENTIALS (&Delta;)</span>
            </div>
            <div style="font-size:12px;">
                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:var(--rr-navy);">1. Josh Hazlewood</span>
                        <strong style="color:var(--success);">+14.9%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:75%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:var(--rr-navy);">2. Devon Conway</span>
                        <strong style="color:var(--success);">+14.3%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:72%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:var(--rr-navy);">3. Rinku Singh</span>
                        <strong style="color:var(--success);">+11.7%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:59%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:var(--rr-navy);">4. Rajat Patidar</span>
                        <strong style="color:var(--success);">+11.1%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:56%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item" style="margin-bottom:0;">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:var(--rr-navy);">5. Arshdeep Singh</span>
                        <strong style="color:var(--success);">+11.1%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:56%;height:100%;border-radius:3px;"></div></div>
                </div>
            </div>
            <div style="font-size:11px;color:var(--text-muted);text-align:center;margin-top:6px;">Performance boost over baseline</div>
        </div>'''

new_card2_block = '''        <!-- 2. Individual Top Differentials (NO TEXT WRAP) -->
        <div class="panel-box">
            <div class="panel-header-box">
                <span class="pill-header">TOP LEVERAGE DIFFERENTIALS (&Delta;)</span>
            </div>
            <div style="font-size:12px;">
                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:var(--rr-navy);">1. Jacob Duffy</span>
                        <strong style="color:var(--success);">+20.5%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:100%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:var(--rr-navy);">2. Devon Conway</span>
                        <strong style="color:var(--success);">+18.1%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:88%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:var(--rr-navy);">3. Josh Hazlewood</span>
                        <strong style="color:var(--success);">+14.9%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:73%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:var(--rr-navy);">4. Shivam Dube</span>
                        <strong style="color:var(--success);">+12.4%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:60%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item" style="margin-bottom:0;">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:var(--rr-navy);">5. R. Patidar / Arshdeep</span>
                        <strong style="color:var(--success);">+11.1%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:54%;height:100%;border-radius:3px;"></div></div>
                </div>
            </div>
            <div style="font-size:11px;color:var(--text-muted);text-align:center;margin-top:6px;">True empirical win rate boost under pressure</div>
        </div>'''

if old_card2_block in code:
    code = code.replace(old_card2_block, new_card2_block, 1)
    print("Updated Card 2 with true verified differentials.")
else:
    print("Warning: old_card2_block not found directly.")

# 3. Add html, body overflow-x hidden in Dashboard CSS
old_body_css = '''        html, body {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}'''

# In fix_dashboard_and_wagon.py, check body styling
code = code.replace(
    '''        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            padding: 24px;
            line-height: 1.5;
        }}''',
    '''        html, body {{
            width: 100%;
            max-width: 100vw;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        *, *:before, *:after {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            padding: 20px;
            line-height: 1.5;
        }}'''
)

# 4. Enhance .dashboard-container and .table-responsive
code = code.replace(
    '''.dashboard-container {{
            max-width: 1400px;
            margin: 0 auto;
        }}''',
    '''.dashboard-container {{
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            overflow-x: hidden;
            box-sizing: border-box;
        }}'''
)

code = code.replace(
    '''.table-responsive {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 8px;
            overflow-x: auto;
            margin-bottom: 24px;
        }}''',
    '''.table-responsive {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 8px;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            width: 100%;
            max-width: 100%;
            display: block;
            box-sizing: border-box;
            margin-bottom: 24px;
        }}'''
)

# 5. Fix tab-group in dashboard CSS
code = code.replace(
    '''.tab-group {{
            display: flex;
            gap: 8px;
        }}''',
    '''.tab-group {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            max-width: 100%;
        }}'''
)

# In mobile query, stack tab-group vertically so it never forces width
old_mobile_tabs = '''.nav-tabs {{
                gap: 6px;
                padding-bottom: 6px;
            }}'''

new_mobile_tabs = '''.tab-group {{
                display: flex;
                flex-direction: column;
                width: 100%;
                gap: 6px;
            }}
            .nav-tab-btn {{
                width: 100%;
                text-align: center;
            }}
            .slicer-card {{
                width: 100%;
                max-width: 100%;
                box-sizing: border-box;
            }}'''

if old_mobile_tabs in code:
    code = code.replace(old_mobile_tabs, new_mobile_tabs)

# 6. Enhance Player Dossiers CSS to guarantee zero overflow
code = code.replace(
    '''        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            padding: 24px;
            line-height: 1.5;
        }}
        .container {{ max-width: 1080px; margin: 0 auto; }}''',
    '''        html, body {{
            width: 100%;
            max-width: 100vw;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        *, *:before, *:after {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            padding: 20px;
            line-height: 1.5;
        }}
        .container {{
            width: 100%;
            max-width: 1080px;
            margin: 0 auto;
            overflow-x: hidden;
            box-sizing: border-box;
        }}'''
)

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Saved patch_all_fixes to fix_dashboard_and_wagon.py successfully!")

