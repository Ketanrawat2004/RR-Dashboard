import pandas as pd

df_bat = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv")
sub = df_bat[df_bat.apply(lambda row: "2143" in str(row.values) or 2143 in row.values, axis=1)]
print("Row with 2143 in FINAL_BATTER_RANKINGS.csv:")
print(sub[["rank", "player_name", "career_bf", "pressure_bf"]])

