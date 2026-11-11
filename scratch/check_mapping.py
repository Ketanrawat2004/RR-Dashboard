import pandas as pd

ctpm = pd.read_csv('season2_data/competition_team_player_mapping.csv')
print("Columns in competition_team_player_mapping:", ctpm.columns.tolist())
print(ctpm.head(3))

pe = pd.read_csv('season2_data/playing_eleven.csv')
matches_df = pd.read_csv('season2_data/matches.csv')
print("Matches shape:", matches_df.shape)
print("Competitions:", matches_df['competition_id'].value_counts() if 'competition_id' in matches_df.columns else "no comp col")

