import json

with open('players_db.json', 'r', encoding='utf-8') as f:
    players = json.load(f)

print("=== DETAILED BREAKDOWN OF CPPI FORMULA COMPONENTS ===")
for p in players:
    if p['name'] in ['Mitchell Starc', 'Josh Hazlewood', 'Jacob Duffy', 'Sediqullah Atal', 'Rajat Patidar', 'Rinku Singh', 'Devon Conway', 'Shivam Dube', 'Ruturaj Gaikwad']:
        cat = p['category'][:3]
        rank = p['rank']
        name = p['name']
        hp_m = p['hp_m']
        hp_wr = p['hp_wr']
        base_wr = p['base_wr']
        lift = p['lift']
        mom = p['mom_hp']
        ko_wr = p['ko_wr']
        cppi = p['cppi']
        bayes_hp = p.get('bayes_hp_wr', 0)
        
        # Calculate CPPI subcomponents according to rr_pressure_analyst formula:
        # 1. Bayes HP WR (35%)
        c_bayes = 0.35 * bayes_hp
        # 2. Bayes KO WR (20%) - assuming bayes_ko
        # 3. MOM component (20%): min(100, (mom / hp_m * 100) * 4) * 0.20
        mom_pct = (mom / hp_m) * 100
        mom_comp = min(100.0, mom_pct * 4.0) * 0.20
        # 4. Lift component (15%): max(0, min(100, 50.0 + lift * 1.5)) * 0.15
        lift_comp = max(0.0, min(100.0, 50.0 + lift * 1.5)) * 0.15
        # 5. Base WR (10%): base_wr * 0.10
        base_comp = base_wr * 0.10
        
        print(f"\n{cat} #{rank:2} {name} (CPPI: {cppi:.2f})")
        print(f"   Matches: {hp_m} | Base WR: {base_wr:.1f}% | HP WR: {hp_wr:.1f}% | Win Diff: {lift:+.1f}% | MOMs: {mom} | KO WR: {ko_wr:.1f}%")
        print(f"   Subcomponents:")
        print(f"     • 35% Bayes HP WR:   {c_bayes:5.2f} pts (Bayes WR: {bayes_hp:.1f}%)")
        print(f"     • 20% MOM Density:   {mom_comp:5.2f} pts (MOM Rate: {mom_pct:.1f}%, Score: {min(100.0, mom_pct*4.0):.1f}/100)")
        print(f"     • 15% Lift (Diff):   {lift_comp:5.2f} pts (Lift Score: {max(0.0, min(100.0, 50.0 + lift*1.5)):.1f}/100)")
        print(f"     • 10% Baseline WR:   {base_comp:5.2f} pts")

print("\n" + "="*70)
print("=== WHAT IF WE SORTED BY PURE WIN DIFFERENTIAL (LIFT)? ===")
print("="*70)

batters = [p for p in players if p['category'] == 'Batter']
bowlers = [p for p in players if p['category'] == 'Bowler']

print("\n--- BATTERS SORTED BY PURE WIN DIFF (LIFT) ---")
for i, p in enumerate(sorted(batters, key=lambda x: -x['lift']), 1):
    print(f"{i:2}. {p['name']:18} | Lift: {p['lift']:+5.1f}% | HP WR: {p['hp_wr']:5.1f}% | Base: {p['base_wr']:5.1f}% | Current CPPI Rank: #{p['rank']}")

print("\n--- BOWLERS SORTED BY PURE WIN DIFF (LIFT) ---")
for i, p in enumerate(sorted(bowlers, key=lambda x: -x['lift']), 1):
    print(f"{i:2}. {p['name']:18} | Lift: {p['lift']:+5.1f}% | HP WR: {p['hp_wr']:5.1f}% | Base: {p['base_wr']:5.1f}% | Current CPPI Rank: #{p['rank']}")
