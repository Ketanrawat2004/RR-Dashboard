import re
import json
import pandas as pd
import numpy as np

# Load Step 4 Authoritative CSVs
df_step4_bat = pd.read_csv('phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv')
df_step4_comp = pd.read_csv('phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_COMPOSITE.csv')
df_step4_rpae = pd.read_csv('phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv')

# Load players_db.json
with open('players_db.json', 'r', encoding='utf-8') as f:
    players_db = json.load(f)

# Load index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Map DB entries
db_bat = {p['player_id']: p for p in players_db if p.get('category') == 'Batter'}
db_bowl = {p['player_id']: p for p in players_db if p.get('category') == 'Bowler'}

# 1. Parse Batters from index.html
m_bat = re.search(r'<table id="table-batters">[\s\S]*?<\/tbody>', html)
bat_rows = re.findall(r'<tr[^>]*>[\s\S]*?<\/tr>', m_bat.group(0))[1:] # skip header

html_batters = []
for r in bat_rows:
    tds = [re.sub(r'<[^>]*>', '', td).strip() for td in re.findall(r'<td\b[^>]*>([\s\S]*?)<\/td>', r)]
    m_name = re.search(r'<div class="name-box">\s*<(?:a|span)[^>]*>([^<]+)<\/(?:a|span)>', r)
    name = m_name.group(1).strip() if m_name else ""
    m_slug = re.search(r'href=[\'"]players/([^\'"]+)\.html[\'"]', r)
    slug = m_slug.group(1) if m_slug else ""
    
    html_batters.append({
        'rank': int(tds[0]),
        'name': name,
        'slug': slug,
        'lev_balls': int(tds[3]),
        'pressure_sr': float(tds[4]),
        'exp_sr': float(tds[5]),
        'rae_diff': tds[6],
        'career_balls': tds[7],
        'rank_bound': tds[8],
        'shrunk_rae': tds[9]
    })

df_html_bat = pd.DataFrame(html_batters)

# Build Batter Reconciliation
bat_recon_rows = []
for idx, s4 in df_step4_bat.iterrows():
    pid = int(s4['player_id'])
    pname = s4['player_name']
    s4_rank = int(s4['rank'])
    s4_p_bf = int(round(s4['pressure_bf']))
    s4_sr = round(float(s4['pressure_sr']), 1)
    s4_exp_sr = round(float(s4['pressure_exp_sr']), 1)
    s4_diff = f"{s4['raw_pressure_rae_rate']:+.2f}"
    s4_score = f"{s4['shrunk_rae_score']:+.2f}"
    s4_ci = s4['rank_ci_90']
    
    # DB
    dbp = db_bat.get(pid)
    db_n = dbp.get('pressure_balls') if dbp else None
    
    # HTML
    html_row = df_html_bat[df_html_bat['rank'] == s4_rank]
    if len(html_row) > 0:
        h = html_row.iloc[0]
        h_name = h['name']
        h_n = h['lev_balls']
        h_sr = h['pressure_sr']
        h_exp_sr = h['exp_sr']
        h_diff = h['rae_diff']
        h_score = h['shrunk_rae']
        h_ci = h['rank_bound']
    else:
        h_name, h_n, h_sr, h_exp_sr, h_diff, h_score, h_ci = "", None, None, None, "", "", ""
        
    discrepancy = (h_n - s4_p_bf) if (h_n is not None) else 'MISSING'
    status = 'MATCH' if (s4_p_bf == db_n == h_n and s4_rank == h['rank']) else 'MISMATCH'
    
    bat_recon_rows.append({
        'rank': s4_rank,
        'player_id': pid,
        'player_name': pname,
        'step4_pressure_bf': s4_p_bf,
        'db_pressure_balls': db_n,
        'html_displayed_leverage_deliveries': h_n,
        'discrepancy': discrepancy,
        'status': status,
        'step4_pressure_sr': s4_sr,
        'html_pressure_sr': h_sr,
        'step4_exp_sr': s4_exp_sr,
        'html_exp_sr': h_exp_sr,
        'step4_shrunk_rae': s4_score,
        'html_shrunk_rae': h_score,
        'step4_rank_ci_90': s4_ci,
        'html_rank_ci_90': h_ci
    })

df_bat_recon = pd.DataFrame(bat_recon_rows)
df_bat_recon.to_csv('phase1_audit/phase2c_post_validation/BATTER_DELIVERY_COUNT_RECONCILIATION.csv', index=False)
print(f"BATTER_DELIVERY_COUNT_RECONCILIATION.csv created: {len(df_bat_recon)} rows.")
print("Batter status breakdown:")
print(df_bat_recon['status'].value_counts())

# 2. Parse Bowlers from index.html
m_bowl = re.search(r'<table id="table-bowlers">[\s\S]*?<\/tbody>', html)
bowl_rows = re.findall(r'<tr[^>]*>[\s\S]*?<\/tr>', m_bowl.group(0))

comp_rows = [r for r in bowl_rows if "bowler-row-composite" in r]
rpae_rows = [r for r in bowl_rows if "bowler-row-rpae" in r]

