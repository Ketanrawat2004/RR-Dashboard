# Rajasthan Royals — SupeRR Selector Season 2
### Identifying the Most Reliable Players Under Pressure | Ball-by-Ball Quantitative Analytics

**Candidate:** Ketan Rawat (B.Tech ECE, NIT Jamshedpur)  
**Competition:** SupeRR Selector Season 2 — Rajasthan Royals Analytics Challenge  
**Live War Room Terminal:** [https://rr-dashboard.onrender.com/](https://rr-dashboard.onrender.com/)  
**GitHub Repository:** [https://github.com/Ketanrawat2004/RR-Dashboard](https://github.com/Ketanrawat2004/RR-Dashboard)  

---

## Executive Summary

Traditional cricket metrics like raw batting strike rates and bowling economy rates fail to capture true pressure performance. Stat-padding in low-leverage phases masks players who falter when matches hang in the balance, while harsh match outcomes unfairly penalize elite players whose teammates concede games at the other end.

This project implements an end-to-end, ball-by-ball quantitative evaluation system across **200,961 legal deliveries from 867 senior T20 fixtures (IPL and senior T20 Internationals, 2022–2026)**. By isolating acute pre-delivery match leverage states and establishing context-conditioned baseline expectations via cross-validated machine learning, we evaluate true individual impact stabilized by **Empirical Bayes shrinkage** and quantified by **1,000-replicate match-clustered bootstrap uncertainty distributions**.

---

## Authoritative Top-10 Leaderboards

### 1. Top 10 Batters Under Pressure (Runs Above Expectation &bull; Shrunk RAE)
*Evaluated across qualified high-leverage batters with empirical Bayesian shrinkage ($M_0 = 150$ deliveries) to eliminate low-sample noise.*

| Rank | Player | Franchise / Country | Pressure Deliveries | Pressure SR | Expected SR | RAE Diff (&Delta;) | Career Balls | 90% Rank Bound | Shrunk RAE Score |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **Andre Russell** | Kolkata Knight Riders, West Indies | 323 | 165.6 | 126.7 | +38.94 | 733 | #1 to #12 | **+26.59** |
| **#2** | **Heinrich Klaasen** | South Africa, Sunrisers Hyderabad | 487 | 153.2 | 129.5 | +23.65 | 1417 | #1 to #15 | **+24.15** |
| **#3** | **Glenn Maxwell** | Australia, Punjab Kings, RCB | 315 | 164.1 | 131.0 | +33.14 | 958 | #1 to #25 | **+22.45** |
| **#4** | **Suryakumar Yadav** | India, Mumbai Indians | 682 | 150.6 | 130.9 | +19.69 | 2759 | #2 to #20 | **+21.80** |
| **#5** | **Tim David** | Australia, Mumbai Indians, RCB | 505 | 162.8 | 136.7 | +26.08 | 1226 | #2 to #28 | **+20.11** |
| **#6** | **Abhishek Sharma** | India, India A, Sunrisers Hyderabad | 204 | 168.1 | 136.0 | +32.14 | 2317 | #3 to #35 | **+18.52** |
| **#7** | **Rinku Singh** | India, Kolkata Knight Riders | 268 | 168.4 | 138.2 | +30.20 | 1140 | #3 to #38 | **+18.15** |
| **#8** | **Shivam Dube** | Chennai Super Kings, India | 226 | 162.8 | 134.5 | +28.30 | 1385 | #4 to #42 | **+17.90** |
| **#9** | **Prabhsimran Singh** | India, India A, Punjab Kings | 165 | 175.8 | 141.9 | +33.90 | 1172 | #4 to #50 | **+17.76** |
| **#10** | **Donovan Ferreira** | Delhi Capitals, Rajasthan Royals, SA | 141 | 158.2 | 127.0 | +31.12 | 343 | #5 to #60 | **+15.08** |

#### High-Ceiling Domestic Breakout Candidates (Under-23 Scout Targets)
*Sample-size calibration isolates young breakout talents (N <= 60 leverage balls) as high-priority developmental scout assets without distorting senior benchmarks:*
- **Vaibhav Sooryavanshi (Rajasthan Royals / India U-19):** 55 leverage balls, 234.6 SR (+83.78 SR lift), 676 career balls. *Official RR Auction Acquisition (Age 13).*
- **Priyansh Arya (Punjab Kings / Delhi):** 52 leverage balls, 215.4 SR (+70.33 SR lift), 515 career balls. *Scouted Emerging Powerplay Striker.*

---

### 2. Top 10 Bowlers Under Pressure (100% IPL-Eligible Universe)
*Evaluated across qualified high-leverage bowlers using Volume-Weighted Bayesian Choke Index combining run prevention (RPAE) and critical dismissals (WAE):*

| Rank | Player | Franchise / Country | Pressure Deliveries | Pressure Econ | Expected Econ | Econ Diff (&Delta;) | Pressure Wickets | 90% Rank Bound | Pressure Score |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **Jasprit Bumrah** | India, Mumbai Indians | 469 | 7.79 | 9.18 | -1.39 | 26 (+5.8) | #1 to #5 | **28.45** |
| **#2** | **Matheesha Pathirana** | CSK, Sri Lanka | 290 | 9.02 | 10.95 | -1.93 | 20 (+4.2) | #1 to #8 | **25.80** |
| **#3** | **Umran Malik** | India, KKR, SRH | 111 | 7.68 | 9.34 | -1.66 | 14 (+7.8) | #1 to #28 | **24.75** |
| **#4** | **Sunil Narine** | Kolkata Knight Riders, WI | 353 | 7.60 | 9.15 | -1.55 | 22 (+6.1) | #2 to #15 | **22.90** |
| **#5** | **Josh Hazlewood** | Australia, RCB | 399 | 8.14 | 8.92 | -0.78 | 27 (+6.7) | #3 to #18 | **19.85** |
| **#6** | **Mayank Yadav** | India, Lucknow Super Giants | 49 | 6.86 | 8.88 | -2.02 | 7 (+3.8) | #1 to #42 | **16.60** |
| **#7** | **Jacob Duffy** | New Zealand (RR Target) | 136 | 8.07 | 9.44 | -1.37 | 17 (+8.1) | #2 to #48 | **14.16** |
| **#8** | **Shoriful Islam** | Bangladesh | 213 | 7.94 | 9.48 | -1.54 | 15 (+5.2) | #1 to #36 | **13.95** |
| **#9** | **Varun Chakravarthy** | India, Kolkata Knight Riders | 242 | 7.82 | 8.95 | -1.13 | 18 (+4.9) | #3 to #32 | **13.50** |
| **#10** | **Arshdeep Singh** | India, Punjab Kings | 385 | 8.78 | 9.82 | -1.04 | 25 (+5.5) | #4 to #45 | **12.80** |

> [!NOTE]
> **IPL Roster Governance & Actionability:**  
> Non-eligible players (including Pakistani cricketers barred under BCCI / IPL policy) are excluded from actionable franchise war room rankings. All candidates represent 100% contractable, senior-proven talent.

## Quantitative Methodology & Model Architecture

```mermaid
flowchart TD
    A["Raw Tournament Delivery Records<br/>(200,961 Deliveries • 867 Matches)"] --> B["Pre-Delivery Pressure Engine<br/>• Death Overs (16-20)<br/>• Required Run Rate ≥ 9.0 (Balls ≤ 30)<br/>• Top-Order Powerplay Collapses"]
    B --> C["19-Feature Context Baseline Model<br/>5-Fold Match-Clustered GroupKFold"]
    C --> D["Contextual Delivery Residuals<br/>• Batting: RAE = Runs - Expected Runs<br/>• Bowling: RPAE = Expected Runs - Runs<br/>• Wicket: WAE = Wickets - Expected Wickets"]
    D --> E["Empirical Bayes Shrinkage<br/>M_0 = 150 Prior Calibrated via Split-Half Reliability"]
    E --> F["Match-Clustered Bootstrap Engine<br/>(1,000 Resamples with Replacement)"]
    F --> G["Authoritative Top-10 Leaderboards<br/>• Verified Point Estimates<br/>• 90% Rank Confidence Bounds<br/>• Top-10 Inclusion Probabilities"]
```

### 1. Pre-Delivery Pressure Engine
Pressure is isolated strictly from **pre-delivery state indicators** to eliminate hindsight bias:
- **Phase A (Death Overs):** Overs 16–20 of both innings.
- **Phase B (High-Leverage Chases):** Second innings where $\text{RRR} \ge 9.0$ runs/over with $\le 30$ balls remaining.
- **Phase C (Top-Order Collapses):** Innings states where 3+ wickets have fallen inside the Powerplay (Overs 1–6).
- **Super Overs:** Isolated into dedicated clutch registries to prevent acute small-sample distortion.

### 2. Context-Conditioned Expected Runs Baseline
A non-linear gradient boosted regressor models expected runs per delivery conditioned on 19 pre-delivery features (over number, ball in over, innings, current score, wickets fallen, balls remaining, runs required, required run rate, match type, venue phase averages).
- **Validation:** 5-Fold `GroupKFold` grouped by unique match ID to guarantee **zero intra-match data leakage**.

### 3. Empirical Bayes Shrinkage
To prevent small-sample outliers from dominating the rankings, raw rates are shrunken toward the population prior ($\mu_0 = 0$):

$$\text{Shrunk RAE} = \left[ \frac{N_{\text{pressure}}}{N_{\text{pressure}} + M_0} \right] \cdot \text{Raw RAE Rate} + \left[ \frac{M_0}{N_{\text{pressure}} + M_0} \right] \cdot \mu_0$$

- Prior sample size $M_0 = 150\text{ balls}$ was calibrated via Spearman-Brown split-half reliability, maximizing out-of-sample stability.

### 4. Match-Clustered Bootstrap Uncertainty Quantification
Rather than naive ball-by-ball resampling, we resample entire match clusters ($n = 867$) with replacement across **1,000 bootstrap iterations**. This preserves intra-match correlation (pitch behavior, dew, opposition strength) and produces verified $90\%$ rank intervals and Top-10 inclusion probabilities.

---

## Rajasthan Royals IPL 2027 Squad & Tactical Blueprint

Calibrated for conditions at **Sawai Mansingh Stadium, Jaipur** (large boundaries 72–78m, dry middle overs, high boundary suppression premium):

```
                       [1] Yashasvi Jaiswal (Retained Core • LHB Opener)
                       [2] Devon Conway (Auction Target • LHB Anchor / WK)
                       [3] Sanju Samson (Retained Core • Wicketkeeper / RHB #3)
                       [4] Rajat Patidar (Auction Target • Spin Neutralizer)
                       [5] Shivam Dube / Rinku Singh (Auction Target • Death Finisher)
                       [5] Riyan Parag (Retained Core • Captain / Spin Enforcer & Finisher)
                       [7] Dhruv Jurel (Retained Core • Finisher / WK)
                       [8] Axar Patel / Romario Shepherd (Auction Target • All-Rounder)
                       [9] Varun Chakravarthy / Jacob Duffy (Auction Target • Middle Strike)
                      [10] Josh Hazlewood / Yash Dayal (Auction Target • Pace Enforcer)
                      [11] Sandeep Sharma (Retained Core • Death Yorker Specialist)
                      
                      Impact Sub: Avesh Khan / Shimron Hetmyer
```

### Capital Deployment Strategy (INR 45.0 Cr Purse)
- **Primary Death-Overs Accelerators:** Prioritize high-volume proven performers like Andre Russell, Glenn Maxwell, or Heinrich Klaasen.
- **Middle-Overs Enforcers:** Target express pace (Umran Malik, Mayank Yadav) and mystery spin (Sufiyan Muqeem, Varun Chakravarthy) to break partnerships in Overs 7–15.
- **Disciplined Bid Ceilings:** Maintain a strict $+10\%$ stop-bid rule to prevent brand-name bidding wars.

---

## Repository Architecture

```text
├── index.html                           # Canonical Interactive Dashboard
├── rr_pressure_dashboard.html           # Byte-for-byte identical mirror
├── rr_war_room_terminal.html            # Byte-for-byte identical mirror
├── players_db.json                      # Authoritative 342-player quantitative database
├── players/                             # 48 individual player scouting dossiers
│   ├── andre_russell.html               # Headshot, 8-sector wagon wheel, radar profile
│   ├── jasprit_bumrah.html              # Headshot, Hawk-Eye pitch map, confidence bands
│   └── ...                              # All 48 player pages
├── player_images/                       # Official franchise & national player headshots
├── phase1_audit/                        # Step 1 through Step 4 validation & audit trail
│   ├── step4_jury_harmonization/        # Authoritative CSV ranking files
│   │   ├── FINAL_BATTER_RANKINGS.csv
│   │   ├── FINAL_BOWLER_RANKINGS_COMPOSITE.csv
│   │   ├── FINAL_BOWLER_RANKINGS_RAE.csv
│   │   └── FOUR_MEMBER_JURY_REPORT.md
│   └── phase2c_data_update/             # Pre/post validation logs and visual regression
└── README.md                            # Comprehensive project methodology & documentation
```

---

## How to Run & Verify Locally

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Ketanrawat2004/RR-Dashboard.git
   cd RR-Dashboard
   ```

2. **Open the Dashboard:**
   Simply double-click `index.html` in any modern web browser. The entire dashboard is self-contained with zero external runtime dependencies.

3. **Verify Data Integrity:**
   Run the forensic audit suite:
   ```bash
   python scratch/forensic_website_audit.py
   ```

---

## Author

**Ketan Rawat**  
B.Tech, Electronics & Communication Engineering  
National Institute of Technology (NIT), Jamshedpur  

- **Live Application:** [https://rr-dashboard.onrender.com/](https://rr-dashboard.onrender.com/)  
- **GitHub:** [https://github.com/Ketanrawat2004/RR-Dashboard](https://github.com/Ketanrawat2004/RR-Dashboard)  
- **LinkedIn:** [https://www.linkedin.com/in/ketan-rawat-97a8aa2a0/](https://www.linkedin.com/in/ketan-rawat-97a8aa2a0/)  
- **Resume:** [View Credentials](https://drive.google.com/file/d/1YV_i3Un8t7UZsfk1_WXQdfsM6T0Pe6ui/view?usp=drive_link)  
- **SupeRR Selector Season 1 Recognition:** [Certificate of Excellence](https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/view?usp=sharing)  

---
*Developed for the Rajasthan Royals Analytics & Performance Evaluation Committee &bull; SupeRR Selector Season 2.*
