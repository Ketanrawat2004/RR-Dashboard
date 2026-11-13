import pandas as pd

df = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv")
for _, r in df.head(10).iterrows():
    print(f"{r['rank_rpae']}. {r['player_name']}: econ={r['pressure_econ']}, exp_econ={r['pressure_exp_econ']}, lift={r['clutch_rpae_lift']}, score={r['shrunk_rpae_score']}")

