import os
import pandas as pd

if os.path.exists("phase1_audit/step3_2_reconciliation/PLAYER_STATISTICS_RECONCILIATION.csv"):
    df = pd.read_csv("phase1_audit/step3_2_reconciliation/PLAYER_STATISTICS_RECONCILIATION.csv")
    print("=== PLAYER_STATISTICS_RECONCILIATION.csv ===")
    print(df.columns.tolist())
    print(df.head(10))
