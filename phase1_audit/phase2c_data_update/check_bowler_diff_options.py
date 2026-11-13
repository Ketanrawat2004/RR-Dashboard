import pandas as pd

df = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv")
for _, r in df.head(10).iterrows():
    diff = r['pressure_econ'] - r['pressure_exp_econ']
    print(f"{r['rank_rpae']}. {r['player_name']}: econ={r['pressure_econ']:.2f}, exp_econ={r['pressure_exp_econ']:.2f}, diff={diff:+.2f}, raw_rpae_rate={r['raw_pressure_rpae_rate']:.2f}, clutch_lift={r['clutch_rpae_lift']:.2f}")

