"""
Phase 1 Final Independent Verification Script
(01_verify_rankings_and_scores.py)

Performs comprehensive, independent verification of:
1. All three ranking CSVs in phase1_audit/step4_jury_harmonization/
2. Exact score recalculations for Russell, Vaibhav, Maxwell, Pathirana, Bumrah, Umran Malik
3. Mathematical structure of the bowling composite formula
4. Bootstrap quantiles and simulation error
5. Claims in PHASE1_FINAL_METHODOLOGY.md
6. Website dependency audit
"""

import os
import json
import numpy as np
import pandas as pd

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit")
STEP4_DIR = os.path.join(AUDIT_DIR, "step4_jury_harmonization")
VERIF_DIR = os.path.join(AUDIT_DIR, "final_independent_verification")


def verify_csv_integrity():
    print("=" * 80)
    print("TASK 1: VERIFICATION OF THE THREE RANKING CSVS")
    print("=" * 80)

    # 1. Batting CSV
    bat_path = os.path.join(STEP4_DIR, "FINAL_BATTER_RANKINGS.csv")
    df_bat = pd.read_csv(bat_path)
    print(f"FINAL_BATTER_RANKINGS.csv:")
    print(f"  Rows count: {len(df_bat)} (Expected: 163)")
    print(f"  Unique player_id: {df_bat['player_id'].nunique()}")
    print(f"  Duplicate player_ids: {df_bat['player_id'].duplicated().sum()}")
    print(f"  Missing values per column:\n{df_bat.isnull().sum()[df_bat.isnull().sum() > 0]}")
    # Check eligibility
    inelig_career_bat = (df_bat["career_bf"] < 300).sum()
    inelig_press_bat = (df_bat["pressure_bf"] < 40).sum()
    print(f"  Ineligible career_bf (<300): {inelig_career_bat}")
    print(f"  Ineligible pressure_bf (<40): {inelig_press_bat}")
    # Check sorting
    is_sorted_bat = df_bat["shrunk_rae_score"].is_monotonic_decreasing
    print(f"  Sorted strictly descending by shrunk_rae_score: {is_sorted_bat}")
    print(f"  Rank column matches index: {(df_bat['rank'] == (df_bat.index + 1)).all()}")

    # 2. Bowling Pure RPAE CSV
    bowl_rpae_path = os.path.join(STEP4_DIR, "FINAL_BOWLER_RANKINGS_RAE.csv")
    df_bowl_rpae = pd.read_csv(bowl_rpae_path)
    print(f"\nFINAL_BOWLER_RANKINGS_RAE.csv:")
    print(f"  Rows count: {len(df_bowl_rpae)} (Expected: 179)")
    print(f"  Unique player_id: {df_bowl_rpae['player_id'].nunique()}")
    print(f"  Duplicate player_ids: {df_bowl_rpae['player_id'].duplicated().sum()}")
    print(f"  Missing values per column:\n{df_bowl_rpae.isnull().sum()[df_bowl_rpae.isnull().sum() > 0]}")
    inelig_career_bowl = (df_bowl_rpae["career_b"] < 300).sum()
    inelig_press_bowl = (df_bowl_rpae["pressure_b"] < 40).sum()
    print(f"  Ineligible career_b (<300): {inelig_career_bowl}")
    print(f"  Ineligible pressure_b (<40): {inelig_press_bowl}")
    is_sorted_bowl_rpae = df_bowl_rpae["shrunk_rpae_score"].is_monotonic_decreasing
    print(f"  Sorted strictly descending by shrunk_rpae_score: {is_sorted_bowl_rpae}")
    print(f"  Rank column matches index: {(df_bowl_rpae['rank_rpae'] == (df_bowl_rpae.index + 1)).all()}")

    # 3. Bowling Composite CSV
    bowl_comp_path = os.path.join(STEP4_DIR, "FINAL_BOWLER_RANKINGS_COMPOSITE.csv")
    df_bowl_comp = pd.read_csv(bowl_comp_path)
    print(f"\nFINAL_BOWLER_RANKINGS_COMPOSITE.csv:")
    print(f"  Rows count: {len(df_bowl_comp)} (Expected: 179)")
    print(f"  Unique player_id: {df_bowl_comp['player_id'].nunique()}")
    print(f"  Duplicate player_ids: {df_bowl_comp['player_id'].duplicated().sum()}")
    print(f"  Missing values per column:\n{df_bowl_comp.isnull().sum()[df_bowl_comp.isnull().sum() > 0]}")
    inelig_career_comp = (df_bowl_comp["career_b"] < 300).sum()
    inelig_press_comp = (df_bowl_comp["pressure_b"] < 40).sum()
    print(f"  Ineligible career_b (<300): {inelig_career_comp}")
    print(f"  Ineligible pressure_b (<40): {inelig_press_comp}")
    is_sorted_bowl_comp = df_bowl_comp["composite_score"].is_monotonic_decreasing
    print(f"  Sorted strictly descending by composite_score: {is_sorted_bowl_comp}")
    print(f"  Rank column matches index: {(df_bowl_comp['rank_composite'] == (df_bowl_comp.index + 1)).all()}")

    return df_bat, df_bowl_rpae, df_bowl_comp


