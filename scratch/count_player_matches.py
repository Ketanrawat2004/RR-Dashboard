import pandas as pd

ctpm = pd.read_csv('season2_data/competition_team_player_mapping.csv')
pe = pd.read_csv('season2_data/playing_eleven.csv')
matches_df = pd.read_csv('season2_data/matches.csv')

# Only matches where is_played == 1 or in playing eleven
pe_played = pe[pe['is_played'] == 1]

targets = ['Jasprit Bumrah', 'Mohammed Siraj', 'Rashid Khan', 'Heinrich Klaasen', 'Rohit Sharma']

for t in targets:
    player_rows = ctpm[ctpm['player_name'].str.contains(t, case=False, na=False)]
    pids = player_rows['player_id'].unique()
    played_matches = pe[pe['player_id'].isin(pids)]['match_id'].nunique()
    actually_played = pe[(pe['player_id'].isin(pids)) & (pe['is_played'] == 1)]['match_id'].nunique()
    print(f"{t}: pids={pids}, matches_in_xi={played_matches}, is_played_1={actually_played}")

