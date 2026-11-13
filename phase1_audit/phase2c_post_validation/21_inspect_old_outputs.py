import os
import pandas as pd

if os.path.exists("output/rr_full_rankings.csv"):
    df = pd.read_csv("output/rr_full_rankings.csv")
    print("=== output/rr_full_rankings.csv ===")
    print(df.columns.tolist())
    for name in ["Andre Russell", "Glenn Maxwell", "Tim David", "Abhishek Sharma", "Matheesha Pathirana", "Jasprit Bumrah", "Umran Malik", "Mayank Yadav"]:
        sub = df[df.apply(lambda r: name in str(r.values), axis=1)]
        if not sub.empty:
            print(f"  {name}:", sub.iloc[0].to_dict())

if os.path.exists("demo_out/03_ranked_all.csv"):
    df2 = pd.read_csv("demo_out/03_ranked_all.csv")
    print("\n=== demo_out/03_ranked_all.csv ===")
    print(df2.columns.tolist())
    for name in ["Andre Russell", "Glenn Maxwell", "Tim David", "Abhishek Sharma", "Matheesha Pathirana", "Jasprit Bumrah", "Umran Malik", "Mayank Yadav"]:
        sub = df2[df2.apply(lambda r: name in str(r.values), axis=1)]
        if not sub.empty:
            print(f"  {name}:", sub.iloc[0].to_dict())