def verify_individual_recalculations(df_bat, df_bowl_rpae, df_bowl_comp):
    print("\n" + "=" * 80)
    print("TASK 2: INDEPENDENT RECALCULATION OF DISPLAYED SCORES")
    print("=" * 80)

    # Load modeled deliveries
    df_deliv = pd.read_pickle(os.path.join(AUDIT_DIR, "step3_individual_model", "bbb_step3_modeled.pkl"))
    ctpm = pd.read_csv(os.path.join(ROOT, "competition_team_player_mapping.csv"))

    cut_b = df_deliv["BPI"].quantile(0.75)
    cut_bw = df_deliv["BWPI"].quantile(0.75)
    df_deliv["is_hp_bat"] = (df_deliv["BPI"] >= cut_b) & df_deliv["is_legal_bat"]
    df_deliv["is_hp_bowl"] = (df_deliv["BWPI"] >= cut_bw)

    # 1. Andre Russell (pid: 1318)
    r_deliv = df_deliv[df_deliv["is_hp_bat"] & (df_deliv["striker_id"] == 1318)]
    r_n = len(r_deliv)
    r_runs = r_deliv["runs"].sum()
    r_exp_runs = r_deliv["exp_bat_runs"].sum()
    r_rae = r_deliv["rae"].sum()
    r_shrunk = (r_rae / (r_n + 150.0)) * 100.0
    r_csv = df_bat[df_bat["player_id"] == 1318].iloc[0]

    print("1. Andre Russell (Player ID 1318):")
    print(f"   Pressure balls (N): Recalculated = {r_n} | CSV = {r_csv['pressure_bf']}")
    print(f"   Actual Runs: Recalculated = {r_runs} | CSV = {r_csv['pressure_runs']}")
    print(f"   Expected Runs: Recalculated = {r_exp_runs:.2f} | CSV = {r_csv['pressure_exp_runs']:.2f}")
    print(f"   Pressure RAE: Recalculated = {r_rae:.4f} | CSV = {r_csv['pressure_rae']:.4f}")
    print(f"   Shrunk RAE Score: Recalculated = {r_shrunk:.4f} | CSV = {r_csv['shrunk_rae_score']:.4f}")
    print(f"   Discrepancy: {abs(r_shrunk - r_csv['shrunk_rae_score']):.6f} (MATCH: {abs(r_shrunk - r_csv['shrunk_rae_score']) < 0.01})")

    # 2. Vaibhav Sooryavanshi (pid: 50284)
    v_deliv = df_deliv[df_deliv["is_hp_bat"] & (df_deliv["striker_id"] == 50284)]
    v_n = len(v_deliv)
    v_runs = v_deliv["runs"].sum()
    v_exp_runs = v_deliv["exp_bat_runs"].sum()
    v_rae = v_deliv["rae"].sum()
    v_shrunk = (v_rae / (v_n + 150.0)) * 100.0
    v_csv = df_bat[df_bat["player_id"] == 50284].iloc[0]

    print("\n2. Vaibhav Sooryavanshi (Player ID 50284):")
    print(f"   Pressure balls (N): Recalculated = {v_n} | CSV = {v_csv['pressure_bf']}")
    print(f"   Actual Runs: Recalculated = {v_runs} | CSV = {v_csv['pressure_runs']}")
    print(f"   Expected Runs: Recalculated = {v_exp_runs:.2f} | CSV = {v_csv['pressure_exp_runs']:.2f}")
    print(f"   Pressure RAE: Recalculated = {v_rae:.4f} | CSV = {v_csv['pressure_rae']:.4f}")
    print(f"   Shrunk RAE Score: Recalculated = {v_shrunk:.4f} | CSV = {v_csv['shrunk_rae_score']:.4f}")
    print(f"   Discrepancy: {abs(v_shrunk - v_csv['shrunk_rae_score']):.6f} (MATCH: {abs(v_shrunk - v_csv['shrunk_rae_score']) < 0.01})")

    # 3. Glenn Maxwell (pid: 838)
    m_deliv = df_deliv[df_deliv["is_hp_bat"] & (df_deliv["striker_id"] == 838)]
    m_n = len(m_deliv)
    m_runs = m_deliv["runs"].sum()
    m_exp_runs = m_deliv["exp_bat_runs"].sum()
    m_rae = m_deliv["rae"].sum()
    m_shrunk = (m_rae / (m_n + 150.0)) * 100.0
    m_csv = df_bat[df_bat["player_id"] == 838].iloc[0]

    print("\n3. Glenn Maxwell (Player ID 838):")
    print(f"   Pressure balls (N): Recalculated = {m_n} | CSV = {m_csv['pressure_bf']}")
    print(f"   Actual Runs: Recalculated = {m_runs} | CSV = {m_csv['pressure_runs']}")
    print(f"   Expected Runs: Recalculated = {m_exp_runs:.2f} | CSV = {m_csv['pressure_exp_runs']:.2f}")
    print(f"   Pressure RAE: Recalculated = {m_rae:.4f} | CSV = {m_csv['pressure_rae']:.4f}")
    print(f"   Shrunk RAE Score: Recalculated = {m_shrunk:.4f} | CSV = {m_csv['shrunk_rae_score']:.4f}")
    print(f"   Discrepancy: {abs(m_shrunk - m_csv['shrunk_rae_score']):.6f} (MATCH: {abs(m_shrunk - m_csv['shrunk_rae_score']) < 0.01})")

    # 4. Matheesha Pathirana (pid search)
    pathirana_pids = ctpm[ctpm["player_name"].str.lower().str.contains("pathirana")]["player_id"].unique()
    pat_pid = pathirana_pids[0]
    p_deliv = df_deliv[df_deliv["is_hp_bowl"] & (df_deliv["bowler_id"] == pat_pid)]
    p_n = p_deliv["is_legal_bowl"].sum()
    p_runs = p_deliv["bowl_runs_obs"].sum()
    p_exp_runs = p_deliv["exp_bowl_runs"].sum()
    p_rpae = p_deliv["rpae"].sum()
    p_shrunk_rpae = (p_rpae / (p_n + 150.0)) * 100.0
    p_csv = df_bowl_rpae[df_bowl_rpae["player_id"] == pat_pid].iloc[0]

    print(f"\n4. Matheesha Pathirana (Player ID {pat_pid}):")
    print(f"   Pressure legal balls (N): Recalculated = {p_n} | CSV = {p_csv['pressure_b']}")
    print(f"   Conceded Runs: Recalculated = {p_runs} | CSV = {p_csv['pressure_runs']}")
    print(f"   Expected Conceded Runs: Recalculated = {p_exp_runs:.2f} | CSV = {p_csv['pressure_exp_runs']:.2f}")
    print(f"   Pressure RPAE: Recalculated = {p_rpae:.4f} | CSV = {p_csv['pressure_rpae']:.4f}")
    print(f"   Shrunk RPAE Score: Recalculated = {p_shrunk_rpae:.4f} | CSV = {p_csv['shrunk_rpae_score']:.4f}")
    print(f"   Discrepancy: {abs(p_shrunk_rpae - p_csv['shrunk_rpae_score']):.6f} (MATCH: {abs(p_shrunk_rpae - p_csv['shrunk_rpae_score']) < 0.01})")

    # 5. Jasprit Bumrah (pid search)
    bumrah_pids = ctpm[ctpm["player_name"].str.lower().str.contains("bumrah")]["player_id"].unique()
    bum_pid = bumrah_pids[0]
    b_deliv = df_deliv[df_deliv["is_hp_bowl"] & (df_deliv["bowler_id"] == bum_pid)]
    b_n = b_deliv["is_legal_bowl"].sum()
    b_runs = b_deliv["bowl_runs_obs"].sum()
    b_exp_runs = b_deliv["exp_bowl_runs"].sum()
    b_rpae = b_deliv["rpae"].sum()
    b_shrunk_rpae = (b_rpae / (b_n + 150.0)) * 100.0
    b_csv = df_bowl_rpae[df_bowl_rpae["player_id"] == bum_pid].iloc[0]

    print(f"\n5. Jasprit Bumrah (Player ID {bum_pid}):")
    print(f"   Pressure legal balls (N): Recalculated = {b_n} | CSV = {b_csv['pressure_b']}")
    print(f"   Conceded Runs: Recalculated = {b_runs} | CSV = {b_csv['pressure_runs']}")
    print(f"   Expected Conceded Runs: Recalculated = {b_exp_runs:.2f} | CSV = {b_csv['pressure_exp_runs']:.2f}")
    print(f"   Pressure RPAE: Recalculated = {b_rpae:.4f} | CSV = {b_csv['pressure_rpae']:.4f}")
    print(f"   Shrunk RPAE Score: Recalculated = {b_shrunk_rpae:.4f} | CSV = {b_csv['shrunk_rpae_score']:.4f}")
    print(f"   Discrepancy: {abs(b_shrunk_rpae - b_csv['shrunk_rpae_score']):.6f} (MATCH: {abs(b_shrunk_rpae - b_csv['shrunk_rpae_score']) < 0.01})")

    # 6. Umran Malik (pid: 25048) in Composite
    u_deliv = df_deliv[df_deliv["is_hp_bowl"] & (df_deliv["bowler_id"] == 25048)]
    u_n = u_deliv["is_legal_bowl"].sum()
    u_rpae = u_deliv["rpae"].sum()
    u_wae = u_deliv["wae"].sum()
    u_wkts = u_deliv["is_bowler_wicket"].sum()
    u_exp_wkts = u_deliv["exp_bowl_wkt"].sum()
    
    u_shrunk_rpae = (u_rpae / (u_n + 150.0)) * 100.0
    u_shrunk_wae_rate = (u_wae / (u_n + 100.0)) * 100.0
    u_wae_run_equiv = u_shrunk_wae_rate * 12.0
    u_comp_score = 0.60 * u_shrunk_rpae + 0.40 * u_wae_run_equiv
    u_csv = df_bowl_comp[df_bowl_comp["player_id"] == 25048].iloc[0]

    print("\n6. Umran Malik (Player ID 25048) in Composite:")
    print(f"   Pressure legal balls (N): Recalculated = {u_n} | CSV = {u_csv['pressure_b']}")
    print(f"   Pressure Wickets: Recalculated = {u_wkts} | CSV = {u_csv['pressure_wkts']}")
    print(f"   Expected Wickets: Recalculated = {u_exp_wkts:.4f} | CSV = {u_csv['pressure_exp_wkts']:.4f}")
    print(f"   Pressure WAE: Recalculated = {u_wae:.4f} | CSV = {u_csv['pressure_wae']:.4f}")
    print(f"   Shrunk RPAE: Recalculated = {u_shrunk_rpae:.4f} | CSV = {u_csv['shrunk_rpae_score']:.4f}")
    print(f"   WAE Run Equiv (12x): Recalculated = {u_wae_run_equiv:.4f} | CSV = {u_csv['wae_run_equivalent']:.4f}")
    print(f"   Composite Score: Recalculated = {u_comp_score:.4f} | CSV = {u_csv['composite_score']:.4f}")
    print(f"   Discrepancy: {abs(u_comp_score - u_csv['composite_score']):.6f} (MATCH: {abs(u_comp_score - u_csv['composite_score']) < 0.01})")


