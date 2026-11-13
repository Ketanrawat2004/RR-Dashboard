# BACKWARD-COMPATIBLE PLAYER DATA SCHEMA SPECIFICATION
**Project:** Rajasthan Royals SupeRR Selector Season 2  
**Document:** Database Schema & Field Mapping Specification  
**Location:** `phase1_audit/phase2a_blueprint/PLAYER_SCHEMA_MAPPING.md`  
**Compliance Standard:** Strictly Read-Only Audit & Verification  
**Phase:** Phase 2A — Implementation Blueprint  

---

## 1. EXECUTIVE SUMMARY

The current production website and its presentation scripts (`build_clean_submission_pptx.py`, `build_player_pages_and_dashboard.py`, `fix_dashboard_and_wagon.py`) rely on `players_db.json`. 

To prevent runtime errors (`KeyError`, JavaScript `undefined`), Phase 2 must deploy a **backward-compatible superset schema**. This schema guarantees that:
1. Every legacy field currently accessed by frontend scripts and Python build pipelines remains present and typed correctly.
2. Every verified Phase 1 Step 4 statistical modeling metric (Shrunk RAE, RPAE, Composite, Clustered CIs, Rank Bounds, Sample Badges) is cleanly integrated.
3. Legacy scripts continue executing without breakage, while modern dashboards gain access to mathematically rigorous contextual metrics.

---

## 2. LEGACY SCHEMA ANALYSIS (`players_db.json`)

The existing `players_db.json` contains exactly 20 player records. Each record possesses 26 fields across numerical, categorical, and qualitative dimensions:

#### Table 2.1: Legacy Field Inventory & Usage
| Field Name | Data Type | Example Value | Where Used in Codebase |
| :--- | :---: | :--- | :--- |
| `name` | `str` | `"Shivam Dube"` | Table display, page title, modal, PPTX title |
| `key` | `str` | `"shivam_dube"` | URL routing (`players/<key>.html`), image matching |
| `category` | `str` | `"Batter"` | Tab segregation (`Batter` vs `Bowler`) |
| `rank` | `int` | `1` | Leaderboard ordering, `data-rank` attribute |
| `teams` | `str` | `"Chennai Super Kings, India"` | Table franchise column, dossier team badges |
| `role_desc` | `str` | `"Specialist Boundary Striker vs Spin"` | Subtitle below name in table and header |
| `tactical_role`| `str` | `"Middle-Overs Spin Enforcer"` | Dossier tactical analysis section |
| `total_m` | `int` | `43` | Dossier career match statistics |
| `base_wr` | `float` | `54.3` | Baseline performance column (`BaselineWin%`) |
| `hp_m` | `int` | `18` | Leverage match volume column (`LeverageMatches`) |
| `hp_wr` | `float` | `66.7` | High-pressure performance column (`PressureWin%`) |
| `lift` | `float` | `12.4` | Performance differential tag (`Win Diff (Δ)`) |
| `mom_hp` | `int` | `1` | Match awards column (`MatchAwards`) |
| `ko_wr` | `float` | `100.0` | Playoff performance column (`PlayoffWin%`) |
| `cppi` | `float` | `66.81` | Overall score column (`CPPIScore`), `data-index` |
| `bayes_hp_wr` | `float` | `62.15` | Legacy shrunk metric |
| `bid_ceiling` | `str` | `"₹11.5 - 13.0 Cr"` | Tactical XI auction recommendation card |
| `tagline` | `str` | `"The Elite Spin Destroyer"` | Dossier hero section banner |
| `summary` | `str` | `"High-leverage middle-overs disruptor..."` | Dossier executive overview paragraph |
| `why_chose` | `str` | `"Unique spin-hitting ability..."` | Dossier selection justification |
| `why_not_others`| `str`| `"Superior boundary percentage..."` | Dossier competitive exclusion rationale |
| `rr_fit` | `str` | `"Complements Samson and Parag..."` | Dossier tactical squad alignment |
| `verdict` | `str` | `"MUST BUY (Core Middle-Order Target)"` | Dossier decision badge |
| `rr_management_summary` | `str` | `"Target aggressively in early rounds..."`| War room auction briefing card |
| `key_tactical_skill` | `str` | `"6-hitting against SLA and leg-spin"` | Tactical breakdown bullet point |
| `comparative_analysis` | `str` | `"Outperforms alternatives by 18%..."` | Statistical benchmark dossier card |

