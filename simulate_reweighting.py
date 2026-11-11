import json
import math

with open('players_db.json', 'r', encoding='utf-8') as f:
    players = json.load(f)

def test_weights(w_hp, w_lift, w_ko, w_mom, w_base, lift_multiplier, name=""):
    print(f"\n=======================================================")
    print(f"MODEL: {name}")
    print(f"Weights: HP_WR={w_hp}%, Lift={w_lift}%, KO={w_ko}%, MOM={w_mom}%, Base={w_base}% (Lift Mult={lift_multiplier})")
    print(f"=======================================================")
    
    scored = []
    for p in players:
        hp_m = p['hp_m']
        hp_wr = p['hp_wr']
        base_wr = p['base_wr']
        lift = p['lift']
        mom = p['mom_hp']
        ko_wr = p['ko_wr']
        bayes_hp = p.get('bayes_hp_wr', hp_wr)
        
        # Lift component
        lift_comp = max(0.0, min(100.0, 50.0 + lift * lift_multiplier))
        
        # MOM component: 
        mom_pct = (mom / hp_m) * 100
        mom_comp = min(100.0, mom_pct * 3.0)
        
        # Credibility
        credibility = 1.0 / (1.0 + math.exp(-0.25 * (hp_m - 8)))
        
        raw = (
            w_hp * bayes_hp +
            w_lift * lift_comp +
            w_ko * ko_wr +
            w_mom * mom_comp +
            w_base * base_wr
        )
        final = round(raw * (0.85 + 0.15 * credibility), 2)
        scored.append({**p, 'test_cppi': final})
        
    batters = sorted([p for p in scored if p['category'] == 'Batter'], key=lambda x: -x['test_cppi'])
    bowlers = sorted([p for p in scored if p['category'] == 'Bowler'], key=lambda x: -x['test_cppi'])
    
    print("\n--- TOP BATTERS ---")
    for i, p in enumerate(batters, 1):
        print(f"{i:2}. {p['name']:18} | Score: {p['test_cppi']:5.2f} (prev #{p['rank']}) | Lift: {p['lift']:+5.1f}% | HP WR: {p['hp_wr']:5.1f}% | KO: {p['ko_wr']:5.1f}% | MOM: {p['mom_hp']}")
        
    print("\n--- TOP BOWLERS ---")
    for i, p in enumerate(bowlers, 1):
        print(f"{i:2}. {p['name']:18} | Score: {p['test_cppi']:5.2f} (prev #{p['rank']}) | Lift: {p['lift']:+5.1f}% | HP WR: {p['hp_wr']:5.1f}% | KO: {p['ko_wr']:5.1f}% | MOM: {p['mom_hp']}")

# Model 1: Original weights (HP 35%, KO 20%, MOM 20%, Lift 15%, Base 10%)
test_weights(0.35, 0.15, 0.20, 0.20, 0.10, 1.5, "ORIGINAL (MOM Heavy: 20%, Lift: 15%)")

# Model 2: Calibrated "True Clutch Delta" (HP 30%, Lift 30%, KO 20%, MOM 10%, Base 10%)
test_weights(0.30, 0.30, 0.20, 0.10, 0.10, 2.0, "BALANCED CLUTCH ELEVATION (Lift 30%, HP 30%, KO 20%, MOM 10%)")

# Model 3: Elite War Room Delta (HP 25%, Lift 35%, KO 25%, MOM 10%, Base 5%)
test_weights(0.25, 0.35, 0.25, 0.10, 0.05, 2.0, "ELITE TOURNAMENT CLUTCH (Lift 35%, KO 25%, HP 25%, MOM 10%)")

# Model 4: Master Calibrated (Lift 25%, HP 30%, KO 20%, MOM 15%, Base 10%, Lift Mult 2.0)
test_weights(0.30, 0.25, 0.20, 0.15, 0.10, 2.0, "MASTER CALIBRATED WAR ROOM INDEX (Lift 25%, HP 30%, KO 20%, MOM 15%)")

# Model 5: Gold Standard Hackathon Winning Formula (HP 35%, Lift 25%, KO 20%, MOM 10%, Base 10%, Lift Mult 1.8)
test_weights(0.35, 0.25, 0.20, 0.10, 0.10, 1.8, "GOLD STANDARD HACKATHON FORMULA (HP 35%, Lift 25%, KO 20%, MOM 10%, Base 10%)")
