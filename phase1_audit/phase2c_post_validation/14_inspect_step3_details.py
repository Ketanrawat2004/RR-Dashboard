import pandas as pd

df_b3 = pd.read_csv("phase1_audit/step3_individual_model/BATTERS_PERFORMANCE_STEP3.csv")
print("=== BATTERS STEP 3 SAMPLE ===")
for name in ["Andre Russell", "Glenn Maxwell", "Tim David", "Abhishek Sharma"]:
    sub = df_b3[df_b3["player_name"] == name]
    if not sub.empty:
        r = sub.iloc[0]
        print(f"Batter {name}: career_bf={r['career_bf']}, p_bf={r['p_bf']}, h0_bf={r['h0_bf']}, h1_bf={r['h1_bf']}")

df_bw3 = pd.read_csv("phase1_audit/step3_individual_model/BOWLERS_PERFORMANCE_STEP3.csv")
print("\n=== BOWLERS STEP 3 SAMPLE ===")
print("Cols in df_bw3:", list(df_bw3.columns))
for name in ["Matheesha Pathirana", "Jasprit Bumrah", "Maheesh Theekshana", "Umran Malik", "Mayank Yadav", "Andre Russell"]:
    sub = df_bw3[df_bw3["player_name"] == name]
    if not sub.empty:
        r = sub.iloc[0]
        print(f"Bowler {name}:", {c: r[c] for c in df_bw3.columns if any(k in c.lower() for k in ["b", "ball", "p_", "press"])})

