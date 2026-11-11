#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RR WAR ROOM - UNCAPPED YOUTH SCOUTING PIPELINE   (SupeRR Selector, Season 2)
=============================================================================

Goal : rank the youngest, uncapped, domestic outliers in a proprietary data pack
       (SMAT = T20, VHT = List-A, Ranji = First-Class) and output the Top 10.

Run  :  pip install pandas numpy openpyxl            (matplotlib optional, for charts)
        python rr_scout_pipeline.py --demo                       # dry-run on synthetic data
        python rr_scout_pipeline.py --data ./pack --out ./out    # real run

Index:  TDSI = Impact(0-100) x AgeMultiplier          (Three-Dimensional Selection Index)
        Impact blends, per discipline (bat / bowl):
          1. FORMAT   : T20 60% | List-A 30% | First-Class 10%
          2. RECENCY  : 2026-27 = 1.0 | 2025-26 = 0.6 | older = 0.3  (keyed on season START year)
          3. RELIABILITY (sample size) : n / (n + k)   -> thin samples are pulled toward the median
        AGE multiplier : exp(-0.17 * (age - 19.5)) beyond 19.5  (matches 17-19 = 1.0, 20-21 ~ 0.85,
                         22-23 ~ 0.60 at the band mid-points).  A step table is available too.

Input conventions (anything unrecognised is ignored; see ALIASES for accepted header names)
  * Name files/sheets with 'bat' or 'bowl' (e.g. smat_2025-26_batting.csv). Combined sheets also work.
  * Format and season are read from a 'Format'/'Season' column or from the file name
    ('smat','vht','ranji' + '2025-26').
  * Minimum columns   batting : Player, Matches, Innings, Runs, BF, NO, 4s, 6s
                      bowling : Player, Matches, Overs (4.3 = 4 overs 3 balls), Runs_Conceded, Wkts
  * Optional (unlock the advanced features; the script degrades gracefully without them)
      batting : PP_Runs/PP_BF, Mid_Runs/Mid_BF, Death_Runs/Death_BF, Runs_vs_Spin/BF_vs_Spin, Dots_Faced
      bowling : Dots, PP_Overs/PP_Runs_Conceded/PP_Wkts, Mid_*, Death_*
      players : Age or DOB, Capped (Y/N or caps), Bowl_Type, Availability, IPL_Matches
                (put these in any sheet, or in a separate players_master.csv)
