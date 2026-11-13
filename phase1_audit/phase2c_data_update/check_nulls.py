import pandas as pd

df_bat = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv")
print("Batters nulls:")
print(df_bat[['pressure_sr', 'pressure_exp_sr', 'raw_pressure_rae_rate', 'shrunk_rae_score']].isna().sum())

df_bowl = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv")
print("\nBowlers nulls:")
print(df_bowl[['pressure_econ', 'pressure_exp_econ', 'raw_pressure_rpae_rate', 'shrunk_rpae_score']].isna().sum())

