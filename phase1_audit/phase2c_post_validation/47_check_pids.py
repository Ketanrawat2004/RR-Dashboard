import pandas as pd

df_bat = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv")
for name in ["Andre Russell", "Glenn Maxwell", "Tim David", "Abhishek Sharma"]:
    sub = df_bat[df_bat["player_name"] == name]
    if not sub.empty:
        print(name, "player_id:", sub.iloc[0]["player_id"])

df_bowl = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_COMPOSITE.csv")
for name in ["Matheesha Pathirana", "Jasprit Bumrah", "Maheesh Theekshana", "Umran Malik", "Mayank Yadav"]:
    sub = df_bowl[df_bowl["player_name"] == name]
    if not sub.empty:
        print(name, "player_id:", sub.iloc[0]["player_id"])