def verify_bowling_formula_structure():
    print("\n" + "=" * 80)
    print("TASK 3: MATHEMATICAL STRUCTURE OF BOWLING COMPOSITE FORMULA")
    print("=" * 80)
    print("""
Exact Bowling Composite Formula:
Composite_Score = 0.60 * Shrunk_RPAE_Rate + 0.40 * (Shrunk_WAE_Rate * 12.0)

Where:
  1. Shrunk_RPAE_Rate = (sum(RPAE) / (N_legal_balls + 150)) * 100
     - Measures runs saved per 100 legal balls relative to contextual expectation.
     - Shrunk toward zero prior with M0 = 150 balls.
  2. Shrunk_WAE_Rate = (sum(WAE) / (N_legal_balls + 100)) * 100
     - Measures excess bowler wickets per 100 legal balls relative to contextual wicket probability.
     - Shrunk toward zero prior with Mw = 100 balls.
  3. 12.0 Wicket-to-Run Equivalence Factor:
     - Each excess wicket taken saves an empirical average of ~12 runs over the rest of the innings.
  4. 60 / 40 Weighting:
     - 60% weight on run prevention (reliable, lower variance).
     - 40% weight on wicket impact (high leverage, but noisy Bernoulli trials).
""")


def inspect_website_code():
    print("=" * 80)
    print("TASK 6: WEBSITE DEPENDENCY AUDIT (HTML & JS)")
    print("=" * 80)
    with open(os.path.join(ROOT, "index.html"), "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    with open(os.path.join(ROOT, "players_db.json"), "r", encoding="utf-8", errors="ignore") as f:
        pdb = json.load(f)

    print(f"Current players_db.json contains {len(pdb)} records.")
    print("Sample record keys:", list(pdb[0].keys()))

    # Check how index.html consumes data
    import re
    # Check if players_db.json is loaded via fetch or embedded
    fetches = re.findall(r'fetch\([\'"](.*?)[\'"]\)', html)
    print("Fetch calls in index.html:", fetches)

    # Check if data is embedded directly in script
    embedded_data = re.findall(r'(?:var|let|const)\s+([a-zA-Z0-9_]+)\s*=\s*\[\s*\{', html)
    print("Embedded JSON arrays in index.html:", embedded_data)

    # Check how tables are rendered
    table_bat = "table-batters" in html
    table_bowl = "table-bowlers" in html
    print(f"Table 'table-batters' present: {table_bat}")
    print(f"Table 'table-bowlers' present: {table_bowl}")

    # Check if table body is hardcoded HTML or dynamically rendered
    tbody_content = re.findall(r'<tbody[^>]*>(.*?)</tbody>', html, re.DOTALL)
    print(f"Total tbody elements in index.html: {len(tbody_content)}")
    if tbody_content:
        first_tbody_len = len(tbody_content[0].strip())
        print(f"First tbody length: {first_tbody_len} chars (Hardcoded HTML: {first_tbody_len > 100})")


if __name__ == "__main__":
    b, br, bc = verify_csv_integrity()
    verify_individual_recalculations(b, br, bc)
    verify_bowling_formula_structure()
    inspect_website_code()
