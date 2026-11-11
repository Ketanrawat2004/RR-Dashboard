import json

with open('players_db.json', 'r', encoding='utf-8') as f:
    players = json.load(f)

batters = sorted([p for p in players if p['category'] == 'Batter'], key=lambda x: x['rank'])
bowlers = sorted([p for p in players if p['category'] == 'Bowler'], key=lambda x: x['rank'])

print("BATTERS:")
for p in batters:
    lift_str = f"+{p['lift']:.1f}%" if p['lift'] > 0 else f"{p['lift']:.1f}%"
    print(f"| **{p['rank']}** | **{p['name']}** | {p['teams']} | {p['hp_m']} | {p['hp_wr']:.1f}% | {lift_str} | {p['mom_hp']} | {p['ko_wr']:.1f}% | **{p['cppi']:.2f}** |")

print("\nBOWLERS:")
for p in bowlers:
    lift_str = f"+{p['lift']:.1f}%" if p['lift'] > 0 else f"{p['lift']:.1f}%"
    print(f"| **{p['rank']}** | **{p['name']}** | {p['teams']} | {p['hp_m']} | {p['hp_wr']:.1f}% | {lift_str} | {p['mom_hp']} | {p['ko_wr']:.1f}% | **{p['cppi']:.2f}** |")
