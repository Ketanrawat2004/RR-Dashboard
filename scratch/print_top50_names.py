import pandas as pd
b_df = pd.read_csv('pressure_output/top50_batters_pressure.csv')
p_df = pd.read_csv('pressure_output/top50_bowlers_pressure.csv')
print("Top 10 batters:", b_df['player_name'].head(10).tolist())
print("Top 10 bowlers:", p_df['player_name'].head(10).tolist())

