import pandas as pd

df = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv")
print(df[["rank_rpae", "player_name", "shrunk_rpae_score", "rank_ci_90"]].head(5))

