import os
import pandas as pd
import numpy as np

# Load modeled deliveries from step3
df = pd.read_pickle("phase1_audit/step3_individual_model/bbb_step3_modeled.pkl")
comps = pd.read_csv("competitions.csv")
comp_map = comps.set_index("comp_id")["match_format"].to_dict()
comp_name_map = comps.set_index("comp_id")["comp_name"].to_dict()
df["match_format"] = df["comp_id"].map(comp_map).fillna("T20")
df["comp_name"] = df["comp_id"].map(comp_name_map).fillna("")

cut_b_75 = df["BPI"].quantile(0.75)
cut_b_80 = df["BPI"].quantile(0.80)
cut_b_85 = df["BPI"].quantile(0.85)

cut_bw_75 = df["BWPI"].quantile(0.75)
cut_bw_80 = df["BWPI"].quantile(0.80)
cut_bw_85 = df["BWPI"].quantile(0.85)

print("Checking Batters:")
for pid, name in [(1318, "Andre Russell"), (898, "Glenn Maxwell"), (6396, "Tim David"), (6283, "Abhishek Sharma")]:
    sub = df[df["striker_id"] == pid]
    p_75 = len(sub[sub["is_legal_bat"] & (sub["BPI"] >= cut_b_75)])
    p_80 = len(sub[sub["is_legal_bat"] & (sub["BPI"] >= cut_b_80)])
    p_85 = len(sub[sub["is_legal_bat"] & (sub["BPI"] >= cut_b_85)])
    ipl_p75 = len(sub[sub["is_legal_bat"] & (sub["BPI"] >= cut_b_75) & (sub["comp_name"].str.contains("IPL|Indian Premier League", case=False))])
    t20i_p75 = len(sub[sub["is_legal_bat"] & (sub["BPI"] >= cut_b_75) & (sub["match_format"] == "T20I")])
    inn2_p75 = len(sub[sub["is_legal_bat"] & (sub["BPI"] >= cut_b_75) & (sub["innings"] == 2)])
    inn1_p75 = len(sub[sub["is_legal_bat"] & (sub["BPI"] >= cut_b_75) & (sub["innings"] == 1)])
    death_p75 = len(sub[sub["is_legal_bat"] & (sub["BPI"] >= cut_b_75) & (sub["overid"] >= 16)])

    print(f"{name} (Target: 192/120/188/113):")
    print(f"  p_75={p_75}, p_80={p_80}, p_85={p_85}, ipl_p75={ipl_p75}, t20i_p75={t20i_p75}, inn2_p75={inn2_p75}, inn1_p75={inn1_p75}, death_p75={death_p75}")

print("\nChecking Bowlers:")
for pid, name in [(8661, "Matheesha Pathirana"), (2933, "Jasprit Bumrah"), (19316, "Maheesh Theekshana"), (25048, "Umran Malik"), (8848, "Mayank Yadav")]:
    sub = df[df["bowler_id"] == pid]
    p_75 = len(sub[sub["BWPI"] >= cut_bw_75])
    p_80 = len(sub[sub["BWPI"] >= cut_bw_80])
    p_85 = len(sub[sub["BWPI"] >= cut_bw_85])
    legal_p75 = len(sub[(sub["BWPI"] >= cut_bw_75) & sub["is_legal_bowl"]])
    ipl_p75 = len(sub[(sub["BWPI"] >= cut_bw_75) & (sub["comp_name"].str.contains("IPL|Indian Premier League", case=False))])
    death_p75 = len(sub[(sub["BWPI"] >= cut_bw_75) & (sub["overid"] >= 16)])

    print(f"{name} (Target: 137/378/117/147/62):")
    print(f"  p_75={p_75}, legal_p75={legal_p75}, p_80={p_80}, p_85={p_85}, ipl_p75={ipl_p75}, death_p75={death_p75}")

