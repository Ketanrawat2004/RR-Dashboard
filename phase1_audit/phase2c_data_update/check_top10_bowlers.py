import pandas as pd

df_comp = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_COMPOSITE.csv")
print("=== TOP 10 COMPOSITE ===")
print(df_comp[['rank_composite', 'player_name', 'composite_score']].head(10))

df_rpae = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv")
print("\n=== TOP 10 PURE RPAE ===")
print(df_rpae[['rank_rpae', 'player_name', 'shrunk_rpae_score']].head(10))

