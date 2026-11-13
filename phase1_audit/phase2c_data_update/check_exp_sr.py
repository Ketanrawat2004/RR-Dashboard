import pandas as pd

df = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv")
for _, r in df.head(5).iterrows():
    print(f"{r['rank']}. {r['player_name']}: career_exp_sr={r['career_exp_sr']}, pressure_exp_sr={r['pressure_exp_sr']}, pressure_sr={r['pressure_sr']}")

