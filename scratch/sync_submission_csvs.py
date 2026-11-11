import json
import pandas as pd

with open("players_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

batters = sorted([p for p in db if p["category"] == "Batter"], key=lambda x: x["rank"])
bowlers = sorted([p for p in db if p["category"] == "Bowler"], key=lambda x: x["rank"])

def make_df(players):
    rows = []
    for p in players:
        rows.append({
            "Rank": p["rank"],
            "Player_Name": p["name"],
            "Player_ID": p.get("id", p.get("key", "")),
            "CPPI_Score": round(p["cppi"], 2),
            "HP_Matches": p["hp_m"],
            "HP_Win_Rate": round(p["hp_wr"], 1),
            "Pressure_Lift": round(p["lift"], 1),
            "Baseline_Win_Rate": round(p["base_wr"], 1),
            "MOM_HP": p.get("mom_hp", 0),
            "KO_Win_Rate": round(p.get("ko_wr", 0), 1),
            "Teams": p.get("teams", "")
        })
    return pd.DataFrame(rows)

df_batters = make_df(batters)
df_bowlers = make_df(bowlers)

df_batters.to_csv("pressure_output/SUBMISSION_top10_batters.csv", index=False)
df_bowlers.to_csv("pressure_output/SUBMISSION_top10_bowlers.csv", index=False)

print("Updated SUBMISSION_top10_batters.csv and SUBMISSION_top10_bowlers.csv to exactly match players_db.json!")
print("\nTop 10 Batters for Unstop:")
for _, r in df_batters.iterrows():
    print(f"Rank {r['Rank']:2d}: {r['Player_Name']}")

print("\nTop 10 Bowlers for Unstop:")
for _, r in df_bowlers.iterrows():
    print(f"Rank {r['Rank']:2d}: {r['Player_Name']}")

