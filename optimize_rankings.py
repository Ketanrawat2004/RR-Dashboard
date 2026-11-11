import csv
import re
from collections import defaultdict
import math

# Load all 5 data files
with open(r'C:\Rajasthan Royals\season2_data\competitions.csv', encoding='utf-8') as f:
    comps = {r['comp_id']: r for r in csv.DictReader(f)}

with open(r'C:\Rajasthan Royals\season2_data\matches.csv', encoding='utf-8') as f:
    matches = {r['match_id']: r for r in csv.DictReader(f)}

with open(r'C:\Rajasthan Royals\season2_data\playing_eleven.csv', encoding='utf-8') as f:
    p11 = list(csv.DictReader(f))

with open(r'C:\Rajasthan Royals\season2_data\competition_team_player_mapping.csv', encoding='utf-8') as f:
    ctpm = list(csv.DictReader(f))

pnames = {r['player_id']: r['player_name'] for r in ctpm}
teams_by_pid = defaultdict(set)
comps_by_pid = defaultdict(set)
for r in ctpm:
    teams_by_pid[r['player_id']].add(r['team_name'])
    comps_by_pid[r['player_id']].add(r['comp_name'])

# Pressure calculation with multi-tier nuance
def get_match_pressure(m):
    result = m.get('result', '').lower()
    stage = m.get('stage', '').lower()
    knockout = int(m.get('knock_out', '0') or '0')
    
    # 1. Stage Stakes (0-40)
    if 'final' in stage and 'semi' not in stage:
        s_score = 40
    elif 'semi' in stage:
        s_score = 35
    elif any(x in stage for x in ['qualifier', 'eliminator', 'playoff']):
        s_score = 30
    elif 'super 4' in stage:
        s_score = 20
    else:
        s_score = 5
        
    # 2. Closeness / Tension (0-40)
    runs_m = re.search(r'won by (\d+) run', result)
    wkts_m = re.search(r'won by (\d+) wicket', result)
    
    if 'super over' in result or 'tied' in result:
        c_score = 40
    elif runs_m:
        mrg = int(runs_m.group(1))
        if mrg <= 5: c_score = 38
        elif mrg <= 10: c_score = 32
        elif mrg <= 15: c_score = 26
        elif mrg <= 25: c_score = 18
        elif mrg <= 35: c_score = 10
        else: c_score = 4
    elif wkts_m:
        mrg = int(wkts_m.group(1))
        if mrg == 1: c_score = 38
        elif mrg == 2: c_score = 32
        elif mrg == 3: c_score = 24
        elif mrg <= 5: c_score = 14
        elif mrg <= 7: c_score = 6
        else: c_score = 2
    else:
        c_score = 2
        
    # 3. Elimination binary (0-20)
    k_score = 20 if knockout == 1 else 0
    
    # 4. Rain / Revised target tension bonus (+5 if DLS revised)
    dls_bonus = 5 if m.get('revised_target') else 0
    
    return min(100, s_score + c_score + k_score + dls_bonus)

match_pressure = {mid: get_match_pressure(m) for mid, m in matches.items()}

# Player aggregates
p_orders = defaultdict(list)
p_matches = defaultdict(int)
p_wins = defaultdict(int)
p_hp_matches = defaultdict(int)
p_hp_wins = defaultdict(int)
p_ko_matches = defaultdict(int)
p_ko_wins = defaultdict(int)
p_mom_all = defaultdict(int)
p_mom_hp = defaultdict(int)
p_is_wk = defaultdict(bool)
p_captain_matches = defaultdict(int)

for row in p11:
    if row.get('is_played', 'true').lower() not in ('true', '1'):
        continue
    pid = row['player_id']
    mid = row['match_id']
    tid = row['team_id']
    
    if mid not in matches:
        continue
    m = matches[mid]
    win = (m.get('win_team_id') == tid)
    mom = (m.get('man_of_the_match') == pid)
    ko = int(m.get('knock_out', '0') or '0') == 1
    ps = match_pressure[mid]
    is_hp = ps >= 30
    
    p_matches[pid] += 1
    if win: p_wins[pid] += 1
    if mom: p_mom_all[pid] += 1
    if ko:
        p_ko_matches[pid] += 1
        if win: p_ko_wins[pid] += 1
    if is_hp:
        p_hp_matches[pid] += 1
        if win: p_hp_wins[pid] += 1
        if mom: p_mom_hp[pid] += 1
        
    bo = row.get('batting_order')
    if bo and bo.isdigit() and int(bo) > 0:
        p_orders[pid].append(int(bo))
    if row.get('is_wk', 'false').lower() in ('true', '1'):
        p_is_wk[pid] = True
    if row.get('is_captain', 'false').lower() in ('true', '1'):
        p_captain_matches[pid] += 1

# Robust role classifier
def classify_player(pid):
    # If designated WK in multiple matches -> Batter
    if p_is_wk[pid]:
        return 'Batter'
    orders = p_orders.get(pid, [])
    if not orders:
        return 'Bowler'
    avg_bo = sum(orders) / len(orders)
    # Positions 1 to 6 are specialized batters / batting ARs
    if avg_bo <= 6.3:
        return 'Batter'
    # Positions 8.2 and above are tailender specialist bowlers
    elif avg_bo >= 8.2:
        return 'Bowler'
    else:
        # 6.4 to 8.1 zone: look at frequency of batting in top 6 vs 8+
        top_6 = sum(1 for o in orders if o <= 6)
        bottom_8 = sum(1 for o in orders if o >= 8)
        if top_6 >= bottom_8:
            return 'Batter'
        else:
            return 'Bowler'

