# Rajasthan Royals - SupeRR Selector Season 2

Player pressure analysis and auction planning project for Rajasthan Royals ahead of the IPL 2027 auction. Built by Ketan Rawat.

The model compares how players perform in tight, high-pressure games against their normal match record, then ranks the top 10 batters and top 10 bowlers suited for Sawai Mansingh Stadium, Jaipur within an INR 45.0 Cr auction budget.

## Dataset

Data is stored in `season2_data/` and covers IPL and T20 International matches from January 2022 to November 2026:

- `matches.csv`: 883 matches
- `competitions.csv`: 141 competitions
- `playing_eleven.csv`: 28,381 player-match records
- `competition_team_player_mapping.csv`: 6,413 mappings across 1,217 players
- `teams.csv`: 38 teams

Out of 883 matches, 178 (20.2%) qualified as high-pressure matches based on stage and margin (`pressure_score >= 30`): tournament knockouts (Finals, Semi-Finals, Playoffs), Super Overs, and finishes within 15 runs or 2 wickets.

## How the Ranking Works

Career averages treat runs and wickets in one-sided matches the same as close chases or knockouts. To separate consistency under pressure from reputation:

1. Calculate each player's High-Pressure Win Rate (`HP_Win_Rate`) and overall Baseline Win Rate (`Baseline_Win_Rate`).
2. Measure Pressure Lift (`HP_Win_Rate - Baseline_Win_Rate`) to see whether the team wins more or less often when that player plays in close games.
3. Apply Bayesian shrinkage (`M = 5.0` prior weight) and minimum sample rules (at least 12 total matches and 8 high-pressure matches), plus a sample-size curve for small counts.
4. Exclude players not eligible for the IPL auction under BCCI rules, and rank batters and bowlers separately.

### CPPI Formula Weights

- High-Pressure Win Rate (Bayesian adjusted): 35%
- Normalized Pressure Lift: 25%
- Knockout Win Rate (Bayesian adjusted): 20%
- High-Pressure Player of the Match Awards: 10%
- Career Baseline Win Rate: 10%

## Top 10 Rankings

### Batters

| Rank | Player | HP Matches | HP Win% | Baseline Win% | Lift | KO Win% | CPPI |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Shivam Dube | 18 | 66.7% | 54.3% | +12.4% | 100.0% | 66.81 |
| 2 | Rinku Singh | 26 | 69.2% | 63.8% | +5.4% | 100.0% | 66.26 |
| 3 | Axar Patel | 28 | 64.3% | 56.5% | +7.8% | 100.0% | 65.82 |
| 4 | Rajat Patidar | 14 | 71.4% | 60.3% | +11.1% | 71.4% | 64.26 |
| 5 | Ruturaj Gaikwad | 14 | 57.1% | 50.6% | +6.5% | 100.0% | 62.41 |
| 6 | Devon Conway | 14 | 64.3% | 46.2% | +18.1% | 66.7% | 61.97 |
| 7 | Virat Kohli | 20 | 70.0% | 62.4% | +7.6% | 71.4% | 61.47 |
| 8 | Bhanuka Rajapaksa | 9 | 66.7% | 56.2% | +10.4% | 100.0% | 59.88 |
| 9 | Shreyas Iyer | 18 | 55.6% | 54.5% | +1.1% | 60.0% | 54.18 |
| 10 | Sediqullah Atal | 8 | 50.0% | 57.9% | -7.9% | 66.7% | 50.07 |

### Bowlers

| Rank | Player | HP Matches | HP Win% | Baseline Win% | Lift | KO Win% | CPPI |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Jacob Duffy | 8 | 75.0% | 54.5% | +20.5% | 100.0% | 68.83 |
| 2 | Josh Hazlewood | 14 | 78.6% | 63.7% | +14.9% | 83.3% | 68.59 |
| 3 | Yash Dayal | 10 | 80.0% | 69.8% | +10.2% | 80.0% | 63.09 |
| 4 | Mitchell Starc | 10 | 60.0% | 68.3% | -8.3% | 100.0% | 62.80 |
| 5 | Varun Chakravarthy | 21 | 61.9% | 58.6% | +3.3% | 100.0% | 62.38 |
| 6 | Romario Shepherd | 25 | 56.0% | 49.0% | +7.0% | 100.0% | 62.00 |
| 7 | Suyash Sharma | 11 | 72.7% | 65.1% | +7.6% | 66.7% | 60.07 |
| 8 | Bhuvneshwar Kumar | 25 | 60.0% | 57.3% | +2.7% | 71.4% | 56.86 |
| 9 | Arshdeep Singh | 25 | 68.0% | 56.9% | +11.1% | 33.3% | 55.26 |
| 10 | Lockie Ferguson | 9 | 55.6% | 49.1% | +6.5% | 50.0% | 52.00 |

Full output tables are in `pressure_output/SUBMISSION_top10_batters.csv` and `pressure_output/SUBMISSION_top10_bowlers.csv`. Five high-profile players with negative pressure lift (Jasprit Bumrah, Mohammed Siraj, Rashid Khan, Heinrich Klaasen, and Rohit Sharma) are also included in the dashboard comparison audit.

## Rajasthan Royals Auction Plan (INR 45.0 Cr)

Built around Sawai Mansingh Stadium conditions (72-78m boundaries, dry middle overs against spin, and evening dew):

- Core Targets: Rinku Singh (INR 11.0 Cr), Shivam Dube (INR 9.5 Cr), Josh Hazlewood (INR 9.0 Cr)
- Support Targets: Devon Conway (INR 6.5 Cr), Yash Dayal (INR 5.5 Cr), Jacob Duffy (INR 2.0 Cr)
- Bidding Rule: Stop bidding if a target goes more than 10% above its cap and switch to backup targets (such as Rajat Patidar, Axar Patel, or Varun Chakravarthy).

## Main Files

- `index.html` (`rr_pressure_dashboard.html`, `rr_war_room_terminal.html`): Interactive HTML dashboard
- `players/`: 25 individual player pages with shot wagon wheels and bowling pitch maps
- `RR_SupeRR_Selector_Season2_Ketan_Rawat.pptx`: 13-slide submission presentation
- `RR_SupeRR_Selector_Season2_Report_Ketan_Rawat.pdf`: 4-page written methodology report
- `pressure_output/`: Submission CSVs, `audit_match_pressure_scores.csv`, charts, and `methodology_report.md`
- `rr_pressure_analyst.py`: Match scoring and player ranking script
- `fix_dashboard_and_wagon.py`: Generates `index.html` and the 25 pages in `players/`
- `build_clean_submission_pptx.py`: Generates the 13-slide `.pptx` file
- `build_submission_pdf.py`: Generates the PDF report

## How to Open or Rebuild

To view the dashboard, open `index.html` in any web browser (all CSS, charts, and player images are bundled inside the HTML files).

To regenerate the dashboard or slide deck from Python:

```bash
python fix_dashboard_and_wagon.py
python build_clean_submission_pptx.py
```

`build_clean_submission_pptx.py` requires `python-pptx`.

## Author

Ketan Rawat (B.Tech ECE, NIT Jamshedpur)

- [LinkedIn](https://www.linkedin.com/in/ketan-rawat-97a8aa2a0/)
- [Resume](https://drive.google.com/file/d/1YV_i3Un8t7UZsfk1_WXQdfsM6T0Pe6ui/view?usp=drive_link)
- [Season 1 Certificate (Additional Top 20)](https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/view?usp=sharing)
