# PHASE 1 — EXISTING WEBSITE PRESERVATION & RE-INTEGRATION PLAN
**Project:** Rajasthan Royals SupeRR Selector Season 2 — Phase 1 Step 4  
**Document:** Technical Specification for Frontend Re-Integration  
**Location:** `phase1_audit/step4_jury_harmonization/WEBSITE_PRESERVATION_PLAN.md`  
**Status:** COMPLETE — STRICT PRESERVATION DESIGN (NO REDESIGN)  

---

## 1. PRESERVATION PRINCIPLES & GOVERNANCE

> [!IMPORTANT]
> **STRICT PRESERVATION RULE:**  
> In accordance with Phase 1 constraints, **zero frontend files (`index.html`, `players_db.json`) have been modified**. This document serves exclusively as an architectural blueprint for a future Phase 2 implementation phase, demonstrating how verified Step 4 calculations will connect to the existing website without altering layout, CSS, routes, or user interactions.

### Non-Negotiable Constraints:
1. **Preserve Layout & Structure:** The grid structure, responsive container (`max-width: 1400px`), header branding, and dark/light mode CSS variables must remain 100% intact.
2. **Preserve Navigation & View Toggles:** The section navigation buttons (`Batting Evaluation`, `Bowling Evaluation`, `IPL 2027 RR Squad & Auction Strategy`, `Leverage Variance Audit`) and their JavaScript toggles (`showSection()`) must remain identical.
3. **Preserve Slicers & Filtering:** The search bar (`#filterInput`), role filter dropdown (`#roleSlicer`), sort dropdown (`#sortSlicer`), and `resetSlicers()` must function exactly as currently implemented.
4. **Preserve Interactive Modals:** Player profile cards and detailed view popups must be populated with verified individual metrics without changing modal DOM structures.

---

## 2. RE-INTEGRATION ARCHITECTURE & DATA MAPPING

### 2.1 Table Structure Mapping (`table-batters` & `table-bowlers`)
The existing table in `index.html` contains 11 columns designed for the legacy CPPI win-rate metrics. In a future implementation phase, these exact columns will be reconnected to verified ball-by-ball metrics:

#### Table 2.1: Column-by-Column Frontend Reconnection Blueprint
| Existing Table Column Header | Current Legacy Data Field | Verified Step 4 Replacement Metric | Cricket & Statistical Rationale |
| :--- | :--- | :--- | :--- |
| **`#`** | `rank` | `rank` (Pure RAE / Composite) | Official leaderboard standing. |
| **`Player & Role`** | `name` + `role_desc` | `player_name` + Tactical Role | Preserves player branding and squad assignment. |
| **`Franchise / State`** | `teams` | `franchises` | Complete team provenance. |
| **`LeverageMatches`** | `hp_m` (Match count) | **`pressure_bf` / `pressure_b` ($N$)** | **Replaces match count with true delivery sample volume.** |
| **`PressureWin%`** | `hp_wr` (Team win rate) | **`pressure_sr` / `pressure_econ`** | **Replaces team win rate with actual performance rate.** |
| **`BaselineWin%`** | `base_wr` (Team win rate) | **`pressure_exp_sr` / `exp_econ`** | **Replaces uncalibrated win rate with contextual expected baseline.** |
| **`Win Diff(Δ)`** | `lift` (Team win diff) | **`raw_pressure_rae_rate` / `rpae`** | **True individual performance lift over contextual expectation.** |
| **`MatchAwards`** | `mom_hp` (MoM count) | **`sample_size_badge`** | **Displays sample reliability badge (High / Moderate / Small Sample).** |
| **`PlayoffWin%`** | `ko_wr` (Playoff win rate) | **`ci95_lower` to `ci95_upper`** | **Replaces uncalibrated playoff rate with 95% Cluster Bootstrap CI.** |
| **`CPPIScore`** | `cppi` (Legacy win-rate) | **`shrunk_rae_score` / `composite`** | **Verified Empirical Bayes shrunk individual score ($M_0 = 150$).** |
| **`Action`** | Modal trigger button | Profile modal trigger button | Unchanged interactive behavior. |

---

## 3. IDENTIFICATION OF RETENTION VS REPLACEMENT COMPONENTS

### 3.1 Existing Features to Preserve Unchanged
- **Header & Visual Identity:** Rajasthan Royals pink (`#EB1A8D`), navy (`#09090B`), and gold branding accents.
- **Client-Side Slicing Engine:** The JavaScript search query parsing and DOM row visibility filtering logic.
- **Section Visibility Management:** The single-page architecture switching between Batters, Bowlers, Squad Strategy, and Audit views.
- **Responsive Table Layouts:** The horizontal scrolling behavior and mobile-friendly column sizing.

### 3.2 Unsupported Legacy Metrics to Retire
The following legacy fields from `players_db.json` will be retired because they represent flawed team attribution rather than individual performance:
- `base_wr` (Career team win percentage).
- `hp_wr` (High-pressure team win percentage).
- `lift` (Win percentage difference).
- `ko_wr` (Knockout match win percentage).
- `cppi` (Composite Pressure Performance Index derived from team win rates).

### 3.3 Enhanced Components for Phase 2 Integration
1. **Dynamic Threshold Slicer:**  
   Add a sleek 3-way toggle button to the filter panel: `[ Top 20% | Top 25% (Default) | Top 30% ]`. This connects directly to the sensitivity tables created in Step 3.1 and Step 3.2, giving decision-makers immediate visibility into rank stability.
2. **Dual-Ranking Bowling Toggle:**  
   Add a simple radio switch above `table-bowlers`: `(•) Pure Run Prevention (Bumrah #1)  ( ) Balanced Composite (Umran #1)`. This resolves the domain tension between run suppression and wicket strike-rate.
3. **Cluster-Robust Uncertainty Visualizer:**  
   Inside the player profile modal, embed the forest-plot confidence interval from `04_bootstrap_cluster_ci_and_stability.png`, showing the user the exact 95% uncertainty interval and 90% rank interval.

---

## 4. EXACT FILES TO BE MODIFIED IN PHASE 2 (FUTURE IMPLEMENTATION)

When Phase 2 website implementation is officially authorized by the user, the following exact files will be updated:
1. `players_db.json`: Replace the 20 legacy win-rate JSON objects with the full, verified Step 4 player records (163 qualified batters and 179 qualified bowlers) containing ball-by-ball RAE, RPAE, bootstrap CIs, and sample badges.
2. `index.html`: Update the table column header labels from legacy win-rate text (`PressureWin%`, `CPPIScore`) to verified analytical text (`Pressure SR/Econ`, `Context Expected`, `Shrunk RAE/RPAE Score`), and point JavaScript table-render functions to the updated JSON keys.

No other files or routes will require alteration.

