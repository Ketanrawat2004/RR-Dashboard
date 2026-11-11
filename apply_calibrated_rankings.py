import json
import math

with open('players_db.json', 'r', encoding='utf-8') as f:
    players = json.load(f)

# Calibrated Gold Standard Formula
for p in players:
    hp_m = p['hp_m']
    hp_wr = p['hp_wr']
    base_wr = p['base_wr']
    lift = p['lift']
    mom = p['mom_hp']
    ko_wr = p['ko_wr']
    bayes_hp = p.get('bayes_hp_wr', hp_wr)
    
    # Lift component: 50 neutral, scaled by 1.8
    lift_comp = max(0.0, min(100.0, 50.0 + lift * 1.8))
    
    # MOM component: 3.0x multiplier, capped at 100
    mom_pct = (mom / hp_m) * 100
    mom_comp = min(100.0, mom_pct * 3.0)
    
    # Credibility sigmoid
    credibility = 1.0 / (1.0 + math.exp(-0.25 * (hp_m - 8)))
    
    raw = (
        0.35 * bayes_hp +
        0.25 * lift_comp +
        0.20 * ko_wr +
        0.10 * mom_comp +
        0.10 * base_wr
    )
    p['cppi'] = round(raw * (0.85 + 0.15 * credibility), 2)

# Separate, sort, and re-rank
batters = sorted([p for p in players if p['category'] == 'Batter'], key=lambda x: -x['cppi'])
bowlers = sorted([p for p in players if p['category'] == 'Bowler'], key=lambda x: -x['cppi'])

for idx, p in enumerate(batters, 1):
    p['rank'] = idx

for idx, p in enumerate(bowlers, 1):
    p['rank'] = idx

# Combine
all_updated = batters + bowlers

with open('players_db.json', 'w', encoding='utf-8') as f:
    json.dump(all_updated, f, indent=4)

print("=== CALIBRATED PLAYERS_DB.JSON APPLIED SUCCESSFULLY ===")
print("\n--- NEW BATTERS ---")
for p in batters:
    print(f"Rank {p['rank']:2}: {p['name']:20} | CPPI: {p['cppi']:5.2f} | Lift: {p['lift']:+5.1f}% | HP WR: {p['hp_wr']:5.1f}% | KO: {p['ko_wr']:5.1f}%")

print("\n--- NEW BOWLERS ---")
for p in bowlers:
    print(f"Rank {p['rank']:2}: {p['name']:20} | CPPI: {p['cppi']:5.2f} | Lift: {p['lift']:+5.1f}% | HP WR: {p['hp_wr']:5.1f}% | KO: {p['ko_wr']:5.1f}%")