---

## 3. STEP 4 MODELING METRICS INVENTORY

The authoritative Step 4 deliverables introduce 27 verified delivery-level performance fields:

#### Table 3.1: Step 4 Modeling Columns
| Step 4 CSV Column | Target Discipline | Mathematical Meaning |
| :--- | :--- | :--- |
| `player_id` | All | Official tournament player identifier |
| `player_name` | All | Canonical full player name |
| `franchises` | All | Semicolon-delimited team affiliations |
| `career_bf` / `career_b` | Bat / Bowl | Total legal deliveries faced / bowled in regular innings ($\ge 300$) |
| `pressure_bf` / `pressure_b`| Bat / Bowl | High-pressure legal deliveries faced / bowled ($\ge 40$) |
| `career_sr` / `career_econ`| Bat / Bowl | Career unadjusted strike rate / economy rate |
| `career_exp_sr` / `career_exp_econ`| Bat / Bowl | Career contextual expected strike rate / economy rate |
| `career_rae_rate` / `career_rpae_rate`| Bat / Bowl | Career unadjusted run residual per 100 balls |
| `pressure_sr` / `pressure_econ` | Bat / Bowl | Pressure unadjusted strike rate / economy rate |
| `pressure_exp_sr` / `pressure_exp_econ` | Bat / Bowl | Pressure contextual expected strike rate / economy rate |
| `raw_pressure_rae_rate` / `raw_pressure_rpae_rate` | Bat / Bowl | Pressure unadjusted run residual per 100 balls |
| `clutch_rae_lift` / `clutch_rpae_lift` | Bat / Bowl | Clutch Lift: Pressure residual minus non-pressure residual |
| `shrunk_rae_score` / `shrunk_rpae_score` | Bat / Bowl | Empirical Bayes shrunk run score ($M_0 = 150$) |
| `pressure_wkts` / `pressure_exp_wkts` | Bowl (Comp) | Actual vs expected bowler-credited pressure dismissals |
| `pressure_wae` | Bowl (Comp) | Excess wickets above expected ($\text{Actual} - \text{Exp}$) |
| `shrunk_wae_rate` | Bowl (Comp) | Empirical Bayes shrunk excess wickets per 100 balls ($M_w = 100$) |
| `wae_run_equivalent` | Bowl (Comp) | WAE converted to runs saved ($12.0 \times \text{Shrunk WAE Rate}$) |
| `composite_score` | Bowl (Comp) | Balanced Composite: $0.60 \times \text{RPAE} + 0.40 \times \text{WAE Run Eq}$ |
| `bootstrap_mean` | All | Mean of 500 match-clustered bootstrap resamples |
| `bootstrap_se` | All | Standard error of match-clustered bootstrap |
| `ci95_lower` / `ci95_upper`| All | Empirical 95% match-clustered confidence interval bounds |
| `rank_ci_90` | All | Non-parametric 90% rank interval (e.g. `#1 to #25`) |
| `top10_prob_pct` | All | Probability of finishing inside Top 10 across bootstrap resamples |
| `sample_size_badge` | All | Volume tier badge (`High Volume`, `Moderate Volume`, `Small Sample Caution`) |

---

## 4. UNIFIED BACKWARD-COMPATIBLE SCHEMA SPECIFICATION

To ensure full backward compatibility with legacy scripts while exposing all Phase 1 Step 4 analytics, the expanded `players_db.json` record schema is defined below:

