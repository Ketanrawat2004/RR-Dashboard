import re
import json
import pandas as pd
import numpy as np

# Load Step 4 CSVs
df_bat = pd.read_csv('phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv')
df_comp = pd.read_csv('phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_COMPOSITE.csv')
df_rpae = pd.read_csv('phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv')

# Load players_db.json
with open('players_db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# Load index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Verify Batters Table
m_bat = re.search(r'<table id="table-batters">[\s\S]*?<\/tbody>', html)
bat_rows = re.findall(r'<tr[^>]*>[\s\S]*?<\/tr>', m_bat.group(0))[1:]

bat_failures = []
for idx, r in enumerate(bat_rows):
    s4 = df_bat.iloc[idx]
    tds = [re.sub(r'<[^>]*>', '', td).strip() for td in re.findall(r'<td\b[^>]*>([\s\S]*?)<\/td>', r)]
    
    rank_html = int(tds[0])
    lev_b_html = int(tds[3])
    p_sr_html = float(tds[4])
    exp_sr_html = float(tds[5])
    diff_html = float(tds[6].replace('+', ''))
    career_b_html = int(tds[7].replace(',', ''))
    rank_bound_html = tds[8]
    shrunk_html = float(tds[9].replace('+', ''))
    
    # Expected Step 4
    if rank_html != int(s4['rank']):
        bat_failures.append((s4['player_name'], 'rank', rank_html, s4['rank']))
    if lev_b_html != int(round(s4['pressure_bf'])):
        bat_failures.append((s4['player_name'], 'pressure_bf', lev_b_html, s4['pressure_bf']))
    if abs(p_sr_html - round(s4['pressure_sr'], 1)) > 0.15:
        bat_failures.append((s4['player_name'], 'pressure_sr', p_sr_html, s4['pressure_sr']))
    if abs(exp_sr_html - round(s4['pressure_exp_sr'], 1)) > 0.15:
        bat_failures.append((s4['player_name'], 'pressure_exp_sr', exp_sr_html, s4['pressure_exp_sr']))
    if abs(diff_html - round(s4['raw_pressure_rae_rate'], 2)) > 0.05:
        bat_failures.append((s4['player_name'], 'raw_pressure_rae_rate', diff_html, s4['raw_pressure_rae_rate']))
    if career_b_html != int(s4['career_bf']):
        bat_failures.append((s4['player_name'], 'career_bf', career_b_html, s4['career_bf']))
    if rank_bound_html != s4['rank_ci_90']:
        bat_failures.append((s4['player_name'], 'rank_ci_90', rank_bound_html, s4['rank_ci_90']))
    if abs(shrunk_html - round(s4['shrunk_rae_score'], 2)) > 0.05:
        bat_failures.append((s4['player_name'], 'shrunk_rae_score', shrunk_html, s4['shrunk_rae_score']))

print(f"Batters checked: {len(bat_rows)}, Failures: {len(bat_failures)}")
if bat_failures:
    print("Sample batter failures:", bat_failures[:5])

# 2. Verify Bowlers Table
m_bowl = re.search(r'<table id="table-bowlers">[\s\S]*?<\/tbody>', html)
bowl_rows = re.findall(r'<tr[^>]*>[\s\S]*?<\/tr>', m_bowl.group(0))

comp_rows = [r for r in bowl_rows if "bowler-row-composite" in r]
rpae_rows = [r for r in bowl_rows if "bowler-row-rpae" in r]

comp_failures = []
for idx, r in enumerate(comp_rows):
    s4 = df_comp.iloc[idx]
    tds = [re.sub(r'<[^>]*>', '', td).strip() for td in re.findall(r'<td\b[^>]*>([\s\S]*?)<\/td>', r)]
    
    rank_html = int(tds[0])
    lev_b_html = int(tds[3])
    p_econ_html = float(tds[4])
    exp_econ_html = float(tds[5])
    diff_html = float(tds[6].replace('+', ''))
    # tds[7] is "20 (+10.1)" -> wkts and wae
    rank_bound_html = tds[8]
    shrunk_html = float(tds[9].replace('+', ''))
    
    if rank_html != int(s4['rank_composite']):
        comp_failures.append((s4['player_name'], 'rank', rank_html, s4['rank_composite']))
    if lev_b_html != int(round(s4['pressure_b'])):
        comp_failures.append((s4['player_name'], 'pressure_b', lev_b_html, s4['pressure_b']))
    if abs(shrunk_html - round(s4['composite_score'], 2)) > 0.05:
        comp_failures.append((s4['player_name'], 'composite_score', shrunk_html, s4['composite_score']))
    if rank_bound_html != s4['rank_ci_90']:
        comp_failures.append((s4['player_name'], 'rank_ci_90', rank_bound_html, s4['rank_ci_90']))

print(f"Bowler Composite rows checked: {len(comp_rows)}, Failures: {len(comp_failures)}")

rpae_failures = []
for idx, r in enumerate(rpae_rows):
    s4 = df_rpae.iloc[idx]
    tds = [re.sub(r'<[^>]*>', '', td).strip() for td in re.findall(r'<td\b[^>]*>([\s\S]*?)<\/td>', r)]
    
    rank_html = int(tds[0])
    lev_b_html = int(tds[3])
    p_econ_html = float(tds[4])
    exp_econ_html = float(tds[5])
    diff_html = float(tds[6].replace('+', ''))
    career_b_html = int(tds[7].replace(',', ''))
    rank_bound_html = tds[8]
    shrunk_html = float(tds[9].replace('+', ''))
    
    if rank_html != int(s4['rank_rpae']):
        rpae_failures.append((s4['player_name'], 'rank', rank_html, s4['rank_rpae']))
    if lev_b_html != int(round(s4['pressure_b'])):
        rpae_failures.append((s4['player_name'], 'pressure_b', lev_b_html, s4['pressure_b']))
    if abs(p_econ_html - round(s4['pressure_econ'], 2)) > 0.05:
        rpae_failures.append((s4['player_name'], 'pressure_econ', p_econ_html, s4['pressure_econ']))
    if abs(exp_econ_html - round(s4['pressure_exp_econ'], 2)) > 0.05:
        rpae_failures.append((s4['player_name'], 'pressure_exp_econ', exp_econ_html, s4['pressure_exp_econ']))
    if career_b_html != int(s4['career_b']):
        rpae_failures.append((s4['player_name'], 'career_b', career_b_html, s4['career_b']))
    if rank_bound_html != s4['rank_ci_90']:
        rpae_failures.append((s4['player_name'], 'rank_ci_90', rank_bound_html, s4['rank_ci_90']))
    if abs(shrunk_html - round(s4['shrunk_rpae_score'], 2)) > 0.05:
        rpae_failures.append((s4['player_name'], 'shrunk_rpae_score', shrunk_html, s4['shrunk_rpae_score']))

print(f"Bowler RPAE rows checked: {len(rpae_rows)}, Failures: {len(rpae_failures)}")

# 3. Verify players_db.json
db_bat = {p['player_id']: p for p in db if p.get('category') == 'Batter'}
db_comp = {p['player_id']: p for p in db if p.get('category') == 'Bowler'}

db_failures = []
for idx, s4 in df_bat.iterrows():
    pid = int(s4['player_id'])
    p = db_bat.get(pid)
    if not p:
        db_failures.append((s4['player_name'], 'missing in db'))
        continue
    if p['pressure_balls'] != int(round(s4['pressure_bf'])):
        db_failures.append((s4['player_name'], 'db_pressure_balls', p['pressure_balls'], s4['pressure_bf']))
    if abs(p['shrunk_score'] - round(s4['shrunk_rae_score'], 2)) > 0.05:
        db_failures.append((s4['player_name'], 'db_shrunk_score', p['shrunk_score'], s4['shrunk_rae_score']))
    if p['rank_ci_90'] != s4['rank_ci_90']:
        db_failures.append((s4['player_name'], 'db_rank_ci_90', p['rank_ci_90'], s4['rank_ci_90']))
    if abs(p['top10_prob_pct'] - round(s4['top10_prob_pct'], 1)) > 0.15:
        db_failures.append((s4['player_name'], 'db_top10_prob_pct', p['top10_prob_pct'], s4['top10_prob_pct']))

for idx, s4 in df_comp.iterrows():
    pid = int(s4['player_id'])
    p = db_comp.get(pid)
    if not p:
        db_failures.append((s4['player_name'], 'missing in db'))
        continue
    if p['pressure_balls'] != int(round(s4['pressure_b'])):
        db_failures.append((s4['player_name'], 'db_pressure_balls', p['pressure_balls'], s4['pressure_b']))
    if abs(p['composite_score'] - round(s4['composite_score'], 2)) > 0.05:
        db_failures.append((s4['player_name'], 'db_composite_score', p['composite_score'], s4['composite_score']))
    if p['rank_ci_90'] != s4['rank_ci_90']:
        db_failures.append((s4['player_name'], 'db_rank_ci_90', p['rank_ci_90'], s4['rank_ci_90']))
    if abs(p['top10_prob_pct'] - round(s4['top10_prob_pct'], 1)) > 0.15:
        db_failures.append((s4['player_name'], 'db_top10_prob_pct', p['top10_prob_pct'], s4['top10_prob_pct']))

print(f"players_db.json checks complete. Total DB Failures: {len(db_failures)}")

