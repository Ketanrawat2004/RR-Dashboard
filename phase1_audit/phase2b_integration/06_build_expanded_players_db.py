import os
import re
import json
import pandas as pd
import numpy as np

ROOT = r"C:\RR NEW"
AUDIT_DIR = os.path.join(ROOT, "phase1_audit")
STEP4_DIR = os.path.join(AUDIT_DIR, "step4_jury_harmonization")
BACKUP_DIR = os.path.join(AUDIT_DIR, "phase2_backup_pre_implementation")

def to_key(name):
    return re.sub(r"[^a-zA-Z0-9]+", "_", name.strip()).strip("_").lower()

def main():
    print("=" * 80)
    print("PHASE 2B: STEP 2 — GENERATE EXPANDED 342-RECORD PLAYERS_DB.JSON")
    print("=" * 80)

    # 1. Load legacy players_db.json
    legacy_path = os.path.join(BACKUP_DIR, "players_db.json")
    with open(legacy_path, "r", encoding="utf-8") as f:
        legacy_db = json.load(f)
    print(f"Loaded {len(legacy_db)} legacy records from backup.")
    legacy_by_name = {r["name"]: r for r in legacy_db}
    legacy_by_key = {r["key"]: r for r in legacy_db}

    # 2. Load Step 4 CSVs
    bat_csv = pd.read_csv(os.path.join(STEP4_DIR, "FINAL_BATTER_RANKINGS.csv"))
    bowl_rae_csv = pd.read_csv(os.path.join(STEP4_DIR, "FINAL_BOWLER_RANKINGS_RAE.csv"))
    bowl_comp_csv = pd.read_csv(os.path.join(STEP4_DIR, "FINAL_BOWLER_RANKINGS_COMPOSITE.csv"))

    print(f"Loaded Batters CSV: {len(bat_csv)} rows")
    print(f"Loaded Bowlers Pure RPAE CSV: {len(bowl_rae_csv)} rows")
    print(f"Loaded Bowlers Composite CSV: {len(bowl_comp_csv)} rows")

    # 3. Load career match counts from playing_eleven.csv
    pe = pd.read_csv(os.path.join(ROOT, "playing_eleven.csv"))
    p_matches = pe.groupby("player_id")["match_id"].nunique().to_dict()

    # 4. Load high-pressure matches from bbb_step3_modeled.pkl
    df_modeled = pd.read_pickle(os.path.join(AUDIT_DIR, "step3_individual_model", "bbb_step3_modeled.pkl"))
    cut_b = df_modeled["BPI"].quantile(0.75)
    cut_bw = df_modeled["BWPI"].quantile(0.75)
    df_modeled["hp_bat"] = (df_modeled["BPI"] >= cut_b) & df_modeled["is_legal_bat"]
    df_modeled["hp_bowl"] = (df_modeled["BWPI"] >= cut_bw)
    hp_m_bat = df_modeled[df_modeled["hp_bat"]].groupby("striker_id")["match_id"].nunique().to_dict()
    hp_m_bowl = df_modeled[df_modeled["hp_bowl"]].groupby("bowler_id")["match_id"].nunique().to_dict()

    # 5. Build Bowler merged lookup
    bowl_merged = bowl_comp_csv.merge(
        bowl_rae_csv[[
            "player_id", "career_econ", "career_exp_econ", "career_rpae_rate",
            "pressure_runs", "pressure_exp_runs", "pressure_econ", "pressure_exp_econ",
            "raw_pressure_rpae_rate", "non_pressure_econ", "non_pressure_rpae_rate", "clutch_rpae_lift"
        ]],
        on="player_id",
        how="left"
    )

    records = []

    # -------------------------------------------------------------
    # BUILD BATTER RECORDS (163)
    # -------------------------------------------------------------
    print("\nProcessing 163 Batters...")
    for idx, r in bat_csv.iterrows():
        pid = int(r["player_id"])
        name = str(r["player_name"])
        key = to_key(name)
        rank = int(r["rank"])
        shrunk_score = round(float(r["shrunk_rae_score"]), 2)

        # Check if legacy record exists
        leg = legacy_by_name.get(name, legacy_by_key.get(key, {}))

        # Matches
        tot_m = int(leg.get("total_m", p_matches.get(pid, 20)))
        hp_m = int(hp_m_bat.get(pid, leg.get("hp_m", 10)))

        # Roles and teams
        teams = str(r.get("franchises", leg.get("teams", "IPL Franchise")))
        role_desc = leg.get("role_desc", "Specialist High-Leverage Batter")
        tactical_role = leg.get("tactical_role", "Middle-Overs & Death Boundary Striker" if r["pressure_bf"] > 100 else "Top-Order Impact Striker")

        # Valuation estimate based on rank & score
        if rank <= 3:
            bid_c = "₹15.0 - 18.0 Cr"
            verdict = "PRIORITY MUST-BUY (Tier 1 Elite)"
        elif rank <= 7:
            bid_c = "₹11.0 - 14.5 Cr"
            verdict = "HIGH TARGET (Core Match-Winner)"
        elif rank <= 12:
            bid_c = "₹7.5 - 10.5 Cr"
            verdict = "STRONG VALUE BUY (Tactical Asset)"
        elif rank <= 25:
            bid_c = "₹4.0 - 7.0 Cr"
            verdict = "ROTATIONAL SQUAD TARGET"
        else:
            bid_c = "₹0.5 - 3.5 Cr"
            verdict = "SQUAD DEPTH OPTION"

        tagline = leg.get("tagline", f"Rank #{rank} Pressure Run Value Generator")
        summary = leg.get("summary", f"{name} generated {r['pressure_rae']:+.2f} runs above contextual expectation across {int(r['pressure_bf'])} high-pressure deliveries with a {r['top10_prob_pct']:.1f}% Top-10 bootstrap inclusion probability.")
        why_chose = leg.get("why_chose", f"Elite pressure scoring rate of {r['raw_pressure_rae_rate']:+.2f} runs/100b relative to phase and wickets in hand.")
        why_not_others = leg.get("why_not_others", f"Maintains superior Empirical Bayes shrunk performance ({shrunk_score:+.2f}) with bounded rank uncertainty ({r['rank_ci_90']}).")
        rr_fit = leg.get("rr_fit", f"Provides Rajasthan Royals with proven leverage boundary scoring firepower across critical match phases.")
        rr_mgmt = leg.get("rr_management_summary", f"Statistically verified high-leverage contributor. Deploy strategically against targeted bowling match-ups.")
        key_skill = leg.get("key_tactical_skill", f"High-pressure boundary striking under RRR pressure ({r['sample_size_badge']})")
        comp_analysis = leg.get("comparative_analysis", f"Demonstrates clutch RAE lift of {r['clutch_rae_lift']:+.2f} runs/100b over baseline non-pressure strike rate.")

        rec = {
            # Legacy 26 fields
            "category": "Batter",
            "rank": rank,
            "name": name,
            "key": key,
            "teams": teams,
            "role_desc": role_desc,
            "total_m": tot_m,
            "base_wr": round(float(r["career_exp_sr"]), 2),
            "hp_m": hp_m,
            "hp_wr": round(float(r["pressure_sr"]), 2),
            "lift": round(float(r["clutch_rae_lift"]), 2),
            "mom_hp": int(leg.get("mom_hp", 0)),
            "ko_wr": round(float(leg.get("ko_wr", 50.0)), 1),
            "bayes_hp_wr": shrunk_score,
            "cppi": shrunk_score,
            "bid_ceiling": leg.get("bid_ceiling", bid_c),
            "tactical_role": tactical_role,
            "summary": summary,
            "why_chose": why_chose,
            "why_not_others": why_not_others,
            "rr_fit": rr_fit,
            "verdict": leg.get("verdict", verdict),
            "tagline": tagline,
            "rr_management_summary": rr_mgmt,
            "key_tactical_skill": key_skill,
            "comparative_analysis": comp_analysis,

            # Modern Step 4 fields
            "player_id": pid,
            "career_balls": int(r["career_bf"]),
            "pressure_balls": int(r["pressure_bf"]),
            "shrunk_score": shrunk_score,
            "raw_pressure_rate": round(float(r["raw_pressure_rae_rate"]), 2),
            "ci95_lower": round(float(r["ci95_lower"]), 2),
            "ci95_upper": round(float(r["ci95_upper"]), 2),
            "rank_ci_90": str(r["rank_ci_90"]),
            "top10_prob_pct": round(float(r["top10_prob_pct"]), 1),
            "sample_size_badge": str(r["sample_size_badge"]),
            
            # Bowling specific fields (None for batters)
            "bowling_framework": None,
            "shrunk_rpae_score": None,
            "composite_score": None,
            "rank_pure_rpae": None,
            "rank_composite": None,
            "rank_shift_vs_rpae": None,
            "pressure_wkts": None,
            "pressure_exp_wkts": None,
            "pressure_wae": None,
            "shrunk_wae_rate": None,
            "wae_run_equivalent": None,
            "bootstrap_mean": round(float(r["bootstrap_mean"]), 2),
            "bootstrap_se": round(float(r["bootstrap_se"]), 2)
        }
        records.append(rec)

    # -------------------------------------------------------------
    # BUILD BOWLER RECORDS (179)
    # -------------------------------------------------------------
    print("\nProcessing 179 Bowlers...")
    for idx, r in bowl_merged.iterrows():
        pid = int(r["player_id"])
        name = str(r["player_name"])
        key = to_key(name)
        rank_comp = int(r["rank_composite"])
        rank_rpae = int(r["rank_pure_rpae"])
        comp_score = round(float(r["composite_score"]), 2)
        shrunk_rpae = round(float(r["shrunk_rpae_score"]), 2)

        # Check legacy record
        leg = legacy_by_name.get(name, legacy_by_key.get(key, {}))

        # Matches
        tot_m = int(leg.get("total_m", p_matches.get(pid, 20)))
        hp_m = int(hp_m_bowl.get(pid, leg.get("hp_m", 10)))

        # Roles and teams
        teams = str(r.get("franchises", leg.get("teams", "IPL Franchise")))
        role_desc = leg.get("role_desc", "High-Impact Pace/Spin Strike Bowler")
        tactical_role = leg.get("tactical_role", "Death Overs & Middle Strike Enforcer" if r["pressure_b"] > 100 else "High-Leverage Matchup Specialist")

        # Valuation estimate based on Composite Rank
        if rank_comp <= 3:
            bid_c = "₹15.0 - 18.0 Cr"
            verdict = "PRIORITY MUST-BUY (Tier 1 Strike Bowler)"
        elif rank_comp <= 7:
            bid_c = "₹10.5 - 14.0 Cr"
            verdict = "HIGH TARGET (Core Pace/Spin Weapon)"
        elif rank_comp <= 12:
            bid_c = "₹7.0 - 10.0 Cr"
            verdict = "STRONG VALUE BUY (Tactical Wicket-Taker)"
        elif rank_comp <= 25:
            bid_c = "₹4.0 - 6.5 Cr"
            verdict = "ROTATIONAL BOWLING TARGET"
        else:
            bid_c = "₹0.5 - 3.5 Cr"
            verdict = "SQUAD DEPTH OPTION"

        tagline = leg.get("tagline", f"Rank #{rank_comp} Composite Strike & Economy Enforcer")
        summary = leg.get("summary", f"{name} secured {r['pressure_wkts']:.0f} wickets (vs {r['pressure_exp_wkts']:.2f} exp) with {r['pressure_rpae']:+.2f} runs saved across {int(r['pressure_b'])} high-pressure deliveries.")
        why_chose = leg.get("why_chose", f"Elite composite impact: 60% run suppression ({shrunk_rpae:+.2f}) combined with 40% strike wicket value ({r['wae_run_equivalent']:+.2f} run eq).")
        why_not_others = leg.get("why_not_others", f"Produces genuine wicket breakthroughs under pressure while maintaining a {r['top10_prob_pct']:.1f}% Top-10 inclusion probability.")
        rr_fit = leg.get("rr_fit", f"Strengthens Rajasthan Royals attack by providing high-pace or deception breakthroughs at clutch moments.")
        rr_mgmt = leg.get("rr_management_summary", f"High-impact bowler. Deploy in specialized overs to break threatening partnerships.")
        key_skill = leg.get("key_tactical_skill", f"High-pressure wicket strike capability ({r['sample_size_badge']})")
        comp_analysis = leg.get("comparative_analysis", f"Pure RPAE rank #{rank_rpae} ({shrunk_rpae:+.2f}) vs Composite rank #{rank_comp} ({comp_score:+.2f}), shift: {int(r['rank_shift_vs_rpae']):+d}.")

        rec = {
            # Legacy 26 fields
            "category": "Bowler",
            "rank": rank_comp,
            "name": name,
            "key": key,
            "teams": teams,
            "role_desc": role_desc,
            "total_m": tot_m,
            "base_wr": round(float(r["career_exp_econ"]), 2) if pd.notna(r.get("career_exp_econ")) else 8.50,
            "hp_m": hp_m,
            "hp_wr": round(float(r["pressure_econ"]), 2) if pd.notna(r.get("pressure_econ")) else 8.20,
            "lift": round(float(r["clutch_rpae_lift"]), 2) if pd.notna(r.get("clutch_rpae_lift")) else round(shrunk_rpae, 2),
            "mom_hp": int(leg.get("mom_hp", 0)),
            "ko_wr": round(float(leg.get("ko_wr", 50.0)), 1),
            "bayes_hp_wr": shrunk_rpae,
            "cppi": comp_score,
            "bid_ceiling": leg.get("bid_ceiling", bid_c),
            "tactical_role": tactical_role,
            "summary": summary,
            "why_chose": why_chose,
            "why_not_others": why_not_others,
            "rr_fit": rr_fit,
            "verdict": leg.get("verdict", verdict),
            "tagline": tagline,
            "rr_management_summary": rr_mgmt,
            "key_tactical_skill": key_skill,
            "comparative_analysis": comp_analysis,

            # Modern Step 4 fields
            "player_id": pid,
            "career_balls": int(r["career_b"]),
            "pressure_balls": int(r["pressure_b"]),
            "shrunk_score": comp_score,
            "raw_pressure_rate": round(float(r["raw_pressure_rpae_rate"]), 2) if pd.notna(r.get("raw_pressure_rpae_rate")) else round(float(r["shrunk_rpae_score"]), 2),
            "ci95_lower": round(float(r["ci95_lower"]), 2),
            "ci95_upper": round(float(r["ci95_upper"]), 2),
            "rank_ci_90": str(r["rank_ci_90"]),
            "top10_prob_pct": round(float(r["top10_prob_pct"]), 1),
            "sample_size_badge": str(r["sample_size_badge"]),

            # Bowling specific fields
            "bowling_framework": "Balanced_Composite",
            "shrunk_rpae_score": shrunk_rpae,
            "composite_score": comp_score,
            "rank_pure_rpae": rank_rpae,
            "rank_composite": rank_comp,
            "rank_shift_vs_rpae": int(r["rank_shift_vs_rpae"]),
            "pressure_wkts": round(float(r["pressure_wkts"]), 1),
            "pressure_exp_wkts": round(float(r["pressure_exp_wkts"]), 2),
            "pressure_wae": round(float(r["pressure_wae"]), 2),
            "shrunk_wae_rate": round(float(r["shrunk_wae_rate"]), 4),
            "wae_run_equivalent": round(float(r["wae_run_equivalent"]), 2),
            "bootstrap_mean": round(float(r["bootstrap_mean"]), 2),
            "bootstrap_se": round(float(r["bootstrap_se"]), 2)
        }
        records.append(rec)

    # Validate final collection
    print(f"\nTotal records created: {len(records)} (Expected: 342 = 163 Batters + 179 Bowlers)")
    assert len(records) == 342, f"Expected 342 records, got {len(records)}"

    n_bat = sum(1 for r in records if r["category"] == "Batter")
    n_bowl = sum(1 for r in records if r["category"] == "Bowler")
    assert n_bat == 163, f"Expected 163 batters, got {n_bat}"
    assert n_bowl == 179, f"Expected 179 bowlers, got {n_bowl}"

    # Write players_db.json
    out_path = os.path.join(ROOT, "players_db.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"Successfully wrote {len(records)} validated player records to {out_path}.")
    print(f"File size: {os.path.getsize(out_path):,} bytes")

if __name__ == "__main__":
    main()