# Build CPPI with Bayesian regularization
# To ensure fairness, we require at least 12 matches and at least 4 high-pressure appearances
records = []
for pid in p_matches:
    if p_matches[pid] < 12 or p_hp_matches[pid] < 4:
        continue
        
    n_all = p_matches[pid]
    n_hp = p_hp_matches[pid]
    n_ko = p_ko_matches[pid]
    
    base_wr = p_wins[pid] / n_all * 100
    
    # Bayesian Shrinkage on HP win rate:
    # Prior mean = base_wr, Prior strength M = 5 matches
    # Adjusted_HP_WR = (HP_Wins + M * (base_wr/100)) / (n_hp + M) * 100
    M = 5.0
    bayes_hp_wr = (p_hp_wins[pid] + M * (base_wr / 100)) / (n_hp + M) * 100
    raw_hp_wr = p_hp_wins[pid] / n_hp * 100
    
    # Knockout win rate with fallback to baseline if 0 KO matches
    if n_ko > 0:
        M_ko = 3.0
        bayes_ko_wr = (p_ko_wins[pid] + M_ko * (base_wr / 100)) / (n_ko + M_ko) * 100
        raw_ko_wr = p_ko_wins[pid] / n_ko * 100
    else:
        bayes_ko_wr = base_wr
        raw_ko_wr = base_wr
        
    # Pressure Lift: difference between HP win rate and baseline
    pressure_lift = raw_hp_wr - base_wr
    
    # Clutch Impact Density (MOM in HP)
    # MOM awards are rare (~1 per match across 22 players, so ~4.5% base probability)
    mom_hp_pct = (p_mom_hp[pid] / n_hp * 100)
    
    # Experience / Sample Size Credibility Curve: log-sigmoid saturation
    # saturated at ~20 HP matches
    credibility = 1.0 / (1.0 + math.exp(-0.25 * (n_hp - 8)))
    
    # CPPI Formula (0-100)
    # 35% Bayes HP Win Rate
    # 20% Bayes Knockout Win Rate
    # 20% Clutch MOM Impact (scaled so 10% MOM rate yields ~20 pts)
    # 15% Pressure Lift (normalized around 50)
    # 10% Baseline Win Rate
    lift_component = max(0.0, min(100.0, 50.0 + pressure_lift * 1.5))
    mom_component = min(100.0, mom_hp_pct * 4.0)
    
    raw_cppi = (
        0.35 * bayes_hp_wr +
        0.20 * bayes_ko_wr +
        0.20 * mom_component +
        0.15 * lift_component +
        0.10 * base_wr
    )
    
    # Final CPPI scaled by credibility
    final_cppi = raw_cppi * (0.85 + 0.15 * credibility)
    
    role = classify_player(pid)
    
    records.append({
        'pid': pid,
        'name': pnames.get(pid, f'Player_{pid}'),
        'role': role,
        'teams': ', '.join(sorted(teams_by_pid[pid])),
        'total_matches': n_all,
        'base_wr': round(base_wr, 1),
        'hp_matches': n_hp,
        'hp_wins': p_hp_wins[pid],
        'raw_hp_wr': round(raw_hp_wr, 1),
        'bayes_hp_wr': round(bayes_hp_wr, 1),
        'pressure_lift': round(pressure_lift, 1),
        'ko_matches': n_ko,
        'ko_wins': p_ko_wins[pid],
        'ko_wr': round(raw_ko_wr, 1),
        'mom_all': p_mom_all[pid],
        'mom_hp': p_mom_hp[pid],
        'mom_hp_pct': round(mom_hp_pct, 1),
        'credibility': round(credibility, 2),
        'cppi': round(final_cppi, 2),
    })

batters = sorted([r for r in records if r['role'] == 'Batter'], key=lambda x: -x['cppi'])
bowlers = sorted([r for r in records if r['role'] == 'Bowler'], key=lambda x: -x['cppi'])

print('=' * 85)
print('TOP 12 BATTERS UNDER PRESSURE')
print('=' * 85)
print(f'{"Rank":<4} {"Player":<24} {"Teams":<28} {"HP M":>5} {"HP WR":>6} {"Lift":>6} {"MOM HP":>6} {"KO WR":>6} {"CPPI":>6}')
print('-' * 85)
for i, r in enumerate(batters[:12], 1):
    print(f'{i:<4} {r["name"]:<24} {r["teams"][:26]:<28} {r["hp_matches"]:>5} {r["raw_hp_wr"]:>5.1f}% {r["pressure_lift"]:>+5.1f}% {r["mom_hp"]:>6} {r["ko_wr"]:>5.1f}% {r["cppi"]:>6.2f}')

print()
print('=' * 85)
print('TOP 12 BOWLERS UNDER PRESSURE')
print('=' * 85)
print(f'{"Rank":<4} {"Player":<24} {"Teams":<28} {"HP M":>5} {"HP WR":>6} {"Lift":>6} {"MOM HP":>6} {"KO WR":>6} {"CPPI":>6}')
print('-' * 85)
for i, r in enumerate(bowlers[:12], 1):
    print(f'{i:<4} {r["name"]:<24} {r["teams"][:26]:<28} {r["hp_matches"]:>5} {r["raw_hp_wr"]:>5.1f}% {r["pressure_lift"]:>+5.1f}% {r["mom_hp"]:>6} {r["ko_wr"]:>5.1f}% {r["cppi"]:>6.2f}')

