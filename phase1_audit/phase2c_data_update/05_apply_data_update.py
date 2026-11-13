import os
import re
import json
import base64
import shutil
import hashlib
import pandas as pd

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit", "phase2c_data_update")
IMG_DIR = os.path.join(ROOT, "player_images")
DB_PATH = os.path.join(ROOT, "players_db.json")

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def get_player_image_b64(key):
    png_path = os.path.join(IMG_DIR, f"{key}.png")
    svg_path = os.path.join(IMG_DIR, f"{key}.svg")
    if os.path.exists(png_path):
        with open(png_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    elif os.path.exists(svg_path):
        with open(svg_path, "rb") as f:
            return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

def format_diff(diff_val):
    if diff_val >= 0:
        return f'<span class="diff-tag diff-pos">+{diff_val:.2f}</span>'
    else:
        return f'<span class="diff-tag diff-neg">{diff_val:.2f}</span>'

def main():
    print("=" * 80)
    print("PHASE 2C: STEP 2 — APPLY DATA-ONLY UPDATE TO INDEX.HTML & SYNCHRONIZE")
    print("=" * 80)

    # 1. Load players_db.json
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    batters = [p for p in db if p["category"] == "Batter"]
    bowlers = [p for p in db if p["category"] == "Bowler"]
    print(f"Loaded {len(batters)} batters and {len(bowlers)} bowlers from players_db.json.")

    # Sort Batters by shrunk_score descending
    batters.sort(key=lambda x: x["shrunk_score"], reverse=True)
    # Bowlers composite sorted by composite_score descending
    bowlers_comp = sorted(bowlers, key=lambda x: x.get("composite_score", x["shrunk_score"]), reverse=True)
    # Bowlers RPAE sorted by shrunk_rpae_score descending
    bowlers_rpae = sorted(bowlers, key=lambda x: x.get("shrunk_rpae_score", x["shrunk_score"]), reverse=True)

    # 2. Build Batters Table Rows
    bat_rows = []
    for r in batters:
        rank = r["rank"]
        name = r["name"]
        key = r["key"]
        teams = r["teams"]
        role = r["role_desc"]
        img_b64 = get_player_image_b64(key)
        
        # Small sample badge inside name box
        badge_html = ""
        if "Small Sample" in r.get("sample_size_badge", ""):
            badge_html = f'<div style="margin-top:2px;"><span style="display:inline-block;padding:2px 6px;border-radius:4px;font-size:10px;font-weight:700;background:#FEF3C7;color:#D97706;border:1px solid #FCD34D;">⚠️ Small Sample (N={r["pressure_balls"]})</span></div>'

        diff_badge = format_diff(r["lift"])
        score_str = f"{r['shrunk_score']:+.2f}"

        row_html = f"""                <tr onclick="window.location.href='players/{key}.html'" data-role="{role}" data-diff="{r['lift']}" data-win="{r['hp_wr']}" data-index="{r['shrunk_score']}" data-rank="{rank}">
                    <td style="font-weight:700;color:#09090B;">{rank}</td>
                    <td>
                        <div class="player-flex">
                            <a href="players/{key}.html" onclick="event.stopPropagation();">
                                <div class="thumb-img"><img src="{img_b64}" alt="{name}"></div>
                            </a>
                            <div class="name-box">
                                <a href="players/{key}.html" onclick="event.stopPropagation();">{name}</a>
                                <div class="team-sub">{role}</div>
                                {badge_html}
                            </div>
                        </div>
                    </td>
                    <td>{teams}</td>
                    <td style="text-align:center;font-weight:600;">{r['pressure_balls']}</td>
                    <td style="text-align:right;font-weight:700;color:#09090B;">{r['hp_wr']:.1f}</td>
                    <td style="text-align:right;color:var(--text-muted);">{r['base_wr']:.1f}</td>
                    <td style="text-align:center;">{diff_badge}</td>
                    <td style="text-align:center;font-weight:600;">{r['career_balls']:,}</td>
                    <td style="text-align:right;font-weight:700;">{r['rank_ci_90']}</td>
                    <td style="text-align:right;font-weight:800;color:#09090B;">{score_str}</td>
                    <td style="text-align:center;">
                        <a href="players/{key}.html" class="action-link" onclick="event.stopPropagation();">View Wagon Wheel &rarr;</a>
                    </td>
                </tr>"""
        bat_rows.append(row_html)

    # 3. Build Bowlers Rows (Composite)
    bowl_comp_rows = []
    for r in bowlers_comp:
        rank = r.get("rank_composite", r["rank"])
        name = r["name"]
        key = r["key"]
        teams = r["teams"]
        role = r["role_desc"]
        img_b64 = get_player_image_b64(key)

        badge_html = ""
        if "Small Sample" in r.get("sample_size_badge", ""):
            badge_html = f'<div style="margin-top:2px;"><span style="display:inline-block;padding:2px 6px;border-radius:4px;font-size:10px;font-weight:700;background:#FEF3C7;color:#D97706;border:1px solid #FCD34D;">⚠️ Small Sample (N={r["pressure_balls"]})</span></div>'

        diff_badge = format_diff(r["lift"])
        score_val = r.get("composite_score", r["shrunk_score"])
        score_str = f"{score_val:+.2f}"
        wkts_str = f"{r.get('pressure_wkts', 0):.0f} ({r.get('pressure_wae', 0):+.1f})"

        row_html = f"""                <tr class="bowler-row-composite" onclick="window.location.href='players/{key}.html'" data-role="{role}" data-diff="{r['lift']}" data-win="{r['hp_wr']}" data-index="{score_val}" data-rank="{rank}">
                    <td style="font-weight:700;color:#09090B;">{rank}</td>
                    <td>
                        <div class="player-flex">
                            <a href="players/{key}.html" onclick="event.stopPropagation();">
                                <div class="thumb-img"><img src="{img_b64}" alt="{name}"></div>
                            </a>
                            <div class="name-box">
                                <a href="players/{key}.html" onclick="event.stopPropagation();">{name}</a>
                                <div class="team-sub">{role}</div>
                                {badge_html}
                            </div>
                        </div>
                    </td>
                    <td>{teams}</td>
                    <td style="text-align:center;font-weight:600;">{r['pressure_balls']}</td>
                    <td style="text-align:right;font-weight:700;color:#09090B;">{r['hp_wr']:.2f}</td>
                    <td style="text-align:right;color:var(--text-muted);">{r['base_wr']:.2f}</td>
                    <td style="text-align:center;">{diff_badge}</td>
                    <td style="text-align:center;font-weight:600;">{wkts_str}</td>
                    <td style="text-align:right;font-weight:700;">{r['rank_ci_90']}</td>
                    <td style="text-align:right;font-weight:800;color:#09090B;">{score_str}</td>
                    <td style="text-align:center;">
                        <a href="players/{key}.html" class="action-link" onclick="event.stopPropagation();">View Pitch Map &rarr;</a>
                    </td>
                </tr>"""
        bowl_comp_rows.append(row_html)

    # 4. Build Bowlers Rows (Pure RPAE)
    bowl_rpae_rows = []
    for r in bowlers_rpae:
        rank = r.get("rank_pure_rpae", r["rank"])
        name = r["name"]
        key = r["key"]
        teams = r["teams"]
        role = r["role_desc"]
        img_b64 = get_player_image_b64(key)

        badge_html = ""
        if "Small Sample" in r.get("sample_size_badge", ""):
            badge_html = f'<div style="margin-top:2px;"><span style="display:inline-block;padding:2px 6px;border-radius:4px;font-size:10px;font-weight:700;background:#FEF3C7;color:#D97706;border:1px solid #FCD34D;">⚠️ Small Sample (N={r["pressure_balls"]})</span></div>'

        diff_badge = format_diff(r["lift"])
        score_val = r.get("shrunk_rpae_score", r["shrunk_score"])
        score_str = f"{score_val:+.2f}"

        row_html = f"""                <tr class="bowler-row-rpae" style="display:none;" onclick="window.location.href='players/{key}.html'" data-role="{role}" data-diff="{r['lift']}" data-win="{r['hp_wr']}" data-index="{score_val}" data-rank="{rank}">
                    <td style="font-weight:700;color:#09090B;">{rank}</td>
                    <td>
                        <div class="player-flex">
                            <a href="players/{key}.html" onclick="event.stopPropagation();">
                                <div class="thumb-img"><img src="{img_b64}" alt="{name}"></div>
                            </a>
                            <div class="name-box">
                                <a href="players/{key}.html" onclick="event.stopPropagation();">{name}</a>
                                <div class="team-sub">{role}</div>
                                {badge_html}
                            </div>
                        </div>
                    </td>
                    <td>{teams}</td>
                    <td style="text-align:center;font-weight:600;">{r['pressure_balls']}</td>
                    <td style="text-align:right;font-weight:700;color:#09090B;">{r['hp_wr']:.2f}</td>
                    <td style="text-align:right;color:var(--text-muted);">{r['base_wr']:.2f}</td>
                    <td style="text-align:center;">{diff_badge}</td>
                    <td style="text-align:center;font-weight:600;">{r['career_balls']:,}</td>
                    <td style="text-align:right;font-weight:700;">{r['rank_ci_90']}</td>
                    <td style="text-align:right;font-weight:800;color:#09090B;">{score_str}</td>
                    <td style="text-align:center;">
                        <a href="players/{key}.html" class="action-link" onclick="event.stopPropagation();">View Pitch Map &rarr;</a>
                    </td>
                </tr>"""
        bowl_rpae_rows.append(row_html)

    # 5. Load original index.html
    index_path = os.path.join(ROOT, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 6. Replace section-batters table
    new_batters_section = f"""<div id="section-batters" class="table-responsive data-section">
        <div class="mobile-table-hint">&larr; Swipe horizontally to view all metrics &rarr;</div>
        <table id="table-batters">
            <thead>
                <tr>
                    <th style="width:34px;text-align:center;">#</th>
                    <th style="text-align:left;">Player & Role</th>
                    <th style="text-align:left;">Franchise / State</th>
                    <th style="text-align:center;">Leverage<br>Deliveries</th>
                    <th style="text-align:right;">Pressure<br>SR</th>
                    <th style="text-align:right;">Expected<br>SR</th>
                    <th style="text-align:center;">RAE Diff<br>(&Delta;)</th>
                    <th style="text-align:center;">Career<br>Balls</th>
                    <th style="text-align:right;">90% Rank<br>Bound</th>
                    <th style="text-align:right;">Shrunk<br>RAE</th>
                    <th style="text-align:center;">Action</th>
                </tr>
            </thead>
            <tbody>
{chr(10).join(bat_rows)}
            </tbody>
        </table>
    </div>"""

    # 7. Replace section-bowlers table with framework toggle
    new_bowlers_section = f"""<div id="section-bowlers" class="table-responsive data-section" style="display:none;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding:6px 2px;flex-wrap:wrap;gap:8px;">
            <div style="font-size:12px;color:var(--text-muted);font-weight:700;text-transform:uppercase;letter-spacing:0.5px;">
                Bowling Evaluation Framework:
            </div>
            <div style="display:flex;gap:6px;flex-wrap:wrap;">
                <button id="btn-bowling-composite" class="nav-tab-btn active" onclick="switchBowlingFramework('composite')" style="padding:6px 14px;font-size:12px;">Balanced Composite (60% RPAE + 40% WAE)</button>
                <button id="btn-bowling-rpae" class="nav-tab-btn" onclick="switchBowlingFramework('rpae')" style="padding:6px 14px;font-size:12px;">Pure Run Prevention (RPAE)</button>
            </div>
        </div>
        <div class="mobile-table-hint">&larr; Swipe horizontally to view all metrics &rarr;</div>
        <table id="table-bowlers">
            <thead>
                <tr>
                    <th style="width:34px;text-align:center;">#</th>
                    <th style="text-align:left;">Player & Role</th>
                    <th style="text-align:left;">Franchise / State</th>
                    <th style="text-align:center;">Leverage<br>Deliveries</th>
                    <th style="text-align:right;">Pressure<br>Econ</th>
                    <th style="text-align:right;">Expected<br>Econ</th>
                    <th style="text-align:center;">Econ Diff<br>(&Delta;)</th>
                    <th id="bowler-th-col8" style="text-align:center;">Pressure<br>Wickets</th>
                    <th style="text-align:right;">90% Rank<br>Bound</th>
                    <th id="bowler-th-score" style="text-align:right;">Composite<br>Score</th>
                    <th style="text-align:center;">Action</th>
                </tr>
            </thead>
            <tbody>
{chr(10).join(bowl_comp_rows)}
{chr(10).join(bowl_rpae_rows)}
            </tbody>
        </table>
    </div>"""

    # Replace section-batters
    html = re.sub(
        r'<div id=["\']section-batters["\'][\s\S]*?<\/table>\s*<\/div>',
        lambda m: new_batters_section,
        html,
        count=1
    )

    # Replace section-bowlers
    html = re.sub(
        r'<div id=["\']section-bowlers["\'][\s\S]*?<\/table>\s*<\/div>',
        lambda m: new_bowlers_section,
        html,
        count=1
    )

    # 8. Update inline JavaScript: Add switchBowlingFramework and update applySlicers
    new_script = """<script>
var currentBowlingFramework = 'composite';

function switchBowlingFramework(mode) {
    currentBowlingFramework = mode;
    var btnComp = document.getElementById('btn-bowling-composite');
    var btnRpae = document.getElementById('btn-bowling-rpae');
    var compRows = document.querySelectorAll('.bowler-row-composite');
    var rpaeRows = document.querySelectorAll('.bowler-row-rpae');
    var thCol8 = document.getElementById('bowler-th-col8');
    var thScore = document.getElementById('bowler-th-score');

    if (mode === 'rpae') {
        if (btnComp) btnComp.classList.remove('active');
        if (btnRpae) btnRpae.classList.add('active');
        if (thCol8) thCol8.innerHTML = 'Career<br>Deliveries';
        if (thScore) thScore.innerHTML = 'Pure RPAE<br>Score';
    } else {
        if (btnRpae) btnRpae.classList.remove('active');
        if (btnComp) btnComp.classList.add('active');
        if (thCol8) thCol8.innerHTML = 'Pressure<br>Wickets';
        if (thScore) thScore.innerHTML = 'Composite<br>Score';
    }
    applySlicers();
}

function resetSlicers() {
    var searchInput = document.getElementById('filterInput');
    var roleSlicer = document.getElementById('roleSlicer');
    var sortSlicer = document.getElementById('sortSlicer');
    if (searchInput) searchInput.value = '';
    if (roleSlicer) roleSlicer.value = 'ALL';
    if (sortSlicer) sortSlicer.value = 'RANK';
    applySlicers();
}

function showSection(sectionId, btn) {
    var sections = document.querySelectorAll('.data-section');
    for (var i = 0; i < sections.length; i++) {
        sections[i].style.display = 'none';
    }
    var buttons = document.querySelectorAll('.nav-tab-btn');
    for (var j = 0; j < buttons.length; j++) {
        buttons[j].classList.remove('active');
    }
    var target = document.getElementById('section-' + sectionId);
    if (target) {
        target.style.display = 'block';
    }
    if (btn) {
        btn.classList.add('active');
    }
    applySlicers();
}

function applySlicers() {
    var query = document.getElementById('filterInput').value.toLowerCase();
    var roleFilter = document.getElementById('roleSlicer').value;
    var sortOrder = document.getElementById('sortSlicer').value;

    var sections = document.querySelectorAll('.data-section');
    var currentSection = null;
    for (var i = 0; i < sections.length; i++) {
        if (sections[i].style.display !== 'none') {
            currentSection = sections[i];
            break;
        }
    }
    if (!currentSection) return;

    var table = currentSection.querySelector('table');
    if (!table) return;

    var tbody = table.querySelector('tbody');
    if (!tbody) return;

    var isBowlerTable = (table.id === 'table-bowlers');
    var allRows = Array.from(tbody.querySelectorAll('tr'));

    // Filter relevant rows based on active bowling framework
    var activeRows = [];
    allRows.forEach(function(row) {
        if (isBowlerTable) {
            var isComp = row.classList.contains('bowler-row-composite');
            var isRpae = row.classList.contains('bowler-row-rpae');
            if (currentBowlingFramework === 'composite' && !isComp) {
                row.style.display = 'none';
                return;
            } else if (currentBowlingFramework === 'rpae' && !isRpae) {
                row.style.display = 'none';
                return;
            }
        }
        activeRows.push(row);
    });

    activeRows.forEach(function(row) {
        var text = row.textContent.toLowerCase();
        var role = (row.getAttribute('data-role') || '').toUpperCase();

        var matchesQuery = !query || text.indexOf(query) !== -1;
        var matchesRole = true;

        if (roleFilter === 'TOP_ORDER') {
            matchesRole = (role.indexOf('TOP') !== -1 || role.indexOf('OPEN') !== -1 || role.indexOf('ANCHOR') !== -1);
        } else if (roleFilter === 'MIDDLE_ORDER') {
            matchesRole = (role.indexOf('MIDDLE') !== -1 || role.indexOf('SPIN') !== -1);
        } else if (roleFilter === 'FINISHER') {
            matchesRole = (role.indexOf('FINISH') !== -1 || role.indexOf('DEATH') !== -1 || role.indexOf('STRIKE') !== -1);
        } else if (roleFilter === 'PACE') {
            matchesRole = (role.indexOf('PACE') !== -1 || role.indexOf('SEAM') !== -1 || role.indexOf('FAST') !== -1 || role.indexOf('SWING') !== -1);
        } else if (roleFilter === 'SPIN') {
            matchesRole = (role.indexOf('SPIN') !== -1 || role.indexOf('ROUNDER') !== -1 || role.indexOf('WRIST') !== -1 || role.indexOf('MYSTERY') !== -1 || role.indexOf('ORTHODOX') !== -1);
        }

        row.style.display = (matchesQuery && matchesRole) ? '' : 'none';
    });

    // Sort rows dynamically
    activeRows.sort(function(a, b) {
        if (sortOrder === 'DIFF') {
            return parseFloat(b.getAttribute('data-diff') || 0) - parseFloat(a.getAttribute('data-diff') || 0);
        } else if (sortOrder === 'WIN') {
            return parseFloat(b.getAttribute('data-win') || 0) - parseFloat(a.getAttribute('data-win') || 0);
        } else if (sortOrder === 'INDEX') {
            return parseFloat(b.getAttribute('data-index') || 0) - parseFloat(a.getAttribute('data-index') || 0);
        } else {
            return parseFloat(a.getAttribute('data-rank') || 0) - parseFloat(b.getAttribute('data-rank') || 0);
        }
    });

    activeRows.forEach(function(row) { tbody.appendChild(row); });
}
</script>"""

    # Replace inline script
    html = re.sub(r'<script\b[^>]*>[\s\S]*?<\/script>', lambda m: new_script, html, count=1)

    # 9. Write canonical index.html
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Updated {index_path} ({len(html):,} chars).")

    # 10. Synchronize to mirror files
    dash_path = os.path.join(ROOT, "rr_pressure_dashboard.html")
    term_path = os.path.join(ROOT, "rr_war_room_terminal.html")
    shutil.copy2(index_path, dash_path)
    shutil.copy2(index_path, term_path)

    # Verify triplet synchronization
    h_idx = sha256_file(index_path)
    h_dash = sha256_file(dash_path)
    h_term = sha256_file(term_path)

    print("\nTriplet Parity Verification:")
    print(f"  index.html                 : Size {os.path.getsize(index_path):,} B | SHA256: {h_idx}")
    print(f"  rr_pressure_dashboard.html : Size {os.path.getsize(dash_path):,} B | SHA256: {h_dash}")
    print(f"  rr_war_room_terminal.html  : Size {os.path.getsize(term_path):,} B | SHA256: {h_term}")

    assert h_idx == h_dash == h_term, "CRITICAL ERROR: Triplet files are not byte-for-byte identical!"
    print("SUCCESS: All 3 production HTML files are 100% byte-for-byte synchronized!")

if __name__ == "__main__":
    main()

