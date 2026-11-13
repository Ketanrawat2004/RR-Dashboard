import pandas as pd

df = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_COMPOSITE.csv")
print(list(df.columns))
print(df[["rank_composite", "player_name", "composite_score", "rank_ci_90"]].head(5))

