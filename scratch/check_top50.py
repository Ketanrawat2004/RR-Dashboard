import pandas as pd

b_df = pd.read_csv('pressure_output/top50_batters_pressure.csv')
p_df = pd.read_csv('pressure_output/top50_bowlers_pressure.csv')

print("Batters columns:", b_df.columns.tolist()[:10])
print("Bowlers columns:", p_df.columns.tolist()[:10])

for name in ['Bumrah', 'Siraj', 'Rashid', 'Klaasen', 'Rohit']:
    hit_b = b_df[b_df['player_name'].str.contains(name, case=False, na=False)]
    hit_p = p_df[p_df['player_name'].str.contains(name, case=False, na=False)]
    if len(hit_b) > 0:
        row = hit_b.iloc[0]
        print(f"Batter {name}: total_matches={row.get('total_matches')}, hp_matches={row.get('hp_matches')}, win_rate={row.get('overall_win_rate')}, hp_win_rate={row.get('hp_win_rate')}")
    if len(hit_p) > 0:
        row = hit_p.iloc[0]
        print(f"Bowler {name}: total_matches={row.get('total_matches')}, hp_matches={row.get('hp_matches')}, win_rate={row.get('overall_win_rate')}, hp_win_rate={row.get('hp_win_rate')}")

