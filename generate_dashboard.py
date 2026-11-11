import json
from pathlib import Path
from optimize_rankings import records

OUTPUT_HTML = Path(r"C:\Rajasthan Royals\pressure_output\pressure_war_room.html")
OUTPUT_HTML_COPY = Path(r"C:\Rajasthan Royals\rr_pressure_dashboard.html")

pak_names = {
    'Mohammad Nawaz', 'Shaheen Afridi', 'Babar Azam', 'Mohammad Rizwan',
    'Haris Rauf', 'Shadab Khan', 'Naseem Shah', 'Iftikhar Ahmed',
    'Fakhar Zaman', 'Imad Wasim', 'Saim Ayub'
}

# Tactical auction notes for key players
TACTICAL_NOTES = {
    'Rajat Patidar': "Target Role: #4 Middle-Overs Spin Enforcer. Solves RR's scoring slowdown in overs 7–15 at Jaipur. Attacks wrist-spin with fearless strike rates.",
    'Rinku Singh': "Target Role: Elite Death Finisher (#6/#7). 100% Knockout Win Rate across 26 high-pressure fixtures. Unmatched chasing composure alongside Dhruv Jurel.",
    'Devon Conway': "Target Role: Top-Order Overseas Anchor. +18.1% Pressure Lift; proven IPL Final Player of the Match pedigree under high stakes.",
    'Sediqullah Atal': "Target Role: High-Ceiling Top-Order Striker. 2 MOM awards under pressure in Emerging Asia Cup. Aggressive boundary hitter.",
    'Ruturaj Gaikwad': "Target Role: Top-Order Anchor. 100% Knockout Win Rate; exceptional game management in playoff run chases.",
    'Shivam Dube': "Target Role: Spin-Choke Destroyer. +12.4% Pressure Lift; dominates slow bowling at Sawai Mansingh Stadium.",
    'Shreyas Iyer': "Target Role: Proven Captain & Middle-Order Leader. 3 HP MOM awards; championship-winning captain with KKR.",
    'Virat Kohli': "Target Role: Master Chase Anchor. 70.0% HP Win Rate; unmatched historical execution in tight target defense/pursuit.",
    'Axar Patel': "Target Role: Left-Arm Bowling All-Rounder. 100% Knockout Win Rate across 28 pressure appearances; versatile balance asset.",
    'Bhanuka Rajapaksa': "Target Role: Aggressive LHB Middle-Order Impact. +10.4% Pressure Lift; fearless against off-spin in high RRR chases.",
    'Mitchell Starc': "Target Role: Frontline Strike Pacer. 3 HP MOM awards in 10 matches (30% MOM rate) including IPL 2024 Final & Q1; 100% Knockout Win Rate.",
    'Josh Hazlewood': "Target Role: Powerplay & Death Overs Control. 78.6% HP Win Rate (+14.9% lift); relentless line and length under pressure.",
    'Jacob Duffy': "Target Role: Overseas Hard-Length Pacer. +20.5% Pressure Lift (75.0% HP WR vs 54.5% baseline); 100% Knockout Win Rate.",
    'Suyash Sharma': "Target Role: Mystery Wrist-Spin Enforcer. 72.7% HP Win Rate; aggressive wicket-taking option through the middle overs.",
    'Lockie Ferguson': "Target Role: Express Middle/Death Pacer. 2 HP MOM awards; 150+ kph pace that rushes batters under pressure.",
    'Yash Dayal': "Target Role: Indian Left-Arm Death Specialist. 80.0% HP Win Rate (+10.2% lift); proven execution defending final overs.",
    'Romario Shepherd': "Target Role: Power Finisher & Heavy-Ball Pacer. 100% Knockout Win Rate across 25 games; 2 MOM awards.",
    'Varun Chakravarthy': "Target Role: Middle-Overs Spin Choke. 100% Knockout Win Rate; unreadable mystery variations in pressure games.",
    'Bhuvneshwar Kumar': "Target Role: Veteran Swing & Death Specialist. 71.4% Knockout Win Rate; IPL's most experienced pressure bowler.",
    'Arshdeep Singh': "Target Role: Frontline Indian Left-Arm Pacer. +11.1% Pressure Lift; T20 World Cup champion death bowler across 25 HP fixtures."
}

