import os
import pandas as pd

df = pd.read_csv("phase1_audit/step3_2_reconciliation/PLAYER_STATISTICS_RECONCILIATION.csv")
for _, r in df.iterrows():
    print(f"[{r['discipline']}] {r['player_name']}: step3={r['step3_reported_p_balls']}, step3_1={r['step3_1_table_p_balls']}, true={r['true_dataset_p_balls']}, reason={r['reason_for_difference'][:60]}")

