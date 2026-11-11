#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
RAJASTHAN ROYALS — DATA PACK PRE-FLIGHT INSPECTOR
SupeRR Selector Season 2 | Data Ingestion Diagnostic Tool
==============================================================================

PURPOSE:
    Run this tool immediately when you receive tomorrow's proprietary data pack.
    It will:
    1. Inspect all files (.csv, .xlsx, .xls) in your folder.
    2. Check sheet names and headers.
    3. Auto-match columns against the 50+ aliases used by rr_scout_pipeline.py.
    4. Detect missing columns (Age, DOB, Capped status, Phase splits).
    5. Output a diagnostic health check so you can run the pipeline with 100% confidence.

USAGE:
    python data_inspector.py --data ./pack
    (or simply: python data_inspector.py)
==============================================================================
"""

import sys
import os
import re
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

# Canonical aliases from rr_scout_pipeline
ALIASES = {
    "player": ["player", "player_name", "name", "batter", "batsman", "bowler", "striker", "cricketer"],
    "team": ["team", "state", "state_team", "franchise", "side", "squad"],
    "season": ["season", "year", "edition", "season_year"],
    "format": ["format", "competition", "tournament", "comp", "league"],
    "matches": ["matches", "mat", "m", "games", "matches_played", "mp"],
    "age": ["age", "age_years"],
    "dob": ["dob", "date_of_birth", "birthdate", "born", "birth_date"],
    "capped": ["capped", "caps", "india_caps", "intl_caps", "international_caps", "capped_status"],
    "runs": ["runs", "runs_scored", "r", "bat_runs", "batting_runs", "total_runs"],
    "bf": ["bf", "balls_faced", "balls", "b", "bat_balls", "balls_played"],
    "sr": ["sr", "strike_rate", "strike rate", "s/r", "strikerate"],
    "overs": ["overs", "ov", "o", "overs_bowled"],
    "rc": ["runs_conceded", "rc", "runs_given", "runs", "r", "runs_against", "conceded"],
    "wkts": ["wkts", "wickets", "w", "wk"],
    "econ": ["econ", "economy", "er", "economy_rate"],
    "pp_runs": ["pp_runs", "powerplay_runs", "runs_pp", "runs_1_6"],
    "death_runs": ["death_runs", "runs_16_20", "runs_death"],
    "pp_overs": ["pp_overs", "powerplay_overs"],
    "death_overs": ["death_overs", "overs_death", "death_ov"],
}

def norm_col(c):
    return re.sub(r"[^a-z0-9]+", "_", str(c).strip().lower()).strip("_")

def inspect_folder(data_dir: Path):
    print("=" * 75)
    print("🏏 RAJASTHAN ROYALS WAR ROOM — DATA PACK PRE-FLIGHT INSPECTION")
    print(f"📁 Target Folder: {data_dir.resolve()}")
    print("=" * 75)

    if not data_dir.exists():
        print(f"\n❌ ERROR: Folder '{data_dir}' does not exist!")
        print(f"👉 Create the folder: mkdir '{data_dir}' and place your data pack inside.\n")
        return

    files = list(data_dir.rglob("*.csv")) + list(data_dir.rglob("*.xlsx")) + list(data_dir.rglob("*.xls"))
    if not files:
        print(f"\n⚠️ WARNING: No CSV or Excel files found in '{data_dir}'.")
        print("👉 Drop tomorrow's data pack files into this folder and re-run.\n")
        return

    print(f"\n✅ Found {len(files)} data file(s):\n")

    summary = []
    has_age_or_dob = False
    has_capped = False
    has_phase_data = False
    total_rows = 0

    for p in sorted(files):
        print(f"📄 File: {p.name}")
        sheets = {}
        if p.suffix.lower() == ".csv":
            try:
                for enc in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        df = pd.read_csv(p, encoding=enc, nrows=5)
                        sheets["Sheet1"] = (df, len(pd.read_csv(p, encoding=enc)))
                        break
                    except UnicodeDecodeError:
                        continue
            except Exception as e:
                print(f"   ❌ Read error: {e}")
                continue
        else:
            try:
                xl = pd.ExcelFile(p)
                for sh in xl.sheet_names:
                    df = xl.parse(sh, nrows=5)
                    full_df = xl.parse(sh)
                    sheets[sh] = (df, len(full_df))
            except Exception as e:
                print(f"   ❌ Read error: {e}")
                continue

        for sh_name, (df_sample, row_count) in sheets.items():
            total_rows += row_count
            cols = [norm_col(c) for c in df_sample.columns]
            matched = {}
            for canon, variants in ALIASES.items():
                for c in cols:
                    if c in variants:
                        matched[canon] = c
                        break

            # Flags
            if "age" in matched or "dob" in matched:
                has_age_or_dob = True
            if "capped" in matched:
                has_capped = True
            if "pp_runs" in matched or "death_runs" in matched or "pp_overs" in matched or "death_overs" in matched:
                has_phase_data = True

            print(f"   📊 [{sh_name}] ({row_count} rows, {len(cols)} columns)")
            print(f"      Matched Core: Player={matched.get('player','❌ MISSING')}, Team={matched.get('team','⚠️ none')}, Season={matched.get('season','⚠️ none')}")
            print(f"      Matched Stats: Runs={matched.get('runs','-')}, BF={matched.get('bf','-')}, Wkts={matched.get('wkts','-')}, Overs={matched.get('overs','-')}")
            print(f"      Special: Age/DOB={matched.get('age') or matched.get('dob') or '❌ Not found'}, Capped={matched.get('capped','❌ Not found')}")
            print()

    print("=" * 75)
    print("🔍 DATA PACK HEALTH DIAGNOSTIC REPORT")
    print("=" * 75)
    print(f"Total Records Ingested : {total_rows} rows")
    print(f"Age / DOB Coverage     : {'✅ DETECTED (Ready for Age Multiplier)' if has_age_or_dob else '⚠️ MISSING (Script will flag players without age)'}")
    print(f"Capped Status Coverage : {'✅ DETECTED (Ready for Uncapped Filter)' if has_capped else '⚠️ MISSING (Use --unknown-capped flag if missing)'}")
    print(f"Phase Split Coverage   : {'✅ DETECTED (Full True SR & FAI Mode)' if has_phase_data else 'ℹ️ AGGREGATE MODE (Script will use proxy features automatically)'}")
    
    print("\n🚀 READY TO RUN COMMAND:")
    print("-----------------------------------------------------------------------")
    print(f"python rr_scout_pipeline.py --data \"{data_dir}\" --out ./out")
    print("-----------------------------------------------------------------------")
    print("💡 If capped status column is absent in the data, add: --unknown-capped flag")
    print("💡 To use discrete age bands (17-19: 1.0, 20-21: 0.85): add --age-mode step")
    print("=======================================================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pre-flight data pack inspector for RR War Room")
    parser.add_argument("--data", type=Path, default=Path("./pack"), help="Path to data pack directory")
    args = parser.parse_args()
    inspect_folder(args.data)
