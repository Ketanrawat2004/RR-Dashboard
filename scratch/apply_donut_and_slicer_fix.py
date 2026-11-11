import re

with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Donut Chart to have rolling animation
old_donut = r'''                <svg viewBox="0 0 160 160" width="112" height="112" style="flex-shrink:0;">
                    <circle cx="80" cy="80" r="58" fill="none" stroke="#EEF2F6" stroke-width="22"/>
                    <!-- Playoff Finals (22%) -->
                    <circle cx="80" cy="80" r="58" fill="none" stroke="#001D48" stroke-width="22"
                            stroke-dasharray="80 364" stroke-dashoffset="0" transform="rotate(-90 80 80)"/>
                    <!-- Defences <= 15 runs (44%) -->
                    <circle cx="80" cy="80" r="58" fill="none" stroke="#EB1A8D" stroke-width="22"
                            stroke-dasharray="160 364" stroke-dashoffset="-80" transform="rotate(-90 80 80)"/>
                    <!-- Chases <= 2 wkts (34%) -->
                    <circle cx="80" cy="80" r="58" fill="none" stroke="#059669" stroke-width="22"
                            stroke-dasharray="124 364" stroke-dashoffset="-240" transform="rotate(-90 80 80)"/>
                    <!-- Center Metric -->
                    <text x="80" y="75" font-size="20" font-weight="800" fill="#111827" text-anchor="middle">174</text>
                    <text x="80" y="91" font-size="9" font-weight="700" fill="#64748B" text-anchor="middle">MATCHES</text>
                </svg>'''

new_donut = r'''                <svg viewBox="0 0 160 160" width="112" height="112" style="flex-shrink:0;overflow:visible;">
                    <circle cx="80" cy="80" r="58" fill="none" stroke="#EEF2F6" stroke-width="22"/>
                    <!-- Rolling Ring Group: Continuous automatic smooth 360deg rotation -->
                    <g class="rolling-donut-ring">
                        <animateTransform attributeName="transform" type="rotate" from="0 80 80" to="360 80 80" dur="12s" repeatCount="indefinite"/>
                        <!-- Playoff Finals (22%) -->
                        <circle cx="80" cy="80" r="58" fill="none" stroke="#001D48" stroke-width="22"
                                stroke-dasharray="80 364" stroke-dashoffset="0" transform="rotate(-90 80 80)"/>
                        <!-- Defences <= 15 runs (44%) -->
                        <circle cx="80" cy="80" r="58" fill="none" stroke="#EB1A8D" stroke-width="22"
                                stroke-dasharray="160 364" stroke-dashoffset="-80" transform="rotate(-90 80 80)"/>
                        <!-- Chases <= 2 wkts (34%) -->
                        <circle cx="80" cy="80" r="58" fill="none" stroke="#059669" stroke-width="22"
                                stroke-dasharray="124 364" stroke-dashoffset="-240" transform="rotate(-90 80 80)"/>
                    </g>
                    <!-- Center Metric (Stationary and upright in the center) -->
                    <text x="80" y="75" font-size="20" font-weight="800" fill="#111827" text-anchor="middle">174</text>
                    <text x="80" y="91" font-size="9" font-weight="700" fill="#64748B" text-anchor="middle">MATCHES</text>
                </svg>'''

if old_donut in code:
    code = code.replace(old_donut, new_donut, 1)
    print("SUCCESS: Replaced donut chart HTML with rolling animation group!")
else:
    print("WARNING: Exact old donut string not matched, checking with regex...")
    pattern = r'<svg viewBox="0 0 160 160".*?MATCHES</text>\s*</svg>'
    match = re.search(pattern, code, re.DOTALL)
    if match:
        code = code[:match.start()] + new_donut + code[match.end():]
        print("SUCCESS: Replaced donut chart via regex!")
    else:
        print("ERROR: Donut chart not found!")

# 2. Add rolling donut CSS animation
donut_css = r'''
        /* Continuous Rolling Donut Animation */
        @keyframes rollingDonut {{
            from {{
                transform: rotate(0deg);
            }}
            to {{
                transform: rotate(360deg);
            }}
        }}
        .rolling-donut-ring {{
            transform-box: fill-box;
            transform-origin: center;
            animation: rollingDonut 12s linear infinite;
        }}
'''

# 3. Update Slicer CSS
old_slicer_css_pattern = r'/\* Slicers & Dynamic Controls \*/.*?\.search-field \{\{.*?\}\}'
new_slicer_css = r'''/* Slicers & Dynamic Controls - Redesigned 2-Tier Control Hub */
        .slicer-card {{
            background: #FFFFFF;
            border: 1px solid var(--border-card);
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .slicer-tabs-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .tab-group {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
        }}

        .nav-tab-btn {{
            background: #F8FAFC;
            border: 1px solid var(--border-card);
            color: #475569;
            font-size: 12px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .nav-tab-btn:hover {{
            background: #F1F5F9;
            color: #111827;
            border-color: #CBD5E1;
        }}

        .nav-tab-btn.active {{
            background: #111827 !important;
            color: #FFFFFF !important;
            border-color: #111827 !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }}

        .slicer-status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            font-weight: 600;
            color: #64748B;
            background: #F8FAFC;
            border: 1px solid var(--border-card);
            padding: 4px 10px;
            border-radius: 16px;
            white-space: nowrap;
        }}

        .status-indicator-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #10B981;
            display: inline-block;
            box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
        }}

        .slicer-controls-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            padding-top: 10px;
            border-top: 1px solid #F1F5F9;
        }}

        .search-wrapper {{
            display: flex;
            align-items: center;
            gap: 8px;
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 0 12px;
            height: 34px;
            flex: 1;
            max-width: 380px;
            min-width: 220px;
            transition: all 0.15s ease;
        }}

        .search-wrapper:focus-within {{
            border-color: #111827;
            background: #FFFFFF;
            box-shadow: 0 0 0 2px rgba(17, 24, 39, 0.08);
        }}

        .search-icon {{
            flex-shrink: 0;
        }}

        .search-field {{
            border: none;
            background: transparent;
            outline: none;
            width: 100%;
            font-size: 12px;
            color: #111827;
            padding: 0;
        }}

        .search-field::placeholder {{
            color: #94A3B8;
        }}

        .slicer-dropdowns {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .slicer-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .slicer-label {{
            font-size: 11px;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }}

        .slicer-select {{
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 12px;
            font-weight: 600;
            color: #111827;
            outline: none;
            cursor: pointer;
            height: 34px;
            transition: border-color 0.15s ease;
        }}

        .slicer-select:focus {{
            border-color: #111827;
        }}

        .slicer-reset-btn {{
            background: #F1F5F9;
            border: 1px solid var(--border-card);
            border-radius: 6px;
            padding: 0 12px;
            font-size: 12px;
            font-weight: 600;
            color: #475569;
            cursor: pointer;
            height: 34px;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .slicer-reset-btn:hover {{
            background: #E2E8F0;
            color: #111827;
        }}'''

