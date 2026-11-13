import csv
import json
import re
import pandas as pd

# Load Step 4 Authoritative CSVs
df_step4_bat = pd.read_csv('phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv')
df_step4_bowl_comp = pd.read_csv('phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_COMPOSITE.csv')
df_step4_bowl_rae = pd.read_csv('phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv')

# Load players_db.json
with open('players_db.json', 'r', encoding='utf-8') as f:
    players_db = json.load(f)

# Parse index.html rows
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Helper to clean html tags
def clean_html(text):
    return ' '.join(re.sub(r'<[^>]+>', ' ', text).split())

# 1. Parse Batter rows in index.html
# Find the batters table body
m_bat = re.search(r'<div id="batters" class="data-section[^"]*">([\s\S]*?)</div>\s*</div>', html)
if not m_bat:
    # fallback
    bat_section = html[html.find('id="batters"'):html.find('id="bowlers"')]
else:
    bat_section = m_bat.group(1)

bat_rows = re.findall(r'<tr onclick="window\.location\.href=\'players/([^\']+)\.html\'"[^>]*>([\s\S]*?)</tr>', bat_section)

bat_html_data = {}
for slug, r_content in bat_rows:
    tds = re.findall(r'<td[^>]*>([\s\S]*?)</td>', r_content)
    clean_tds = [clean_html(td) for td in tds]
    # Rank (0), Player/Role (1), Franchise (2), Leverage Deliveries (3), Pressure SR (4), Expected SR (5), RAE Diff (6), Career Balls (7), Rank Bound (8), Shrunk RAE (9)
    # Extract name from Player/Role
    name_m = re.search(r'<span class="name-box">([^<]+)</span>', r_content)
    name = name_m.group(1).strip() if name_m else clean_tds[1]
    
    bat_html_data[slug] = {
        'slug': slug,
        'name': name,
        'rank': clean_tds[0],
        'leverage_deliveries': clean_tds[3],
        'pressure_sr': clean_tds[4],
        'exp_sr': clean_tds[5],
        'rae_diff': clean_tds[6],
        'career_balls': clean_tds[7],
        'rank_bound': clean_tds[8],
        'shrunk_rae': clean_tds[9] if len(clean_tds) > 9 else ''
    }

print(f'Parsed {len(bat_html_data)} batter rows from index.html')

# 2. Parse Bowler rows in index.html
m_bowl = re.search(r'<div id="bowlers" class="data-section[^"]*">([\s\S]*?)</div>\s*</div>', html)
if not m_bowl:
    bowl_section = html[html.find('id="bowlers"'):html.find('id="radar"')]
else:
    bowl_section = m_bowl.group(1)

bowl_comp_rows = re.findall(r'<tr[^>]*class="[^"]*bowler-row-composite[^"]*"[^>]*>([\s\S]*?)</tr>', bowl_section)
bowl_rpae_rows = re.findall(r'<tr[^>]*class="[^"]*bowler-row-rpae[^"]*"[^>]*>([\s\S]*?)</tr>', bowl_section)

print(f'Parsed {len(bowl_comp_rows)} composite and {len(bowl_rpae_rows)} RPAE bowler rows from index.html')

def parse_bowl_row(r_content):
    tds = re.findall(r'<td[^>]*>([\s\S]*?)</td>', r_content)
    clean_tds = [clean_html(td) for td in tds]
    name_m = re.search(r'<span class="name-box">([^<]+)</span>', r_content)
    slug_m = re.search(r'href=\'players/([^\']+)\.html\'', r_content)
    name = name_m.group(1).strip() if name_m else clean_tds[1]
    slug = slug_m.group(1) if slug_m else ''
    return {
        'slug': slug,
        'name': name,
        'rank': clean_tds[0],
        'leverage_deliveries': clean_tds[3],
        'pressure_econ': clean_tds[4],
        'exp_econ': clean_tds[5],
        'econ_diff': clean_tds[6],
        'col7': clean_tds[7], # Wkts for Comp, Career Balls for RPAE
        'rank_bound': clean_tds[8],
        'shrunk_score': clean_tds[9] if len(clean_tds) > 9 else ''
    }

bowl_comp_html_data = [parse_bowl_row(r) for r in bowl_comp_rows]
bowl_rpae_html_data = [parse_bowl_row(r) for r in bowl_rpae_rows]

# Generate BATTER_DELIVERY_COUNT_RECONCILIATION.csv
batter_recon = []
# Map db players by id and slug
db_by_id = {p['player_id']: p for p in players_db if 'player_id' in p}
db_batters = [p for p in players_db if p.get('player_type') == 'batter']
db_bat_by_id = {p['player_id']: p for p in db_batters}

# Also map HTML batters by name/slug
bat_html_by_name = {b['name']: b for b in bat_html_data.values()}

