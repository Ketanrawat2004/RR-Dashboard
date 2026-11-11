import pandas as pd
df_b = pd.read_csv('pressure_output/SUBMISSION_top10_batters.csv')
df_p = pd.read_csv('pressure_output/SUBMISSION_top10_bowlers.csv')

print("=== SUBMISSION BATTERS ===")
for _, r in df_b.iterrows():
    print(f"Rank {r['Rank']:2d}: {r['Player_Name']:20} | CPPI: {r['CPPI_Score']:.2f} | HP WR: {r['HP_Win_Rate']:.1f}% | Lift: {r['Pressure_Lift']:+.1f}%")

print("\n=== SUBMISSION BOWLERS ===")
for _, r in df_p.iterrows():
    print(f"Rank {r['Rank']:2d}: {r['Player_Name']:20} | CPPI: {r['CPPI_Score']:.2f} | HP WR: {r['HP_Win_Rate']:.1f}% | Lift: {r['Pressure_Lift']:+.1f}%")

