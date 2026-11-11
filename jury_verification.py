import json
import csv
from collections import defaultdict
from rr_pressure_analyst import get_match_pressure

with open('players_db.json', 'r', encoding='utf-8') as f:
    db_players = json.load(f)

with open('season2_data/matches.csv', encoding='utf-8') as f:
    matches = {r['match_id']: r for r in csv.DictReader(f)}

with open('season2_data/playing_eleven.csv', encoding='utf-8') as f:
    p11 = list(csv.DictReader(f))

with open('season2_data/competition_team_player_mapping.csv', encoding='utf-8') as f:
    ctpm = list(csv.DictReader(f))

name_to_pids = defaultdict(set)
pid_to_name = {}
for r in ctpm:
    pid = r['player_id']
    pname = r['player_name'].strip()
    name_to_pids[pname.lower()].add(pid)
    pid_to_name[pid] = pname

match_pressure = {mid: get_match_pressure(m) for mid, m in matches.items()}

print('=== VERIFYING PLAYERS_DB.JSON STATS AGAINST RAW DATA ===')
discrepancies = []

for p in db_players:
    name = p['name'].strip()
    pids = name_to_pids.get(name.lower(), set())
    if not pids:
        for nm, pset in name_to_pids.items():
            if name.lower() in nm or nm in name.lower():
                pids = pset
                break
                
    matches_played = [r for r in p11 if r['player_id'] in pids and r.get('is_played','true').lower() in ('true','1')]
    tot_m = len(matches_played)
    
    hp_m = 0
    hp_w = 0
    tot_w = 0
    ko_m = 0
    ko_w = 0
    mom_hp = 0
    
    for r in matches_played:
        mid = r['match_id']
        tid = r['team_id']
        pid = r['player_id']
        if mid not in matches: continue
        m = matches[mid]
        win = (m.get('win_team_id') == tid)
        ko = (int(m.get('knock_out', '0') or '0') == 1)
        is_hp = match_pressure[mid]['is_high_pressure']
        mom = (m.get('man_of_the_match') == pid)
        
        if win: tot_w += 1
        if ko:
            ko_m += 1
            if win: ko_w += 1
        if is_hp:
            hp_m += 1
            if win: hp_w += 1
            if mom: mom_hp += 1
            
    base_wr = round(tot_w / tot_m * 100, 1) if tot_m > 0 else 0
    hp_wr = round(hp_w / hp_m * 100, 1) if hp_m > 0 else 0
    lift = round(hp_wr - base_wr, 1)
    
    diff_hp_wr = abs(hp_wr - p['hp_wr'])
    diff_base_wr = abs(base_wr - p['base_wr'])
    diff_lift = abs(lift - p['lift'])
    
    status = 'MATCH' if (diff_hp_wr < 0.2 and diff_base_wr < 0.2 and diff_lift < 0.2) else 'MISMATCH'
    if status == 'MISMATCH':
        discrepancies.append((name, p['hp_wr'], hp_wr, p['base_wr'], base_wr, p['lift'], lift))
    cat = p['category'][:3]
    rank = p['rank']
    hp_m_db = p['hp_m']
    hp_wr_db = p['hp_wr']
    lift_db = p['lift']
    print(f"{cat} #{rank:2} {name:20} | TotM: {tot_m:2} (db: {p['total_m']:2}) | HP M: {hp_m:2} (db: {hp_m_db:2}) | HP WR: {hp_wr:5.1f}% (db: {hp_wr_db:5.1f}%) | Lift: {lift:+5.1f}% (db: {lift_db:+5.1f}%) | {status}")

print('\nTotal Discrepancies:', len(discrepancies))