clean_records = []
for r in records:
    if r['name'] in pak_names:
        continue
    pid = r['pid']
    name = r['name']
    clean_records.append({
        'id': pid,
        'name': name,
        'role': r['role'],
        'teams': r['teams'],
        'matches': r['total_matches'],
        'base_wr': r['base_wr'],
        'hp_matches': r['hp_matches'],
        'hp_wins': r['hp_wins'],
        'hp_wr': r['raw_hp_wr'],
        'lift': r['pressure_lift'],
        'mom_hp': r['mom_hp'],
        'mom_all': r['mom_all'],
        'ko_matches': r['ko_matches'],
        'ko_wins': r['ko_wins'],
        'ko_wr': r['ko_wr'],
        'cppi': r['cppi'],
        'note': TACTICAL_NOTES.get(name, "Evaluated in dataset across IPL & T20I fixtures. Performance metrics reflect match leverage index scores >= 30.")
    })

data_json = json.dumps(clean_records)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rajasthan Royals — Pressure Performance Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-page: #0b1120;
            --bg-card: #131c31;
            --bg-card-hover: #18243e;
            --border: #233252;
            --border-subtle: #1a2742;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --rr-pink: #d946ef;
            --rr-pink-soft: rgba(217, 70, 239, 0.12);
            --accent-blue: #38bdf8;
            --green: #22c55e;
            --red: #ef4444;
            --amber: #f59e0b;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-primary);
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            padding: 24px;
        }}

        .container {{
            max-width: 1360px;
            margin: 0 auto;
        }}

        /* Header */
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 16px;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .brand-badge {{
            background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%);
            color: white;
            font-weight: 700;
            font-size: 13px;
            padding: 6px 12px;
            border-radius: 6px;
            letter-spacing: 0.5px;
        }}

        .brand-title h1 {{
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .brand-title p {{
            font-size: 13px;
            color: var(--text-secondary);
        }}

        .meta-pill {{
            font-size: 12px;
            color: var(--text-secondary);
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 6px 14px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .meta-dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--green);
        }}

        /* KPI Cards */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}

        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 16px 20px;
            border-radius: 8px;
        }}

        .kpi-label {{
            font-size: 12px;
            font-weight: 500;
            color: var(--text-secondary);
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .kpi-value {{
            font-size: 24px;
            font-weight: 600;
            color: var(--text-primary);
            font-feature-settings: "tnum";
            font-variant-numeric: tabular-nums;
        }}

        .kpi-subtext {{
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 4px;
        }}

        /* Controls */
        .controls-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 14px;
        }}

        .controls-left {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .btn-group {{
            display: inline-flex;
            background: var(--bg-page);
            padding: 3px;
            border-radius: 6px;
            border: 1px solid var(--border);
        }}

        .tab-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 500;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .tab-btn:hover {{
            color: var(--text-primary);
        }}

        .tab-btn.active {{
            background: var(--bg-card-hover);
            color: var(--text-primary);
            box-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }}

        .search-box {{
            background: var(--bg-page);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 7px 12px;
            font-size: 13px;
            border-radius: 6px;
            width: 240px;
            outline: none;
        }}

        .search-box:focus {{
            border-color: var(--accent-blue);
        }}

        .filter-select {{
            background: var(--bg-page);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 7px 12px;
            font-size: 13px;
            border-radius: 6px;
            outline: none;
            cursor: pointer;
        }}

        .btn-export {{
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-secondary);
            padding: 7px 14px;
            font-size: 13px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s;
        }}

        .btn-export:hover {{
            color: var(--text-primary);
            border-color: var(--text-muted);
        }}

        /* Table */
        .table-wrap {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }}

        th {{
            background: #111a2e;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 12px 14px;
            border-bottom: 1px solid var(--border);
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
        }}

        th:hover {{
            color: var(--text-primary);
        }}

        th.sort-active {{
            color: var(--accent-blue);
        }}

        td {{
            padding: 12px 14px;
            border-bottom: 1px solid var(--border-subtle);
            color: var(--text-primary);
            font-variant-numeric: tabular-nums;
            white-space: nowrap;
        }}

        tr:hover td {{
            background: var(--bg-card-hover);
            cursor: pointer;
        }}

        .rank-num {{
            color: var(--text-muted);
            font-weight: 600;
            width: 30px;
        }}

        .rank-top {{
            color: var(--amber);
            font-weight: 700;
        }}

        .player-info {{
            display: flex;
            flex-direction: column;
        }}

        .player-name {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        .player-teams {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .pill-role {{
            font-size: 11px;
            font-weight: 500;
            padding: 2px 8px;
            border-radius: 4px;
            background: rgba(148, 163, 184, 0.1);
            color: var(--text-secondary);
            display: inline-block;
        }}

        .lift-pos {{
            color: var(--green);
            font-weight: 600;
        }}

        .lift-neg {{
            color: var(--red);
            font-weight: 600;
        }}

        .score-badge {{
            font-weight: 700;
            font-size: 13px;
            color: var(--accent-blue);
        }}

        /* Detail Drawer / Modal */
        .drawer-overlay {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.6);
            display: none;
            justify-content: flex-end;
            z-index: 1000;
        }}

        .drawer-overlay.open {{
            display: flex;
        }}

        .drawer {{
            width: 440px;
            max-width: 100%;
            background: #111a2e;
            border-left: 1px solid var(--border);
            height: 100%;
            overflow-y: auto;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            box-shadow: -10px 0 30px rgba(0,0,0,0.5);
        }}

        .drawer-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }}

        .drawer-title {{
            font-size: 18px;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .drawer-subtitle {{
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 2px;
        }}

        .drawer-close {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 22px;
            cursor: pointer;
            padding: 4px;
        }}

        .drawer-close:hover {{
            color: var(--text-primary);
        }}

        .metric-block {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 14px;
        }}

        .metric-row {{
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            font-size: 13px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .metric-row:last-child {{
            border-bottom: none;
        }}

        .tactical-box {{
            background: rgba(217, 70, 239, 0.08);
            border: 1px solid rgba(217, 70, 239, 0.3);
            border-radius: 6px;
            padding: 14px;
        }}

        .tactical-title {{
            font-size: 12px;
            font-weight: 600;
            color: var(--rr-pink);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}

        .tactical-text {{
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.5;
        }}

        /* Footer */
        footer {{
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: var(--text-muted);
            flex-wrap: wrap;
            gap: 12px;
        }}

        .method-note {{
            max-width: 800px;
            font-size: 12px;
            color: var(--text-secondary);
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Top Nav -->
        <header>
            <div class="brand">
                <div class="brand-badge">RAJASTHAN ROYALS</div>
                <div class="brand-title">
                    <h1>Performance Analytics & Auction Strategy</h1>
                    <p>Pressure Performance Index (2022–2026 IPL & T20I Dataset)</p>
                </div>
            </div>
            <div class="meta-pill">
                <span class="meta-dot"></span>
                <span>883 Matches Analyzed &bull; 180 High-Pressure Fixtures</span>
            </div>
        </header>

        <!-- KPI Cards -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Dataset Scope</div>
                <div class="kpi-value">883</div>
                <div class="kpi-subtext">371 IPL + 512 T20I Matches (2022–2026)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">High-Pressure Matches</div>
                <div class="kpi-value">180</div>
                <div class="kpi-subtext">Top 20.4% Leverage Fixtures (MLI &ge; 30)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Top Batter (Pressure)</div>
                <div class="kpi-value" style="color: var(--rr-pink);">Rajat Patidar</div>
                <div class="kpi-subtext">CPPI 63.28 &bull; +11.1% Pressure Lift &bull; 71.4% HP WR</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Top Bowler (Pressure)</div>
                <div class="kpi-value" style="color: var(--accent-blue);">Mitchell Starc</div>
                <div class="kpi-subtext">CPPI 66.63 &bull; 3 HP Player of Match &bull; 100% KO WR</div>
            </div>
        </div>

        <!-- Controls Panel -->
        <div class="controls-panel">
            <div class="controls-left">
                <div class="btn-group">
                    <button class="tab-btn" onclick="setRole('All', this)">All Players</button>
                    <button class="tab-btn active" onclick="setRole('Batter', this)">Top Batters</button>
                    <button class="tab-btn" onclick="setRole('Bowler', this)">Top Bowlers</button>
                </div>
                <input type="text" id="searchInput" class="search-box" placeholder="Search player or team..." oninput="renderTable()">
                <select id="minMatchSelect" class="filter-select" onchange="renderTable()">
                    <option value="8" selected>Min HP Matches: 8 (Official)</option>
                    <option value="4">Min HP Matches: 4 (Broad)</option>
                    <option value="12">Min HP Matches: 12 (High Sample)</option>
                </select>
            </div>
            <button class="btn-export" onclick="exportCSV()">Export Table to CSV</button>
        </div>

        <!-- Main Data Table -->
        <div class="table-wrap">
            <table id="playersTable">
                <thead>
                    <tr>
                        <th style="width: 45px;">#</th>
                        <th onclick="sortBy('name')">Player</th>
                        <th onclick="sortBy('role')">Role</th>
                        <th onclick="sortBy('matches')" style="text-align: right;">Total M</th>
                        <th onclick="sortBy('hp_matches')" style="text-align: right;">HP M</th>
                        <th onclick="sortBy('hp_wr')" style="text-align: right;">HP Win %</th>
                        <th onclick="sortBy('base_wr')" style="text-align: right;">Base Win %</th>
                        <th onclick="sortBy('lift')" style="text-align: right;">Pressure Lift</th>
                        <th onclick="sortBy('mom_hp')" style="text-align: right;">HP MOM</th>
                        <th onclick="sortBy('ko_wr')" style="text-align: right;">KO Win %</th>
                        <th onclick="sortBy('cppi')" class="sort-active" style="text-align: right;">CPPI Score &darr;</th>
                    </tr>
                </thead>
                <tbody id="tableBody"></tbody>
            </table>
        </div>

        <!-- Methodology Footer -->
        <footer>
            <div class="method-note">
                <strong>Methodology Note:</strong> High-pressure matches defined via Match Leverage Index (MLI) using stage stakes (Finals, Playoffs), contest closeness (&le;15 runs / &le;2 wickets), and elimination flags. Composite Pressure Performance Index (CPPI) incorporates Bayesian shrinkage win rate (35%), knockout win rate (20%), Player of Match density (20%), pressure lift delta (15%), and baseline competency (10%), filtered for IPL Auction eligibility.
            </div>
            <div>Analyst: Ketan Rawat (NIT Jamshedpur) &bull; RR War Room</div>
        </footer>
    </div>

    <!-- Slide-over Drawer for Player Inspection -->
    <div id="drawerOverlay" class="drawer-overlay" onclick="closeDrawer(event)">
        <div class="drawer" onclick="event.stopPropagation()">
            <div class="drawer-header">
                <div>
                    <div id="dName" class="drawer-title">Player Name</div>
                    <div id="dTeams" class="drawer-subtitle">Teams</div>
                </div>
                <button class="drawer-close" onclick="closeDrawer()">&times;</button>
            </div>

            <div class="metric-block">
                <div style="font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px;">Pressure Performance Audit</div>
                <div class="metric-row">
                    <span style="color: var(--text-secondary);">CPPI Overall Score</span>
                    <span id="dCppi" style="font-weight: 700; color: var(--accent-blue);">63.28</span>
                </div>
                <div class="metric-row">
                    <span style="color: var(--text-secondary);">High-Pressure Matches</span>
                    <span id="dHpM">14</span>
                </div>
                <div class="metric-row">
                    <span style="color: var(--text-secondary);">HP Win Rate</span>
                    <span id="dHpWr" style="font-weight: 600;">71.4%</span>
                </div>
                <div class="metric-row">
                    <span style="color: var(--text-secondary);">Baseline Career Win Rate</span>
                    <span id="dBaseWr">60.4%</span>
                </div>
                <div class="metric-row">
                    <span style="color: var(--text-secondary);">Pressure Lift (&Delta;)</span>
                    <span id="dLift" style="font-weight: 600;">+11.1%</span>
                </div>
                <div class="metric-row">
                    <span style="color: var(--text-secondary);">Knockout Win Rate</span>
                    <span id="dKoWr">71.4%</span>
                </div>
                <div class="metric-row">
                    <span style="color: var(--text-secondary);">Player of Match (HP Games)</span>
                    <span id="dMom">2</span>
                </div>
            </div>

            <div class="tactical-box">
                <div class="tactical-title">Rajasthan Royals Tactical Fit (IPL 2027)</div>
                <p id="dTactical" class="tactical-text">Tactical profile.</p>
            </div>
        </div>
    </div>

    <script>
        const PLAYERS = {data_json};

        let currentRole = 'Batter';
        let currentSort = 'cppi';
        let currentSortDir = -1; // -1 = desc, 1 = asc

        function setRole(role, btn) {{
            currentRole = role;
            document.querySelectorAll('.btn-group .tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderTable();
        }}

        function sortBy(col) {{
            if (currentSort === col) {{
                currentSortDir *= -1;
            }} else {{
                currentSort = col;
                currentSortDir = col === 'name' || col === 'role' ? 1 : -1;
            }}
            renderTable();
        }}

        function renderTable() {{
            const search = document.getElementById('searchInput').value.toLowerCase().trim();
            const minHp = parseInt(document.getElementById('minMatchSelect').value, 10);

            let filtered = PLAYERS.filter(p => {{
                if (currentRole !== 'All' && p.role !== currentRole) return false;
                if (p.hp_matches < minHp) return false;
                if (search) {{
                    const matchName = p.name.toLowerCase().includes(search);
                    const matchTeam = p.teams.toLowerCase().includes(search);
                    if (!matchName && !matchTeam) return false;
                }}
                return true;
            }});

            filtered.sort((a, b) => {{
                let valA = a[currentSort];
                let valB = b[currentSort];
                if (typeof valA === 'string') {{
                    return valA.localeCompare(valB) * currentSortDir;
                }}
                return (valA - valB) * currentSortDir;
            }});

            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            filtered.forEach((p, idx) => {{
                const tr = document.createElement('tr');
                tr.onclick = () => openDrawer(p);

                const liftClass = p.lift > 0 ? 'lift-pos' : (p.lift < 0 ? 'lift-neg' : '');
                const liftSign = p.lift > 0 ? '+' : '';
                const rankClass = idx < 3 ? 'rank-num rank-top' : 'rank-num';

                tr.innerHTML = `
                    <td class="${{rankClass}}">${{idx + 1}}</td>
                    <td>
                        <div class="player-info">
                            <span class="player-name">${{p.name}}</span>
                            <span class="player-teams">${{p.teams.split(',').slice(0, 2).join(', ')}}</span>
                        </div>
                    </td>
                    <td><span class="pill-role">${{p.role}}</span></td>
                    <td style="text-align: right; color: var(--text-secondary);">${{p.matches}}</td>
                    <td style="text-align: right; font-weight: 500;">${{p.hp_matches}}</td>
                    <td style="text-align: right; font-weight: 600;">${{p.hp_wr.toFixed(1)}}%</td>
                    <td style="text-align: right; color: var(--text-secondary);">${{p.base_wr.toFixed(1)}}%</td>
                    <td style="text-align: right;" class="${{liftClass}}">${{liftSign}}${{p.lift.toFixed(1)}}%</td>
                    <td style="text-align: right;">${{p.mom_hp}}</td>
                    <td style="text-align: right; color: var(--text-secondary);">${{p.ko_wr.toFixed(1)}}%</td>
                    <td style="text-align: right;"><span class="score-badge">${{p.cppi.toFixed(2)}}</span></td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function openDrawer(p) {{
            document.getElementById('dName').innerText = p.name;
            document.getElementById('dTeams').innerText = p.teams;
            document.getElementById('dCppi').innerText = p.cppi.toFixed(2);
            document.getElementById('dHpM').innerText = p.hp_matches + ' matches (' + p.hp_wins + ' wins)';
            document.getElementById('dHpWr').innerText = p.hp_wr.toFixed(1) + '%';
            document.getElementById('dBaseWr').innerText = p.base_wr.toFixed(1) + '%';
            
            const liftEl = document.getElementById('dLift');
            liftEl.innerText = (p.lift > 0 ? '+' : '') + p.lift.toFixed(1) + '%';
            liftEl.className = p.lift > 0 ? 'lift-pos' : (p.lift < 0 ? 'lift-neg' : '');

            document.getElementById('dKoWr').innerText = p.ko_wr.toFixed(1) + '% (' + p.ko_matches + ' knockouts)';
            document.getElementById('dMom').innerText = p.mom_hp + ' awards';
            document.getElementById('dTactical').innerText = p.note;

            document.getElementById('drawerOverlay').classList.add('open');
        }}

        function closeDrawer(e) {{
            document.getElementById('drawerOverlay').classList.remove('open');
        }}

        function exportCSV() {{
            const search = document.getElementById('searchInput').value.toLowerCase().trim();
            const minHp = parseInt(document.getElementById('minMatchSelect').value, 10);
            let filtered = PLAYERS.filter(p => {{
                if (currentRole !== 'All' && p.role !== currentRole) return false;
                if (p.hp_matches < minHp) return false;
                if (search && !p.name.toLowerCase().includes(search) && !p.teams.toLowerCase().includes(search)) return false;
                return true;
            }});

            let csv = "Rank,Player,Role,Teams,Total_Matches,HP_Matches,HP_Win_Rate,Base_Win_Rate,Pressure_Lift,HP_MOM,KO_Win_Rate,CPPI\\n";
            filtered.forEach((p, i) => {{
                csv += `"${{i+1}}","${{p.name}}","${{p.role}}","${{p.teams}}",${{p.matches}},${{p.hp_matches}},${{p.hp_wr}},${{p.base_wr}},${{p.lift}},${{p.mom_hp}},${{p.ko_wr}},${{p.cppi}}\\n`;
            }});

            const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.setAttribute("download", `RR_Pressure_Rankings_${{currentRole}}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}

        // Initial render
        renderTable();
    </script>
</body>
</html>
"""

with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(OUTPUT_HTML_COPY, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✓ Clean, Professional Dashboard compiled to: {OUTPUT_HTML}")
print(f"✓ Copy saved to: {OUTPUT_HTML_COPY}")