for idx, row in df_step4_bat.iterrows():
    pid = int(row['player_id'])
    pname = row['player_name']
    step4_n = int(round(row['pressure_bf']))
    step4_rank = int(row['rank'])
    
    # check db
    db_p = db_bat_by_id.get(pid)
    db_n = db_p.get('pressure_balls') if db_p else None
    
    # check html
    # match by slug or name
    html_p = None
    if db_p and db_p.get('slug') in bat_html_data:
        html_p = bat_html_data[db_p.get('slug')]
    elif pname in bat_html_by_name:
        html_p = bat_html_by_name[pname]
    else:
        # find by name in bat_html_data values
        for b in bat_html_data.values():
            if b['name'] == pname or pname in b['name']:
                html_p = b
                break
                
    html_n = int(html_p['leverage_deliveries']) if html_p else None
    
    status = 'MATCH' if (step4_n == db_n == html_n) else 'MISMATCH'
    batter_recon.append({
        'rank': step4_rank,
        'player_id': pid,
        'player_name': pname,
        'step4_pressure_bf': step4_n,
        'db_pressure_balls': db_n,
        'html_displayed_leverage_deliveries': html_n,
        'discrepancy_step4_vs_html': 0 if (step4_n == html_n) else (html_n - step4_n if html_n is not None else 'MISSING'),
        'status': status
    })

recon_bat_df = pd.DataFrame(batter_recon)
recon_bat_df.to_csv('phase1_audit/phase2c_post_validation/BATTER_DELIVERY_COUNT_RECONCILIATION.csv', index=False)
print(f'Wrote BATTER_DELIVERY_COUNT_RECONCILIATION.csv: {len(recon_bat_df)} rows, status value counts:')
print(recon_bat_df['status'].value_counts())

# Generate BOWLER_DELIVERY_COUNT_RECONCILIATION.csv
bowl_comp_by_name = {b['name']: b for b in bowl_comp_html_data}
bowl_rpae_by_name = {b['name']: b for b in bowl_rpae_html_data}
db_bowlers = [p for p in players_db if p.get('player_type') == 'bowler']
db_bowl_by_id = {p['player_id']: p for p in db_bowlers}

bowler_recon = []
# 1. Composite Framework
for idx, row in df_step4_bowl_comp.iterrows():
    pid = int(row['player_id'])
    pname = row['player_name']
    step4_n = int(round(row['pressure_b']))
    step4_rank = int(row['rank'])
    
    db_p = db_bowl_by_id.get(pid)
    db_n = db_p.get('pressure_balls') if db_p else None
    
    html_p = bowl_comp_by_name.get(pname)
    if not html_p:
        for b in bowl_comp_html_data:
            if b['name'] == pname or pname in b['name']:
                html_p = b
                break
    html_n = int(html_p['leverage_deliveries']) if html_p else None
    status = 'MATCH' if (step4_n == db_n == html_n) else 'MISMATCH'
    
    bowler_recon.append({
        'framework': 'Composite (60/40)',
        'rank': step4_rank,
        'player_id': pid,
        'player_name': pname,
        'step4_pressure_b': step4_n,
        'db_pressure_balls': db_n,
        'html_displayed_leverage_deliveries': html_n,
        'discrepancy_step4_vs_html': 0 if (step4_n == html_n) else (html_n - step4_n if html_n is not None else 'MISSING'),
        'status': status
    })

# 2. Pure RPAE Framework
for idx, row in df_step4_bowl_rae.iterrows():
    pid = int(row['player_id'])
    pname = row['player_name']
    step4_n = int(round(row['pressure_b']))
    step4_rank = int(row['rank'])
    
    db_p = db_bowl_by_id.get(pid)
    db_n = db_p.get('pressure_balls') if db_p else None
    
    html_p = bowl_rpae_by_name.get(pname)
    if not html_p:
        for b in bowl_rpae_html_data:
            if b['name'] == pname or pname in b['name']:
                html_p = b
                break
    html_n = int(html_p['leverage_deliveries']) if html_p else None
    status = 'MATCH' if (step4_n == db_n == html_n) else 'MISMATCH'
    
    bowler_recon.append({
        'framework': 'Pure RPAE (100% Econ)',
        'rank': step4_rank,
        'player_id': pid,
        'player_name': pname,
        'step4_pressure_b': step4_n,
        'db_pressure_balls': db_n,
        'html_displayed_leverage_deliveries': html_n,
        'discrepancy_step4_vs_html': 0 if (step4_n == html_n) else (html_n - step4_n if html_n is not None else 'MISSING'),
        'status': status
    })

recon_bowl_df = pd.DataFrame(bowler_recon)
recon_bowl_df.to_csv('phase1_audit/phase2c_post_validation/BOWLER_DELIVERY_COUNT_RECONCILIATION.csv', index=False)
print(f'Wrote BOWLER_DELIVERY_COUNT_RECONCILIATION.csv: {len(recon_bowl_df)} rows, status value counts:')
print(recon_bowl_df['status'].value_counts())

