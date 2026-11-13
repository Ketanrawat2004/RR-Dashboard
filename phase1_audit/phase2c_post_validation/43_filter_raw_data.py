import pandas as pd
import numpy as np

bbb = pd.read_csv("ball_by_ball.csv", low_memory=False)
matches = pd.read_csv("matches.csv")
comps = pd.read_csv("competitions.csv")

# Merge
m_c = matches.merge(comps, on="comp_id", how="left")
df = bbb.merge(m_c, on="match_id", how="left")

print("Total deliveries:", len(df))

# Let's inspect batter delivery subsets for Russell, Maxwell, David, Abhishek
for name in ["Andre Russell", "Glenn Maxwell", "Tim David", "Abhishek Sharma"]:
    sub = df[df["striker"] == name]
    print(f"\n--- Batter {name} (Total rows: {len(sub)}) ---")
    print("  By match_format:", sub["match_format"].value_counts().to_dict())
    print("  By comp_name:", sub["comp_name"].value_counts().to_dict())
    print("  By innings:", sub["innings"].value_counts().to_dict())
    if "is_pressure" in sub.columns:
        print("  By is_pressure:", sub["is_pressure"].value_counts().to_dict())

