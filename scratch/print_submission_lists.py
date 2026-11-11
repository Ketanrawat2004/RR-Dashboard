import pandas as pd

b = pd.read_csv('pressure_output/SUBMISSION_top10_batters.csv')
bw = pd.read_csv('pressure_output/SUBMISSION_top10_bowlers.csv')
print("=== TOP 10 BATTERS ===")
for _, r in b.iterrows():
    print(f"{int(r['Rank'])}. {r['Player_Name']} (CPPI: {r['CPPI_Score']:.2f}, HP WR: {r['HP_Win_Rate']}%, Lift: {r['Pressure_Lift']}%)")

print("\n=== TOP 10 BOWLERS ===")
for _, r in bw.iterrows():
    print(f"{int(r['Rank'])}. {r['Player_Name']} (CPPI: {r['CPPI_Score']:.2f}, HP WR: {r['HP_Win_Rate']}%, Lift: {r['Pressure_Lift']}%)")