"""
from __future__ import annotations

import argparse
import difflib
import math
import re
import sys
import unicodedata
import warnings
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROLES = ["Powerplay Enforcer", "Spin-Hitting Finisher", "Death Bowler", "Impact/Mystery Spinner"]
FORMATS = ["T20", "LA", "FC"]

# Verified RR 2026 squad additions + core (re-check against the Nov-17 retention list before submitting)
RR_ROSTER_2026 = [
    "Yash Raj Punja", "Vignesh Puthur", "Sushant Mishra", "Ravi Singh", "Aman Rao", "Aman Rao Perala",
    "Brijesh Sharma", "Kuldeep Sen", "Vaibhav Suryavanshi", "Vaibhav Sooryavanshi", "Shubham Dubey",
    "Yudhvir Singh Charak", "Dhruv Jurel", "Riyan Parag", "Yashasvi Jaiswal", "Tushar Deshpande",
]


# =============================================================================
# 0. CONFIGURATION  (every knob you may want to defend in the PDF lives here)
# =============================================================================
@dataclass
class Config:
    auction_date: date = date(2026, 12, 16)

    # ---- Dimension 1: format suitability -------------------------------------------------
    format_weights: dict = field(default_factory=lambda: {"T20": 0.60, "LA": 0.30, "FC": 0.10})

    # ---- Dimension 2: recency (key = season START year; "2025-26" -> 2025) -----------------
    recency_by_start_year: dict = field(default_factory=lambda: {2026: 1.0, 2025: 0.6})
    recency_default: float = 0.3
    recency_label_override: dict = field(default_factory=dict)   # e.g. {"2025-26": 0.8}

    # ---- Dimension 3: age -----------------------------------------------------------------
    age_mode: str = "exp"                      # "exp" (smooth) | "step" (your table)
    age_anchor: float = 19.5
    age_lambda: float = 0.17                   # M(20.5)=0.84, M(22.5)=0.60
    age_steps: tuple = ((0, 19.999, 1.0), (20, 21.999, 0.85), (22, 23.999, 0.60))
    age_step_beyond: float = 0.30
    age_min: float = 16.0
    age_max: float = 23.999
    age_roll_forward_years: float = 0.0        # if 'Age' is as of an earlier snapshot date

    # ---- statistical shrinkage (pseudo-observations at league par) -----------------------
    prior_bat_sr_balls: float = 60
    prior_bat_bnd_balls: float = 100
    prior_bat_phase_balls: float = 30
    prior_dismissals: float = 2.0
    prior_bowl_econ_balls: float = 60
    prior_bowl_dot_balls: float = 120
    prior_bowl_wk_balls: float = 120
    prior_bowl_phase_balls: float = 36
    prior_wkts: float = 1.5

    rel_k_balls: dict = field(default_factory=lambda: {"T20": 150, "LA": 300, "FC": 600})
    est_balls_per_inn: dict = field(default_factory=lambda: {"T20": 14, "LA": 30, "FC": 60})
    min_qual_balls: dict = field(default_factory=lambda: {"T20": 60, "LA": 120, "FC": 240})
    min_cohort: int = 12
    min_feature_coverage: float = 0.40
    conf_c0: float = 0.25                      # confidence = E / (E + c0)
    dual_weight: float = 0.25                  # all-rounder utility bonus
    min_conf: float = 0.35
    min_role_affinity: float = 0.0
    min_age_peer_z: float = 0.5                # "outlier vs same-age peers" gate

    # ---- Top-N selection -----------------------------------------------------------------
    top_n: int = 10
    min_per_role: int = 1
    max_per_role: int = 4
    availability_mode: str = "lenient"         # lenient: block only known-contracted | strict: require known-available
    unknown_capped_policy: str = "exclude"     # exclude | flag
    exclude_rr_roster: bool = True
    allow_ipl_debuted: bool = True             # Puthur precedent: IPL-debuted but uncapped is OK
    manual_exclude: set = field(default_factory=set)

    # role weights by format (archetypes are T20 roles)
    role_fmt_w: dict = field(default_factory=lambda: {"T20": 1.0, "LA": 0.25, "FC": 0.0})


# feature -> weight, per (discipline, format). Missing features are dropped and weights renormalised.
FEATURE_WEIGHTS = {
    ("bat", "T20"): {"true_sr_idx": .30, "bnd_ball_pct": .25, "fai": .15, "bf_per_dis": .15, "six_pct": .15},
    ("bat", "LA"): {"true_sr_idx": .30, "bf_per_dis": .30, "bnd_ball_pct": .20, "bat_avg": .20},
    ("bat", "FC"): {"bat_avg": .50, "runs_per_inn": .30, "true_sr_idx": .20},
    ("bowl", "T20"): {"neg_econ_dev": .30, "dot_pct": .25, "wk_per100b": .25, "neg_phase_econ_dev": .20},
    ("bowl", "LA"): {"neg_econ_dev": .30, "wk_per100b": .30, "dot_pct": .20, "neg_bowl_avg": .20},
    ("bowl", "FC"): {"neg_bowl_avg": .35, "neg_bowl_sr": .35, "neg_econ_dev": .30},
}

# role -> (discipline, {feature: weight})  (features are robust z-scores)
ROLE_SPECS = {
    "Powerplay Enforcer": ("bat", {"true_sr_idx": .25, "bnd_ball_pct": .20, "pp_sr_idx": .25,
                                   "pp_bf_share": .15, "low_no_rate": .15}),
    "Spin-Hitting Finisher": ("bat", {"six_pct": .25, "spin_sr_idx": .25, "death_sr_idx": .20,
                                      "fai": .10, "no_rate": .10, "late_bf_share": .10}),
    "Death Bowler": ("bowl", {"neg_death_econ_dev": .30, "death_wk_per100b": .15, "dot_pct": .20,
                              "neg_econ_dev": .15, "death_balls_share": .20}),
    "Impact/Mystery Spinner": ("bowl", {"wk_per100b": .30, "neg_econ_dev": .25, "dot_pct": .20,
                                        "mid_wk_per100b": .10, "wrist_flag": .15}),
}

# Used automatically when <20% of players have phase data. Roles are then PROXIES (flagged in role_basis):
#  finisher vs opener is separated by not-out rate + six%, death bowler = best pace wicket-taker/economy profile.
ROLE_SPECS_PROXY = {
    "Powerplay Enforcer": ("bat", {"true_sr_idx": .30, "bnd_ball_pct": .25, "low_no_rate": .30, "bf_per_dis": .15}),
    "Spin-Hitting Finisher": ("bat", {"six_pct": .30, "true_sr_idx": .25, "no_rate": .30, "bnd_ball_pct": .15}),
    "Death Bowler": ("bowl", {"neg_econ_dev": .35, "wk_per100b": .30, "dot_pct": .20, "death_balls_share": .15}),
    "Impact/Mystery Spinner": ROLE_SPECS["Impact/Mystery Spinner"],
}


def log(*a):
    print("[scout]", *a, flush=True)


# =============================================================================
# 1. SMALL UTILITIES
# =============================================================================
def norm_col(c) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(c).strip().lower()).strip("_")


def norm_name(s) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"\(.*?\)|\[.*?\]", " ", s)                 # (c), (wk)
    s = re.sub(r"[†*]", " ", s)
    # Handle 'LastName, FirstName' reversal
    if "," in s:
        parts = s.split(",", 1)
        s = f"{parts[1].strip()} {parts[0].strip()}"
    s = s.replace(".", " ").replace("-", " ").replace("'", "")
    s = re.sub(r"[^A-Za-z\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def title_name(k: str) -> str:
    return " ".join(w.capitalize() for w in str(k).split())


def to_num(s: pd.Series) -> pd.Series:
    if s.dtype == object:
        s = (s.astype(str).str.replace(",", "", regex=False).str.replace("*", "", regex=False).str.strip()
             .replace({"-": np.nan, "--": np.nan, "": np.nan, "nan": np.nan, "None": np.nan, "NA": np.nan}))
    return pd.to_numeric(s, errors="coerce")


def overs_to_balls(s: pd.Series) -> pd.Series:
    """4.3 -> 27 balls (cricket notation). Handles both cricket 4.3 and decimal 4.5 safely on a per-row basis."""
    x = pd.to_numeric(s, errors="coerce")
    whole = np.floor(x)
    frac = np.round((x - whole) * 10)
    # If frac <= 5: standard cricket notation (e.g. 4.3 = 4*6 + 3 = 27 balls)
    # If frac == 6: standard typo for next full over (e.g. 4.6 = 5 overs = 30 balls)
    # If frac > 6: decimal overs (e.g. 4.8 overs = round(4.8 * 6) = 29 balls)
    balls = np.where(frac <= 5, whole * 6 + frac,
            np.where(frac == 6, (whole + 1) * 6,
                     np.round(x * 6)))
    return pd.Series(balls, index=s.index)


def parse_season_start(x):
    s = str(x)
    m = re.search(r"(20\d{2})", s)
    if m:
        return int(m.group(1))
    m = re.search(r"\b(\d{2})\s*[-/]\s*(\d{2})\b", s)
    return 2000 + int(m.group(1)) if m else np.nan


FMT_PATTERNS = [
    ("LA", r"vht|hazare|(?<![a-z0-9])vijay|list[\s_\-]?a(?![a-z])|(?<![a-z])la(?![a-z])|(?<![a-z])odi(?![a-z])|50[\s_\-]?over"),
    ("FC", r"ranji|first[\s_\-]?class|(?<![a-z])fc(?![a-z])|multi[\s_\-]?day|duleep|irani"),
    ("T20", r"smat|mushtaq|syed|(?<![a-z0-9])t[\s_\-]?20(?!\d)|twenty"),
]


def infer_format(text):
    t = str(text).lower()
    for code, pat in FMT_PATTERNS:
        if re.search(pat, t):
            return code
    return np.nan


def norm_cdf(z):
    return 0.5 * (1.0 + np.vectorize(math.erf)(np.asarray(z, dtype=float) / math.sqrt(2.0)))


def col(df, name):
    return df[name] if name in df.columns else pd.Series(np.nan, index=df.index)


# =============================================================================
# 2. SCHEMA ALIASES  ->  canonical column names
# =============================================================================
def _lk(d):
    return {a: canon for canon, al in d.items() for a in al}


COMMON = _lk({
    "player": ["player", "player_name", "name", "batter", "batsman", "bowler", "striker", "cricketer"],
    "team": ["team", "state", "state_team", "franchise", "side", "squad"],
    "season": ["season", "year", "edition", "season_year"],
    "format": ["format", "competition", "tournament", "comp", "league"],
    "matches": ["matches", "mat", "m", "games", "matches_played", "mp"],
    "age": ["age", "age_years"],
    "dob": ["dob", "date_of_birth", "birthdate", "born", "birth_date"],
    "bowl_type": ["bowl_type", "bowling_style", "bowling_type", "bowling", "bowl_style"],
    "capped": ["capped", "caps", "india_caps", "intl_caps", "international_caps", "capped_status"],
    "availability": ["availability", "ipl_status", "auction_status", "status", "contract_status"],
    "ipl_matches": ["ipl_matches", "ipl_mat", "ipl_games"],
    "ipl_team": ["ipl_team", "ipl_franchise", "franchise_2026"],
})
BAT = _lk({
    "innings": ["innings", "inns", "inn", "bat_inns", "batting_innings", "i"],
    "runs": ["runs", "runs_scored", "r", "bat_runs", "batting_runs", "total_runs"],
    "bf": ["bf", "balls_faced", "balls", "b", "bat_balls", "balls_played"],
    "no": ["no", "not_outs", "notouts", "not_out"],
    "fours": ["4s", "fours", "four"],
    "sixes": ["6s", "sixes", "six"],
    "dots_faced": ["dots_faced", "bat_dots", "dot_balls_faced"],
    "pp_runs": ["pp_runs", "powerplay_runs", "runs_pp", "runs_1_6", "pp_runs_scored"],
    "pp_bf": ["pp_bf", "powerplay_balls", "bf_pp", "balls_pp", "balls_1_6", "pp_balls_faced"],
    "mid_runs": ["mid_runs", "middle_runs", "runs_7_15", "runs_mid", "mid_runs_scored"],
    "mid_bf": ["mid_bf", "middle_balls", "balls_7_15", "bf_mid", "mid_balls_faced"],
    "death_runs": ["death_runs", "runs_16_20", "runs_death", "death_runs_scored"],
    "death_bf": ["death_bf", "death_balls_faced", "balls_16_20", "bf_death"],
    "runs_vs_spin": ["runs_vs_spin", "spin_runs", "runs_against_spin"],
    "bf_vs_spin": ["bf_vs_spin", "balls_vs_spin", "spin_balls", "balls_against_spin"],
})
BOWL = _lk({
    "overs": ["overs", "ov", "o", "overs_bowled"],
    "balls_bowled": ["balls_bowled", "bb", "legal_balls", "balls", "balls_delivered"],
    "rc": ["runs_conceded", "rc", "runs_given", "runs", "r", "runs_against", "conceded"],
    "wkts": ["wkts", "wickets", "w", "wk"],
    "maidens": ["maidens", "mdns", "md"],
    "dots_bowled": ["dots", "dot_balls", "dots_bowled", "dot_balls_bowled", "0s"],
    "pp_overs": ["pp_overs", "powerplay_overs"],
    "pp_balls": ["pp_balls", "pp_balls_bowled"],
    "pp_rc": ["pp_rc", "pp_runs_conceded", "pp_runs", "powerplay_runs_conceded"],
    "pp_wkts": ["pp_wkts", "pp_wickets", "wkts_pp", "powerplay_wickets"],
    "mid_overs": ["mid_overs", "middle_overs"],
    "mid_balls": ["mid_balls", "mid_balls_bowled"],
    "mid_rc": ["mid_rc", "mid_runs_conceded", "mid_runs", "middle_runs_conceded"],
    "mid_wkts": ["mid_wkts", "mid_wickets", "wkts_mid", "middle_wickets"],
    "death_overs": ["death_overs"],
    "death_balls": ["death_balls", "death_balls_bowled"],
    "death_rc": ["death_rc", "death_runs_conceded", "death_runs"],
    "death_wkts": ["death_wkts", "death_wickets", "wkts_death"],
})
TEXT_COLS = {"player", "team", "season", "format", "bowl_type", "capped", "availability", "ipl_team", "dob"}


def fix_header(df: pd.DataFrame) -> pd.DataFrame:
    """Excel sheets often carry title rows above the header."""
    if sum(str(c).lower().startswith("unnamed") for c in df.columns) > len(df.columns) / 2:
        for i in range(min(10, len(df))):
            vals = [norm_col(v) for v in df.iloc[i].tolist()]
            if any(v in ("player", "name", "player_name", "batter", "bowler") for v in vals):
                out = df.iloc[i + 1:].copy()
                out.columns = df.iloc[i].tolist()
                return out.reset_index(drop=True)
    return df


def detect_kind(df, name):
    part = name.split("__")[-1].lower()
    if "bowl" in part and "bat" not in part:
        return "bowl"
    if "bat" in part and "bowl" not in part:
        return "bat"
    cols = {norm_col(c) for c in df.columns}
    has_bowl = bool(cols & {"wkts", "wickets", "overs", "economy", "econ", "balls_bowled", "runs_conceded", "maidens"})
    has_bat = bool(cols & {"bf", "balls_faced", "4s", "6s", "fours", "sixes", "strike_rate", "sr", "not_outs", "no", "hs"})
    if has_bowl and has_bat:
        return "both"
    if has_bowl:
        return "bowl"
    if has_bat:
        return "bat"
    if cols & {"age", "dob", "date_of_birth", "capped", "bowl_type", "bowling_style", "availability"}:
        return "attrs"
    return None


def standardize(df, kind):
    lk = dict(COMMON)
    if kind in ("bat", "both"):
        lk.update(BAT)
    if kind in ("bowl", "both"):
        for k, v in BOWL.items():
            if kind == "bowl" or k not in lk:
                lk[k] = v
    ren, seen = {}, set()
    for c in df.columns:
        canon = lk.get(norm_col(c))
        if canon and canon not in seen:
            ren[c] = canon
            seen.add(canon)
    return df.rename(columns=ren)[list(ren.values())]


# =============================================================================
# 3. LOAD + CLEAN + MERGE
# =============================================================================
def read_tables(data_dir: Path):
    tables = []
    for p in sorted(Path(data_dir).rglob("*")):
        try:
            if p.suffix.lower() == ".csv":
                tables.append((p.stem, pd.read_csv(p)))
            elif p.suffix.lower() in (".xlsx", ".xlsm", ".xls"):
                for sh, d in pd.read_excel(p, sheet_name=None).items():
                    tables.append((f"{p.stem}__{sh}", d))
        except Exception as e:  # noqa
            log(f"  ! could not read {p.name}: {e}")
    return tables


def ingest(tables, cfg):
    bat_f, bowl_f, attr_f, report = [], [], [], []
    for name, raw in tables:
        df = fix_header(raw)
        kind = detect_kind(df, name)
        if kind is None:
            report.append((name, "skipped (no recognisable columns)"))
            continue
        std = standardize(df, kind)
        if "player" not in std.columns:
            report.append((name, "skipped (no player column)"))
            continue
        std = std[std["player"].notna()].copy()
        std["player"] = std["player"].astype(str).str.strip()
        std = std[~std["player"].str.lower().isin(["player", "name", "total", "nan", ""])]

        file_fmt = infer_format(name)
        std["fmt"] = std["format"].map(infer_format) if "format" in std else np.nan
        std["fmt"] = std["fmt"].fillna(file_fmt)
        sraw = std["season"] if "season" in std else pd.Series([name] * len(std), index=std.index)
        std["season_label"] = sraw.astype(str)
        std["season_start"] = sraw.map(parse_season_start)
        if std["season_start"].isna().all():
            std["season_start"] = parse_season_start(name)
        std["season_start"] = std["season_start"].fillna(0)

        for c in std.columns:
            if c not in TEXT_COLS and c not in ("fmt", "season_label", "season_start"):
                std[c] = to_num(std[c])

        bat_cols = set(BAT.values())
        bowl_cols = set(BOWL.values())
        has_stats = False
        if kind in ("bat", "both") and ("runs" in std.columns or "bf" in std.columns):
            b = std[[c for c in std.columns if c in bat_cols | COMMON_KEEP]].copy()
            b = b[b[["runs", "bf"]].notna().any(axis=1)]
            if "innings" not in b.columns:
                b["innings"] = b["matches"] if "matches" in b else np.nan
            bat_f.append(b)
            has_stats = True
        if kind in ("bowl", "both") and any(c in std.columns for c in ("overs", "balls_bowled", "wkts")):
            w = std[[c for c in std.columns if c in bowl_cols | COMMON_KEEP]].copy()
            if "balls_bowled" not in w.columns or w["balls_bowled"].isna().all():
                w["balls_bowled"] = overs_to_balls(w["overs"]) if "overs" in w else np.nan
            for ph in ("pp", "mid", "death"):
                if f"{ph}_overs" in w.columns and (f"{ph}_balls" not in w.columns or w[f"{ph}_balls"].isna().all()):
                    w[f"{ph}_balls"] = overs_to_balls(w[f"{ph}_overs"])
            w = w[w[["balls_bowled", "wkts", "rc"]].notna().any(axis=1)] if "rc" in w else w
            bowl_f.append(w)
            has_stats = True
        attr_cols = [c for c in ("player", "age", "dob", "bowl_type", "capped", "availability", "ipl_matches",
                                 "ipl_team", "team", "season_start") if c in std.columns]
        if len(attr_cols) > 2:
            attr_f.append(std[attr_cols].copy())
        report.append((name, f"{kind}: {len(std)} rows" + ("" if has_stats else " (attributes only)")))
    return bat_f, bowl_f, attr_f, report


COMMON_KEEP = {"player", "team", "season_label", "season_start", "fmt", "matches", "bowl_type"}


def build_name_map(names):
    """Map raw names -> canonical normalised key. Merges 'T Raheja' with 'Tushar Raheja' (if unambiguous)
    and near-duplicate spellings. Everything merged is written to the audit file."""
    norm = {n: norm_name(n) for n in set(names) if isinstance(n, str) and norm_name(n)}
    forms = sorted(set(norm.values()))
    parent = {f: f for f in forms}
    audit = []

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b, why):
        ra, rb = find(a), find(b)
        if ra != rb:
            keep, drop = (ra, rb) if len(ra) >= len(rb) else (rb, ra)
            parent[drop] = keep
            audit.append({"merged": drop, "into": keep, "reason": why})

    by_sur = defaultdict(list)
    for f in forms:
        t = f.split()
        if len(t) >= 2:
            by_sur[t[-1]].append(f)
    for sur, fs in by_sur.items():
        if len(fs) < 2:
            continue
        full = [f for f in fs if len(f.split()[0]) > 1]
        init = [f for f in fs if len(f.split()[0]) == 1]
        for i in range(len(full)):
            for j in range(i + 1, len(full)):
                a, b = full[i], full[j]
                fa, fb = a.rsplit(" ", 1)[0], b.rsplit(" ", 1)[0]
                if fa[0] == fb[0] and difflib.SequenceMatcher(None, fa, fb).ratio() >= 0.88 and fa != fb:
                    union(a, b, "near-duplicate spelling")
        for f in init:
            cands = {find(x) for x in full if x.split()[0][0] == f.split()[0][0]}
            if len(cands) == 1:
                union(next(iter(cands)), f, "initial matches a single full name")
            elif len(cands) > 1:
                audit.append({"merged": f, "into": "AMBIGUOUS", "reason": f"matches {sorted(cands)}"})
    canon = {f: find(f) for f in forms}
    return {raw: canon[nf] for raw, nf in norm.items()}, pd.DataFrame(audit)


def aggregate(df, sum_cols):
    cols = [c for c in sum_cols if c in df.columns]
    g = df.groupby(["pkey", "season_start", "fmt"], dropna=False)
    out = g[cols].sum(min_count=1)
    if "team" in df.columns:
        out["team"] = g["team"].first()
    out["season_label"] = g["season_label"].first()
    return out.reset_index()


SUM_BAT = ["matches", "innings", "runs", "bf", "no", "fours", "sixes", "dots_faced", "pp_runs", "pp_bf", "mid_runs",
           "mid_bf", "death_runs", "death_bf", "runs_vs_spin", "bf_vs_spin"]
SUM_BOWL = ["matches", "balls_bowled", "rc", "wkts", "maidens", "dots_bowled", "pp_balls", "pp_rc", "pp_wkts",
            "mid_balls", "mid_rc", "mid_wkts", "death_balls", "death_rc", "death_wkts"]


# =============================================================================
# 4. ADVANCED T20 FEATURE ENGINEERING
# =============================================================================
def par_rate(df, num, den, keys):
    """League par = sum(num)/sum(den) per (format, season) cohort, over rows where both exist."""
    if num not in df.columns or den not in df.columns:
        return pd.Series(np.nan, index=df.index)
    m = df[num].notna() & df[den].notna()
    tmp = pd.DataFrame({"n": df[num].where(m, 0.0), "d": df[den].where(m, 0.0)})
    for k in keys:
        tmp[k] = df[k].values
    g = tmp.groupby(keys)
    return g["n"].transform("sum") / g["d"].transform("sum").replace(0, np.nan)


def batting_features(b, cfg):
    b = b.copy()
    keys = ["fmt", "season_start"]
    for c in SUM_BAT:
        if c not in b.columns:
            b[c] = np.nan
    est = b["fmt"].map(cfg.est_balls_per_inn).astype(float)
    b["n_obs"] = b["bf"].where(b["bf"] > 0, b["innings"] * est)
    bf = b["bf"].where(b["bf"] > 0)
    b["sr"] = 100 * b["runs"] / bf

    # ---- True Strike Rate (phase-adjusted, shrunk):  100 x Runs / ExpectedRuns -------------
    par_rpb = par_rate(b, "runs", "bf", keys)
    exp = bf * par_rpb
    pp_par, mid_par, de_par = (par_rate(b, f"{p}_runs", f"{p}_bf", keys) for p in ("pp", "mid", "death"))
    ph_bf = b[["pp_bf", "mid_bf", "death_bf"]].sum(axis=1, min_count=3)
    ph_ok = (ph_bf >= 0.9 * bf) & pp_par.notna() & mid_par.notna() & de_par.notna()
    exp_ph = b["pp_bf"] * pp_par + b["mid_bf"] * mid_par + b["death_bf"] * de_par
    exp = exp.where(~ph_ok, exp_ph)
    b["phase_adjusted"] = ph_ok
    K = cfg.prior_bat_sr_balls
    b["true_sr_idx"] = 100 * (b["runs"] + K * par_rpb) / (exp + K * par_rpb)

    # ---- Boundary % (balls) and diagnostic run-share --------------------------------------
    b["bnd"] = b[["fours", "sixes"]].sum(axis=1, min_count=2)
    Kb = cfg.prior_bat_bnd_balls
    par_bnd = par_rate(b, "bnd", "bf", keys)
    par_six = par_rate(b, "sixes", "bf", keys)
    b["bnd_ball_pct"] = 100 * (b["bnd"] + Kb * par_bnd) / (bf + Kb)
    b["six_pct"] = 100 * (b["sixes"] + Kb * par_six) / (bf + Kb)
    b["bnd_run_share"] = 100 * (4 * b["fours"] + 6 * b["sixes"]) / b["runs"].where(b["runs"] > 0)

    # ---- Stability --------------------------------------------------------------------------
    dis = (b["innings"] - b["no"]).clip(lower=0)
    Kd = cfg.prior_dismissals
    b["_dis"] = dis
    par_bfd = par_rate(b, "bf", "_dis", keys)
    par_avg = par_rate(b, "runs", "_dis", keys)
    b["bf_per_dis"] = (bf + Kd * par_bfd) / (dis + Kd)
    b["bat_avg"] = (b["runs"] + Kd * par_avg) / (dis + Kd)
    b["runs_per_inn"] = (b["runs"] + 2 * par_rate(b, "runs", "innings", keys)) / (b["innings"] + 2)
    b["_no_i"] = b["no"]
    par_no = par_rate(b, "_no_i", "innings", keys)
    b["no_rate"] = (b["no"] + 3 * par_no) / (b["innings"] + 3)
    b["low_no_rate"] = -b["no_rate"]

    # ---- Phase features + Finishing Acceleration Index ---------------------------------------
    Kp = cfg.prior_bat_phase_balls
    b["pp_sr_idx"] = 100 * ((b["pp_runs"] + Kp * pp_par) / (b["pp_bf"] + Kp)) / pp_par
    b["death_sr_idx"] = 100 * ((b["death_runs"] + Kp * de_par) / (b["death_bf"] + Kp)) / de_par
    b["_pre_runs"] = b["pp_runs"] + b["mid_runs"]
    b["_pre_bf"] = b["pp_bf"] + b["mid_bf"]
    par_pre = par_rate(b, "_pre_runs", "_pre_bf", keys)
    d = (b["death_runs"] + Kp * de_par) / (b["death_bf"] + Kp)
    p = (b["_pre_runs"] + 2 * Kp * par_pre) / (b["_pre_bf"] + 2 * Kp)
    b["fai"] = (d / p) / (de_par / par_pre)          # 1.00 = league-typical acceleration into the death
    b["pp_bf_share"] = (b["pp_bf"] / bf).where(ph_ok)
    b["late_bf_share"] = (b["death_bf"] / bf).where(ph_ok)
    Ks = cfg.prior_bat_phase_balls
    spin_par = par_rate(b, "runs_vs_spin", "bf_vs_spin", keys)
    b["spin_sr_idx"] = 100 * ((b["runs_vs_spin"] + Ks * spin_par) / (b["bf_vs_spin"] + Ks)) / spin_par
    return b.drop(columns=[c for c in b.columns if c.startswith("_")])


def bowling_features(w, cfg):
    w = w.copy()
    keys = ["fmt", "season_start"]
    for c in SUM_BOWL:
        if c not in w.columns:
            w[c] = np.nan
    balls = w["balls_bowled"].where(w["balls_bowled"] > 0)
    w["n_obs"] = balls
    w["econ"] = 6 * w["rc"] / balls

    par = par_rate(w, "rc", "balls_bowled", keys)
    exp = balls * par
    pars = {ph: par_rate(w, f"{ph}_rc", f"{ph}_balls", keys) for ph in ("pp", "mid", "death")}
    ph_balls = w[["pp_balls", "mid_balls", "death_balls"]].sum(axis=1, min_count=3)
    ph_ok = (ph_balls >= 0.9 * balls) & pars["pp"].notna() & pars["mid"].notna() & pars["death"].notna()
    exp_ph = sum(w[f"{ph}_balls"] * pars[ph] for ph in pars)
    exp = exp.where(~ph_ok, exp_ph)
    w["phase_adjusted"] = ph_ok

    # ---- Economy deviation vs phase-par (runs/over, negative = better than league) --------------
    w["econ_dev"] = 6 * (w["rc"] - exp) / (balls + cfg.prior_bowl_econ_balls)
    w["neg_econ_dev"] = -w["econ_dev"]

    # ---- Dot-ball %, wicket frequency, classical averages --------------------------------------
    Kd, Kw = cfg.prior_bowl_dot_balls, cfg.prior_bowl_wk_balls
    par_dot = par_rate(w, "dots_bowled", "balls_bowled", keys)
    w["dot_pct"] = 100 * (w["dots_bowled"] + Kd * par_dot) / (balls + Kd)
    par_w = par_rate(w, "wkts", "balls_bowled", keys)
    w["wk_per100b"] = 100 * (w["wkts"] + Kw * par_w) / (balls + Kw)
    Kk = cfg.prior_wkts
    w["bowl_avg"] = (w["rc"] + Kk * par_rate(w, "rc", "wkts", keys)) / (w["wkts"] + Kk)
    w["bowl_sr"] = (balls + Kk * par_rate(w, "balls_bowled", "wkts", keys)) / (w["wkts"] + Kk)
    w["neg_bowl_avg"], w["neg_bowl_sr"] = -w["bowl_avg"], -w["bowl_sr"]

    # ---- Phase-specific economy deviation and wicket frequency --------------------------------
    Kp = cfg.prior_bowl_phase_balls
    for ph in ("pp", "mid", "death"):
        pb = w[f"{ph}_balls"]
        w[f"{ph}_econ_dev"] = 6 * (w[f"{ph}_rc"] - pb * pars[ph]) / (pb + Kp)
        parw = par_rate(w, f"{ph}_wkts", f"{ph}_balls", keys)
        w[f"{ph}_wk_per100b"] = 100 * (w[f"{ph}_wkts"] + Kp * parw) / (pb + Kp)
    hl_balls = w["pp_balls"] + w["death_balls"]
    w["neg_phase_econ_dev"] = -((w["pp_econ_dev"] * w["pp_balls"] + w["death_econ_dev"] * w["death_balls"]) / hl_balls)
    w["neg_death_econ_dev"] = -w["death_econ_dev"]
    w["death_balls_share"] = (w["death_balls"] / balls).where(ph_ok)
    w["pp_balls_share"] = (w["pp_balls"] / balls).where(ph_ok)
    return w


# =============================================================================
# 5. SCORING: robust z-scores -> impact score -> player blend
# =============================================================================
def cohort_z(df, feats, qual, cfg):
    """Robust z (median/MAD) inside (format, season) cohorts of *qualified* rows; falls back to format-level."""
    Z = pd.DataFrame(index=df.index)
    k1 = [df["fmt"], df["season_start"]]
    k2 = [df["fmt"]]

    def stats(xq, keys):
        g = xq.groupby(keys)
        med = g.transform("median")
        return med, (xq - med).abs().groupby(keys).transform("median"), g.transform("std"), g.transform("count")

    for f in feats:
        if f not in df.columns:
            continue
        x = df[f].astype(float)
        xq = x.where(qual)
        m1, a1, s1, c1 = stats(xq, k1)
        m2, a2, s2, _ = stats(xq, k2)
        use1 = c1 >= cfg.min_cohort
        med, mad, sd = m1.where(use1, m2), a1.where(use1, a2), s1.where(use1, s2)
        scale = (1.4826 * mad)
        scale = scale.where(scale > 1e-9, sd).where(lambda s: s > 1e-9)
        Z[f] = ((x - med) / scale).clip(-3, 3)
    return Z


def weighted_z(Z, weights, min_cov):
    cols = [c for c in weights if c in Z.columns]
    if not cols:
        return pd.Series(np.nan, index=Z.index), pd.Series(0.0, index=Z.index)
    W = np.array([weights[c] for c in cols], dtype=float)
    X = Z[cols].values
    ok = ~np.isnan(X)
    den = (ok * W).sum(axis=1)
    num = np.nansum(X * W, axis=1)
    cov = den / sum(weights.values())
    wz = np.where((den > 0) & (cov >= min_cov), num / np.where(den > 0, den, 1), np.nan)
    return pd.Series(wz, index=Z.index), pd.Series(cov, index=Z.index)


def score_rows(df, disc, cfg):
    """Adds per-row Z features, composite score (0-100) and reliability."""
    qual = df["n_obs"] >= df["fmt"].map(cfg.min_qual_balls)
    feats = sorted({f for (d, _), spec in FEATURE_WEIGHTS.items() if d == disc for f in spec}
                   | {f for r, (d, spec) in ROLE_SPECS.items() if d == disc for f in spec if f != "wrist_flag"})
    Z = cohort_z(df, feats, qual, cfg)
    df = df.copy()
    wz = pd.Series(np.nan, index=df.index)
    cov = pd.Series(0.0, index=df.index)
    for fmt in FORMATS:
        m = df["fmt"] == fmt
        if not m.any():
            continue
        a, c = weighted_z(Z[m], FEATURE_WEIGHTS[(disc, fmt)], cfg.min_feature_coverage)
        wz[m], cov[m] = a, c
    df["_wz"] = wz
    comp = cohort_z(df, ["_wz"], qual, cfg)["_wz"]       # re-standardise: weighted means shrink the spread
    df["score"] = 100 * norm_cdf(comp.fillna(np.nan).values)
    df["feat_cov"] = cov
    k = df["fmt"].map(cfg.rel_k_balls)
    df["rel"] = df["n_obs"] / (df["n_obs"] + k)
    for f in Z.columns:
        df[f"z_{f}"] = Z[f]
    return df.drop(columns=["_wz"])


def recency_weight(season_start, label, cfg):
    if isinstance(label, str) and label in cfg.recency_label_override:
        return cfg.recency_label_override[label]
    if pd.isna(season_start) or season_start == 0:
        return cfg.recency_default
    return cfg.recency_by_start_year.get(int(season_start), cfg.recency_default)


def wmean_by(r, cols, wcol):
    out = {}
    for c in cols:
        if c not in r.columns:
            continue
        m = r[c].notna() & r[wcol].notna() & (r[wcol] > 0)
        num = (r.loc[m, wcol] * r.loc[m, c]).groupby(r.loc[m, "pkey"]).sum()
        den = r.loc[m, wcol].groupby(r.loc[m, "pkey"]).sum()
        out[c] = num / den
    return pd.DataFrame(out)


def combine_player(rows, disc, cfg, raw_cols):
    r = rows.dropna(subset=["score"]).copy()
    if r.empty:
        return pd.DataFrame()
    r["wf"] = r["fmt"].map(cfg.format_weights).fillna(0.0)
    r["rec"] = [recency_weight(s, l, cfg) for s, l in zip(r["season_start"], r["season_label"])]
    r["w"] = r["wf"] * r["rec"] * r["rel"]
    r["wr"] = r["fmt"].map(cfg.role_fmt_w).fillna(0.0) * r["rec"] * r["rel"]
    sw = r.groupby("pkey")["w"].sum()
    score = (r["w"] * r["score"]).groupby(r["pkey"]).sum() / sw.replace(0, np.nan)
    conf = sw / (sw + cfg.conf_c0)
    out = pd.DataFrame({f"{disc}_score": score, f"{disc}_conf": conf,
                        f"{disc}_final": conf * score + (1 - conf) * 50.0})
    for f in FORMATS:                                       # per-format breakdown for the PDF
        rf = r[r["fmt"] == f].copy()
        rf["wx"] = rf["rec"] * rf["rel"]
        if len(rf):
            out[f"{disc}_score_{f}"] = (rf["wx"] * rf["score"]).groupby(rf["pkey"]).sum() / \
                                       rf["wx"].groupby(rf["pkey"]).sum().replace(0, np.nan)
    out[f"{disc}_n"] = r.groupby("pkey")["n_obs"].sum()
    out[f"{disc}_phase_cov"] = r.groupby("pkey")["phase_adjusted"].mean()
    zcols = [c for c in r.columns if c.startswith("z_")]
    rawb = wmean_by(r, raw_cols, "wr").add_prefix(f"{disc}__")
    zb = wmean_by(r, zcols, "wr").add_prefix(f"{disc}__")
    return pd.concat([out, rawb, zb], axis=1)


# =============================================================================
# 6. AGE, ELIGIBILITY, ROLES, CLUSTERING
# =============================================================================
def age_multiplier(age, cfg):
    a = np.asarray(age, dtype=float)
    if cfg.age_mode == "exp":
        m = np.where(a <= cfg.age_anchor, 1.0, np.exp(-cfg.age_lambda * (a - cfg.age_anchor)))
    else:
        m = np.full_like(a, cfg.age_step_beyond)
        for lo, hi, v in cfg.age_steps:
            m = np.where((a >= lo) & (a <= hi), v, m)
    return np.where(np.isnan(a), np.nan, m)


def parse_capped(v):
    if pd.isna(v):
        return np.nan
    s = str(v).strip().lower()
    # Explicit uncapped patterns (including state/domestic phrases)
    if any(k in s for k in ["uncapped", "domestic", "u19", "u-19", "u 19", "emerging", "associate"]):
        return False
    if s in {"n", "no", "false", "0", "u", "none", "-"}:
        return False
    # Explicit capped patterns
    if any(k in s for k in ["india capped", "intl capped", "international cap", "senior cap"]):
        return True
    if s in {"y", "yes", "true", "1", "capped", "c", "intl", "international", "india"}:
        return True
    try:
        return float(s) > 0
    except ValueError:
        return np.nan


def parse_avail(v):
    if pd.isna(v):
        return "unknown"
    s = str(v).strip().lower()
    if s in {"released", "unsold", "unsigned", "uncontracted", "available", "registered", "free", "pool"}:
        return "available"
    if s in {"contracted", "retained", "signed", "traded", "sold"}:
        return "blocked"
    return "unknown"


def bowl_class(v):
    if pd.isna(v):
        return "unknown"
    s = str(v).lower()
    if re.search(r"spin|break|googly|orthodox|chinaman|wrist|carrom|mystery|off|leg", s):
        return "spin"
    if re.search(r"fast|medium|pace|seam|swing", s):
        return "pace"
    return "unknown"


def wrist_flag(v):
    if pd.isna(v):
        return np.nan
    return 1.0 if re.search(r"leg|googly|mystery|carrom|chinaman|wrist|unorthodox", str(v).lower()) else -0.5


def kmeans(X, k=4, iters=60, seed=7):
    rng = np.random.default_rng(seed)
    n = len(X)
    C = [X[rng.integers(n)]]
    for _ in range(1, k):
        d2 = np.min(((X[:, None, :] - np.array(C)[None]) ** 2).sum(-1), axis=1)
        p = d2 / d2.sum() if d2.sum() > 0 else np.full(n, 1 / n)
        C.append(X[rng.choice(n, p=p)])
    C = np.array(C)
    for _ in range(iters):
        lab = ((X[:, None, :] - C[None]) ** 2).sum(-1).argmin(1)
        newC = np.array([X[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
        if np.allclose(newC, C):
            break
        C = newC
    d = ((X[:, None, :] - C[None]) ** 2).sum(-1)
    return d.argmin(1), np.sqrt(d.min(1))


def role_affinities(P, cfg):
    """Affinity per tactical role = weighted mean of the relevant robust z-scores.
    Switches to proxy specs (and says so) when the pack has no phase data."""
    def share(c):
        d = c.split("__")[0]
        has = P[f"{d}_final"].notna() if f"{d}_final" in P.columns else pd.Series(False, index=P.index)
        return P.loc[has, c].notna().mean() if (c in P.columns and has.any()) else 0.0

    proxy = {"bat": share("bat__z_pp_sr_idx") < 0.2, "bowl": share("bowl__z_neg_death_econ_dev") < 0.2}
    for d, flag in proxy.items():
        if flag and ((d == "bat" and "bat__true_sr_idx" in P.columns) or (d == "bowl" and "bowl__econ_dev" in P.columns)):
            log(f"WARNING: no usable {d} phase data -> {d} roles use PROXY specs (see role_basis). "
                "Ask for ball-by-ball / phase splits to make them real.")
    aff = pd.DataFrame(index=P.index)
    basis = pd.Series("", index=P.index)
    for role, (disc, spec_phase) in ROLE_SPECS.items():
        use_proxy = proxy[disc]
        spec = ROLE_SPECS_PROXY[role][1] if use_proxy else spec_phase
        cols = {f: P[f"{disc}__z_{f}"] for f in spec if f"{disc}__z_{f}" in P.columns}
        if "wrist_flag" in spec:
            cols["wrist_flag"] = P["bowl_type"].map(wrist_flag)
        if not cols:
            aff[role] = np.nan
            continue
        a, _ = weighted_z(pd.DataFrame(cols), spec, cfg.min_feature_coverage)
        elig = pd.Series(True, index=P.index)
        if role == "Death Bowler":
            elig = P["bowl_class"].isin(["pace", "unknown"])
        if role == "Impact/Mystery Spinner":
            elig = P["bowl_class"].isin(["spin", "unknown"])
        aff[role] = a.where(elig)
        basis = basis.where(~(aff[role].notna() & (basis == "")), "proxy (no phase data)" if use_proxy else "phase-based")
    return aff, basis


# =============================================================================
# 7. MAIN PIPELINE
# =============================================================================
def run_pipeline(data_dir: Path, out_dir: Path, cfg: Config, demo=False):
    out_dir.mkdir(parents=True, exist_ok=True)
    log(f"loading {data_dir}")
    tables = read_tables(data_dir)
    bat_f, bowl_f, attr_f, rep = ingest(tables, cfg)
    for n, s in rep:
        log(f"  {n}: {s}")
    if not bat_f and not bowl_f:
        sys.exit("No batting/bowling tables recognised - check file names/headers (see ALIASES).")

    # -- merge keys -----------------------------------------------------------------------------
    all_names = pd.concat([f["player"] for f in bat_f + bowl_f + attr_f], ignore_index=True)
    name_map, audit = build_name_map(all_names)
    audit.to_csv(out_dir / "audit_name_merges.csv", index=False)
    log(f"name merge: {len(set(all_names))} raw spellings -> {len(set(name_map.values()))} players "
        f"({len(audit)} merges logged for review)")

    def key(df):
        df = df.copy()
        df["pkey"] = df["player"].map(name_map)
        return df[df["pkey"].notna() & df["fmt"].notna()] if "fmt" in df else df[df["pkey"].notna()]

    bat = aggregate(key(pd.concat(bat_f, ignore_index=True)), SUM_BAT) if bat_f else pd.DataFrame()
    bowl = aggregate(key(pd.concat(bowl_f, ignore_index=True)), SUM_BOWL) if bowl_f else pd.DataFrame()
    for nm_, d_ in (("batting", bat), ("bowling", bowl)):
        if len(d_):
            c_ = d_.groupby(["fmt", "season_label"]).size()
            log(f"{nm_} rows (player-seasons) by format/season: " + "; ".join(f"{a}/{b}={n}" for (a, b), n in c_.items()))
    missing_f = [f for f in FORMATS if f not in set(bat.get("fmt", [])) | set(bowl.get("fmt", []))]
    if missing_f:
        log(f"WARNING: no data recognised for format(s) {missing_f} - check file names contain smat/vht/ranji or add a Format column")
    bat.to_csv(out_dir / "01_clean_batting.csv", index=False)
    bowl.to_csv(out_dir / "01_clean_bowling.csv", index=False)

    # -- attributes (latest non-null per player) -------------------------------------------------
    A = pd.concat([f.assign(pkey=f["player"].map(name_map)) for f in attr_f], ignore_index=True) if attr_f \
        else pd.DataFrame(columns=["pkey"])
    A = A[A["pkey"].notna()]
    if "season_start" in A:
        A = A.sort_values("season_start")
    attrs = A.groupby("pkey").last() if len(A) else pd.DataFrame(index=pd.Index([], name="pkey"))

    # -- row-level features and scores -----------------------------------------------------------
    rows = {}
    if len(bat):
        rows["bat"] = score_rows(batting_features(bat, cfg), "bat", cfg)
    if len(bowl):
        rows["bowl"] = score_rows(bowling_features(bowl, cfg), "bowl", cfg)

    bat_raw = ["sr", "true_sr_idx", "bnd_ball_pct", "six_pct", "bnd_run_share", "fai", "pp_sr_idx", "death_sr_idx",
               "spin_sr_idx", "bf_per_dis"]
    bowl_raw = ["econ", "econ_dev", "dot_pct", "wk_per100b", "pp_econ_dev", "death_econ_dev", "death_wk_per100b"]
    parts = []
    if "bat" in rows:
        parts.append(combine_player(rows["bat"], "bat", cfg, bat_raw))
    if "bowl" in rows:
        parts.append(combine_player(rows["bowl"], "bowl", cfg, bowl_raw))
    P = pd.concat(parts, axis=1)
    P.index.name = "pkey"
    P = P.join(attrs, how="left")
    for c in ("bat_final", "bowl_final", "bat_conf", "bowl_conf"):
        if c not in P:
            P[c] = np.nan
    P["bowl_type"] = P["bowl_type"] if "bowl_type" in P else np.nan
    P["bowl_class"] = P["bowl_type"].map(bowl_class)
    # latest team label
    team_src = pd.concat([d[["pkey", "season_start", "team"]] for d in (bat, bowl) if len(d) and "team" in d])
    P["team"] = team_src.sort_values("season_start").groupby("pkey")["team"].last()
    P["player"] = [title_name(k) for k in P.index]

    # -- Age + multiplier (Dimension 3) ----------------------------------------------------------
    if "dob" in P and P["dob"].notna().any():
        dob_raw = P["dob"]
        s_num = pd.to_numeric(dob_raw, errors="coerce")
        is_serial = (s_num > 25000) & (s_num < 55000)
        dob = pd.Series(pd.NaT, index=P.index, dtype="datetime64[ns]")
        if is_serial.any():
            dob.loc[is_serial] = pd.to_datetime(s_num.loc[is_serial], unit="D", origin="1899-12-30", errors="coerce")
        rem = ~is_serial & dob_raw.notna()
        if rem.any():
            dob.loc[rem] = pd.to_datetime(dob_raw.loc[rem], format="mixed", errors="coerce")
        age_dob = (pd.Timestamp(cfg.auction_date) - dob).dt.days / 365.25
    else:
        age_dob = pd.Series(np.nan, index=P.index)
    age_col = pd.to_numeric(P["age"], errors="coerce") + cfg.age_roll_forward_years if "age" in P else np.nan
    P["age"] = age_dob.fillna(age_col)
    P["age_mult"] = age_multiplier(P["age"].values, cfg)

    # -- Impact, TDSI ----------------------------------------------------------------------------
    b, w = P["bat_final"], P["bowl_final"]
    prim = np.fmax(b, w)
    both = b.notna() & w.notna() & (P["bat_conf"] >= 0.5) & (P["bowl_conf"] >= 0.5)
    sec = pd.Series(np.where(both, np.minimum(b, w), np.nan), index=P.index)
    P["dual_utility"] = both
    P["impact"] = np.clip(prim + cfg.dual_weight * np.maximum(0, sec.fillna(0) - 50), 0, 100)
    P["confidence"] = np.fmax(P["bat_conf"], P["bowl_conf"])
    P["tdsi"] = P["impact"] * P["age_mult"]

    # age-peer outlier z (is this player exceptional *for his age*?)
    bucket = np.floor(P["age"])
    grp = P.groupby(bucket)["impact"]
    med, mad, cnt = grp.transform("median"), (P["impact"] - grp.transform("median")).abs().groupby(bucket).transform("median"), grp.transform("count")
    gmed, gmad = P["impact"].median(), (P["impact"] - P["impact"].median()).abs().median()
    use = cnt >= 8
    med, mad = med.where(use, gmed), mad.where(use, gmad)
    P["age_peer_z"] = (P["impact"] - med) / (1.4826 * mad.replace(0, np.nan))

    # -- Roles (Powerplay Enforcer / Spin-Hitting Finisher / Death Bowler / Impact-Mystery Spinner) --
    aff, basis = role_affinities(P, cfg)
    P = pd.concat([P, aff.add_prefix("aff_")], axis=1)
    P["role_basis"] = basis
    A_ = aff.values
    allnan = np.isnan(A_).all(axis=1)
    best = np.where(allnan, 0, np.nanargmax(np.where(np.isnan(A_), -9, A_), axis=1))
    P["role"] = [ROLES[i] if (not n and A_[j, i] >= cfg.min_role_affinity) else "Unclassified"
                 for j, (i, n) in enumerate(zip(best, allnan))]
    srt = np.sort(np.where(np.isnan(A_), -9, A_), axis=1)
    P["role_margin"] = np.where(allnan, np.nan, srt[:, -1] - srt[:, -2])

    # -- Economic Valuation & Auction Bidding Engine (WAR / VORP to INR) -------------------------
    base_val = 0.30  # Standard uncapped base price: 30 Lakhs (0.30 Cr)
    rarity_bonus = P["role"].map({
        "Death Bowler": 0.40,
        "Impact/Mystery Spinner": 0.35,
        "Powerplay Enforcer": 0.25,
        "Spin-Hitting Finisher": 0.20
    }).fillna(0.10)
    tdsi_clean = P["tdsi"].fillna(45.0)
    P["market_value_cr"] = (base_val + np.maximum(0, (tdsi_clean - 45) / 55) * 1.50 + rarity_bonus).round(2)
    P["expected_bid_lakhs"] = np.where(tdsi_clean >= 75, 60, np.where(tdsi_clean >= 65, 45, 30))
    P["walk_away_limit_lakhs"] = np.minimum(100, np.round(P["market_value_cr"] * 65)).fillna(30).astype(int)
    P["surplus_value_cr"] = (P["market_value_cr"] - P["expected_bid_lakhs"] / 100.0).round(2)
    X = np.nan_to_num(A_, nan=-1.0)
    if len(P) >= 8:
        lab, dist = kmeans(X, k=4)
        P["cluster_id"], P["cluster_dist"] = lab, dist
        maj = {c: Counter(P.loc[lab == c, "role"]).most_common(1)[0][0] for c in np.unique(lab)}
        agree = np.mean([maj[c] == r for c, r in zip(lab, P["role"])])
        log(f"k-means (k=4) vs affinity-role agreement: {agree:.0%}  (low = many hybrid profiles)")

    # -- Eligibility gates -----------------------------------------------------------------------
    P["capped_flag"] = P["capped"].map(parse_capped) if "capped" in P else np.nan
    P["avail"] = P["availability"].map(parse_avail) if "availability" in P else "unknown"
    rr_keys = {norm_name(n) for n in RR_ROSTER_2026}
    P["in_rr_squad"] = P.index.isin(rr_keys)
    why = []
    for k, r in P.iterrows():
        f = []
        if pd.isna(r["age"]):
            f.append("age unknown")
        elif not (cfg.age_min <= r["age"] <= cfg.age_max):
            f.append("age out of band")
        if r["capped_flag"] is True or r["capped_flag"] == True:  # noqa: E712
            f.append("capped")
        elif pd.isna(r["capped_flag"]) and cfg.unknown_capped_policy == "exclude":
            f.append("capped status unknown")
        if r["in_rr_squad"] and cfg.exclude_rr_roster:
            f.append("already RR")
        if r["avail"] == "blocked" or (cfg.availability_mode == "strict" and r["avail"] != "available"):
            f.append("not available")
        if not cfg.allow_ipl_debuted and pd.to_numeric(r.get("ipl_matches"), errors="coerce") > 0:
            f.append("IPL-debuted")
        if r["confidence"] < cfg.min_conf or pd.isna(r["confidence"]):
            f.append("thin evidence")
        if r["role"] == "Unclassified":
            f.append("no role fit")
        if pd.notna(r["age_peer_z"]) and r["age_peer_z"] < cfg.min_age_peer_z:
            f.append("not an age-peer outlier")
        if k in {norm_name(x) for x in cfg.manual_exclude}:
            f.append("manual exclude")
        why.append("; ".join(f))
    P["excluded_because"] = why
    P["eligible"] = P["excluded_because"] == ""
    P["availability_note"] = np.where(P["avail"] == "unknown", "CHECK vs Nov-17 retention/release list", "")

    # -- Explanations (percentiles of blended raw features) -------------------------------------
    def pct(s):
        return s.rank(pct=True) * 100

    expl = []
    for k, r in P.iterrows():
        bits = []
        if r["role"] in ("Powerplay Enforcer", "Spin-Hitting Finisher"):
            for lab_, c in [("SR-idx", "bat__true_sr_idx"), ("Bnd%", "bat__bnd_ball_pct"), ("6s%", "bat__six_pct"),
                            ("PP-idx", "bat__pp_sr_idx"), ("Death-idx", "bat__death_sr_idx"), ("FAI", "bat__fai")]:
                if c in P and pd.notna(r.get(c)):
                    bits.append((pct(P[c])[k], f"{lab_} {r[c]:.1f} (p{pct(P[c])[k]:.0f})"))
        elif r["role"] in ("Death Bowler", "Impact/Mystery Spinner"):
            for lab_, c, inv in [("EconDev", "bowl__econ_dev", True), ("Dot%", "bowl__dot_pct", False),
                                 ("W/100b", "bowl__wk_per100b", False), ("DeathEconDev", "bowl__death_econ_dev", True)]:
                if c in P and pd.notna(r.get(c)):
                    p_ = (100 - pct(P[c])[k]) if inv else pct(P[c])[k]
                    bits.append((p_, f"{lab_} {r[c]:+.2f} (p{p_:.0f})" if inv else f"{lab_} {r[c]:.1f} (p{p_:.0f})"))
        bits.sort(reverse=True)
        expl.append(" | ".join(t for _, t in bits[:3]))
    P["evidence"] = expl

    # -- Top-N with role balance -----------------------------------------------------------------
    pool = P[P["eligible"]].sort_values("tdsi", ascending=False)
    picks = []
    for role in ROLES:
        c = pool[pool["role"] == role]
        for _ in range(cfg.min_per_role):
            c = c[~c.index.isin(picks)]
            if len(c):
                picks.append(c.index[0])
    cnt = Counter(pool.loc[picks, "role"]) if picks else Counter()
    for k, r in pool.iterrows():
        if len(picks) >= cfg.top_n:
            break
        if k in picks or cnt[r["role"]] >= cfg.max_per_role:
            continue
        picks.append(k)
        cnt[r["role"]] += 1
    top = P.loc[picks].sort_values("tdsi", ascending=False).head(cfg.top_n)
    if len(top) < cfg.top_n:
        reasons = P["excluded_because"].str.split("; ").explode().value_counts()
        log(f"WARNING: only {len(top)} players pass every gate. Why players were excluded:")
        for k_, v_ in reasons.items():
            if k_:
                log(f"    {v_:5d}  {k_}")
        if reasons.get("age unknown", 0) > 0.5 * len(P):
            log("    -> most players have no Age/DOB: add a players_master.csv (Player, DOB or Age, Capped, Bowl_Type, Availability)")

    # -- Write outputs ---------------------------------------------------------------------------
    econ_cols = ["market_value_cr", "expected_bid_lakhs", "walk_away_limit_lakhs", "surplus_value_cr"]
    show = ["player", "team", "age", "age_mult", "role", "tdsi", "impact", "confidence", "age_peer_z"] + econ_cols + \
           ["bat_final", "bowl_final", "dual_utility", "role_basis", "evidence", "avail", "availability_note", "capped_flag"]
    show += [c for c in P.columns if c.startswith(("bat_score_", "bowl_score_", "aff_"))]
    ranked = P.sort_values("tdsi", ascending=False)
    ranked.to_csv(out_dir / "03_ranked_all.csv", columns=[c for c in show + ["eligible", "excluded_because"] if c in P.columns])
    P.to_csv(out_dir / "02_player_features_full.csv")
    top.insert(0, "rank", range(1, len(top) + 1))
    top.to_csv(out_dir / "04_top10_targets.csv", columns=["rank"] + [c for c in show if c in P.columns], index=False)
    boards = [pool[pool["role"] == r].head(5).assign(board=r) for r in ROLES]
    pd.concat(boards).to_csv(out_dir / "05_role_boards_top5.csv", columns=["board"] + [c for c in show if c in P.columns], index=False)
    P[P["age"].isna() | P["capped_flag"].isna() | (P["avail"] == "unknown")][["player", "age", "capped_flag", "avail"]] \
        .to_csv(out_dir / "audit_missing_fields.csv")
    cov = pd.DataFrame({k: v[[c for c in v.columns if c in bat_raw + bowl_raw]].notna().mean() for k, v in rows.items()})
    cov.index.name = "feature"
    cov.to_csv(out_dir / "audit_feature_coverage.csv")
    write_summary(top, cfg, out_dir, demo, rows)
    try_charts(top, ranked, out_dir)
    log(f"done -> {out_dir.resolve()}")
    return top, P


def write_summary(top, cfg, out_dir, demo, rows):
    ph = {k: float(v.loc[v["fmt"] == "T20", "phase_adjusted"].mean()) for k, v in rows.items()}
    L = ["# RR War Room - Top targets (auto-generated)", ""]
    if demo:
        L += ["> **DEMO RUN ON SYNTHETIC DATA - names and numbers are fictional.**", ""]
    L += [f"Auction date used for age: {cfg.auction_date} | age mode: {cfg.age_mode} | "
          f"format weights: {cfg.format_weights} | recency: {cfg.recency_by_start_year} (default {cfg.recency_default})", "",
          f"Phase-adjusted T20 rows: batting {ph.get('bat', 0):.0%}, bowling {ph.get('bowl', 0):.0%} "
          "(0% = no phase columns in the pack, so league-level par was used and phase features are blank).", "",
          "| # | Player | Team | Age | Role | TDSI | Valuation | Target Bid | Walk-Away | Surplus | Evidence |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in top.iterrows():
        L.append(f"| {int(r['rank'])} | {r['player']} | {r.get('team', '')} | {r['age']:.1f} | {r['role']} | "
                 f"{r['tdsi']:.1f} | ₹{r.get('market_value_cr', 0):.2f}Cr | ₹{int(r.get('expected_bid_lakhs', 30))}L | "
                 f"₹{int(r.get('walk_away_limit_lakhs', 60))}L | +₹{r.get('surplus_value_cr', 0):.2f}Cr | {r['evidence']} |")
    L += ["", "## Before you submit", "- Re-run `availability` against the IPL retention/release list (deadline 17 Nov) and the registered pool (closes 23 Nov).",
          "- Cross-check any headline stat against Cricinfo/Cricbuzz; report the data-pack number as the primary.",
          "- Players with `availability_note` set are not confirmed available."]
    (out_dir / "top10_summary.md").write_text("\n".join(L), encoding="utf-8")


def try_charts(top, ranked, out_dir):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return
    colors = {"Powerplay Enforcer": "#d6336c", "Spin-Hitting Finisher": "#1971c2",
              "Death Bowler": "#2b8a3e", "Impact/Mystery Spinner": "#f08c00"}
    fig, ax = plt.subplots(figsize=(8, 5))
    t = top.iloc[::-1]
    ax.barh(t["player"], t["tdsi"], color=[colors.get(r, "#888") for r in t["role"]])
    ax.set_xlabel("TDSI (0-100)")
    ax.set_title("Top targets by Three-Dimensional Selection Index")
    fig.tight_layout()
    fig.savefig(out_dir / "chart_top10_tdsi.png", dpi=160)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 5))
    r = ranked.dropna(subset=["age", "impact"])
    ax.scatter(r["age"], r["impact"], s=10, c="#bbbbbb")
    ax.scatter(top["age"], top["impact"], s=45, c=[colors.get(x, "#888") for x in top["role"]])
    ax.set_xlabel("Age at auction")
    ax.set_ylabel("Impact (0-100)")
    ax.set_title("Impact vs age - the outliers are top-left")
    fig.tight_layout()
    fig.savefig(out_dir / "chart_age_vs_impact.png", dpi=160)
    plt.close(fig)


# =============================================================================
# 8. DEMO DATA (synthetic - lets you dry-run the whole pipeline today)
# =============================================================================
def make_demo_pack(folder: Path, seed=11, n=320):
    rng = np.random.default_rng(seed)
    folder.mkdir(parents=True, exist_ok=True)
    first = ["Aarav", "Vihaan", "Reyansh", "Arjun", "Kabir", "Ishaan", "Dev", "Rohan", "Karan", "Nikhil", "Sahil", "Tanmay",
             "Yash", "Harsh", "Manav", "Pranav", "Rudra", "Veer", "Om", "Ayaan", "Neel", "Jai", "Tejas", "Kunal"]
    last = ["Sharma", "Verma", "Iyer", "Nair", "Patel", "Yadav", "Singh", "Reddy", "Rao", "Mehta", "Gupta", "Das", "Khan",
            "Joshi", "Kulkarni", "Bhat", "Chauhan", "Thakur", "Pandey", "Menon", "Saini", "Dubey", "Tiwari", "Mishra"]
    combos = [(f, l) for f in first for l in last]
    rng.shuffle(combos)
    states = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel"]
    pl = []
    for i in range(n):
        f, l = combos[i]
        kind = rng.choice(["opener", "middle", "finisher", "pace", "spin", "allr"], p=[.17, .15, .15, .22, .21, .10])
        pl.append(dict(name=f"{f} {l}", kind=kind, skill=rng.normal(0, 1), state=states[i % 8],
                       age=float(np.clip(rng.normal(23.5, 3.8), 17, 34)), capped=rng.random() < .05,
                       btype={"pace": rng.choice(["Right-arm fast", "Left-arm fast-medium", "Right-arm medium"]),
                              "spin": rng.choice(["Right-arm leg-break", "Left-arm orthodox", "Right-arm off-break",
                                                  "Leg-break googly", "Mystery spin (carrom)"]),
                              "allr": "Right-arm off-break"}.get(kind, ""),
                       avail=rng.choice(["Contracted", "Released", "Unsold", "Unsigned", ""], p=[.25, .2, .2, .2, .15])))
    # plant a few young stars so the demo has something to find
    for j in range(8):
        pl[j]["age"] = float(rng.uniform(18, 21.5))
        pl[j]["skill"] = 2.2 + rng.random() * .6
        pl[j]["capped"] = False
        pl[j]["avail"] = "Unsold"
        pl[j]["kind"] = ["opener", "finisher", "pace", "spin"][j % 4]
        pl[j]["btype"] = {"pace": "Left-arm fast", "spin": "Mystery spin (carrom)"}.get(pl[j]["kind"], "")

    def rows_for(season, fmt, scale):
        bat, bowl = [], []
        for p in pl:
            if rng.random() > {"T20": .8, "LA": .6, "FC": .5}[fmt]:
                continue
            m = int(rng.integers(3, 12 if fmt == "T20" else 9))
            nm = {"T20": m, "LA": m, "FC": max(2, m // 2)}[fmt]
            sk = p["skill"]
            if p["kind"] in ("opener", "middle", "finisher", "allr"):
                inn = max(1, nm - int(rng.integers(0, 2)))
                per = {"T20": 16, "LA": 38, "FC": 85}[fmt]
                bf = int(inn * rng.uniform(.6, 1.3) * per)
                sr = {"T20": 128, "LA": 88, "FC": 52}[fmt] * (1 + .06 * sk) * rng.uniform(.93, 1.07)
                runs = int(bf * sr / 100)
                no = int(rng.integers(0, max(1, inn // 2 + (2 if p["kind"] == "finisher" else 0))))
                sixes = int(runs * (.10 if p["kind"] == "finisher" else .06) * (1 + .1 * sk) / 6 * 1.5)
                fours = int(runs * .35 / 4)
                r = dict(Player=p["name"], Team=p["state"], Season=season, Matches=nm, Innings=inn, NO=no, Runs=runs,
                         BF=bf, **{"4s": fours, "6s": sixes})
                if fmt == "T20":
                    sh = {"opener": (.62, .33, .05), "middle": (.15, .6, .25), "finisher": (.0, .35, .65),
                          "allr": (.1, .5, .4)}[p["kind"]]
                    mult = (1.05, .92, 1.32)
                    for ph, share, mu in zip(("PP", "Mid", "Death"), sh, mult):
                        b_ = int(bf * share)
                        r[f"{ph}_BF"] = b_
                        r[f"{ph}_Runs"] = int(b_ * sr / 100 * mu * rng.uniform(.95, 1.05))
                    r["Runs_vs_Spin"] = int(bf * .3 * sr / 100 * rng.uniform(.9, 1.1))
                    r["BF_vs_Spin"] = int(bf * .3)
                bat.append(r)
            if p["kind"] in ("pace", "spin", "allr"):
                ov = int(nm * (3.2 if p["kind"] != "allr" else 1.5)) + 1
                balls = ov * 6 + int(rng.integers(0, 6))
                base = {"T20": 8.2, "LA": 5.4, "FC": 3.1}[fmt]
                econ = base * (1 - .05 * sk) * rng.uniform(.93, 1.07)
                rc = int(balls * econ / 6)
                wk = int(rng.poisson(max(.2, balls / 6 * {"T20": .30, "LA": .17, "FC": .10}[fmt] * (1 + .12 * sk))))
                dots = int(balls * np.clip(rng.normal(.40 + .02 * sk, .03), .25, .6))
                r = dict(Player=p["name"], Team=p["state"], Season=season, Matches=nm,
                         Overs=f"{balls // 6}.{balls % 6}", Runs_Conceded=rc, Wkts=wk, Dots=dots)
                if fmt == "T20":
                    sh = (.35, .25, .40) if p["kind"] == "pace" else (.15, .75, .10)
                    mult = (.95, .93, 1.25)
                    for ph, share, mu in zip(("PP", "Mid", "Death"), sh, mult):
                        b_ = int(balls * share)
                        r[f"{ph}_Overs"] = f"{b_ // 6}.{b_ % 6}"
                        r[f"{ph}_Runs_Conceded"] = int(b_ * econ / 6 * mu * rng.uniform(.95, 1.05))
                        r[f"{ph}_Wkts"] = int(rng.poisson(max(.05, b_ / 6 * .3)))
                bowl.append(r)
        return pd.DataFrame(bat), pd.DataFrame(bowl)

    for season in ("2024-25", "2025-26"):
        for fmt, tag in (("T20", "smat"), ("LA", "vht"), ("FC", "ranji")):
            b, w = rows_for(season, fmt, 1)
            if season == "2025-26" and tag == "vht":     # messy-name test: 'F Last' initials
                b["Player"] = [x.split()[0][0] + " " + x.split()[1] if i % 9 == 0 else x for i, x in enumerate(b["Player"])]
            b.to_csv(folder / f"{tag}_{season}_batting.csv", index=False)
            w.to_csv(folder / f"{tag}_{season}_bowling.csv", index=False)
    pd.DataFrame([dict(Player=p["name"], DOB=(pd.Timestamp("2026-12-16") - pd.Timedelta(days=int(p["age"] * 365.25))).date(),
                       Capped="Y" if p["capped"] else "N", Bowl_Type=p["btype"], Availability=p["avail"])
                  for p in pl]).to_csv(folder / "players_master.csv", index=False)
    pd.DataFrame([dict(Player=p["name"], skill=p["skill"], kind=p["kind"], age=p["age"]) for p in pl]) \
        .to_csv(folder.parent / (folder.name + "_TRUTH.csv"), index=False)
    log(f"demo pack written to {folder}")


# =============================================================================
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="RR War Room - uncapped youth scouting pipeline")
    ap.add_argument("--data", type=Path, default=Path("./pack"))
    ap.add_argument("--out", type=Path, default=Path("./out"))
    ap.add_argument("--auction-date", type=str, default="2026-12-16")
    ap.add_argument("--age-mode", choices=["exp", "step"], default="exp")
    ap.add_argument("--strict-availability", action="store_true")
    ap.add_argument("--unknown-capped", choices=["exclude", "flag"], default="exclude",
                    help="'flag' keeps players whose capped status is missing (verify by hand!)")
    ap.add_argument("--demo", action="store_true", help="generate a synthetic pack and run on it")
    a = ap.parse_args()
    cfg = Config(auction_date=date.fromisoformat(a.auction_date), age_mode=a.age_mode,
                 availability_mode="strict" if a.strict_availability else "lenient",
                 unknown_capped_policy=a.unknown_capped)
    if a.demo:
        a.data, a.out = Path("./demo_pack"), Path("./demo_out")
        make_demo_pack(a.data)
    top, _ = run_pipeline(a.data, a.out, cfg, demo=a.demo)
    with pd.option_context("display.width", 260, "display.max_colwidth", 60):
        print("\n" + "="*85)
        print("★★★  RAJASTHAN ROYALS WAR ROOM — TOP 10 TARGETS & VALUATION ENGINE  ★★★")
        print("="*85)
        cols_to_print = ["rank", "player", "age", "role", "tdsi", "market_value_cr", "expected_bid_lakhs", "walk_away_limit_lakhs", "surplus_value_cr", "evidence"]
        rename_print = {
            "market_value_cr": "Valuation(₹Cr)",
            "expected_bid_lakhs": "Target(₹L)",
            "walk_away_limit_lakhs": "WalkAway(₹L)",
            "surplus_value_cr": "Surplus(₹Cr)"
        }
        df_print = top[cols_to_print].rename(columns=rename_print).round(2)
        print(df_print.to_string(index=False))
        print("="*85 + "\n")
