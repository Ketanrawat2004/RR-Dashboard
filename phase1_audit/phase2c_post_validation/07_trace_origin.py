import os
import pandas as pd

# Let's inspect step3 files
files_to_check = [
    "phase1_audit/step3_individual_model/BATTERS_TOP10_PROVISIONAL.csv",
    "phase1_audit/step3_individual_model/BATTERS_PERFORMANCE_STEP3.csv",
    "phase1_audit/step3_individual_model/BOWLERS_TOP10_PROVISIONAL.csv",
    "phase1_audit/step3_individual_model/BOWLERS_PERFORMANCE_STEP3.csv",
    "phase1_audit/step3_1_validation/MODEL_FOLD_VALIDATION.csv",
    "phase1_audit/step3_2_reconciliation/DELIVERY_ACCOUNTING_RECONCILIATION.csv",
    "phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv",
    "phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_COMPOSITE.csv",
    "phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv",
]

for f in files_to_check:
    if os.path.exists(f):
        print("="*60)
        print("FILE:", f)
        df = pd.read_csv(f)
        cols = [c for c in df.columns if any(k in c.lower() for k in ["name", "player", "ball", "bf", "press", "leverage"])]
        print("Relevant columns:", cols)
        
        # Check Andre Russell
        sub_russell = df[df.apply(lambda row: "Russell" in str(row.values), axis=1)]
        if not sub_russell.empty:
            print("  Russell in", f, ":", sub_russell[cols].to_dict(orient="records"))
            
        # Check Bumrah
        sub_bumrah = df[df.apply(lambda row: "Bumrah" in str(row.values), axis=1)]
        if not sub_bumrah.empty:
            print("  Bumrah in", f, ":", sub_bumrah[cols].to_dict(orient="records"))

        # Check Pathirana
        sub_path = df[df.apply(lambda row: "Pathirana" in str(row.values), axis=1)]
        if not sub_path.empty:
            print("  Pathirana in", f, ":", sub_path[cols].to_dict(orient="records"))

        # Check Umran Malik
        sub_umran = df[df.apply(lambda row: "Umran" in str(row.values), axis=1)]
        if not sub_umran.empty:
            print("  Umran in", f, ":", sub_umran[cols].to_dict(orient="records"))

