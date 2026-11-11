import csv
import re
from collections import defaultdict

with open(r'season2_data\competitions.csv', encoding='utf-8') as f:
    comps = {r['comp_id']: r for r in csv.DictReader(f)}

with open(r'season2_data\matches.csv', encoding='utf-8') as f:
    matches = {r['match_id']: r for r in csv.DictReader(f)}

with open(r'season2_data\playing_eleven.csv', encoding='utf-8') as f:
    p11 = list(csv.DictReader(f))

with open(r'season2_data\competition_team_player_mapping.csv', encoding='utf-8') as f:
    ctpm = list(csv.DictReader(f))

pnames = {r['player_id']: r['player_name'] for r in ctpm}

def get_match_pressure(m):
    result = m.get('result', '').lower()
    stage = m.get('stage', '').lower()
    knockout = int(m.get('knock_out', '0') or '0')
    if 'final' in stage and 'semi' not in stage: s_score = 40
    elif 'semi' in stage: s_score = 35
    elif any(x in stage for x in ['qualifier', 'eliminator', 'playoff']): s_score = 30
    elif 'super 4' in stage: s_score = 20
    else: s_score = 5
    runs_m = re.search(r'won by (\d+) run', result)
    wkts_m = re.search(r'won by (\d+) wicket', result)
    if 'super over' in result or 'tied' in result: c_score = 40
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
    else: c_score = 2
    k_score = 20 if knockout == 1 else 0
    dls_bonus = 5 if m.get('revised_target') else 0
    return min(100, s_score + c_score + k_score + dls_bonus)

match_pressure = {mid: get_match_pressure(m) for mid, m in matches.items()}

p_matches = defaultdict(int)
p_wins = defaultdict(int)
p_hp_matches = defaultdict(int)
p_hp_wins = defaultdict(int)
p_ko_matches = defaultdict(int)
p_ko_wins = defaultdict(int)
p_mom_hp = defaultdict(int)

for row in p11:
    if row.get('is_played', 'true').lower() not in ('true', '1'):
        continue
    pid = row['player_id']
    mid = row['match_id']
    tid = row['team_id']
    if mid not in matches: continue
    m = matches[mid]
    win = (m.get('win_team_id') == tid)
    mom = (m.get('man_of_the_match') == pid)
    ko = int(m.get('knock_out', '0') or '0') == 1
    ps = match_pressure[mid]
    is_hp = ps >= 30
    
    p_matches[pid] += 1
    if win: p_wins[pid] += 1
    if ko:
        p_ko_matches[pid] += 1
        if win: p_ko_wins[pid] += 1
    if is_hp:
        p_hp_matches[pid] += 1
        if win: p_hp_wins[pid] += 1
        if mom: p_mom_hp[pid] += 1

five = ['Jasprit Bumrah', 'Mohammed Siraj', 'Rashid Khan', 'Heinrich Klaasen', 'Rohit Sharma']

for name in five:
    matching_pids = [pid for pid, pname in pnames.items() if name.lower() in pname.lower()]
    print(f"=== {name} ===")
    for pid in matching_pids:
        tm = p_matches[pid]
        tw = p_wins[pid]
        hpm = p_hp_matches[pid]
        hpw = p_hp_wins[pid]
        kom = p_ko_matches[pid]
        kow = p_ko_wins[pid]
        b_wr = (tw / tm * 100) if tm > 0 else 0
        hp_wr = (hpw / hpm * 100) if hpm > 0 else 0
        lift = hp_wr - b_wr
        print(f"  PID {pid} ({pnames[pid]}): Total Matches={tm}, Wins={tw} ({b_wr:.1f}%), HP Matches={hpm}, HP Wins={hpw} ({hp_wr:.1f}%), Lift={lift:+.1f}%, KO Matches={kom}, KO Wins={kow}")