def parse_bowl_list(rows):
    res = []
    for r in rows:
        tds = [re.sub(r'<[^>]*>', '', td).strip() for td in re.findall(r'<td\b[^>]*>([\s\S]*?)<\/td>', r)]
        m_name = re.search(r'<div class="name-box">\s*<(?:a|span)[^>]*>([^<]+)<\/(?:a|span)>', r)
        name = m_name.group(1).strip() if m_name else ""
        m_slug = re.search(r'href=[\'"]players/([^\'"]+)\.html[\'"]', r)
        slug = m_slug.group(1) if m_slug else ""
        res.append({
            'rank': int(tds[0]),
            'name': name,
            'slug': slug,
            'lev_balls': int(tds[3]),
            'pressure_econ': float(tds[4]),
            'exp_econ': float(tds[5]),
            'econ_diff': tds[6],
            'col7': tds[7],
            'rank_bound': tds[8],
            'shrunk_score': tds[9]
        })
    return pd.DataFrame(res)

df_html_comp = parse_bowl_list(comp_rows)
df_html_rpae = parse_bowl_list(rpae_rows)

bowl_recon_rows = []

# A. Composite Bowlers
for idx, s4 in df_step4_comp.iterrows():
    pid = int(s4['player_id'])
    pname = s4['player_name']
    s4_rank = int(s4['rank_composite'])
    s4_p_b = int(round(s4['pressure_b']))
    s4_score = f"{s4['composite_score']:+.2f}"
    s4_ci = s4['rank_ci_90']
    
    dbp = db_bowl.get(pid)
    db_n = dbp.get('pressure_balls') if dbp else None
    
    html_row = df_html_comp[df_html_comp['rank'] == s4_rank]
    if len(html_row) > 0:
        h = html_row.iloc[0]
        h_name = h['name']
        h_n = h['lev_balls']
        h_econ = h['pressure_econ']
        h_exp_econ = h['exp_econ']
        h_score = h['shrunk_score']
        h_ci = h['rank_bound']
    else:
        h_name, h_n, h_econ, h_exp_econ, h_score, h_ci = "", None, None, None, "", ""
        
    discrepancy = (h_n - s4_p_b) if (h_n is not None) else 'MISSING'
    status = 'MATCH' if (s4_p_b == db_n == h_n and s4_rank == h['rank']) else 'MISMATCH'
    
    bowl_recon_rows.append({
        'framework': 'Composite (60/40)',
        'rank': s4_rank,
        'player_id': pid,
        'player_name': pname,
        'step4_pressure_b': s4_p_b,
        'db_pressure_balls': db_n,
        'html_displayed_leverage_deliveries': h_n,
        'discrepancy': discrepancy,
        'status': status,
        'html_pressure_econ': h_econ,
        'html_exp_econ': h_exp_econ,
        'step4_shrunk_score': s4_score,
        'html_shrunk_score': h_score,
        'step4_rank_ci_90': s4_ci,
        'html_rank_ci_90': h_ci
    })

# B. Pure RPAE Bowlers
for idx, s4 in df_step4_rpae.iterrows():
    pid = int(s4['player_id'])
    pname = s4['player_name']
    s4_rank = int(s4['rank_rpae'])
    s4_p_b = int(round(s4['pressure_b']))
    s4_econ = round(float(s4['pressure_econ']), 2)
    s4_exp_econ = round(float(s4['pressure_exp_econ']), 2)
    s4_score = f"{s4['shrunk_rpae_score']:+.2f}"
    s4_ci = s4['rank_ci_90']
    
    dbp = db_bowl.get(pid)
    db_n = dbp.get('pressure_balls') if dbp else None
    
    html_row = df_html_rpae[df_html_rpae['rank'] == s4_rank]
    if len(html_row) > 0:
        h = html_row.iloc[0]
        h_name = h['name']
        h_n = h['lev_balls']
        h_econ = h['pressure_econ']
        h_exp_econ = h['exp_econ']
        h_score = h['shrunk_score']
        h_ci = h['rank_bound']
    else:
        h_name, h_n, h_econ, h_exp_econ, h_score, h_ci = "", None, None, None, "", ""
        
    discrepancy = (h_n - s4_p_b) if (h_n is not None) else 'MISSING'
    status = 'MATCH' if (s4_p_b == db_n == h_n and s4_rank == h['rank']) else 'MISMATCH'
    
    bowl_recon_rows.append({
        'framework': 'Pure RPAE (100% Econ)',
        'rank': s4_rank,
        'player_id': pid,
        'player_name': pname,
        'step4_pressure_b': s4_p_b,
        'db_pressure_balls': db_n,
        'html_displayed_leverage_deliveries': h_n,
        'discrepancy': discrepancy,
        'status': status,
        'html_pressure_econ': h_econ,
        'html_exp_econ': h_exp_econ,
        'step4_shrunk_score': s4_score,
        'html_shrunk_score': h_score,
        'step4_rank_ci_90': s4_ci,
        'html_rank_ci_90': h_ci
    })

df_bowl_recon = pd.DataFrame(bowl_recon_rows)
df_bowl_recon.to_csv('phase1_audit/phase2c_post_validation/BOWLER_DELIVERY_COUNT_RECONCILIATION.csv', index=False)
print(f"BOWLER_DELIVERY_COUNT_RECONCILIATION.csv created: {len(df_bowl_recon)} rows.")
print("Bowler status breakdown:")
print(df_bowl_recon['status'].value_counts())
