import json
import pandas as pd

df_bat = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv")
with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

for r in df_bat.head(5).itertuples():
    print(f"{r.rank}. {r.player_name}: sr={r.pressure_sr}, exp_sr={r.pressure_exp_sr}, diff={r.pressure_sr - r.pressure_exp_sr:.2f}, lift={r.clutch_rae_lift}")

