import pandas as pd

df_bat = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv")
print("Batting cols:", list(df_bat.columns))
print(df_bat.head(3))

df_bowl = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv")
print("Bowling cols:", list(df_bowl.columns))
print(df_bowl.head(3))

