import pandas as pd
import json

print("=== SUBMISSION_top10_batters.csv ===")
try:
    df_b = pd.read_csv('pressure_output/SUBMISSION_top10_batters.csv')
    print(df_b[['rank', 'player_name', 'teams', 'hp_matches', 'hp_win_rate', 'overall_win_rate', 'pressure_lift', 'cppi']].to_string())
except Exception as e:
    print("Error:", e)

print("\n=== SUBMISSION_top10_bowlers.csv ===")
try:
    df_p = pd.read_csv('pressure_output/SUBMISSION_top10_bowlers.csv')
    print(df_p[['rank', 'player_name', 'teams', 'hp_matches', 'hp_win_rate', 'overall_win_rate', 'pressure_lift', 'cppi']].to_string())
except Exception as e:
    print("Error:", e)

