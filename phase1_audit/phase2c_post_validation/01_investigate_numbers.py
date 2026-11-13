import os
import pandas as pd
import glob

# Search in step4, step3, step3_1, step3_2, final_independent_verification
search_patterns = [
    "phase1_audit/**/*.csv",
    "phase1_audit/**/*.txt",
    "phase1_audit/**/*.md",
]

print("--- Checking FINAL_BATTER_RANKINGS.csv ---")
df_bat = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv")
for name in ["Andre Russell", "Glenn Maxwell", "Tim David", "Abhishek Sharma"]:
    sub = df_bat[df_bat["player_name"] == name]
    if not sub.empty:
        r = sub.iloc[0]
        print(f"Batter {name}: career_bf={r['career_bf']}, pressure_bf={r['pressure_bf']}")

print("\n--- Checking FINAL_BOWLER_RANKINGS_COMPOSITE.csv ---")
df_bowl_comp = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_COMPOSITE.csv")
for name in ["Matheesha Pathirana", "Jasprit Bumrah", "Maheesh Theekshana", "Umran Malik", "Mayank Yadav"]:
    sub = df_bowl_comp[df_bowl_comp["player_name"] == name]
    if not sub.empty:
        r = sub.iloc[0]
        print(f"Bowler (Comp) {name}: career_b={r['career_b']}, pressure_b={r['pressure_b']}")

print("\n--- Checking FINAL_BOWLER_RANKINGS_RAE.csv ---")
df_bowl_rpae = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv")
for name in ["Matheesha Pathirana", "Jasprit Bumrah", "Maheesh Theekshana", "Umran Malik", "Mayank Yadav"]:
    sub = df_bowl_rpae[df_bowl_rpae["player_name"] == name]
    if not sub.empty:
        r = sub.iloc[0]
        print(f"Bowler (RPAE) {name}: career_b={r['career_b']}, pressure_b={r['pressure_b']}")