match_css = re.search(old_slicer_css_pattern, code, re.DOTALL)
if match_css:
    code = code[:match_css.start()] + new_slicer_css + donut_css + code[match_css.end():]
    print("SUCCESS: Replaced slicer CSS and injected donut CSS!")
else:
    print("ERROR: Slicer CSS pattern not found!")

# 4. Update Slicer HTML
old_slicer_html_pattern = r'<!-- Power BI Interactive Slicer Bar -->.*?<div class="slicer-card">.*?</div>\s*</div>'
new_slicer_html = r'''<!-- Power BI Interactive Slicer Bar - Compact, Balanced 2-Tier Control Hub -->
    <div class="slicer-card">
        <!-- Top Row: Section Navigation Tabs & Scope Status Badge -->
        <div class="slicer-tabs-row">
            <div class="tab-group">
                <button class="nav-tab-btn active" onclick="showSection('batters', this)">Batting Evaluation (Top 10)</button>
                <button class="nav-tab-btn" onclick="showSection('bowlers', this)">Bowling Evaluation (Top 10)</button>
                <button class="nav-tab-btn" onclick="showSection('tactical-xi', this)">IPL 2027 RR Squad &amp; Auction Strategy</button>
                <button class="nav-tab-btn" onclick="showSection('superstars', this)">Leverage Variance Audit</button>
            </div>
            <div class="slicer-status-badge">
                <span class="status-indicator-dot"></span>
                <span>IPL 2027 Pool &bull; 1,217 Evaluated</span>
            </div>
        </div>

        <!-- Bottom Row: Filter & Search Controls (Balanced, Full-Width, No Empty Void) -->
        <div class="slicer-controls-row">
            <div class="search-wrapper">
                <svg class="search-icon" viewBox="0 0 20 20" width="15" height="15" fill="none" stroke="#64748B" stroke-width="2">
                    <circle cx="8.5" cy="8.5" r="5.5"></circle>
                    <line x1="12.5" y1="12.5" x2="17" y2="17"></line>
                </svg>
                <input type="text" id="filterInput" class="search-field" placeholder="Search player name, franchise, state, or role..." onkeyup="applySlicers()">
            </div>

            <div class="slicer-dropdowns">
                <div class="slicer-item">
                    <label for="roleSlicer" class="slicer-label">ROLE:</label>
                    <select id="roleSlicer" class="slicer-select" onchange="applySlicers()">
                        <option value="ALL">All Roles</option>
                        <option value="TOP">Top Order &amp; Anchors (#1&ndash;#3)</option>
                        <option value="MIDDLE">Middle-Overs Enforcers (#4&ndash;#5)</option>
                        <option value="FINISHER">Finishers / Death Specialists (#5&ndash;#7)</option>
                        <option value="SEAM">Fast Bowlers / Seam</option>
                        <option value="SPIN">Spin / All-Rounders</option>
                    </select>
                </div>

                <div class="slicer-item">
                    <label for="sortSlicer" class="slicer-label">SORT:</label>
                    <select id="sortSlicer" class="slicer-select" onchange="applySlicers()">
                        <option value="RANK">Rank (Ascending)</option>
                        <option value="DIFF">Win Differential (&Delta;)</option>
                        <option value="WIN">High-Leverage Win%</option>
                        <option value="INDEX">Index Score (CPPI)</option>
                    </select>
                </div>

                <button class="slicer-reset-btn" onclick="resetSlicers()" title="Reset all filters">Reset</button>
            </div>
        </div>
    </div>'''

match_html = re.search(old_slicer_html_pattern, code, re.DOTALL)
if match_html:
    code = code[:match_html.start()] + new_slicer_html + code[match_html.end():]
    print("SUCCESS: Replaced slicer HTML structure!")
else:
    print("ERROR: Slicer HTML pattern not found!")

# 5. Add resetSlicers() to JS
js_reset = r'''
function resetSlicers() {
    var searchInput = document.getElementById('filterInput');
    var roleSlicer = document.getElementById('roleSlicer');
    var sortSlicer = document.getElementById('sortSlicer');
    if (searchInput) searchInput.value = '';
    if (roleSlicer) roleSlicer.value = 'ALL';
    if (sortSlicer) sortSlicer.value = 'RANK';
    applySlicers();
}
'''

if 'function resetSlicers' not in code:
    code = code.replace("function showSection", js_reset + "\nfunction showSection", 1)
    print("SUCCESS: Added resetSlicers() function to JavaScript!")

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Saved updated fix_dashboard_and_wagon.py!")

