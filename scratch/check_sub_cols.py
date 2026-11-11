import pandas as pd
df_b = pd.read_csv('pressure_output/SUBMISSION_top10_batters.csv')
df_p = pd.read_csv('pressure_output/SUBMISSION_top10_bowlers.csv')
print("Batters columns:", df_b.columns.tolist())
print(df_b.head(10))
print("\nBowlers columns:", df_p.columns.tolist())
print(df_p.head(10))