```json
{
  "// LEGACY CORE IDENTIFIERS": "Preserved for existing frontend DOM and scripts",
  "name": "Andre Russell",
  "key": "andre_russell",
  "category": "Batter",
  "rank": 1,
  "teams": "Kolkata Knight Riders, West Indies",
  "role_desc": "Elite High-Leverage Finisher & Death-Over Striker",
  
  "// LEGACY STATISTICAL FIELDS": "Mapped to prevent undefined/KeyError in legacy templates",
  "total_m": 127,
  "hp_m": 323,
  "base_wr": 126.69,
  "hp_wr": 165.63,
  "lift": 38.94,
  "mom_hp": 8,
  "ko_wr": 62.5,
  "bayes_hp_wr": 26.59,
  "cppi": 26.59,
  
  "// PHASE 1 STEP 4 STATISTICAL MODELING ENGINE FIELDS": "New authoritative data",
  "player_id": 1318,
  "career_balls": 1198,
  "career_runs": 2262,
  "career_sr": 188.81,
  "career_exp_sr": 134.42,
  "career_rae_rate": 54.39,
  "pressure_balls": 323,
  "pressure_runs": 535,
  "pressure_exp_runs": 409.21,
  "pressure_sr": 165.63,
  "pressure_exp_sr": 126.69,
  "pressure_rae": 125.79,
  "raw_pressure_rate": 38.94,
  "non_pressure_sr": 197.37,
  "clutch_lift": -3.42,
  "shrunk_score": 26.59,
  "shrunk_rae_score": 26.59,
  "bootstrap_mean": 25.68,
  "bootstrap_se": 8.13,
  "ci95_lower": 9.23,
  "ci95_upper": 41.02,
  "rank_ci_90": "#1 to #25",
  "top10_prob_pct": 84.8,
  "sample_size_badge": "High Volume (N >= 150)",
  
  "// BOWLING SPECIFIC COMPOSITE FIELDS (Null for Batters)": "Harmonized Framework",
  "bowling_framework": null,
  "pressure_wkts": null,
  "pressure_exp_wkts": null,
  "pressure_wae": null,
  "shrunk_wae_rate": null,
  "wae_run_equivalent": null,
  "composite_score": null,
  
  "// QUALITATIVE TACTICAL FIELDS": "Populated for dossier and presentation cards",
  "bid_ceiling": "₹16.0 - 18.0 Cr",
  "tactical_role": "Death-Overs Power Match-up Dominator",
  "tagline": "The Undisputed Death-Overs Force",
  "summary": "Statistically proven as the highest-impact boundary striker under high pressure in tournament history...",
  "why_chose": "Generated +125.79 runs above contextual expectation with an 84.8% Top-10 bootstrap inclusion probability...",
  "why_not_others": "Outstrips all alternatives in death-over boundary strike rate by >25 runs per 100 balls...",
  "rr_fit": "Provides Rajasthan Royals with unmatched finishing firepower alongside Riyan Parag and Shimron Hetmyer...",
  "verdict": "PRIORITY RETENTION / TOP AUCTION TARGET",
  "rr_management_summary": "Unmatched leverage scorer. Deploy strictly in overs 16-20 to exploit pace at the death.",
  "key_tactical_skill": "Boundary striking vs high-pace hard lengths in Overs 17-20",
  "comparative_analysis": "Exceeds median death-overs batsman strike rate by +38.9 runs per 100 balls facing elite bowling."
}
```

---

## 5. BOWLER SCHEMA MAPPING (DUAL FRAMEWORK HANDLING)

Bowlers require an explicit field `bowling_framework` to denote whether their primary display score represents Pure RPAE (`"Pure_RPAE"`) or Balanced Composite (`"Balanced_Composite"`):

#### Table 5.1: Bowler Framework Field Population
| Field | Bowler in Pure RPAE Ranking (e.g. Bumrah) | Bowler in Balanced Composite Ranking (e.g. Umran Malik) |
| :--- | :---: | :---: |
| `category` | `"Bowler"` | `"Bowler"` |
| `cppi` | `17.54` (`shrunk_rpae_score`) | `24.75` (`composite_score`) |
| `shrunk_score` | `17.54` | `24.75` |
| `shrunk_rpae_score` | `17.54` | `11.81` |
| `composite_score` | `10.82` | `24.75` |
| `bowling_framework` | `"Pure_RPAE"` | `"Balanced_Composite"` |
| `pressure_wkts` | `19.0` | `14.0` |
| `pressure_exp_wkts` | `19.82` | `6.23` |
| `pressure_wae` | `-0.82` | `+7.77` |
| `wae_run_equivalent` | `-3.38` | `+44.17` |

---

## 6. FIELD CONFLICT PREVENTION & VALIDATION CHECKS

1. **Float vs String Formatting:** All financial auction numbers (`bid_ceiling`) remain formatted as display strings (`"₹12.0 - 14.5 Cr"`), preventing Python `pptx` formatting crashes.
2. **Missing Key Guard:** Every single record in `players_db.json` must contain all 36 keys defined above. If a field is not applicable (e.g., `pressure_wkts` for a batter), it must be assigned `null` (`None` in Python), never omitted.
3. **Key Slug Normalization:** `key` must strictly follow `re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')` to guarantee 1-to-1 match with `players/<key>.html` file paths and `player_images/<key>.png`.

