"""
Phase 1 Read-Only Repository, Pipeline & Dashboard/Website Audit (02_repo_and_website_audit.py)
Inspects and reproduces repository scoring pipelines, verifies players_db.json, CSVs,
hardcoded wagon/pitch specs, narratives, PPTX, PDF scripts, and HTML DOM/JS logic.
"""

import ast
import hashlib
import json
import os
import re
import subprocess
from html.parser import HTMLParser
import numpy as np
import pandas as pd
from pptx import Presentation

ROOT = r"c:\Rajasthan Royals"
OUT_DIR = os.path.join(ROOT, "phase1_audit")
os.makedirs(OUT_DIR, exist_ok=True)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest().upper()


def extract_ast_dict_or_list(filepath: str, var_name: str):
    with open(filepath, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == var_name:
                    return ast.literal_eval(node.value)
    return None


def main():
    lines = []
    def log(msg=""):
        lines.append(msg)
        print(msg)

    log("=" * 80)
    log("PHASE 1 — REPOSITORY, PIPELINE, DELIVERABLE & WEBSITE AUDIT")
    log("=" * 80)

    # 1. HTML entry files comparison + git history
    log("\n[1] ENTRY HTML FILES & GIT STATE")
    for fn in ["index.html", "rr_pressure_dashboard.html", "rr_war_room_terminal.html"]:
        p = os.path.join(ROOT, fn)
        if os.path.exists(p):
            log(f"  {fn:<30} | {os.path.getsize(p):>10,} B | {sha256_file(p)}")
    try:
        git_log = subprocess.check_output(["git", "log", "-n", "12", "--oneline"], cwd=ROOT, text=True).strip()
        log("  Recent git commits:\n" + "\n".join("    " + x for x in git_log.splitlines()))
    except Exception as e:
        log(f"  git log error: {e}")

    # 2. Reproduce rr_pressure_analyst.py vs optimize_rankings.py vs apply_calibrated_rankings.py vs DB
    log("\n[2] REPRODUCE & COMPARE EXISTING SCORING SCRIPTS VS DELIVERABLES")
    matches = pd.read_csv(os.path.join(ROOT, "matches.csv"))
    p11 = pd.read_csv(os.path.join(ROOT, "playing_eleven.csv"))
    bbb = pd.read_csv(os.path.join(ROOT, "ball_by_ball.csv"), low_memory=False)
    ctpm = pd.read_csv(os.path.join(ROOT, "competition_team_player_mapping.csv"))
    comps = pd.read_csv(os.path.join(ROOT, "competitions.csv"))

    # Inspect top50 CSVs bug
    top50_bat = pd.read_csv(os.path.join(ROOT, "pressure_output", "top50_batters_pressure.csv"))
    top50_bowl = pd.read_csv(os.path.join(ROOT, "pressure_output", "top50_bowlers_pressure.csv"))
    log(f"  top50_batters_pressure rows={len(top50_bat)}, cols={list(top50_bat.columns)}")
    log(f"  top50_bowlers_pressure rows={len(top50_bowl)}, cols={list(top50_bowl.columns)}")
    same_players = list(top50_bat["player_name"]) == list(top50_bowl["player_name"])
    same_cppi = np.allclose(top50_bat["cppi"], top50_bowl["cppi"])
    log(f"  CRITICAL BUG CHECK: top50_batters == top50_bowlers player_name order: {same_players}, identical cppi: {same_cppi}")
    log(f"  top50_batters bbb_bonus non-zero count: {(top50_bat['bbb_bonus'] != 0).sum()} / {len(top50_bat)}")
    log(f"  top50_batters contains bowlers like Hazlewood/Starc/Rashid/Duffy: {[x for x in top50_bat['player_name'] if any(b in x for b in ['Hazlewood','Starc','Rashid','Duffy','Arshdeep','Bumrah'])]}")

    # Load players_db.json & audit_match_pressure_scores.csv
    with open(os.path.join(ROOT, "players_db.json"), "r", encoding="utf-8") as f:
        pdb = json.load(f)
    audit_mps = pd.read_csv(os.path.join(ROOT, "pressure_output", "audit_match_pressure_scores.csv"))
    sub_bat = pd.read_csv(os.path.join(ROOT, "pressure_output", "SUBMISSION_top10_batters.csv"))
    sub_bowl = pd.read_csv(os.path.join(ROOT, "pressure_output", "SUBMISSION_top10_bowlers.csv"))

    # Reconstruct rr_pressure_analyst.py MLI exact formula on matches.csv
    def calc_mli_analyst(df_m):
        res = df_m["result"].astype(str).str.lower()
        stage = df_m["stage"].astype(str).str.lower()
        ko = df_m["knock_out"].fillna(0).astype(int)
        stage_pts = np.where(stage.str.contains("final") & ~stage.str.contains("semi|quarter"), 40,
                    np.where(stage.str.contains("semi|qualifier|eliminator"), 35,
                    np.where(stage.str.contains("super"), 20, 10)))
        close_pts = np.zeros(len(df_m), dtype=int)
        for idx, r in enumerate(res):
            if "super over" in r or "tied" in r:
                close_pts[idx] = 40
            elif "run" in r:
                m = re.search(r"by (\d+) run", r)
                if m:
                    runs = int(m.group(1))
                    close_pts[idx] = 40 if runs <= 5 else (30 if runs <= 15 else (18 if runs <= 30 else 5))
            elif "wicket" in r or "wkt" in r:
                m = re.search(r"by (\d+) w", r)
                if m:
                    wkts = int(m.group(1))
                    close_pts[idx] = 40 if wkts <= 1 else (35 if wkts <= 2 else (25 if wkts <= 3 else (15 if wkts <= 5 else 5)))
        ko_pts = np.where((ko == 1) | stage.str.contains("final|semi|qualifier|eliminator"), 20, 0)
        score = stage_pts + close_pts + ko_pts
        return pd.Series(score, index=df_m.index), pd.Series(score >= 55, index=df_m.index)

    matches["calc_mli"], matches["calc_hp"] = calc_mli_analyst(matches)
    matches["calc_ko"] = (matches["knock_out"] == 1) | matches["stage"].str.lower().str.contains("final|semi|qualifier|eliminator", na=False)
    merged_mps = matches[["match_id", "calc_mli", "calc_hp"]].merge(audit_mps[["match_id", "pressure_score", "is_high_pressure"]], on="match_id")
    log(f"  audit_match_pressure_scores matches calc_mli==pressure_score count: {(merged_mps['calc_mli'] == merged_mps['pressure_score']).sum()} / {len(merged_mps)}")
    if (merged_mps['calc_mli'] != merged_mps['pressure_score']).any():
        diff_m = merged_mps[merged_mps['calc_mli'] != merged_mps['pressure_score']]
        log(f"  Differences vs audit_match_pressure_scores: {len(diff_m)}")
        log(diff_m.head(10).merge(matches[["match_id","stage","result"]], on="match_id").to_string())

    # Compare per-player stats in players_db.json + superstars_audit against ACTUAL matches + p11 (raw vs deduped) + bbb!
    p11_dedup = p11.drop_duplicates(["match_id", "player_id"]).copy()
    p11_m = p11_dedup.merge(matches[["match_id", "win_team_id", "man_of_the_match", "calc_hp", "calc_ko"]], on="match_id", how="left")
    p11_m["is_win"] = (p11_m["team_id"] == p11_m["win_team_id"])
    p11_m["is_mom"] = (p11_m["player_id"] == p11_m["man_of_the_match"])
    p11_m_valid = p11_m[p11_m["win_team_id"].notna()]  # excluding NR/abandoned/tied

    # Also check how many matches each player plays under audit_match_pressure_scores.is_high_pressure AND format/year subsets!
    p11_amp = p11_dedup.merge(matches[["match_id", "comp_id", "match_date", "win_team_id", "man_of_the_match", "calc_ko"]], on="match_id").merge(
        audit_mps[["match_id", "pressure_score", "is_high_pressure"]], on="match_id"
    ).merge(comps[["comp_id", "comp_name", "match_format", "season"]], on="comp_id")
    p11_amp["is_win"] = p11_amp["team_id"] == p11_amp["win_team_id"]
    p11_amp["is_mom"] = p11_amp["player_id"] == p11_amp["man_of_the_match"]

    # Also build raw p11 (with duplicates, and NaN counted as loss like rr_pressure_analyst)
    p11_raw_m = p11.merge(matches[["match_id", "win_team_id", "man_of_the_match", "calc_hp", "calc_ko"]], on="match_id", how="left")
    p11_raw_m["is_win"] = (p11_raw_m["team_id"] == p11_raw_m["win_team_id"])
    p11_raw_m["is_mom"] = (p11_raw_m["player_id"] == p11_raw_m["man_of_the_match"])

    # Also compute true career ball-by-ball stats for each player by ID (matched cleanly via player_id from ctpm!)
    pid_lookup = ctpm.drop_duplicates("player_id").set_index("player_name")["player_id"].to_dict()
    # Handle duplicate names safely:
    pid_map_all = ctpm[["player_id", "player_name"]].drop_duplicates()

    # Load superstars_audit & specs from fix_dashboard_and_wagon.py
    fix_path = os.path.join(ROOT, "fix_dashboard_and_wagon.py")
    bat_wagon = extract_ast_dict_or_list(fix_path, "BATTER_WAGON_SPECS")
    bowl_pitch = extract_ast_dict_or_list(fix_path, "BOWLER_PITCH_SPECS")
    superstars = extract_ast_dict_or_list(fix_path, "superstars_audit")
    footer_notes = extract_ast_dict_or_list(fix_path, "PLAYER_FOOTER_NOTES")

    # Compute true ball-by-ball phase stats per player_id
    bbb_clean = bbb[bbb["innings"].isin([1, 2])].copy()
    bbb_clean["is_legal_bat"] = ~bbb_clean["extras_type"].isin(["wide"])  # bat balls faced exclude wides
    bbb_clean["is_legal_bowl"] = ~bbb_clean["extras_type"].isin(["wide", "Overstep", "other"])
    ext = bbb_clean["extras_type"].fillna("")
    # Standard bowler runs conceded lower-bound observable: runs + (1 if wide/Overstep/other else 0) + extras_2_runs where NB
    bbb_clean["bowl_runs_min"] = bbb_clean["runs"] + np.where(ext.isin(["wide", "Overstep", "other"]), 1, 0) + np.where(ext.isin(["Overstep", "other"]), bbb_clean["extras_2_runs"], 0)
    bbb_clean["phase"] = np.where(bbb_clean["overid"] <= 6, "pp", np.where(bbb_clean["overid"] <= 15, "mid", "death"))

    log("\n[3] AUDIT OF ALL 25 DASHBOARD PLAYERS: players_db.json + superstars_audit VS OFFICIAL CSVs")
    all_dash_players = pdb + (superstars if superstars else [])
    player_audit_rows = []
    for p in all_dash_players:
        name = p["name"]
        # Find best matching player_id in ctpm
        cand = pid_map_all[pid_map_all["player_name"].str.lower() == name.lower()]
        if len(cand) == 0:
            # try substring
            cand = pid_map_all[pid_map_all["player_name"].str.lower().str.contains(name.lower().split()[-1])]
        pid = int(cand.iloc[0]["player_id"]) if len(cand) == 1 else -1
        # if duplicate match (none expected for these 25 except if any), inspect
        if len(cand) > 1:
            # pick one with most bbb deliveries
            counts = [(int(r["player_id"]), int(((bbb["striker_id"] == r["player_id"]) | (bbb["bowler_id"] == r["player_id"])).sum())) for _, r in cand.iterrows()]
            pid = max(counts, key=lambda x: x[1])[0]

        pm_dedup = p11_m[p11_m["player_id"] == pid]
        pm_raw = p11_raw_m[p11_raw_m["player_id"] == pid]
        pm_valid = p11_m_valid[p11_m_valid["player_id"] == pid]

        tot_dedup = len(pm_dedup)
        hp_dedup = int(pm_dedup["calc_hp"].sum())
        hp_wr_dedup = round(100.0 * pm_dedup.loc[pm_dedup["calc_hp"], "is_win"].mean(), 1) if hp_dedup > 0 else np.nan
        base_wr_dedup = round(100.0 * pm_dedup["is_win"].mean(), 1) if tot_dedup > 0 else np.nan
        base_wr_valid = round(100.0 * pm_valid["is_win"].mean(), 1) if len(pm_valid) > 0 else np.nan
        ko_m_dedup = int(pm_dedup["calc_ko"].sum())
        ko_wr_dedup = round(100.0 * pm_dedup.loc[pm_dedup["calc_ko"], "is_win"].mean(), 1) if ko_m_dedup > 0 else np.nan
        mom_hp_dedup = int((pm_dedup["calc_hp"] & pm_dedup["is_mom"]).sum())

        # Reproduce apply_calibrated_rankings formula directly on DB fields
        db_tot = p.get("total_m", np.nan)
        db_hp = p.get("hp_m", np.nan)
        db_hp_wr = p.get("hp_wr", np.nan)
        db_base_wr = p.get("base_wr", np.nan)
        db_lift = p.get("lift", np.nan)
        db_ko_wr = p.get("ko_wr", np.nan)
        db_mom = p.get("mom_hp", np.nan)
        db_bayes = p.get("bayes_hp_wr", np.nan)
        db_cppi = p.get("cppi", np.nan)

        # Check formula 1 (apply_calibrated_rankings.py) using DB numbers
        calc_bayes_5 = round((db_hp * db_hp_wr / 100.0 + 5.0 * (db_base_wr / 100.0)) / (db_hp + 5.0) * 100.0, 1) if db_hp else np.nan
        lift_comp = max(0.0, min(100.0, 50.0 + db_lift * 1.8))
        mom_comp = min(100.0, (db_mom / db_hp) * 100.0 * 3.0) if db_hp else 0.0
        cred = 1.0 / (1.0 + np.exp(-0.25 * (db_hp - 8)))
        calc_cppi_cal = round((0.35 * db_bayes + 0.25 * lift_comp + 0.20 * db_ko_wr + 0.10 * mom_comp + 0.10 * db_base_wr) * (0.85 + 0.15 * cred), 2)

        # True BBB batting & bowling stats
        sb = bbb_clean[bbb_clean["striker_id"] == pid]
        sb_leg = sb[sb["is_legal_bat"]]
        bat_bf = len(sb_leg)
        bat_runs = int(sb["runs"].sum())
        bat_sr = round(100.0 * bat_runs / bat_bf, 1) if bat_bf > 0 else np.nan
        phase_sr = {}
        for ph in ["pp", "mid", "death"]:
            s_ph = sb[sb["phase"] == ph]
            bf_ph = int(s_ph["is_legal_bat"].sum())
            phase_sr[ph] = round(100.0 * s_ph["runs"].sum() / bf_ph, 1) if bf_ph > 0 else np.nan

        bw = bbb_clean[bbb_clean["bowler_id"] == pid]
        bw_balls = int(bw["is_legal_bowl"].sum())
        bw_runs = int(bw["bowl_runs_min"].sum())
        bw_econ = round(6.0 * bw_runs / bw_balls, 2) if bw_balls > 0 else np.nan
        phase_econ = {}
        for ph in ["pp", "mid", "death"]:
            b_ph = bw[bw["phase"] == ph]
            bl_ph = int(b_ph["is_legal_bowl"].sum())
            phase_econ[ph] = round(6.0 * b_ph["bowl_runs_min"].sum() / bl_ph, 2) if bl_ph > 0 else np.nan

        pm_amp = p11_amp[p11_amp["player_id"] == pid]
        amp_hp = int(pm_amp["is_high_pressure"].sum())
        amp_hp_wr = round(100.0 * pm_amp.loc[pm_amp["is_high_pressure"], "is_win"].mean(), 1) if amp_hp > 0 else np.nan
        amp_ipl_tot = int((pm_amp["match_format"] == "T20").sum())
        amp_t20i_tot = int((pm_amp["match_format"] == "T20I").sum())

        log(f"  {p.get('category','AUDIT'):<7} #{p.get('rank','-'):<3} {name:<20} | pid={pid:<5} | DB(tot={db_tot},hp={db_hp},hpWR={db_hp_wr},bWR={db_base_wr},koWR={db_ko_wr},mom={db_mom},bayes={db_bayes},CPPI={db_cppi}) | CSV(tot={tot_dedup}[IPL:{amp_ipl_tot},T20I:{amp_t20i_tot}],raw={len(pm_raw)},hp_amp={amp_hp}/WR={amp_hp_wr},hp_ana={hp_dedup}/WR={hp_wr_dedup},bWR={base_wr_dedup},koWR={ko_wr_dedup},mom_ana={mom_hp_dedup}) | calcBayes5={calc_bayes_5} | calcCalCPPI={calc_cppi_cal}")
        log(f"      BBB actuals -> BAT(BF={bat_bf},R={bat_runs},SR={bat_sr}, PP={phase_sr['pp']},MID={phase_sr['mid']},DEATH={phase_sr['death']}) | BOWL(Balls={bw_balls},Econ={bw_econ}, PP={phase_econ['pp']},MID={phase_econ['mid']},DEATH={phase_econ['death']})")

        player_audit_rows.append({
            "category": p.get("category", "SUPERSTAR_AUDIT"),
            "rank": p.get("rank", np.nan),
            "name": name,
            "pid": pid,
            "db_total_m": db_tot,
            "csv_dedup_total_m": tot_dedup,
            "csv_raw_total_m": len(pm_raw),
            "db_hp_m": db_hp,
            "csv_hp_m": hp_dedup,
            "db_hp_wr": db_hp_wr,
            "csv_hp_wr": hp_wr_dedup,
            "db_base_wr": db_base_wr,
            "csv_base_wr_incl_nr": base_wr_dedup,
            "csv_base_wr_excl_nr": base_wr_valid,
            "db_ko_wr": db_ko_wr,
            "csv_ko_wr": ko_wr_dedup,
            "db_mom_hp": db_mom,
            "csv_mom_hp": mom_hp_dedup,
            "db_bayes_hp_wr": db_bayes,
            "recalc_bayes_m5": calc_bayes_5,
            "db_cppi": db_cppi,
            "recalc_cppi_calibrated": calc_cppi_cal,
            "bat_bf": bat_bf,
            "bat_runs": bat_runs,
            "bat_sr": bat_sr,
            "bat_pp_sr": phase_sr["pp"],
            "bat_mid_sr": phase_sr["mid"],
            "bat_death_sr": phase_sr["death"],
            "bowl_legal_balls": bw_balls,
            "bowl_econ_min": bw_econ,
            "bowl_pp_econ": phase_econ["pp"],
            "bowl_mid_econ": phase_econ["mid"],
            "bowl_death_econ": phase_econ["death"],
        })

    pd.DataFrame(player_audit_rows).to_csv(os.path.join(OUT_DIR, "REPO_PLAYER_DISCREPANCIES.csv"), index=False)

    # 4. Audit Hardcoded BATTER_WAGON_SPECS, BOWLER_PITCH_SPECS, and PLAYER_FOOTER_NOTES vs DB & BBB
    log("\n[4] HARDCODED WAGON WHEEL & PITCH MAP SPECS AUDIT")
    sector_keys = ["long_off", "long_on", "mid_wicket", "square_leg", "fine_leg", "third_man", "point", "cover"]
    for k, w in bat_wagon.items():
        s = sum(w[sk] for sk in sector_keys)
        # Find matching player in player_audit_rows
        row = next((r for r in player_audit_rows if r["name"].lower().replace(" ", "_") == k), None)
        if row:
            log(f"  BATTER_WAGON {k:<18}: sector_sum={s}% (!=100 if wrong) | FakePhaseSR=({w['pp_sr']}, {w['mid_sr']}, {w['death_sr']}) vs TRUE BBB PhaseSR=({row['bat_pp_sr']}, {row['bat_mid_sr']}, {row['bat_death_sr']})")
        else:
            log(f"  BATTER_WAGON {k:<18}: sector_sum={s}%")
    # Missing batters falling back to Rajat Patidar
    bat_dash_keys = [p["key"] for p in all_dash_players if "BAT" in str(p.get("category", "")) or p["key"] in ("heinrich_klaasen", "rohit_sharma")]
    missing_wagon = [k for k in bat_dash_keys if k not in bat_wagon]
    log(f"  Batters MISSING from BATTER_WAGON_SPECS (silently fall back to rajat_patidar!): {missing_wagon}")

    for k, b in bowl_pitch.items():
        lsum = sum(x[1] for x in b["lengths"])
        row = next((r for r in player_audit_rows if r["name"].lower().replace(" ", "_") == k), None)
        if row:
            log(f"  BOWLER_PITCH {k:<20}: len_sum={lsum}% | FakePhaseEcon=({b['pp_econ']}, {b['mid_econ']}, {b['death_econ']}) vs TRUE BBB PhaseEcon=({row['bowl_pp_econ']}, {row['bowl_mid_econ']}, {row['bowl_death_econ']})")
    bowl_dash_keys = [p["key"] for p in all_dash_players if "BOWL" in str(p.get("category", "")) or p["key"] in ("jasprit_bumrah", "mohammed_siraj", "rashid_khan")]
    missing_pitch = [k for k in bowl_dash_keys if k not in bowl_pitch]
    log(f"  Bowlers MISSING from BOWLER_PITCH_SPECS (silently fall back to mitchell_starc!): {missing_pitch}")

    # Check narrative vs DB contradictions
    log("\n[5] NARRATIVE CONTRADICTIONS IN players_db.json & PLAYER_FOOTER_NOTES")
    for p in pdb:
        k = p["key"]
        why = p.get("why_chose", "") + " | " + p.get("why_not_others", "") + " | " + p.get("auction_eval", "")
        fn = (footer_notes.get(k, {}).get("methodology", "") + " " + footer_notes.get(k, {}).get("thought_process", "")) if footer_notes else ""
        # Check for wrong CPPI/rank/WR/match counts mentioned in text
        m_rank = re.findall(r"#(\d+)", p.get("why_not_others", ""))
        m_wr = re.findall(r"(\d+\.\d+)%", why)
        m_games = re.findall(r"in (\d+) (?:pressure|HP|matches|fixtures)", why, flags=re.I)
        log(f"  {p['category']} #{p['rank']} {p['name']}: DB=(tot={p['total_m']},hp={p['hp_m']},hpWR={p['hp_wr']},baseWR={p['base_wr']},lift={p['lift']},mom={p['mom_hp']},cppi={p['cppi']})")
        log(f"     DB text snippet -> why_chose='{p['why_chose'][:120]}...' | why_not='#ranks:{m_rank}'")
        if fn:
            log(f"     Footer note     -> '{fn[:140]}...'")

    # 6. Compare SUBMISSION CSVs vs players_db.json & optimize_rankings.py
    log("\n[6] SUBMISSION CSVs VS players_db.json & SCRIPT REPRODUCTION")
    for label, sub_df, cat in [("BATTERS", sub_bat, "Batter"), ("BOWLERS", sub_bowl, "Bowler")]:
        db_sub = sorted([x for x in pdb if x.get("category", "").lower() == cat.lower()], key=lambda x: x["rank"])
        name_col = "Player_Name" if "Player_Name" in sub_df.columns else "player_name"
        cppi_col = "CPPI_Score" if "CPPI_Score" in sub_df.columns else "CPPI"
        names_sub = list(sub_df[name_col])
        names_db = [x["name"] for x in db_sub]
        cppis_sub = [round(float(x), 2) for x in sub_df[cppi_col]]
        cppis_db = [round(float(x["cppi"]), 2) for x in db_sub]
        log(f"  {label}: CSV names == DB names: {names_sub == names_db} | CPPI match: {cppis_sub == cppis_db}")
        if cppis_sub != cppis_db or names_sub != names_db:
            log(f"    CSV: {list(zip(names_sub, cppis_sub))}")
            log(f"    DB : {list(zip(names_db, cppis_db))}")

    # Check how audit_match_pressure_scores compares to >=30 threshold and Margin Matrix
    log(f"  audit_match_pressure_scores is_high_pressure True count: {int(audit_mps['is_high_pressure'].sum())} / {len(audit_mps)} (min score where True={audit_mps.loc[audit_mps['is_high_pressure'],'pressure_score'].min()}, max where False={audit_mps.loc[~audit_mps['is_high_pressure'],'pressure_score'].max()})")
    # Check matches count if <= 2025 season (why DB total_m is smaller than 883-match CSV total!)
    m_comp_check = matches[["match_id", "comp_id"]].merge(comps[["comp_id", "season"]], on="comp_id")
    m_le_2025 = set(m_comp_check[~m_comp_check["season"].isin(["2026"])]["match_id"])
    for nm, pid in [("Shivam Dube", 4755), ("Rinku Singh", 4708), ("Rajat Patidar", 5039), ("Jacob Duffy", 22920), ("Arshdeep Singh", 6464)]:
        tot_le25 = int(((p11_dedup["player_id"] == pid) & (p11_dedup["match_id"].isin(m_le_2025))).sum())
        log(f"  Season<=2025 match count check: {nm:<18} DB={next(x['total_m'] for x in pdb if x['name']==nm)} | All={int((p11_dedup['player_id']==pid).sum())} | Pre-2026={tot_le25}")

    # Reproduce optimize_rankings.py / rr_pressure_analyst formula directly on audit_match_pressure_scores + deduped p11
    grp_rows = []
    for pid, g in p11_amp.groupby("player_id"):
        tot = len(g)
        hp_g = g[g["is_high_pressure"]]
        hp_n = len(hp_g)
        if hp_n < 8 or tot < 15:
            continue
        b_wr = 100.0 * g["is_win"].mean()
        h_wr = 100.0 * hp_g["is_win"].mean()
        lift = h_wr - b_wr
        ko_g = g[g["calc_ko"]]
        ko_wr = 100.0 * ko_g["is_win"].mean() if len(ko_g) > 0 else b_wr
        mom_hp = int((g["is_high_pressure"] & g["is_mom"]).sum())
        bayes_5 = (hp_g["is_win"].sum() + 5.0 * (b_wr / 100.0)) / (hp_n + 5.0) * 100.0
        lift_comp = max(0.0, min(100.0, 50.0 + lift * 1.8))
        mom_comp = min(100.0, (mom_hp / hp_n) * 100.0 * 3.0)
        cred = 1.0 / (1.0 + np.exp(-0.25 * (hp_n - 8)))
        cppi_cal = (0.35 * bayes_5 + 0.25 * lift_comp + 0.20 * ko_wr + 0.10 * mom_comp + 0.10 * b_wr) * (0.85 + 0.15 * cred)
        pname = ctpm.loc[ctpm["player_id"] == pid, "player_name"].iloc[0] if (ctpm["player_id"] == pid).any() else str(pid)
        grp_rows.append({"pid": pid, "name": pname, "tot": tot, "hp": hp_n, "hp_wr": round(h_wr,1), "b_wr": round(b_wr,1), "lift": round(lift,1), "ko_wr": round(ko_wr,1), "mom_hp": mom_hp, "cppi_cal": round(cppi_cal,2)})
    rep_df = pd.DataFrame(grp_rows).sort_values("cppi_cal", ascending=False)
    log(f"  Reproduced calibrated match-level CPPI across ALL {len(rep_df)} qualified players (using audit_match_pressure_scores on 883 matches, no role/country filter) Top 15:")
    log(rep_df.head(15).to_string(index=False))

    # 7. Audit PowerPoint PPTX content
    log("\n[7] POWERPOINT DECK AUDIT (RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx)")
    pptx_path = os.path.join(ROOT, "pressure_output", "RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx")
    if os.path.exists(pptx_path):
        prs = Presentation(pptx_path)
        log(f"  Slides count: {len(prs.slides)}")
        for idx, slide in enumerate(prs.slides, 1):
            texts = []
            tables_info = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    t = " ".join(p.text.strip() for p in shape.text_frame.paragraphs if p.text.strip())
                    if t:
                        texts.append(t)
                if shape.has_table:
                    tbl = shape.table
                    hdr = [c.text.strip().replace("\n", " ") for c in tbl.rows[0].cells]
                    r1 = [c.text.strip().replace("\n", " ") for c in tbl.rows[1].cells] if len(tbl.rows) > 1 else []
                    tables_info.append(f"Table({len(tbl.rows)}x{len(tbl.columns)} hdr={hdr[:5]} r1={r1[:5]})")
            title = texts[0][:100] if texts else "(no title)"
            log(f"  Slide {idx:2d}: {title}")
            for ti in tables_info:
                log(f"      {ti}")
            full_t = " | ".join(texts)
            if any(k in full_t for k in ["Conway", "Patidar", "Starc", "Dube", "Duffy", "Cr", "Lift", "Atal", "Delhi"]):
                log(f"      Snippet: {full_t[:220]}")

    # 8. Audit PDF scripts & Markdown report consistency
    log("\n[8] PDF SCRIPTS & REPORT INCONSISTENCY SCAN")
    for fn in ["build_submission_pdf.py", "build_clean_submission_pptx.py", "pressure_output/methodology_report.md"]:
        fp = os.path.join(ROOT, fn)
        with open(fp, "r", encoding="utf-8") as f:
            txt = f.read()
        has_dube_bid = re.findall(r"(Shivam Dube[^.\n]{0,120}(?:Cr|Bid|Delhi))", txt, flags=re.I)
        has_atal = re.findall(r"(Sediqullah Atal[^.\n]{0,120})", txt, flags=re.I)
        has_rinku_bid = re.findall(r"(Rinku Singh[^.\n]{0,120}Cr)", txt, flags=re.I)
        log(f"  File: {fn} | size={len(txt):,} chars")
        for m in (has_dube_bid + has_atal + has_rinku_bid)[:6]:
            log(f"    -> {m.strip()[:150]}")

    # 9. Audit Website DOM & 25 Player Pages
    log("\n[9] WEBSITE & PLAYER HTML PAGES AUDIT")
    idx_path = os.path.join(ROOT, "index.html")
    with open(idx_path, "r", encoding="utf-8") as f:
        idx_html = f.read()
    log(f"  index.html size: {len(idx_html):,} chars")
    nav_btns = re.findall(r"onclick=\"showSection\('([^']+)'[^>]*>([^<]+)<", idx_html)
    log(f"  Navigation tabs ({len(nav_btns)}): {nav_btns}")
    slicers = re.findall(r"<option value=\"([^\"]+)\"[^>]*>([^<]+)</option>", idx_html)
    log(f"  Slicer dropdown options: {slicers}")
    b64_imgs = re.findall(r"data:image/([a-zA-Z0-9]+);base64,", idx_html)
    log(f"  Embedded base64 images in index.html: {len(b64_imgs)} ({b64_imgs})")
    hrefs = re.findall(r'href="([^"]+)"', idx_html)
    player_hrefs = [h for h in hrefs if "players/" in h]
    other_hrefs = [h for h in hrefs if "players/" not in h]
    log(f"  Player links in index.html: {len(player_hrefs)} unique={len(set(player_hrefs))}")
    log(f"  Other hrefs in index.html: {other_hrefs[:15]}")
    ext_scripts = re.findall(r'<script[^>]+src="([^"]+)"', idx_html)
    log(f"  External scripts: {ext_scripts}")
    margin_vals = re.findall(r"(\d+\.\d+%)\s*</td>", idx_html)
    log(f"  Percentage table cells in index.html (count={len(margin_vals)}), sample: {margin_vals[:15]}")

    # Verify all player HTML links resolve and inspect a sample page
    players_dir = os.path.join(ROOT, "players")
    existing_pages = set(os.listdir(players_dir))
    linked_pages = set(os.path.basename(h) for h in player_hrefs)
    log(f"  Player pages on disk: {len(existing_pages)} | Linked from index.html: {len(linked_pages)} | Missing targets: {linked_pages - existing_pages} | Unlinked pages: {existing_pages - linked_pages}")
    sample_page = os.path.join(players_dir, "shivam_dube.html")
    with open(sample_page, "r", encoding="utf-8") as f:
        sp_html = f.read()
    has_svg = sp_html.count("<svg")
    back_links = re.findall(r'href="([^"]*index\.html[^"]*)"', sp_html)
    log(f"  Sample player page (shivam_dube.html): size={len(sp_html):,} chars, SVGs={has_svg}, back_links={back_links}")

    out_txt = os.path.join(OUT_DIR, "02_repo_and_website_audit.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log(f"\nSaved: {out_txt}")
    log(f"Saved: {os.path.join(OUT_DIR, 'REPO_PLAYER_DISCREPANCIES.csv')}")


if __name__ == "__main__":
    main()
