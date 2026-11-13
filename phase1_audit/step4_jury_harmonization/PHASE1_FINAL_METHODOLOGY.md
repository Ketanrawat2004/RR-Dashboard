# PHASE 1 — FINAL METHODOLOGY DOCUMENT
**Project:** Rajasthan Royals SupeRR Selector Season 2  
**Document:** Authoritative Methodology Specification  
**Location:** `phase1_audit/step4_jury_harmonization/PHASE1_FINAL_METHODOLOGY.md`  
**Status:** CONSOLIDATED & HARMONIZED — PHASE 1 AUDIT COMPLETE  
**Compliance Standard:** Strictly Read-Only Audit & Verification

---

## 1. DATASET PROVENANCE & ENVIRONMENT VERIFICATION

The performance modeling engine is built exclusively upon the six official Rajasthan Royals datasets located in the root repository `C:\RR NEW\`.

#### Table 1.1: Official Dataset Provenance & Cryptographic Verification
| Dataset Filename | Exact Path | File Size | SHA-256 Checksum | Data Records | Physical Lines | Accessibility |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **`ball_by_ball.csv`** | `C:\RR NEW\ball_by_ball.csv` | 41,071,609 bytes | `a3926f49d2c684dca2a5d2de535a02c5ee46ea654ca1e79dd31c69e7544e9889` | 200,999 | 201,000 | Verified Read-Only |
| **`matches.csv`** | `C:\RR NEW\matches.csv` | 131,876 bytes | `62562ec8067ae2c48d613e5c7075cce963cfae2e6d97c672b1527786419fecff` | 883 | 884 | Verified Read-Only |
| **`competitions.csv`** | `C:\RR NEW\competitions.csv` | 9,997 bytes | `ee95a9d20c52a0a2df362706346aa8624195155f36e84d9c4e0915ca850d995c` | 141 | 142 | Verified Read-Only |
| **`teams.csv`** | `C:\RR NEW\teams.csv` | 12,309 bytes | `e3505c2a1e809311e9f168fbc97c385a4cf6858e6e58b14644a835b0b2e3f538` | 353 | 354 | Verified Read-Only |
| **`playing_eleven.csv`** | `C:\RR NEW\playing_eleven.csv` | 1,023,382 bytes | `25bc4a0dfcaec487f54c330c6a512702747195b084931bc7754f21d6fe6942ad` | 28,381 | 28,382 | Verified Read-Only |
| **`competition_team_player_mapping.csv`** | `C:\RR NEW\competition_team_player_mapping.csv` | 338,409 bytes | `068bb9ee3331b52f416c1410129cf653b6fa0f911ec7176461fbdd863df7e193` | 6,413 | 6,414 | Verified Read-Only |

---

## 2. DELIVERY POPULATION & LEGAL ACCOUNTING RULES

The exact delivery accounting established in Step 3.2 serves as the single source of truth across all models:
- **Total Deliveries Recorded:** Exactly **200,999 deliveries** across 867 unique matches.
- **Regular Innings (Innings 1 & 2):** **200,961 deliveries** (105,727 in Innings 1; 95,234 in Innings 2).
- **Super Overs (Innings 3 & 4):** **38 deliveries** (isolated in `phase1_audit/so_bbb.pkl`).
- **Batting Legal Balls Faced:** **193,251 deliveries** in regular innings (193,285 total). Under Law 22 of the MCC Laws of Cricket, wides are **not** balls faced. Under Law 21, no-balls **are** legal balls faced by the batter.
- **Bowling Legal Deliveries Bowled:** **192,412 deliveries** in regular innings (192,445 total). Under cricket laws, bowlers must re-bowl both wides and no-balls; therefore, legal bowling balls strictly exclude both 7,710 wides and 839 no-balls ($200,961 - 7,710 - 839 = \mathbf{192,412}$).
- **Extras Classification:**
  - `wide`: 7,710 regular deliveries (+1 run to bowler, +0 to batter).
  - `Overstep`: 576 regular deliveries (front-foot crease violation; +1 run to bowler, ball faced by batter).
  - `other`: 263 regular deliveries (+1 run to bowler, ball faced by batter; proven to be no-balls by 135 off-the-bat scoring events).
  - `byes`: 529 deliveries (fielding extra; excluded from bowler conceded runs).
  - `legbyes`: 2,747 regular deliveries (fielding extra; excluded from bowler conceded runs).
  - `Penalty`: 1 regular delivery (team penalty extra; excluded from bowler conceded runs).
- **Dismissal Classification:** Exactly **10,868 regular dismissals**:
  - Bowler-credited wickets: **10,261** (Caught: 7,549; Bowled: 1,772; LBW: 709; Stumped: 214; Hit Wicket: 17).
  - Non-bowler dismissals: **607** (RunOut: 598; Retired Out: 6; Obstructing Field: 3).

---

## 3. SUPER OVER TREATMENT

- Super Over deliveries (38 balls across 6 matches, 12 innings) represent an ultra-extreme leverage state with unique incentives (free hits, unlimited resource spending, 2-wicket team innings cap).
- In accordance with rigorous statistical practices, Super Over deliveries are **isolated from regular-innings model training** to prevent extreme 6-ball outliers from distorting general baseline distributions.
- Super Over aggregates are maintained in a dedicated data structure (`so_bbb.pkl`) and made accessible as supplementary evidence for clutch tie-breaking.

---

## 4. PRESSURE DEFINITIONS: BPI & BWPI

Pressure is defined as situational leverage—the degree to which the outcome of a single delivery swings the match:
- **Batting Pressure Index (BPI):** Evaluated strictly on legal balls faced by batters ($n = 193,251$).
  $$\text{BPI} = f(\text{Phase}, \text{Balls Remaining}, \text{Wickets in Hand}, \text{Required Run Rate}, \text{Target Closeness})$$
  High pressure is defined as $\text{BPI} \ge 75\text{th percentile}$ ($BPI \ge 55.64$).
- **Bowling Pressure Index (BWPI):** Evaluated across all bowling deliveries ($n = 200,961$).
  $$\text{BWPI} = f(\text{Phase}, \text{Balls Remaining}, \text{Wickets in Hand}, \text{Required Run Rate}, \text{Defending Total Margin})$$
  High pressure is defined as $\text{BWPI} \ge 75\text{th percentile}$ ($BWPI \ge 56.30$).
- **Situational Scope:** High-pressure deliveries capture death overs (Overs 17–20), high-RRR chases (>9.5 RRR in Innings 2), and high-stress collapses in the powerplay (e.g. 25/3).

---

## 5. CONTEXTUAL EXPECTED PERFORMANCE MODELING

- **Target Variables:**
  - Batting: Expected runs off the bat per legal delivery ($\text{exp\_bat\_runs}$).
  - Bowling: Expected bowler-conceded runs per delivery ($\text{exp\_bowl\_runs}$).
  - Bowler Wicket: Expected probability of a bowler-credited dismissal ($\text{exp\_bowl\_wkt}$).
- **Feature Set (19 Pre-Delivery Contextual Variables):**
  - Temporal: `innings`, `overid`, `over_ball_num`, `legal_balls_before`, `balls_remaining_pre`.
  - Match State: `score_before`, `wkts_before`, `wkts_in_hand_pre`, `crr_pre_smoothed`.
  - Chase Context: `is_inn2`, `target_clean`, `runs_req_clean`, `rrr_clean`, `chase_stress`.
  - Phase Interactions: `pp_flag`, `mid_flag`, `death_flag`, `death_wkts`, `season_num`.
  - **Zero Data Leakage:** All 19 features are strictly observable before the delivery run-up begins.
- **Model Architecture:**
  - Non-linear Histogram Gradient Boosted Regressors (`HistGBR`) with monotonic score constraints.
  - Cross-Validation: 5-Fold `GroupKFold` split on `match_id` (867 independent clusters).
  - Out-of-Fold Performance: RMSE 1.7284 (batting) and 1.7310 (bowling), outperforming Phase $\times$ Wickets baselines across all 5 folds ($p < 10^{-60}$ on paired match-level t-tests).

---

## 6. INDIVIDUAL BATTING PERFORMANCE METHODOLOGY: PURE RAE

- **Residual Definition:**
  $$\text{RAE}_i = \text{Actual Runs}_i - \text{Expected Runs}_i$$
- **Rejection of "Wicket-Saved" Component:**
  - Audited in Step 3.1: Batter dismissal hazard models achieve a Brier Skill Score ($BSS$) of only $+0.77\%$. Delivery-level outs are near-random Bernoulli events.
  - Scaling wicket survival to run equivalence ($1 \text{ wkt} \approx 12 \text{ runs}$) heavily distorts ratings, rewarding lucky small-sample survival and penalizing elite death-over boundary hitters (Russell, Maxwell, Klaasen).
  - **Decision:** **Adopt Pure Shrunk RAE.** All batting evaluations are based entirely on contextual run scoring above expectation.

---

## 7. INDIVIDUAL BOWLING PERFORMANCE METHODOLOGIES

To provide complete analytical transparency, bowling performance is evaluated under two distinct, principled frameworks:

### Framework A: Pure RPAE (Run Prevention Above Expected)
$$\text{RPAE}_i = \text{Expected Conceded Runs}_i - \text{Actual Conceded Runs}_i$$
- Evaluates a bowler's ability to restrict scoring relative to delivery context.
- **Primary Beneficiary:** Elite economy suppressors (e.g. Jasprit Bumrah, Maheesh Theekshana, Sunil Narine).

### Framework B: Balanced Composite (RPAE + WAE)
$$\text{WAE}_i = \text{Actual Bowler Wickets}_i - \text{Expected Wickets}_i$$
$$\text{Composite Score} = 0.60 \times \text{Shrunk RPAE Rate} + 0.40 \times (\text{Shrunk WAE Rate} \times 12.0)$$
- **Wicket-to-Run Equivalence Factor:** In T20 cricket, taking a wicket saves an empirical average of $12.0$ runs over the remainder of an innings.
- **Disclosed Limitation:** The delivery-level bowler wicket model has an AUC of $0.5854$ and a BSS of $+0.55\%$. While aggregate decile calibration is strong ($ECE < 0.0003$), single-ball wicket predictability is weak.
- **Primary Beneficiary:** Elite strike bowlers who take high-volume pressure wickets (e.g. Umran Malik, Mayank Yadav).

---

## 8. EMPIRICAL BAYES SHRINKAGE FRAMEWORK

To prevent small-sample anomalies from topping leaderboard rankings, observed residuals are shrunk toward the population mean ($0.0$):
$$\text{Shrunk Score} = \left(\frac{\sum \text{Residual}}{N + M_0}\right) \times 100$$
- **Prior Strength Parameter ($M_0$):**
  - Batting RAE: $M_0 = 150.0$ balls faced.
  - Bowling RPAE: $M_0 = 150.0$ legal deliveries bowled.
  - Bowling WAE: $M_w = 100.0$ legal deliveries bowled.
- **Validation:** 50 Monte Carlo randomized split-half splits confirmed that $M_0 = 150$ maximizes out-of-sample Spearman-Brown rank reliability while preventing low-volume runaway ratings.

---

## 9. MATCH-CLUSTERED BOOTSTRAP UNCERTAINTY ESTIMATION

- Classical unclustered standard errors ($\sigma_w / \sqrt{N + M_0}$) underestimate variance by $25\%\text{--}40\%$ by treating deliveries as independent.
- **Engine:** A 500-replicate non-parametric Match-Clustered Bootstrap resamples entire matches with replacement:
  - Preserves intra-match correlations (dew, pitch deterioration, boundary sizes).
  - Produces cluster-robust $95\%$ empirical confidence intervals for player scores.
  - Produces non-parametric $90\%$ rank bounds (e.g. #1 to #25) and Top-10 inclusion probabilities.

---

## 10. ELIGIBILITY CRITERIA & SAMPLE-SIZE GOVERNANCE

To qualify for official ranking:
1. **Career Volume Gate:** $\ge 300$ legal balls faced (batting) or legal deliveries bowled (bowling).
2. **Pressure Volume Gate:** $\ge 40$ high-pressure legal balls.
3. **Mandatory Sample-Size Badging:**
   - **High Volume ($N \ge 150$ balls):** Statistically robust; tight confidence intervals.
   - **Moderate Volume ($75 \le N < 150$ balls):** Reliable sample; moderate interval spread.
   - **Small Sample Caution ($40 \le N < 75$ balls):** High talent upside, but wide uncertainty bounds. UI must display warning badge.

---

## 11. THRESHOLD SENSITIVITY GOVERNANCE

- The Top 25% cutoff is **NOT** a biological or mathematical constant; it is a **principled benchmark design choice**.
- Sensitivity tests across Top 15%, 20%, 25%, and 30% show high rank stability ($\rho \approx 0.89\text{--}0.91$).
- **Mandate:** Production user interfaces should include a dynamic sensitivity slicer (Top 20% vs Top 25% vs Top 30%) to allow decision-makers to verify ranking stability under alternate leverage thresholds.

---

## 12. DISTINCTION BETWEEN VALIDATED CALCULATIONS AND DESIGN CHOICES

#### Table 12.1: Methodological Classification
| Component | Classification | Mathematical Justification & Evidence |
| :--- | :--- | :--- |
| **Delivery Accounting & Extras** | **Validated Calculation** | Exact 1-to-1 match with MCC cricket law and physical CSV line counts. |
| **HistGBR Expected Runs Model** | **Validated Calculation** | Out-of-fold RMSE 1.7284 ($p < 10^{-60}$ across 867 independent match clusters). |
| **Match-Clustered Bootstrap CIs** | **Validated Calculation** | Clustered resampling accounts for pitch/dew intra-match correlation. |
| **Pure RAE Batting Metric** | **Validated Calculation** | Eliminates binary dismissal noise ($BSS < 0.8\%$). Mathematically unbiased. |
| **Top 25% Pressure Threshold** | **Design Choice** | Maximizes high-leverage delivery volume ($n=48,323$) while qualifying 160+ players. |
| **Prior Strength ($M_0 = 150$)** | **Design Choice** | Maximizes out-of-sample Spearman-Brown split-half reliability. |
| **60/40 Bowling Composite Weights**| **Design Choice** | Balances economic run suppression ($60\%$) with wicket value ($40\%$). |
| **Wicket Equivalence ($12$ Runs)** | **Design Choice** | Empirical average of runs saved by a wicket across T20 match historical data. |
| **Career $\ge 300$, Pressure $\ge 40$** | **Design Choice** | Pragmatic eligibility filter ensuring sufficient sample exposure. |

