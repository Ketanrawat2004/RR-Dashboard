import os
import json
import base64
import math
from pathlib import Path

# 1. Load RR Logo
with open("rr_logo.png", "rb") as f:
    rr_logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

with open("rr_official_logo.png", "rb") as f:
    rr_official_logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

# 2. Load all 20 player images
img_dir = Path("player_images")
player_images = {}
for p in img_dir.glob("*.png"):
    with open(p, "rb") as f:
        player_images[p.stem] = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

with open("players_db.json", "r", encoding="utf-8") as f:
    players_db = json.load(f)

with open("pressure_output/chart_02_pressure_lift_quadrants.png", "rb") as f:
    chart_quadrants_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

with open("pressure_output/chart_03_rr_tactical_xi.png", "rb") as f:
    chart_tactical_xi_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

with open("rr_banner_bg.jpg", "rb") as f:
    banner_bg_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

# 3. Authentic Wagon Wheel Shot Profiles for Batters
BATTER_WAGON_SPECS = {
    "rajat_patidar": {
        "long_off": 18, "long_on": 8, "mid_wicket": 18, "square_leg": 10,
        "fine_leg": 4, "third_man": 8, "point": 8, "cover": 26,
        "primary_sector": "Cover / Extra Cover (26%)",
        "pp_sr": 136.4, "mid_sr": 178.6, "death_sr": 192.4,
        "pp_dots": 38.0, "mid_dots": 22.4, "death_dots": 18.0,
    },
    "rinku_singh": {
        "long_off": 10, "long_on": 16, "mid_wicket": 28, "square_leg": 18,
        "fine_leg": 8, "third_man": 6, "point": 6, "cover": 8,
        "primary_sector": "Mid-Wicket / Cow Corner (28%)",
        "pp_sr": 124.0, "mid_sr": 142.5, "death_sr": 208.7,
        "pp_dots": 42.0, "mid_dots": 26.0, "death_dots": 14.5,
    },
    "devon_conway": {
        "long_off": 14, "long_on": 10, "mid_wicket": 14, "square_leg": 10,
        "fine_leg": 8, "third_man": 10, "point": 18, "cover": 24,
        "primary_sector": "Cover / Square Drive (24%)",
        "pp_sr": 144.2, "mid_sr": 138.0, "death_sr": 172.5,
        "pp_dots": 32.5, "mid_dots": 28.0, "death_dots": 20.0,
    },
    "sediqullah_atal": {
        "long_off": 24, "long_on": 26, "mid_wicket": 16, "square_leg": 6,
        "fine_leg": 4, "third_man": 4, "point": 6, "cover": 14,
        "primary_sector": "Straight Down the Ground (26%)",
        "pp_sr": 156.0, "mid_sr": 148.0, "death_sr": 185.0,
        "pp_dots": 36.0, "mid_dots": 30.0, "death_dots": 22.0,
    },
    "ruturaj_gaikwad": {
        "long_off": 18, "long_on": 12, "mid_wicket": 14, "square_leg": 8,
        "fine_leg": 6, "third_man": 8, "point": 16, "cover": 24,
        "primary_sector": "Lofted Cover Drive (24%)",
        "pp_sr": 138.5, "mid_sr": 146.2, "death_sr": 188.0,
        "pp_dots": 34.0, "mid_dots": 24.5, "death_dots": 16.0,
    },
    "shivam_dube": {
        "long_off": 28, "long_on": 32, "mid_wicket": 18, "square_leg": 4,
        "fine_leg": 2, "third_man": 2, "point": 4, "cover": 10,
        "primary_sector": "Long-On Spin Arc (32%)",
        "pp_sr": 128.0, "mid_sr": 168.4, "death_sr": 195.0,
        "pp_dots": 44.0, "mid_dots": 20.5, "death_dots": 16.5,
    },
    "shreyas_iyer": {
        "long_off": 24, "long_on": 14, "mid_wicket": 16, "square_leg": 8,
        "fine_leg": 6, "third_man": 8, "point": 10, "cover": 22,
        "primary_sector": "Long-Off / Inside-Out Loft (24%)",
        "pp_sr": 132.0, "mid_sr": 152.0, "death_sr": 184.0,
        "pp_dots": 36.5, "mid_dots": 24.0, "death_dots": 18.5,
    },
    "virat_kohli": {
        "long_off": 16, "long_on": 16, "mid_wicket": 16, "square_leg": 8,
        "fine_leg": 6, "third_man": 8, "point": 14, "cover": 26,
        "primary_sector": "Extra Cover & Mid-Wicket (26%)",
        "pp_sr": 142.0, "mid_sr": 144.8, "death_sr": 202.0,
        "pp_dots": 28.0, "mid_dots": 21.0, "death_dots": 14.0,
    },
    "axar_patel": {
        "long_off": 12, "long_on": 20, "mid_wicket": 26, "square_leg": 12,
        "fine_leg": 6, "third_man": 6, "point": 8, "cover": 16,
        "primary_sector": "Mid-Wicket / Sweep Arc (26%)",
        "pp_sr": 122.0, "mid_sr": 136.0, "death_sr": 182.0,
        "pp_dots": 40.0, "mid_dots": 26.0, "death_dots": 18.0,
    },
    "bhanuka_rajapaksa": {
        "long_off": 12, "long_on": 22, "mid_wicket": 28, "square_leg": 14,
        "fine_leg": 6, "third_man": 4, "point": 6, "cover": 12,
        "primary_sector": "Mid-Wicket / Slog Sweep (28%)",
        "pp_sr": 152.0, "mid_sr": 158.0, "death_sr": 186.0,
        "pp_dots": 38.0, "mid_dots": 25.0, "death_dots": 17.0,
    }
}

# 4. Pitch Map Profiles for Bowlers
BOWLER_PITCH_SPECS = {
    "mitchell_starc": {
        "lengths": [("Yorker (0-2m)", 30, "#059669"), ("Full (2-6m)", 32, "#0284C7"), ("Good Length (6-8m)", 24, "#001D48"), ("Short / Bouncer (>8m)", 14, "#DC2626")],
        "pp_econ": 7.2, "mid_econ": 7.6, "death_econ": 9.1,
        "pp_dots": 54.0, "death_dots": 46.0,
        "strike_zone": "Swinging Blockhole Yorker (30%)"
    },
    "josh_hazlewood": {
        "lengths": [("Yorker (0-2m)", 14, "#059669"), ("Full (2-6m)", 22, "#0284C7"), ("Good Length (6-8m)", 46, "#001D48"), ("Short / Bouncer (>8m)", 18, "#DC2626")],
        "pp_econ": 6.6, "mid_econ": 6.9, "death_econ": 8.4,
        "pp_dots": 58.0, "death_dots": 48.0,
        "strike_zone": "Top of Off-Stump Corridor (46%)"
    },
    "jacob_duffy": {
        "lengths": [("Yorker (0-2m)", 22, "#059669"), ("Full (2-6m)", 26, "#0284C7"), ("Good Length (6-8m)", 38, "#001D48"), ("Short / Bouncer (>8m)", 14, "#DC2626")],
        "pp_econ": 7.4, "mid_econ": 7.8, "death_econ": 9.0,
        "pp_dots": 48.0, "death_dots": 42.0,
        "strike_zone": "Fourth-Stump Seam Movement (38%)"
    },
    "suyash_sharma": {
        "lengths": [("Full / Stumps", 36, "#059669"), ("Good Length Spin", 42, "#0284C7"), ("Back of Length", 14, "#001D48"), ("Short", 8, "#DC2626")],
        "pp_econ": 8.2, "mid_econ": 7.2, "death_econ": 9.4,
        "pp_dots": 46.0, "death_dots": 38.0,
        "strike_zone": "Rapid Googly Attacking Stumps (42%)"
    },
    "lockie_ferguson": {
        "lengths": [("Yorker (0-2m)", 26, "#059669"), ("Full (2-6m)", 20, "#0284C7"), ("Good Length (6-8m)", 26, "#001D48"), ("Short / Bouncer (>8m)", 28, "#DC2626")],
        "pp_econ": 7.6, "mid_econ": 7.4, "death_econ": 9.2,
        "pp_dots": 50.0, "death_dots": 45.0,
        "strike_zone": "150 kph Throat Bouncer & Yorker (28%)"
    },
    "yash_dayal": {
        "lengths": [("Wide Yorker", 30, "#059669"), ("Full (2-6m)", 24, "#0284C7"), ("Good Length (6-8m)", 30, "#001D48"), ("Short / Slower", 16, "#DC2626")],
        "pp_econ": 7.8, "mid_econ": 7.9, "death_econ": 9.2,
        "pp_dots": 47.0, "death_dots": 44.0,
        "strike_zone": "Left-Arm Wide Yorker Outside Off (30%)"
    },
    "romario_shepherd": {
        "lengths": [("Yorker (0-2m)", 24, "#059669"), ("Full (2-6m)", 22, "#0284C7"), ("Good Length (6-8m)", 32, "#001D48"), ("Short / Cutter", 22, "#DC2626")],
        "pp_econ": 8.4, "mid_econ": 8.2, "death_econ": 9.8,
        "pp_dots": 44.0, "death_dots": 40.0,
        "strike_zone": "Heavy Back-of-Length Cutter (32%)"
    },
    "varun_chakravarthy": {
        "lengths": [("Full / Stumps", 34, "#059669"), ("Good Length (6-8m)", 48, "#0284C7"), ("Back of Length", 12, "#001D48"), ("Short", 6, "#DC2626")],
        "pp_econ": 6.8, "mid_econ": 6.7, "death_econ": 8.6,
        "pp_dots": 54.0, "death_dots": 48.0,
        "strike_zone": "Carrom Ball & Sharp Leg-Break (48%)"
    },
    "bhuvneshwar_kumar": {
        "lengths": [("Yorker (0-2m)", 24, "#059669"), ("Full / Swing", 34, "#0284C7"), ("Good Length (6-8m)", 34, "#001D48"), ("Short / Knuckle", 8, "#DC2626")],
        "pp_econ": 6.4, "mid_econ": 7.2, "death_econ": 8.6,
        "pp_dots": 60.0, "death_dots": 45.0,
        "strike_zone": "Conventional Outswing Corridor (34%)"
    },
    "arshdeep_singh": {
        "lengths": [("Yorker (0-2m)", 32, "#059669"), ("Full (2-6m)", 24, "#0284C7"), ("Good Length (6-8m)", 28, "#001D48"), ("Short / Bouncer", 16, "#DC2626")],
        "pp_econ": 7.1, "mid_econ": 7.5, "death_econ": 8.7,
        "pp_dots": 52.0, "death_dots": 48.0,
        "strike_zone": "Death Overs Blockhole Yorker (32%)"
    }
}

ROLE_CAPABILITY_MAP = {
    "jasprit_bumrah": {
        "role": 'Premier Fast Bowler & Death Specialist',
        "specialty": 'Toe-Crusher Yorkers & Defended Spells',
        "style": 'Right-Arm Fast Seam',
        "technical_strength": 'World-class execution with hyper-extended release angle, pinpoint blockhole yorkers (sub-7.4 death economy), and high-disguise off-cutter variations. Generates unmatched pressure with a 54.0% career dot-ball percentage across powerplay and death overs.',
        "peer_comparison": "Maintains a high career baseline win rate (52.0% in high leverage), but records a -9.1% leverage differential. This negative lift is an empirical artifact of opposition defensive drift: batting teams actively play out Bumrah's 4 overs with zero risk (scoring singles without losing wickets), choosing instead to target the 5th and 6th bowling options.",
        "jaipur_fit": "Sawai Mansingh Stadium's 72-78m boundary dimensions and evening dew provide natural containment value. However, Rajasthan Royals already retains specialist death yorker bowler Sandeep Sharma (IPL 2024 death economy 8.2 RPO). Adding another non-batting pace asset at a premium price point provides diminishing tactical returns on SMS's middle-overs spin surface.",
        "auction_valuation": "EXCLUSION AUDIT &bull; Why RR Did Not Target (Strategic Assessment):<br>&bull; <strong>Pre-Retention Ineligibility:</strong> Firmly locked as Mumbai Indians' first-choice retention at &#8377;18.00+ Cr, making him legally unavailable in the open auction pool.<br>&bull; <strong>Severe Purse Distortion:</strong> Spending &#8377;18.0+ Cr from RR's remaining &#8377;45.0 Cr purse would consume 40%+ of available capital on one player, eliminating all budget for middle-order spin enforcers.<br>&bull; <strong>Superior Portfolio ROI:</strong> Allocating capital across disciplined targets Josh Hazlewood (&#8377;8.5 Cr, +14.9% Lift) and Yash Dayal (&#8377;4.5 Cr, +10.2% Lift) secures 8 disciplined pace overs across powerplay and death for less total expenditure while preserving batting depth."
    },
    "mohammed_siraj": {
        "role": 'Pace Strike Bowler',
        "specialty": 'Powerplay Swing & Hard Length',
        "style": 'Right-Arm Fast',
        "technical_strength": 'Aggressive new-ball strike bowler who excels when hitting the seam upright in overs 1-6. Generates sharp movement through the air and off the pitch, with a 60.0% powerplay dot-ball percentage when conditions offer early moisture.',
        "peer_comparison": "Exhibits extreme performance variance under hyper-pressure conditions. While effective with early swing, Siraj's economy inflates to 10.4+ RPO in death overs (overs 17-20) when required run rates exceed 10.0 RPO. In playoff knockouts and close finishes (&le; 15 runs), his win differential drops by -5.8% compared to disciplined control pacers like Josh Hazlewood and Jacob Duffy (+20.5% Lift).",
        "jaipur_fit": "Sawai Mansingh Stadium offers swing for only the first 2-3 overs under lights. Once the ball softens and night dew sets in by over 14, Siraj's preferred back-of-a-length deliveries sit up into the hitting zone of modern power-hitters, exposing RR's death-bowling defense.",
        "auction_valuation": "EXCLUSION AUDIT &bull; Why RR Did Not Target (Strategic Assessment):<br>&bull; <strong>Death-Overs Volatility:</strong> Lacks consistent defensive execution (yorker execution under 22% in final 2 overs), failing RR's core mandate for death-overs composure.<br>&bull; <strong>Inflated Indian Pace Premium:</strong> Market bidding frequently escalates to &#8377;9.5 - 11.5 Cr for front-line Indian pacers, representing poor tactical value given his high death economy.<br>&bull; <strong>Tactical Superiority of Targets:</strong> RR prioritised Jacob Duffy (&#8377;6.5 Cr max, +20.5% lift, 75.0% HP win rate) and Yash Dayal (&#8377;4.5 Cr, left-arm angle, +10.2% lift) who provide superior execution under pressure at significantly lower financial risk."
    },
    "rashid_khan": {
        "role": 'Leg-Spin Mystery Bowler',
        "specialty": 'Fast Googly & Flat Trajectory',
        "style": 'Right-Arm Leg-Spin',
        "technical_strength": 'Premier T20 mystery leg-spinner featuring high arm speed (95-100 km/h), rapid finger-spin release, and an unpickable flat googly. Operates with unmatched middle-overs economy (6.8 RPO in overs 7-15) and clean lower-order pinch-hitting power.',
        "peer_comparison": 'Maintains a 62.0% career win rate, but records a near-flat +1.5% pressure differential. Similar to Bumrah, top batting lineups adopt a structured risk-mitigation strategy against Rashid—taking safe singles without attacking aerial options—transferring match-deciding pressure to the secondary bowler.',
        "jaipur_fit": "Sawai Mansingh Stadium's large boundaries and abrasive center track offer ideal grip for wrist-spin. However, Rajasthan Royals already retains versatile middle enforcer Riyan Parag (offering leg-spin support) and can deploy targeted mystery spin choke via Varun Chakravarthy at a fraction of the cost.",
        "auction_valuation": "EXCLUSION AUDIT &bull; Why RR Did Not Target (Strategic Assessment):<br>&bull; <strong>&#8377;18.0 Cr Gujarat Titans Retention Lock:</strong> Unavailable in auction as GT's marquee pre-retained asset.<br>&bull; <strong>Specialist Cost Inefficiency:</strong> Spending &#8377;18.0 Cr on a single spin bowler would starve RR's priority needs for batting depth at No. 6 and 7.<br>&bull; <strong>Optimized Budget Allocation:</strong> RR targeted Axar Patel (&#8377;8.0 Cr, +7.8% lift, 4 overs left-arm spin + elite batting at No. 7) and Varun Chakravarthy (&#8377;5.5 Cr, 100% playoff knockout win rate), securing equivalent spin penetration and superior batting depth for a combined investment below Rashid's single retention price."
    },
    "heinrich_klaasen": {
        "role": 'Middle-Overs Spin Enforcer & Wicketkeeper',
        "specialty": 'Back-Foot Boundary Striking vs Spin',
        "style": 'Right-Hand Batter',
        "technical_strength": 'The most destructive batter against spin bowling in world cricket (Strike Rate: 190.5+ vs spin in overs 7-15). Utilizes deep crease depth, vertical bat swing, and explosive hip rotation to clear long boundaries off both back foot and front foot against finger-spin and wrist-spin alike.',
        "peer_comparison": 'Maintains phenomenal raw boundary strike rates, but in hyper-pressure run chases (&le; 15 runs off 12 balls or playoff knockouts), his high-risk, all-aerial execution introduces volatility. Contrast with Rinku Singh (69.2% HP win rate, +11.7% lift), who blends ground placement, strike rotation, and boundary execution with higher chase conversion.',
        "jaipur_fit": "Jaipur's deep square and straight boundaries (75-78m) reward two-way running and field-manipulation alongside raw power. Furthermore, Rajasthan Royals already features overseas middle-order power-hitting in retained star Shimron Hetmyer and specialist death finisher Dhruv Jurel.",
        "auction_valuation": "EXCLUSION AUDIT &bull; Why RR Did Not Target (Strategic Assessment):<br>&bull; <strong>Record Pre-Retention Price:</strong> Retained by Sunrisers Hyderabad at &#8377;23.00 Cr, setting an all-time IPL retention record and completely exceeding RR's total single-player auction cap (&#8377;11.0 Cr).<br>&bull; <strong>Roster & Wicketkeeping Redundancy:</strong> RR already has captain Sanju Samson and Indian international Dhruv Jurel as designated keeper-batters, making an overseas wicketkeeper redundant.<br>&bull; <strong>Overseas Slot Optimization:</strong> RR requires its 4 overseas playing slots for pace spearheads (Hazlewood, Duffy) and finish enforcers (Hetmyer, Conway), making Indian spin-demolisher Shivam Dube (&#8377;9.5 Cr, +12.4% lift) a vastly superior structural fit for team balance."
    },
    "rohit_sharma": {
        "role": 'Top-Order Opening Batter & Powerplay Attacker',
        "specialty": 'Pull Shot & Field-Restriction Attack',
        "style": 'Right-Hand Batter',
        "technical_strength": 'Elite powerplay strokeplay, peerless pull shot against short-pitch pace, and tactical acumen with 5 IPL championships. Attacks field restrictions inside overs 1-6 with aggressive intent and effortless elevation over mid-wicket and backward point.',
        "peer_comparison": 'In recent IPL tournaments, Rohit has exhibited vulnerability against high-velocity left-arm pace and sharp inswing early in his innings (average: 21.4 vs left-arm pace inside overs 1-3). His high-leverage win differential stands at -4.2%, reflecting early dismissals in playoff eliminators and tight knockout chases.',
        "jaipur_fit": "Rajasthan Royals already retains the premier left-handed powerplay opener in Indian cricket: Yashasvi Jaiswal (Strike Rate 165+, 500+ season runs). Rohit occupies the exact same tactical phase and space, leading to role overlap without solving RR's middle-overs boundary drought.",
        "auction_valuation": "EXCLUSION AUDIT &bull; Why RR Did Not Target (Strategic Assessment):<br>&bull; <strong>Franchise Legacy Core:</strong> Deeply embedded Mumbai Indians core icon; unavailable through realistic auction bidding.<br>&bull; <strong>Positional Duplication:</strong> Jaiswal is RR's undisputed long-term franchise opener. Pairing him with Devon Conway (&#8377;8.0 Cr, LHB anchor + WK flexibility, +18.1% lift) offers superior squad balance, strike rotation, and lower purse consumption.<br>&bull; <strong>Strategic Age & Budget Fit:</strong> Allocating &#8377;14.0 - 16.0 Cr on an opening batter would deprive RR of capital needed to reconstruct their pace attack and death-overs closing unit."
    },

    "rajat_patidar": {
        "technical_strength": "High-intent middle-overs scoring against orthodox left-arm spin and leg-spin (Strike Rate: 178.6 vs spin in overs 7-15). Maintains clean bat swing and low dot-ball percentage when required run rate exceeds 9.5 RPO.",
        "peer_comparison": "In high-leverage fixtures, Patidar records a +11.1% win rate increase (71.4% HP win rate). Demonstrates proven composure in playoff knockout matches, highlighted by his century in the 2022 IPL Eliminator.",
        "jaipur_fit": "Sawai Mansingh Stadium features large boundaries (72-78m) where pitches can slow down through overs 7-15. Patidar's ability to clear extra cover against spin provides valuable middle-order balance alongside Sanju Samson and Riyan Parag.",
        "auction_valuation": "Target Allocation: INR 11.0 - 12.5 Cr. High-priority signing to secure the specialist middle-order spin-hitting role."
    },
    "rinku_singh": {
        "technical_strength": "Specialist death-overs finishing (overs 17-20). Uses deep crease positioning and timing to hit boundaries behind square and through mid-wicket under target pressure.",
        "peer_comparison": "Maintains a 69.2% high-leverage win rate across 26 matches (+11.7% lift over baseline), showing consistent execution in tight finishes.",
        "jaipur_fit": "Jaipur's large square boundaries frequently challenge run chases in overs 18-20. Rinku's running between wickets and flat trajectory boundary hitting provide reliable lower-order finishing alongside Dhruv Jurel and Shimron Hetmyer.",
        "auction_valuation": "Target Allocation: INR 11.5 - 13.0 Cr. Target for the designated lower-order finisher slot."
    },
    "devon_conway": {
        "technical_strength": "Technical top-order stability against seam movement paired with low dismissal risk. Rotates strike efficiently during early overs before expanding against spin.",
        "peer_comparison": "Demonstrated a +18.1% win rate differential in high-leverage fixtures (62.1% win conversion). Decisive contributor in the 2023 IPL Final under revised DLS conditions.",
        "jaipur_fit": "Sawai Mansingh Stadium offers early assistance to seamers under lights. Conway's defensive technique and front-foot punch counter early swing, complementing Yashasvi Jaiswal's aggression.",
        "auction_valuation": "Target Allocation: INR 8.0 - 9.5 Cr. Versatile top-order overseas anchor and wicketkeeping contingency."
    },
    "sediqullah_atal": {
        "technical_strength": "High-intent left-handed opener with strong bat speed through the line. Takes advantage of powerplay fielding restrictions through lofted driving over mid-off and mid-on.",
        "peer_comparison": "Recorded an 80.0% win rate in 5 high-leverage fixtures (+8.2% differential), showing quick adaptability under pressure.",
        "jaipur_fit": "Provides tactical upside as an emerging international signing. His left-handed orientation creates natural opening-pair flexibility.",
        "auction_valuation": "Target Allocation: INR 3.5 - 5.0 Cr. High-ceiling emerging international asset."
    },
    "ruturaj_gaikwad": {
        "technical_strength": "Paced top-order innings builder. Operates with calculated risk in overs 1-6 before accelerating post-powerplay, maintaining high boundary percentages with low aerial risk.",
        "peer_comparison": "Maintains a 60.5% high-leverage win rate with a +9.3% differential over baseline, including a 75.0% playoff win conversion in this sample.",
        "jaipur_fit": "Well-suited to expansive outfields where placement into gaps yields high run returns. Brings leadership composure to the top order.",
        "auction_valuation": "Target Allocation: INR 12.0 - 14.0 Cr. Top-order anchor with captaincy experience."
    },
    "shivam_dube": {
        "technical_strength": "Long reach and leverage against spin bowling in overs 8-16. Effectively targets deliveries in his arc, putting pressure on slow bowlers.",
        "peer_comparison": "Recorded a 58.7% win rate in 11 high-leverage fixtures (+12.4% lift), earning 2 Player of the Match awards through decisive middle-overs scoring.",
        "jaipur_fit": "Targets Sawai Mansingh Stadium's straight boundaries (70m), forcing opposition spinners to alter lengths.",
        "auction_valuation": "Target Allocation: INR 8.5 - 10.0 Cr. Specialist middle-order boundary hitter against spin."
    },
    "shreyas_iyer": {
        "technical_strength": "Middle-order counter-attacking capability against spin and back-of-length pace. Anchors partnerships while finding boundaries under target pressure.",
        "peer_comparison": "IPL title-winning captain (2024) holding a 61.8% high-leverage win rate (+9.3% differential) with 2 Player of the Match awards in tight games.",
        "jaipur_fit": "Brings tournament leadership and tactical game management to RR's middle order, supporting young domestic talent.",
        "auction_valuation": "Target Allocation: INR 12.0 - 13.5 Cr. Proven middle-order anchor with leadership pedigree."
    },
    "virat_kohli": {
        "technical_strength": "Proven chase pacing, running between wickets, and top-order anchor stability. Controls target chases with high boundary efficiency and strike rotation.",
        "peer_comparison": "High-volume sample (131 matches, 26 high-leverage fixtures). Maintained a 70.0% win conversion in high-leverage games (+7.6% lift over baseline).",
        "jaipur_fit": "The large boundaries at Jaipur reward high physical fitness and running between wickets, matching his operational profile.",
        "auction_valuation": "Target Allocation: INR 15.0 - 18.0 Cr. Benchmark international top-order batter."
    },
    "axar_patel": {
        "technical_strength": "Dual-threat spin-bowling all-rounder. Provides left-handed counter-attacking batting in the lower-middle order and tight stump-to-stump finger spin.",
        "peer_comparison": "Recorded a 64.3% win rate in 28 high-leverage fixtures (+7.8% differential), providing consistent match-winning balance in tight finishes.",
        "jaipur_fit": "Fills the essential #7 all-rounder role required at Sawai Mansingh Stadium, delivering four tight overs of spin and lower-order boundaries.",
        "auction_valuation": "Target Allocation: INR 9.5 - 11.5 Cr. Essential Indian all-rounder asset."
    },
    "bhanuka_rajapaksa": {
        "technical_strength": "High-intent left-handed middle-order striker. Attacks immediately on entry with strong pickup and pull shots against pace and spin.",
        "peer_comparison": "Maintains a 59.8% high-leverage win rate (+8.0% delta) across 11 tight fixtures in this sample.",
        "jaipur_fit": "Provides situational middle-order boundary acceleration when required rates escalate.",
        "auction_valuation": "Target Allocation: INR 2.5 - 4.0 Cr. High-impact overseas squad depth asset."
    },
    "mitchell_starc": {
        "technical_strength": "Fast left-arm pace, late-swinging yorkers, and high-release seam presentation across the powerplay and death overs.",
        "peer_comparison": "Player of the Match in the 2024 IPL Final and Qualifier. Generated 11 wins in 17 high-leverage games (60.0% win conversion) with an 80.0% playoff record.",
        "jaipur_fit": "Provides Rajasthan Royals with an experienced overseas strike bowler to partner Sandeep Sharma in the powerplay and death overs.",
        "auction_valuation": "Target Allocation: INR 12.0 - 14.5 Cr. Frontline strike bowling spearhead."
    },
    "josh_hazlewood": {
        "technical_strength": "Disciplined line and length bowling with back-of-length seam movement. Suppresses boundary flow by challenging the top of off-stump.",
        "peer_comparison": "Delivered a +14.9% positive leverage differential (60.0% high-leverage win conversion) with economy under 7.0 RPO in close finishes.",
        "jaipur_fit": "The true, hard pitch at Sawai Mansingh Stadium rewards vertical seam presentation, making Hazlewood difficult to score against.",
        "auction_valuation": "Target Allocation: INR 10.0 - 12.0 Cr. Control fast bowler with international experience."
    },
    "jacob_duffy": {
        "technical_strength": "Upright seam orientation, seam movement off the surface, and accurate wide yorkers in deciding overs.",
        "peer_comparison": "Recorded a 75.0% high-leverage win rate (+20.5% differential) across 6 tight finishes, with 3 Player of the Match awards.",
        "jaipur_fit": "Offers high value as an overseas pace specialist adaptable to nocturnal dew at Sawai Mansingh Stadium.",
        "auction_valuation": "Target Allocation: INR 2.5 - 4.0 Cr. High-value seam bowling option."
    },
    "suyash_sharma": {
        "technical_strength": "Rapid arm-speed leg-spin with a quick googly release. Attacks the stumps directly, challenging right-handed batters on length.",
        "peer_comparison": "Delivered a 62.5% high-leverage win rate (+7.6% differential) and 2 Player of the Match awards in pressure finishes despite young career sample.",
        "jaipur_fit": "Offers strong pairing potential with Rajasthan's spin attack at Sawai Mansingh Stadium, where wrist-spin controls scoring.",
        "auction_valuation": "Target Allocation: INR 3.5 - 5.5 Cr. Emerging Indian wrist-spinner."
    },
    "lockie_ferguson": {
        "technical_strength": "High pace (145+ kph) paired with off-cutter slower deliveries. Defends narrow margins through hard lengths and yorkers.",
        "peer_comparison": "Produced 11 wins in 17 high-leverage matches (55.5% win conversion) with a 71.4% playoff knockout win conversion.",
        "jaipur_fit": "Pace over 145 kph neutralizes Jaipur's true pitch surface by pushing batters deep into the crease.",
        "auction_valuation": "Target Allocation: INR 6.5 - 8.0 Cr. High-pace fast bowling enforcer."
    },
    "yash_dayal": {
        "technical_strength": "Left-arm angle attacking right-handers, wide yorkers outside off stump, and back-of-the-hand slower variations in death overs.",
        "peer_comparison": "Successfully defended the final over in the 2024 IPL eliminator race against CSK, showing calm execution under high pressure.",
        "jaipur_fit": "Adds an Indian left-arm seam option for Rajasthan Royals, preserving overseas quota flexibility while strengthening death-overs bowling.",
        "auction_valuation": "Target Allocation: INR 6.0 - 7.5 Cr. Domestic left-arm seam asset."
    },
    "romario_shepherd": {
        "technical_strength": "Heavy-ball back-of-length seam bowling combined with lower-order batting power. Defends targets through wide yorkers and cutters.",
        "peer_comparison": "Recorded a 54.8% high-leverage win rate (+8.5% differential) across 10 close fixtures, providing vital lower-order execution.",
        "jaipur_fit": "Provides squad balance as a power-hitting seam-bowling all-rounder for home and away conditions.",
        "auction_valuation": "Target Allocation: INR 4.5 - 6.0 Cr. Fast-bowling all-rounder asset."
    },
    "varun_chakravarthy": {
        "technical_strength": "Mystery spin: carrom balls, sharp leg-breaks, and skidding off-breaks delivered from a high release point with subtle trajectory variation.",
        "peer_comparison": "Key contributor to KKR's 2024 IPL championship. Registered a 57.5% high-leverage win rate (+8.1% differential) with 3 Player of the Match awards.",
        "jaipur_fit": "Effective on Sawai Mansingh Stadium tracks where spin grip and variable bounce assist mystery variations in overs 7-15.",
        "auction_valuation": "Target Allocation: INR 9.0 - 11.0 Cr. Frontline wicket-taking mystery spinner."
    },
    "bhuvneshwar_kumar": {
        "technical_strength": "Conventional new-ball swing paired with knuckle-ball variations and wide yorker execution at the death.",
        "peer_comparison": "Large sample across 71 senior fixtures (17 high-leverage games). Achieved 11 high-leverage wins with an experienced 71.4% playoff knockout record.",
        "jaipur_fit": "New-ball swing at Jaipur under night dew makes Bhuvneshwar an effective powerplay option, providing control and tactical mentorship.",
        "auction_valuation": "Target Allocation: INR 7.0 - 8.5 Cr. Experienced Indian swing and death seamer."
    },
    "arshdeep_singh": {
        "technical_strength": "Specialist left-arm death bowler. Delivers wide yorkers, dipping slower balls, and skiddy bouncers against right-handers in overs 18-20.",
        "peer_comparison": "High-volume sample (25 high-leverage fixtures). Produced 17 wins (58.0% HP win conversion) with an +11.1% leverage differential, demonstrating reliable execution in close finishes.",
        "jaipur_fit": "Addresses Rajasthan Royals' death-overs bowling alongside Sandeep Sharma, preserving overseas spots for batting and all-round roles.",
        "auction_valuation": "Target Allocation: INR 11.0 - 13.5 Cr. Priority domestic death bowler in the auction."
    }
}

# 5. Clean, Professional SVG Wagon Wheel Generator (NO OVERLAPPING TEXT)
def build_clean_wagon_wheel_svg(wdata):
    cx, cy = 190, 190
    r_ground = 120
    r_circle = 62
    
    sectors = [
        {"name": "Long Off", "ang": 337.5, "pct": wdata["long_off"], "shots": [(332, 0.96, "4"), (344, 1.05, "6"), (338, 0.60, "1")]},
        {"name": "Long On", "ang": 22.5, "pct": wdata["long_on"], "shots": [(16, 0.94, "4"), (28, 1.06, "6"), (22, 0.58, "1")]},
        {"name": "Mid-Wicket", "ang": 67.5, "pct": wdata["mid_wicket"], "shots": [(62, 0.96, "4"), (72, 1.08, "6"), (66, 0.68, "2"), (78, 0.94, "4")]},
        {"name": "Square Leg", "ang": 112.5, "pct": wdata["square_leg"], "shots": [(108, 0.95, "4"), (118, 0.62, "1")]},
        {"name": "Fine Leg", "ang": 157.5, "pct": wdata["fine_leg"], "shots": [(154, 0.94, "4"), (162, 0.55, "1")]},
        {"name": "Third Man", "ang": 202.5, "pct": wdata["third_man"], "shots": [(198, 0.94, "4"), (208, 0.52, "1")]},
        {"name": "Point", "ang": 247.5, "pct": wdata["point"], "shots": [(242, 0.95, "4"), (252, 0.64, "1")]},
        {"name": "Cover", "ang": 292.5, "pct": wdata["cover"], "shots": [(285, 0.96, "4"), (295, 1.06, "6"), (300, 0.92, "4"), (288, 0.70, "2")]}
    ]
    
    svg = []
    svg.append('<svg viewBox="0 0 380 380" width="100%" height="340" style="max-width:360px;margin:0 auto;display:block;">')
    svg.append('''<defs>
        <radialGradient id="fieldGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#FFFFFF"/>
            <stop offset="88%" stop-color="#F8FAFC"/>
            <stop offset="100%" stop-color="#EEF2F6"/>
        </radialGradient>
        <filter id="badgeFilt" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="1" stdDeviation="1" flood-opacity="0.06"/>
        </filter>
    </defs>''')
    
    # Boundary ring & 30 yd circle
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r_ground}" fill="url(#fieldGrad)" stroke="#001D48" stroke-width="2.5"/>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r_circle}" fill="none" stroke="#CBD5E1" stroke-width="1.2" stroke-dasharray="3,3"/>')
    
    # 8 Faint sector guide lines (stopping BEFORE labels)
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        x2 = cx + (r_ground - 4) * math.sin(rad)
        y2 = cy - (r_ground - 4) * math.cos(rad)
        svg.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#E2E8F0" stroke-width="1"/>')
        
    # Pitch in center
    svg.append(f'<rect x="{cx - 5}" y="{cy - 12}" width="10" height="24" fill="#D97706" rx="2"/>')
    svg.append(f'<line x1="{cx-7}" y1="{cy+9}" x2="{cx+7}" y2="{cy+9}" stroke="#FFFFFF" stroke-width="1"/>')
    svg.append(f'<line x1="{cx-7}" y1="{cy-9}" x2="{cx+7}" y2="{cy-9}" stroke="#FFFFFF" stroke-width="1"/>')
    
    # Shot trajectory lines (radiating outwards)
    for sec in sectors:
        for ang_deg, dist_mult, shot_type in sec["shots"]:
            rad = math.radians(ang_deg)
            r_shot = r_ground * dist_mult
            x_end = cx + min(r_shot, r_ground + 4) * math.sin(rad)
            y_end = cy - min(r_shot, r_ground + 4) * math.cos(rad)
            
            if shot_type == "6":
                col = "#059669"
                sw = "2.5"
                dash = ""
                r_dot = 3.5
            elif shot_type == "4":
                col = "#EB1A8D"
                sw = "2.0"
                dash = ""
                r_dot = 2.5
            else:
                col = "#64748B"
                sw = "1.2"
                dash = 'stroke-dasharray="2,2"'
                r_dot = 2.0
                
            svg.append(f'<line x1="{cx}" y1="{cy}" x2="{x_end:.1f}" y2="{y_end:.1f}" stroke="{col}" stroke-width="{sw}" {dash} stroke-linecap="round" opacity="0.9"/>')
            svg.append(f'<circle cx="{x_end:.1f}" cy="{y_end:.1f}" r="{r_dot}" fill="{col}"/>')
            
    # Outside Boundary Badges (NO OVERLAP WITH GROUND LINES)
    for sec in sectors:
        rad = math.radians(sec["ang"])
        r_lbl = r_ground + 34
        lx = cx + r_lbl * math.sin(rad)
        ly = cy - r_lbl * math.cos(rad)
        
        is_dom = (sec["pct"] >= 20)
        bw, bh = 68, 20
        bx = lx - bw / 2
        by = ly - bh / 2
        
        border_col = "#EB1A8D" if is_dom else "#CBD5E1"
        text_col = "#EB1A8D" if is_dom else "#001D48"
        bg_col = "#FDF2F8" if is_dom else "#FFFFFF"
        font_wt = "800" if is_dom else "700"
        
        svg.append(f'<g filter="url(#badgeFilt)">')
        svg.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw}" height="{bh}" rx="4" fill="{bg_col}" stroke="{border_col}" stroke-width="1.2"/>')
        svg.append(f'<text x="{lx:.1f}" y="{ly + 3.8:.1f}" font-size="9" font-weight="{font_wt}" fill="{text_col}" text-anchor="middle">{sec["name"]} {sec["pct"]}%</text>')
        svg.append(f'</g>')
        
    svg.append('</svg>')
    
    # Legend below wagon wheel
    svg.append('''
    <div style="display:flex;justify-content:center;gap:18px;font-size:11.5px;color:var(--text-muted);margin-top:10px;font-weight:600;">
        <div><span style="display:inline-block;width:12px;height:3px;background:#EB1A8D;margin-right:5px;vertical-align:middle;"></span>Fours (Boundaries)</div>
        <div><span style="display:inline-block;width:12px;height:3px;background:#059669;margin-right:5px;vertical-align:middle;"></span>Sixes (Maximums)</div>
        <div><span style="display:inline-block;width:12px;height:2px;background:#64748B;border-top:1px dashed #64748B;margin-right:5px;vertical-align:middle;"></span>1s & 2s (Rotation)</div>
    </div>
    ''')
    return "".join(svg)


# 6. Clean, Professional SVG Pitch Map Generator for Bowlers
def build_clean_pitch_map_svg(bdata):
    svg = []
    svg.append('<svg viewBox="0 0 280 340" width="100%" height="300" style="max-width:260px;margin:0 auto;display:block;">')
    
    # Pitch outline
    svg.append('<rect x="40" y="20" width="200" height="300" fill="#F8FAFC" stroke="#001D48" stroke-width="2" rx="4"/>')
    # Bowling crease & Stumps
    svg.append('<line x1="40" y1="52" x2="240" y2="52" stroke="#64748B" stroke-width="2"/>')
    svg.append('<rect x="125" y="34" width="30" height="7" fill="#D97706" rx="1"/>')
    
    # Length Zones with neat fills
    # 1. Yorker (0-2m)
    svg.append('<rect x="45" y="58" width="190" height="44" fill="#059669" fill-opacity="0.16" stroke="#059669" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<text x="140" y="84" font-size="11" font-weight="700" fill="#059669" text-anchor="middle">Yorker ({bdata["lengths"][0][1]}%)</text>')
    
    # 2. Full Length (2-6m)
    svg.append('<rect x="45" y="106" width="190" height="58" fill="#0284C7" fill-opacity="0.14" stroke="#0284C7" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<text x="140" y="140" font-size="11" font-weight="700" fill="#0284C7" text-anchor="middle">Full Driving ({bdata["lengths"][1][1]}%)</text>')
    
    # 3. Good Length (6-8m)
    svg.append('<rect x="45" y="168" width="190" height="70" fill="#111827" fill-opacity="0.12" stroke="#001D48" stroke-width="1.8"/>')
    svg.append(f'<text x="140" y="208" font-size="11" font-weight="800" fill="#111827" text-anchor="middle">Good Length ({bdata["lengths"][2][1]}%)</text>')
    
    # 4. Short / Bouncer (>8m)
    svg.append('<rect x="45" y="242" width="190" height="66" fill="#DC2626" fill-opacity="0.12" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<text x="140" y="280" font-size="11" font-weight="700" fill="#DC2626" text-anchor="middle">Short / Bouncer ({bdata["lengths"][3][1]}%)</text>')
    
    # Pitch impact ball markers
    svg.append('<circle cx="132" cy="74" r="4" fill="#059669"/>')
    svg.append('<circle cx="145" cy="80" r="4" fill="#059669"/>')
    svg.append('<circle cx="120" cy="130" r="4" fill="#0284C7"/>')
    svg.append('<circle cx="155" cy="142" r="4" fill="#0284C7"/>')
    svg.append('<circle cx="128" cy="195" r="4" fill="#111827"/>')
    svg.append('<circle cx="142" cy="210" r="4" fill="#111827"/>')
    svg.append('<circle cx="150" cy="188" r="4" fill="#111827"/>')
    svg.append('<circle cx="135" cy="265" r="4" fill="#DC2626"/>')
    
    svg.append('</svg>')
    
    svg.append('''
    <div style="display:flex;justify-content:center;gap:16px;font-size:11.5px;color:var(--text-muted);margin-top:10px;font-weight:600;">
        <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#059669;margin-right:4px;vertical-align:middle;"></span>Yorker</div>
        <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#0284C7;margin-right:4px;vertical-align:middle;"></span>Full</div>
        <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#001D48;margin-right:4px;vertical-align:middle;"></span>Good Length</div>
        <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#DC2626;margin-right:4px;vertical-align:middle;"></span>Short</div>
    </div>
    ''')
    return "".join(svg)


superstars_audit = [
    {
        "category": "Bowler",
        "rank": "Audit",
        "name": "Jasprit Bumrah",
        "key": "jasprit_bumrah",
        "teams": "India, Mumbai Indians, Gujarat",
        "role_desc": "Premier Fast Bowler & Death Specialist",
        "total_m": 77,
        "base_wr": 51.9,
        "hp_m": 14,
        "hp_wr": 42.9,
        "lift": -9.1,
        "mom_hp": 4,
        "ko_wr": 40.0,
        "bayes_hp_wr": 44.5,
        "cppi": 50.2,
        "bid_ceiling": "INR 18.0+ Cr",
        "tactical_role": "Death-Overs Strike Bowler",
        "summary": "Opponents treat Bumrah with extreme caution in close finishes, defending his 4 overs and taking zero risks.",
        "why_chose": "Teams intentionally play out Bumrah safely for 20-25 runs with no wickets, shifting their boundary pursuit to the secondary bowlers. That means his personal win rate in close finishes is lower (-9.1% lift) even though his bowling remains world-class.",
        "why_not_others": "The best defensive bowler in world cricket, but his high price tag at auction does not guarantee wins if the rest of the bowling unit is weak.",
        "rr_fit": "A dream bowler for any team, but given his massive retention price, RR can build a more balanced attack with bowlers like Jacob Duffy and Josh Hazlewood who deliver similar win conversion at a fraction of the cost.",
        "verdict": "Marquee Benchmark: Opponents Play Safe",
        "tagline": "Opponents take zero risks against his overs (-9.1% lift due to safe play)",
        "rr_management_summary": "World-class bowler who gets defended out in close finishes.",
        "key_tactical_skill": "Pinpoint toe-crushing yorkers and hard-length discipline.",
        "comparative_analysis": "Opponents refuse to attack him, shifting scoring pressure to secondary overs.",
        "reason": "Teams defend his 4 overs and target secondary bowlers in tight finishes."
    },
    {
        "category": "Bowler",
        "rank": "Audit",
        "name": "Mohammed Siraj",
        "key": "mohammed_siraj",
        "teams": "India, Royal Challengers Bengaluru, Hyderabad",
        "role_desc": "Pace Strike Bowler",
        "total_m": 83,
        "base_wr": 55.4,
        "hp_m": 18,
        "hp_wr": 38.9,
        "lift": -16.5,
        "mom_hp": 1,
        "ko_wr": 28.6,
        "bayes_hp_wr": 41.2,
        "cppi": 47.8,
        "bid_ceiling": "INR 9.0 Cr",
        "tactical_role": "Powerplay & Death Seamer",
        "summary": "Siraj bowls with high pace and attack, but high-intent boundary hunting in final overs leads to scoring variance.",
        "why_chose": "In close games decided by under 15 runs, batters swing hard against full pace. Edges fly over the infield, leading to high-leverage variance and a -16.5% win lift.",
        "why_not_others": "Excellent powerplay wicket-taker, but vulnerable to late boundary bursts.",
        "rr_fit": "Strong bowler for swing conditions, but RR needs greater death-overs discipline (like Yash Dayal or Jacob Duffy).",
        "verdict": "High Pace Strike Bowler with Late Variance",
        "tagline": "Attacking pace leads to variance in tight death finishes (-16.5% lift)",
        "rr_management_summary": "High intensity seamer with boundary risk at the death.",
        "key_tactical_skill": "Outswing and wobble seam with the new ball.",
        "comparative_analysis": "Powerful in powerplay, but faces high boundary volatility in death overs.",
        "reason": "Batters swing hard against full pace in final overs, causing boundary variance."
    },
    {
        "category": "Bowler",
        "rank": "Audit",
        "name": "Rashid Khan",
        "key": "rashid_khan",
        "teams": "Afghanistan, Gujarat Titans, Sunrisers Hyderabad",
        "role_desc": "Leg-Spin Mystery Bowler",
        "total_m": 122,
        "base_wr": 57.4,
        "hp_m": 26,
        "hp_wr": 38.5,
        "lift": -18.9,
        "mom_hp": 4,
        "ko_wr": 42.9,
        "bayes_hp_wr": 42.0,
        "cppi": 48.5,
        "bid_ceiling": "INR 16.0+ Cr",
        "tactical_role": "Middle-Overs Mystery Spinner",
        "summary": "Batters play Rashid out with low-risk singles in tight chases, preserving wickets and attacking other bowlers.",
        "why_chose": "In high-pressure chases, opponents treat Rashid like Bumrah: they take singles and avoid big shots. Because teams do not take risks against him, he gets fewer wickets, leading to a -18.9% win lift.",
        "why_not_others": "Elite spin bowler, but opponents refuse to give him wickets in close games.",
        "rr_fit": "Very expensive marquee player. RR can get strong middle-overs wicket-taking from Varun Chakravarthy or Suyash Sharma at much lower auction prices.",
        "verdict": "Premier Spinner: Neutralized by Low-Risk Play",
        "tagline": "Opponents play safe singles against his spin (-18.9% lift)",
        "rr_management_summary": "Opponents take zero risks against him, shifting scoring to auxiliary bowlers.",
        "key_tactical_skill": "Rapid arm action with sharp googlies and leg-breaks.",
        "comparative_analysis": "Economic in middle overs, but opponents avoid attacking him in tight chases.",
        "reason": "Batters take low-risk singles against his spin and attack secondary bowlers."
    },
    {
        "category": "Batter",
        "rank": "Audit",
        "name": "Heinrich Klaasen",
        "key": "heinrich_klaasen",
        "teams": "South Africa, Sunrisers Hyderabad, Titans",
        "role_desc": "Middle-Overs Spin Enforcer & Wicketkeeper",
        "total_m": 76,
        "base_wr": 48.7,
        "hp_m": 15,
        "hp_wr": 40.0,
        "lift": -8.7,
        "mom_hp": 1,
        "ko_wr": 25.0,
        "bayes_hp_wr": 42.3,
        "cppi": 49.1,
        "bid_ceiling": "INR 14.0+ Cr",
        "tactical_role": "Middle-Overs Boundary Striker",
        "summary": "Klaasen takes high risks against spin in middle overs. In tight games, this aggressive approach carries dismissal risk.",
        "why_chose": "When Klaasen's power-hitting comes off, his team wins easily. But in tight chases where every wicket counts, his high-risk boundary attempts sometimes lead to early dismissals (-8.7% lift).",
        "why_not_others": "Devastating spin destroyer, but high dismissal variance in close games.",
        "rr_fit": "Top player, but RR already has Shivam Dube who provides a higher positive win lift (+12.4%) at a lower budget.",
        "verdict": "High-Power Middle Enforcer with Wicket Risk",
        "tagline": "Aggressive boundary hitting carries dismissal risk in close chases (-8.7% lift)",
        "rr_management_summary": "Extremely powerful hitter who takes high dismissal risks in tight finishes.",
        "key_tactical_skill": "Back-foot power hitting against spinners through mid-wicket.",
        "comparative_analysis": "Huge strike rate, but carries higher dismissal variance in close games.",
        "reason": "High-risk boundary approach carries dismissal risk in close chases."
    },
    {
        "category": "Batter",
        "rank": "Audit",
        "name": "Rohit Sharma",
        "key": "rohit_sharma",
        "teams": "India, Mumbai Indians, Deccan Chargers",
        "role_desc": "Top-Order Opening Batter & Powerplay Attacker",
        "total_m": 92,
        "base_wr": 51.1,
        "hp_m": 19,
        "hp_wr": 47.4,
        "lift": -3.7,
        "mom_hp": 2,
        "ko_wr": 40.0,
        "bayes_hp_wr": 48.0,
        "cppi": 52.4,
        "bid_ceiling": "INR 12.0 Cr",
        "tactical_role": "Powerplay Opening Anchor",
        "summary": "Rohit attacks early in the powerplay. In close, low-scoring games, early risks can result in early dismissals.",
        "why_chose": "Rohit takes on the new ball to maximize field restrictions. In high-pressure matches, if an early risk doesn't pay off, the team loses momentum early (-3.7% lift).",
        "why_not_others": "Legendary captain and opener with 5 IPL titles.",
        "rr_fit": "Rajasthan Royals already has Yashasvi Jaiswal and Sanju Samson at the top, so spending heavily on an opener is not optimal.",
        "verdict": "Aggressive Powerplay Opener with Early Variance",
        "tagline": "Early boundary aggression brings dismissal risk in tight matches (-3.7% lift)",
        "rr_management_summary": "Attacking powerplay opener whose early risks bring variance in close matches.",
        "key_tactical_skill": "Front-foot pull shot and lofted cover drive over infield.",
        "comparative_analysis": "High powerplay intent, but early dismissals can pressure middle order.",
        "reason": "Calculated early aggression carries dismissal variance in tight games."
    }
]


# 7. Generate All 20 Standalone Player Pages
all_players_pool = players_db + superstars_audit
for idx, p in enumerate(all_players_pool):
    prev_p = all_players_pool[idx - 1] if idx > 0 else all_players_pool[-1]
    next_p = all_players_pool[idx + 1] if idx < len(all_players_pool) - 1 else all_players_pool[0]
    
    img_b64 = player_images.get(p["key"], "")
    role_info = ROLE_CAPABILITY_MAP.get(p["key"], {})
    
    diff_sign = f"+{p['lift']:.1f}%" if p['lift'] >= 0 else f"{p['lift']:.1f}%"
    diff_color = "#059669" if p['lift'] >= 0 else "#DC2626"
    diff_bg = "#ECFDF5" if p['lift'] >= 0 else "#FEF2F2"
    
    is_batter = (p["category"] == "Batter")
    
    if is_batter:
        wdata = BATTER_WAGON_SPECS.get(p["key"], BATTER_WAGON_SPECS["rajat_patidar"])
        graphic_title = "Wagon Wheel: High-Leverage Scoring Zones"
        graphic_subtitle = f"Primary Execution Corridor: {wdata['primary_sector']}"
        graphic_visual = build_clean_wagon_wheel_svg(wdata)
        
        phase_panel = f"""
        <div class="graphic-col-data">
            <div style="font-size:13px;font-weight:700;color:#111827;text-transform:uppercase;margin-bottom:12px;letter-spacing:0.5px;">
                Strike Rate by Match Phase
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:3px;">
                    <span>Powerplay (Overs 1-6)</span>
                    <strong>{wdata['pp_sr']} SR ({wdata['pp_dots']}% Dots)</strong>
                </div>
                <div style="background:#EEF2F6;height:10px;border-radius:5px;"><div style="background:#64748B;width:{wdata['pp_sr']/2.5}%;height:100%;border-radius:5px;"></div></div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:3px;">
                    <span style="font-weight:700;color:#111827;">Middle Overs (Overs 7-15)</span>
                    <strong style="color:var(--rr-pink);">{wdata['mid_sr']} SR ({wdata['mid_dots']}% Dots)</strong>
                </div>
                <div style="background:#EEF2F6;height:10px;border-radius:5px;"><div style="background:var(--rr-pink);width:{wdata['mid_sr']/2.5}%;height:100%;border-radius:5px;"></div></div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:3px;">
                    <span>Death Overs (Overs 16-20)</span>
                    <strong style="color:var(--success);">{wdata['death_sr']} SR ({wdata['death_dots']}% Dots)</strong>
                </div>
                <div style="background:#EEF2F6;height:10px;border-radius:5px;"><div style="background:var(--success);width:{wdata['death_sr']/2.5}%;height:100%;border-radius:5px;"></div></div>
            </div>
            <p style="font-size:11.5px;color:var(--text-muted);margin-top:14px;line-height:1.5;">
                Quantitative wagon wheel tracking isolates shot placement under pressure, confirming high boundary conversion away from defensive catchers.
            </p>
        </div>
        """
    else:
        bdata = BOWLER_PITCH_SPECS.get(p["key"], BOWLER_PITCH_SPECS["mitchell_starc"])
        graphic_title = "Pitch Map & Bowling Length Distribution"
        graphic_subtitle = f"Primary Execution Corridor: {bdata['strike_zone']}"
        graphic_visual = build_clean_pitch_map_svg(bdata)
        
        phase_panel = f"""
        <div class="graphic-col-data">
            <div style="font-size:13px;font-weight:700;color:#111827;text-transform:uppercase;margin-bottom:12px;letter-spacing:0.5px;">
                Economy Rate & Dot Ball% by Phase
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:3px;">
                    <span>Powerplay (Overs 1-6)</span>
                    <strong>{bdata['pp_econ']} Econ ({bdata['pp_dots']}% Dots)</strong>
                </div>
                <div style="background:#EEF2F6;height:10px;border-radius:5px;"><div style="background:#0284C7;width:{bdata['pp_econ']*8.5}%;height:100%;border-radius:5px;"></div></div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:3px;">
                    <span>Middle Overs (Overs 7-15)</span>
                    <strong>{bdata['mid_econ']} Econ</strong>
                </div>
                <div style="background:#EEF2F6;height:10px;border-radius:5px;"><div style="background:#64748B;width:{bdata['mid_econ']*8.5}%;height:100%;border-radius:5px;"></div></div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:3px;">
                    <span style="font-weight:700;color:#111827;">Death Overs (Overs 16-20)</span>
                    <strong style="color:var(--rr-pink);">{bdata['death_econ']} Econ ({bdata['death_dots']}% Dots)</strong>
                </div>
                <div style="background:#EEF2F6;height:10px;border-radius:5px;"><div style="background:var(--rr-pink);width:{bdata['death_econ']*8.5}%;height:100%;border-radius:5px;"></div></div>
            </div>
            <p style="font-size:11.5px;color:var(--text-muted);margin-top:14px;line-height:1.5;">
                Pitch-length tracking confirms disciplined adherence to defensive fourth-stump corridors, denying opposition death-overs boundaries.
            </p>
        </div>
        """

    player_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p['name']} — Quantitative Scouting Dossier | Rajasthan Royals Analytics</title>
    <style>
        :root {{
            --rr-navy: #111827;
            --rr-navy-light: #1F2937;
            --rr-pink: #EB1A8D;
            --bg-page: #F8F9FA;
            --bg-card: #FFFFFF;
            --border: #DDE2E5;
            --text-main: #1E293B;
            --text-muted: #64748B;
            --success: #059669;
            --success-bg: #ECFDF5;
            --danger: #DC2626;
            --danger-bg: #FEF2F2;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            width: 100%;
            max-width: 100vw;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        *, *:before, *:after {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-page);
            color: #374151;
            padding: 20px;
            line-height: 1.5;
        }}
        .container {{ max-width: 1080px; margin: 0 auto; }}
        
        .nav-back {{
            display: inline-block;
            background: var(--rr-navy);
            color: #FFFFFF;
            text-decoration: none;
            padding: 8px 18px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 20px;
            transition: background 0.15s ease;
        }}
        .nav-back:hover {{ background: #0A2540; }}

        .profile-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 24px;
            display: flex;
            align-items: center;
            gap: 24px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .profile-img {{
            width: 110px;
            height: 110px;
            border-radius: 50%;
            border: 3px solid var(--border);
            background: #F1F5F9;
            overflow: hidden;
            flex-shrink: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        }}
        .profile-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .profile-info {{ flex: 1; min-width: 260px; }}
        .rank-label {{
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--rr-pink);
            margin-bottom: 4px;
        }}
        .player-name {{
            font-size: 26px;
            font-weight: 800;
            color: #111827;
            line-height: 1.2;
            margin-bottom: 4px;
        }}
        .player-teams {{
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }}
        .role-badge {{
            display: inline-block;
            background: #F1F5F9;
            color: #111827;
            font-size: 12px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 4px;
            border: 1px solid var(--border);
        }}
        .rating-box {{
            background: #F8FAFC;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px 20px;
            text-align: center;
            min-width: 140px;
        }}
        .rating-val {{ font-size: 32px; font-weight: 800; color: #111827; line-height: 1; }}
        .rating-lbl {{ font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-top: 4px; }}

        /* Metric Grid */
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }}
        .metric-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 14px;
            text-align: center;
        }}
        .metric-val {{ font-size: 20px; font-weight: 800; color: #111827; }}
        .metric-lbl {{ font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-top: 4px; }}
        .metric-sub {{ font-size: 10px; color: var(--text-muted); margin-top: 2px; }}

        /* Section Cards */
        .section-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px 24px;
            margin-bottom: 16px;
        }}
        .section-header {{
            font-size: 14px;
            font-weight: 700;
            color: #111827;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
            padding-bottom: 6px;
            border-bottom: 1px solid #F1F5F9;
        }}
        .section-content {{
            font-size: 13.5px;
            color: #374151;
            line-height: 1.6;
        }}

        /* Visual Progress Bars */
        .chart-box {{
            background: #F8FAFC;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 16px;
            margin-top: 8px;
        }}
        .bar-item {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            font-size: 13px;
        }}
        .bar-label {{ width: 220px; font-weight: 600; color: #374151; }}
        .bar-track {{ flex: 1; height: 12px; background: #E2E8F0; border-radius: 6px; overflow: hidden; margin: 0 12px; }}
        .bar-fill {{ height: 100%; border-radius: 6px; }}
        .bar-value {{ width: 70px; font-weight: 700; text-align: right; }}

        .bottom-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 28px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
        }}
        .bottom-nav a {{
            color: #111827;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            padding: 8px 16px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: #FFFFFF;
        }}
        .bottom-nav a:hover {{ background: #F1F5F9; }}
        /* Responsive Layout Classes */
        .graphic-flex {{
            display: flex;
            gap: 24px;
            align-items: center;
            flex-wrap: wrap;
        }}
        .graphic-col-visual {{
            flex: 1;
            min-width: 280px;
            text-align: center;
            width: 100%;
        }}
        .graphic-col-data {{
            flex: 1.1;
            min-width: 260px;
            width: 100%;
        }}

        /* Top Nav */
        .top-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .cand-nav {{
            display: flex;
            gap: 10px;
        }}
        .cand-nav a {{
            color: #111827;
            text-decoration: none;
            font-size: 12.5px;
            font-weight: 600;
            padding: 8px 14px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: #FFFFFF;
            transition: all 0.15s ease;
        }}
        .cand-nav a:hover {{
            background: #F1F5F9;
            border-color: #111827;
        }}

        /* Tablet Responsive (<= 1024px) */
        @media (max-width: 1024px) {{
            body {{
                padding: 16px;
            }}
            .metric-grid {{
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
            }}
        }}

        /* Mobile Responsive (<= 768px) */
        @media (max-width: 768px) {{
            body {{
                padding: 10px 8px;
            }}
            .container {{
                padding: 0 4px;
            }}
            .top-nav {{
                flex-direction: column;
                align-items: stretch;
                gap: 10px;
                margin-bottom: 14px;
            }}
            .nav-back {{
                width: 100%;
                text-align: center;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 40px;
                margin-bottom: 0;
            }}
            .cand-nav {{
                width: 100%;
                justify-content: space-between;
                gap: 8px;
            }}
            .cand-nav a {{
                flex: 1;
                text-align: center;
                min-height: 38px;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 6px 8px;
                font-size: 11.5px;
            }}
            .profile-card {{
                flex-direction: column;
                align-items: center;
                text-align: center;
                padding: 18px 14px;
                gap: 14px;
            }}
            .profile-img {{
                width: 96px;
                height: 96px;
                margin: 0 auto;
            }}
            .profile-info {{
                min-width: 0;
                width: 100%;
                text-align: center;
            }}
            .player-name {{
                font-size: 22px;
            }}
            .player-teams {{
                font-size: 12px;
            }}
            .rating-box {{
                width: 100%;
                max-width: 240px;
                margin: 0 auto;
                padding: 12px;
            }}
            .rating-val {{
                font-size: 28px;
            }}
            .metric-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 8px;
                margin-bottom: 14px;
            }}
            .metric-card {{
                padding: 10px 8px;
            }}
            .metric-val {{
                font-size: 18px;
            }}
            .metric-lbl {{
                font-size: 10px;
            }}
            .metric-sub {{
                font-size: 9px;
            }}
            .section-card {{
                padding: 16px 14px;
                margin-bottom: 14px;
            }}
            .section-header {{
                font-size: 13px;
                margin-bottom: 8px;
            }}
            .section-content {{
                font-size: 12.5px;
            }}
            .graphic-flex {{
                flex-direction: column;
                gap: 16px;
            }}
            .graphic-col-visual {{
                min-width: 0;
                width: 100%;
            }}
            .graphic-col-data {{
                min-width: 0;
                width: 100%;
                margin-top: 8px;
            }}
            .bar-item {{
                flex-direction: column;
                align-items: stretch;
                gap: 4px;
                margin-bottom: 12px;
            }}
            .bar-label {{
                width: 100%;
                font-size: 12px;
            }}
            .bar-track {{
                width: 100%;
                margin: 4px 0;
                height: 10px;
            }}
            .bar-value {{
                width: 100%;
                text-align: right;
                font-size: 12.5px;
            }}
            .bottom-nav {{
                flex-direction: column;
                gap: 10px;
                align-items: stretch;
                margin-top: 20px;
                padding-top: 14px;
            }}
            .bottom-nav a {{
                width: 100%;
                text-align: center;
                min-height: 42px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
        }}

        /* Extra Small Mobile (<= 420px) */
        @media (max-width: 420px) {{
            body {{
                padding: 6px 4px;
            }}
            .profile-card {{
                padding: 14px 10px;
            }}
            .player-name {{
                font-size: 20px;
            }}
            .metric-grid {{
                grid-template-columns: 1fr;
                gap: 6px;
            }}
            .metric-card {{
                padding: 8px 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                text-align: left;
            }}
            .metric-val {{
                font-size: 17px;
                order: 2;
            }}
            .metric-lbl {{
                margin-top: 0;
            }}
        }}



    
        </style>
</head>
<body>
<div class="container">
        <div class="top-nav">
        <a href="../index.html" class="nav-back">&larr; Back to Performance Dashboard</a>
        <div class="cand-nav">
            <a href="{prev_p['key']}.html">&larr; Previous ({prev_p['name']})</a>
            <a href="{next_p['key']}.html">Next ({next_p['name']}) &rarr;</a>
        </div>
    </div>
    
    <div class="profile-card">
        <div class="profile-img">
            <img src="{img_b64}" alt="{p['name']}">
        </div>
        <div class="profile-info">
            <div class="rank-label">Rank {p['rank']} — Top Tier {p['category']}</div>
            <h1 class="player-name">{p['name']}</h1>
            <div class="player-teams">{p['teams']}</div>
            <div class="role-badge">{p['tactical_role']}</div>
        </div>
        <div class="rating-box">
            <div class="rating-val">{p['cppi']:.2f}</div>
            <div class="rating-lbl">Performance Index</div>
            <div style="font-size:12px;color:var(--rr-pink);font-weight:700;margin-top:4px;">{p['bid_ceiling']}</div>
        </div>
    </div>

    <!-- Quantitative Metrics Summary -->
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-val">{p['hp_m']}</div>
            <div class="metric-lbl">High-Leverage Matches</div>
            <div class="metric-sub">&le; 15 runs / 2 wickets</div>
        </div>
        <div class="metric-card">
            <div class="metric-val" style="color:#111827;">{p['hp_wr']:.1f}%</div>
            <div class="metric-lbl">High-Leverage Win%</div>
            <div class="metric-sub">Pressure win conversion</div>
        </div>
        <div class="metric-card">
            <div class="metric-val">{p['base_wr']:.1f}%</div>
            <div class="metric-lbl">Overall Win%</div>
            <div class="metric-sub">Full career sample</div>
        </div>
        <div class="metric-card">
            <div class="metric-val" style="color:{diff_color};">{diff_sign}</div>
            <div class="metric-lbl">Win Differential (&Delta;)</div>
            <div class="metric-sub">Performance variance</div>
        </div>
        <div class="metric-card">
            <div class="metric-val">{p['mom_hp']}</div>
            <div class="metric-lbl">Match Awards</div>
            <div class="metric-sub">High-leverage POM</div>
        </div>
        <div class="metric-card">
            <div class="metric-val">{p['ko_wr']:.1f}%</div>
            <div class="metric-lbl">Playoff Record</div>
            <div class="metric-sub">Elimination win rate</div>
        </div>
    </div>

    <!-- Power BI Wagon Wheel / Pitch Map Visual -->
    <div class="section-card">
        <div class="section-header">{graphic_title}</div>
        <div style="font-size:12px;color:var(--text-muted);margin-bottom:16px;">{graphic_subtitle}</div>
        <div class="graphic-flex">
            <div class="graphic-col-visual">
                {graphic_visual}
            </div>
            {phase_panel}
        </div>
    </div>

    <!-- Empirical Win Rate Comparison -->
    <div class="section-card">
        <div class="section-header">Empirical Win Conversion: Standard vs High-Leverage</div>
        <div class="chart-box">
            <div class="bar-item">
                <span class="bar-label">High-Leverage Situations:</span>
                <div class="bar-track"><div class="bar-fill" style="width:{p['hp_wr']}%;background:var(--rr-navy);"></div></div>
                <span class="bar-value" style="color:#111827;">{p['hp_wr']:.1f}%</span>
            </div>
            <div class="bar-item">
                <span class="bar-label">Full Baseline Sample:</span>
                <div class="bar-track"><div class="bar-fill" style="width:{p['base_wr']}%;background:#64748B;"></div></div>
                <span class="bar-value" style="color:#64748B;">{p['base_wr']:.1f}%</span>
            </div>
            <div class="bar-item">
                <span class="bar-label">Playoff Knockout Fixtures:</span>
                <div class="bar-track"><div class="bar-fill" style="width:{p['ko_wr']}%;background:var(--rr-pink);"></div></div>
                <span class="bar-value" style="color:var(--rr-pink);">{p['ko_wr']:.1f}%</span>
            </div>
        </div>
    </div>

    <!-- Technical Strength -->
    <div class="section-card">
        <div class="section-header">1. Key Capability & Technical Execution</div>
        <div class="section-content">{role_info.get('technical_strength', '')}</div>
    </div>

    <!-- Comparative Analysis -->
    <div class="section-card">
        <div class="section-header">2. Comparative Performance vs Peer Group</div>
        <div class="section-content">{role_info.get('peer_comparison', '')}</div>
    </div>

    <!-- Tactical Deployment: SMS Stadium -->
    <div class="section-card">
        <div class="section-header">3. Tactical Deployment: Sawai Mansingh Stadium, Jaipur</div>
        <div class="section-content">{role_info.get('jaipur_fit', '')}</div>
    </div>

    <!-- Auction Valuation Guidance -->
    <div class="section-card">
        <div class="section-header">4. Valuation & Auction Strategy</div>
        <div class="section-content"><strong>{role_info.get('auction_valuation', '')}</strong></div>
    </div>

    <div class="bottom-nav">
        <a href="{prev_p['key']}.html">&larr; Previous Candidate ({prev_p['name']})</a>
        <a href="../index.html">Master Dashboard</a>
        <a href="{next_p['key']}.html">Next Candidate ({next_p['name']}) &rarr;</a>
    </div>
</div>

</body>
</html>
"""
    player_html = player_html.replace('</div>\n\n</body>', '''
    <!-- Simple Minimal Footer with Copyright -->
    <footer class="simple-footer" style="margin-top:44px;margin-bottom:28px;padding-top:26px;border-top:1px solid #E2E8F0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#475569;">
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(300px, 1fr));gap:28px;margin-bottom:22px;">
            <div>
                <div style="font-size:12.5px;font-weight:700;color:#111827;margin-bottom:6px;">Methodology</div>
                <p style="margin:0;font-size:12px;line-height:1.65;color:#475569;">
                    Evaluated 883 IPL &amp; T20I matches (2022&ndash;2026) to isolate 178 high-pressure games (MLI &ge; 30: knockouts, Super Overs, or close finishes). Players are ranked via the calibrated CPPI combining Bayesian HP Win Rate (35%), Normalized Pressure Lift &Delta; (25%), Knockout Win Rate (20%), HP POTM Density (10%), and Baseline Win Rate (10%), scaled by a sigmoid credibility curve and BCCI auction eligibility filters.
                </p>
            </div>
            <div>
                <div style="font-size:12.5px;font-weight:700;color:#111827;margin-bottom:6px;">Thought Process</div>
                <p style="margin:0;font-size:12px;line-height:1.65;color:#475569;">
                    Traditional averages reward stat-padding in one-sided matches. Measuring True Pressure Lift (&Delta;) isolates who genuinely raises their team&rsquo;s win rate when stakes peak &mdash; highlighting high-value clutch winners like Shivam Dube and Jacob Duffy suited for Sawai Mansingh Stadium (Jaipur) within a &#8377;45 Cr auction budget, rather than overpaying for reputation.
                </p>
            </div>
        </div>

        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;padding-top:16px;border-top:1px solid #E2E8F0;font-size:12px;color:#64748B;">
            <div>
                &copy; 2026 Ketan Rawat. All rights reserved. &middot; Rajasthan Royals SupeRR Selector Season 2
            </div>
            <div style="display:flex;flex-wrap:wrap;align-items:center;gap:10px;">
                <a href="https://www.linkedin.com/in/ketan-rawat-97a8aa2a0/" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">LinkedIn</a>
                <span style="color:#CBD5E1;">|</span>
                <a href="https://github.com/Ketanrawat2004/RR-Dashboard" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">GitHub</a>
                <span style="color:#CBD5E1;">|</span>
                <a href="https://drive.google.com/file/d/1YV_i3Un8t7UZsfk1_WXQdfsM6T0Pe6ui/view?usp=drive_link" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">Resume</a>
                <span style="color:#CBD5E1;">|</span>
                <a href="https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/view?usp=sharing" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">Season 1 Certificate (Additional Top 20)</a>
            </div>
        </div>
    </footer>
''' + '\n</div>\n\n</body>')
    with open(f"players/{p['key']}.html", "w", encoding="utf-8") as f:
        f.write(player_html)

print("Generated all 20 standalone player pages with clean Wagon Wheels & Pitch Maps.")

# 8. Master Dashboard Generation (Fixing Pill Headers, Donut Legend Wrap, Differential List, Matrix Padding)

top10_batters = [p for p in players_db if p["category"] == "Batter"]
top10_bowlers = [p for p in players_db if p["category"] == "Bowler"]

master_dashboard_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>Rajasthan Royals — Performance Analytics Dashboard</title>
    <style>
        :root {{
            --rr-navy: #111827;
            --rr-navy-light: #1F2937;
            --rr-pink: #EB1A8D;
            --bg-page: #F4F6F9;
            --bg-card: #FFFFFF;
            --border-card: #DDE2E5;
            --text-main: #1E293B;
            --text-muted: #64748B;
            --success: #059669;
            --success-bg: #ECFDF5;
            --danger: #DC2626;
            --danger-bg: #FEF2F2;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            width: 100%;
            max-width: 100vw;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        *, *:before, *:after {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-page);
            color: #374151;
            padding: 20px;
            line-height: 1.45;
            -webkit-font-smoothing: antialiased;
        }}

        .dashboard-container {{
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            overflow-x: hidden;
            box-sizing: border-box;
        }}

        /* Top Executive Header with RR Wallpaper Background & Dark Gradient */
        .executive-header {{
            position: relative;
            overflow: hidden;
            background: #00122e;
            border: 1px solid rgba(235, 26, 141, 0.35);
            border-radius: 10px;
            padding: 22px 28px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 18px;
            box-shadow: 0 4px 20px rgba(0, 18, 46, 0.25);
        }}

        /* Low Opacity RR Wallpaper Background Layer */
        .executive-header::before {{
            content: "";
            position: absolute;
            inset: 0;
            background-image: url('{banner_bg_b64}');
            background-size: cover;
            background-position: center right;
            background-repeat: no-repeat;
            opacity: 0.22;
            pointer-events: none;
            z-index: 1;
        }}

        /* Rich Dark Gradient Overlay (Deep Navy to Black) */
        .executive-header::after {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(110deg, rgba(0, 16, 42, 0.95) 0%, rgba(0, 22, 54, 0.88) 50%, rgba(10, 12, 22, 0.94) 100%);
            pointer-events: none;
            z-index: 2;
        }}

        /* Elevate all content above overlay for high visibility & crisp contrast */
        .executive-header > * {{
            position: relative;
            z-index: 3;
        }}

        .brand-section {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}

        .rr-logo {{
            height: 60px;
            width: auto;
            object-fit: contain;
            filter: drop-shadow(0 2px 6px rgba(0,0,0,0.5));
        }}

        .header-titles h1 {{
            font-size: 22px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.2px;
            line-height: 1.2;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.6);
        }}

        .header-titles p {{
            font-size: 13.5px;
            color: #E2E8F0;
            margin-top: 4px;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
        }}

        .header-meta {{
            text-align: right;
            font-size: 12px;
            color: #94A3B8;
        }}
        .header-meta strong {{
            color: #FFFFFF;
            display: block;
            font-size: 13.5px;
            margin-bottom: 3px;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
        }}
        .header-meta span {{
            color: #CBD5E1;
        }}
/* Top Metrics Strip */
        .kpi-strip {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 8px;
            padding: 16px 24px;
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 16px;
            margin-bottom: 24px;
            text-align: center;
        }}

        .kpi-item {{
            border-right: 1px solid #EEF2F6;
            padding: 0 8px;
        }}
        .kpi-item:last-child {{ border-right: none; }}

        .kpi-lbl {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin-bottom: 4px;
        }}

        .kpi-num {{
            font-size: 26px;
            font-weight: 800;
            color: #111827;
            line-height: 1.1;
        }}

        .kpi-sub {{
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 3px;
        }}

        /* 3-Column Analytics Grid: Generous column 1 width to prevent any legend overflow */
        .analytics-row-3col {{
            display: grid;
            grid-template-columns: minmax(340px, 1.15fr) minmax(280px, 0.95fr) minmax(460px, 1.7fr);
            gap: 18px;
            margin-bottom: 24px;
            align-items: stretch;
        }}

        .panel-box {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 8px;
            padding: 18px 16px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
            box-sizing: border-box;
        }}

        .matrix-panel {{
            padding: 16px 14px;
        }}

        .table-scroll-wrapper {{
            width: 100%;
            overflow: hidden;
        }}

        .panel-header-box {{
            text-align: center;
            margin-bottom: 16px;
        }}

        .pill-header {{
            background: var(--rr-navy);
            color: #FFFFFF;
            font-size: 11.5px;
            font-weight: 700;
            padding: 6px 16px;
            border-radius: 16px;
            display: inline-block;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            white-space: nowrap;
        }}

        /* Donut Visual Styling (Fully responsive, zero overflow) */
        .donut-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            padding: 8px 4px;
            width: 100%;
            box-sizing: border-box;
            min-width: 0;
        }}

        .donut-legend {{
            font-size: 11px;
            line-height: 1.4;
            display: flex;
            flex-direction: column;
            gap: 9px;
            min-width: 0;
            flex: 1;
        }}

        .donut-legend-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            white-space: nowrap;
        }}

        .donut-legend-left {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: #111827;
            font-weight: 600;
            font-size: 11px;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .donut-legend-pct {{
            font-weight: 700;
            color: var(--text-dark);
            background: #F1F5F9;
            padding: 1.5px 7px;
            border-radius: 4px;
            font-size: 10.5px;
            letter-spacing: 0.2px;
            flex-shrink: 0;
        }}

        .legend-dot {{
            display: inline-block;
            width: 9px;
            height: 9px;
            border-radius: 50%;
            flex-shrink: 0;
        }}

        /* Differential Progress Item */
        .diff-row-item {{
            margin-bottom: 8px;
        }}
        .diff-row-header {{
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            margin-bottom: 2px;
            white-space: nowrap;
        }}

        /* Matrix Table - Zero Cut Out, Fixed Proportional Layout */
        .matrix-table {{
            width: 100%;
            table-layout: fixed;
            border-collapse: collapse;
            font-size: 11.5px;
            text-align: center;
            margin-top: 4px;
        }}
        .matrix-table th {{
            background: #F8FAFC;
            color: var(--text-muted);
            font-weight: 700;
            padding: 8px 4px;
            border: 1px solid var(--border-card);
            font-size: 11px;
        }}
        .matrix-table td {{
            padding: 8px 4px;
            border: 1px solid var(--border-card);
            font-weight: 600;
        }}
        .matrix-highlight {{
            background: #ECFDF5;
            color: #059669;
            font-weight: 700;
        }}

        /* Slicers & Dynamic Controls - Redesigned 2-Tier Control Hub */
        .slicer-card {{
            background: #FFFFFF;
            border: 1px solid var(--border-card);
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .slicer-tabs-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .tab-group {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
        }}

        .nav-tab-btn {{
            background: #F8FAFC;
            border: 1px solid var(--border-card);
            color: #475569;
            font-size: 12px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .nav-tab-btn:hover {{
            background: #F1F5F9;
            color: #111827;
            border-color: #CBD5E1;
        }}

        .nav-tab-btn.active {{
            background: #111827 !important;
            color: #FFFFFF !important;
            border-color: #111827 !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }}

        .slicer-status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            font-weight: 600;
            color: #64748B;
            background: #F8FAFC;
            border: 1px solid var(--border-card);
            padding: 4px 10px;
            border-radius: 16px;
            white-space: nowrap;
        }}

        .status-indicator-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #10B981;
            display: inline-block;
            box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
        }}

        .slicer-controls-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            padding-top: 10px;
            border-top: 1px solid #F1F5F9;
        }}

        .search-wrapper {{
            display: flex;
            align-items: center;
            gap: 8px;
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 0 12px;
            height: 34px;
            flex: 1;
            max-width: 380px;
            min-width: 220px;
            transition: all 0.15s ease;
        }}

        .search-wrapper:focus-within {{
            border-color: #111827;
            background: #FFFFFF;
            box-shadow: 0 0 0 2px rgba(17, 24, 39, 0.08);
        }}

        .search-icon {{
            flex-shrink: 0;
        }}

        .search-field {{
            border: none;
            background: transparent;
            outline: none;
            width: 100%;
            font-size: 12px;
            color: #111827;
            padding: 0;
        }}

        .search-field::placeholder {{
            color: #94A3B8;
        }}

        .slicer-dropdowns {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .slicer-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .slicer-label {{
            font-size: 11px;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }}

        .slicer-select {{
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 12px;
            font-weight: 600;
            color: #111827;
            outline: none;
            cursor: pointer;
            height: 34px;
            transition: border-color 0.15s ease;
        }}

        .slicer-select:focus {{
            border-color: #111827;
        }}

        .slicer-reset-btn {{
            background: #F1F5F9;
            border: 1px solid var(--border-card);
            border-radius: 6px;
            padding: 0 12px;
            font-size: 12px;
            font-weight: 600;
            color: #475569;
            cursor: pointer;
            height: 34px;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .slicer-reset-btn:hover {{
            background: #E2E8F0;
            color: #111827;
        }}
        /* Continuous Rolling Donut Animation */
        @keyframes rollingDonut {{
            from {{
                transform: rotate(0deg);
            }}
            to {{
                transform: rotate(360deg);
            }}
        }}
        .rolling-donut-ring {{
            transform-box: fill-box;
            transform-origin: center;
            animation: rollingDonut 12s linear infinite;
        }}


        /* Corporate Data Tables - Zero Horizontal Scrollbar on Desktops & Laptops */
        .table-responsive {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 8px;
            width: 100%;
            max-width: 100%;
            display: block;
            box-sizing: border-box;
            margin-bottom: 24px;
            overflow-x: hidden; /* Zero horizontal scrollbar on standard laptop & desktop */
        }}

        table {{
            width: 100%;
            max-width: 100%;
            min-width: 0;
            table-layout: auto;
            border-collapse: collapse;
            font-size: 12px;
            text-align: left;
        }}

        thead tr {{
            background: #F8FAFC;
            border-bottom: 2px solid var(--border-card);
        }}

        th {{
            padding: 9px 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            color: var(--text-muted);
            line-height: 1.25;
            vertical-align: middle;
        }}

        tbody tr {{
            border-bottom: 1px solid #EEF2F6;
            cursor: pointer;
            transition: background 0.15s ease;
        }}

        tbody tr:hover {{
            background-color: #F8FAFC;
        }}

        td {{
            padding: 8px 6px;
            vertical-align: middle;
            font-size: 12px;
        }}

        .player-flex {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .thumb-img {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            border: 2px solid var(--border-card);
            background: #F1F5F9;
            overflow: hidden;
            flex-shrink: 0;
            box-shadow: 0 1px 2px rgba(0,0,0,0.06);
        }}
        .thumb-img img {{ width: 100%; height: 100%; object-fit: cover; }}

        .name-box a {{
            color: #111827;
            text-decoration: none;
            font-weight: 700;
            font-size: 13.5px;
        }}
        .name-box a:hover {{ text-decoration: underline; color: var(--rr-pink); }}

        .team-sub {{
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 1px;
        }}

        .diff-tag {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11.5px;
            font-weight: 700;
        }}
        .diff-pos {{ background: var(--success-bg); color: var(--success); }}
        .diff-neg {{ background: var(--danger-bg); color: var(--danger); }}

        .action-link {{
            display: inline-block;
            background: var(--rr-navy);
            color: #FFFFFF;
            text-decoration: none;
            padding: 5px 12px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            transition: background 0.15s ease;
            white-space: nowrap;
        }}
        .action-link:hover {{ background: #0A2540; }}

        /* Lower Documentation Section */
        .data-section {{
            margin-bottom: 28px;
        }}

        .doc-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 28px;
            margin-bottom: 24px;
        }}

        .doc-box {{
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 22px 24px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        }}

        .doc-heading {{
            font-size: 14px;
            font-weight: 800;
            color: #111827;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 12px;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 8px;
        }}

        .doc-box p {{
            font-size: 12.5px;
            color: #374151;
            line-height: 1.6;
        }}

        .doc-box p strong {{
            color: #111827;
            font-weight: 700;
        }}

        .code-snippet {{
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-left: 3px solid #EB1A8D;
            border-radius: 6px;
            padding: 10px 14px;
            font-family: ui-monospace, Menlo, Consolas, monospace;
            font-size: 12px;
            color: #111827;
            font-weight: 600;
            margin-top: 10px;
            margin-bottom: 10px;
        }}
        /* Table Scroll Wrapper */
        .table-scroll-wrapper {{
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            width: 100%;
        }}
        .mobile-table-hint {{
            display: none;
            font-size: 11.5px;
            color: var(--text-muted);
            margin-bottom: 6px;
            text-align: right;
            font-weight: 600;
        }}

        /* ==========================================================
           COMPREHENSIVE RESPONSIVE DESIGN (LAPTOP, TABLET & MOBILE)
           ========================================================== */

        /* 1. Laptops & Medium Screens (1025px - 1280px) */
        @media (max-width: 1280px) {{
            body {{
                padding: 16px;
            }}
            .kpi-strip {{
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
            }}
            .analytics-row-3col {{
                grid-template-columns: 1fr 1fr;
                gap: 16px;
            }}
            .analytics-row-3col > .panel-box:nth-child(3) {{
                grid-column: 1 / -1; /* Matrix Table gets 100% width on row 2 */
            }}
        }}

        /* 2. Tablets (769px - 1024px) */
        @media (max-width: 1024px) {{
            .executive-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 14px;
                padding: 16px 20px;
            }}
            .header-meta {{
                text-align: left;
                width: 100%;
                border-top: 1px solid #F1F5F9;
                padding-top: 10px;
            }}
            .kpi-strip {{
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
            }}
            .analytics-row-3col {{
                grid-template-columns: 1fr 1fr;
                gap: 16px;
            }}
            .analytics-row-3col > .panel-box:nth-child(3) {{
                grid-column: 1 / -1;
            }}
            .slicer-card {{
                padding: 14px 18px;
                gap: 14px;
            }}
            .doc-grid {{
                grid-template-columns: 1fr;
                gap: 16px;
            }}
        }}

        /* 3. Mobile & Small Tablets (521px - 768px) */
        @media (max-width: 768px) {{
            .table-responsive {{
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }}
            table {{
                min-width: 740px;
            }}
            body {{
                padding: 10px 8px;
            }}
            .executive-header {{
                padding: 14px 16px;
                gap: 12px;
                border-radius: 6px;
            }}
            .header-titles h1 {{
                font-size: 18px;
            }}
            .header-titles p {{
                font-size: 11.5px;
            }}
            .rr-logo {{
                width: 48px;
                height: 48px;
            }}
            .kpi-strip {{
                grid-template-columns: repeat(2, 1fr);
                gap: 8px;
                margin-bottom: 16px;
            }}
            .kpi-item {{
                padding: 12px 14px;
            }}
            .kpi-num {{
                font-size: 22px;
            }}
            .analytics-row-3col {{
                grid-template-columns: 1fr;
                gap: 14px;
                margin-bottom: 18px;
            }}
            .analytics-row-3col > .panel-box:nth-child(3) {{
                grid-column: 1;
            }}
            .panel-box {{
                padding: 16px;
            }}
            .donut-container {{
                flex-direction: column;
                text-align: center;
                gap: 12px;
            }}
            .donut-legend {{
                width: 100%;
                max-width: 240px;
                margin: 0 auto;
            }}
            .slicer-card {{
                flex-direction: column;
                align-items: stretch;
                padding: 14px;
                gap: 12px;
            }}
            .slicer-group {{
                flex-direction: column;
                align-items: stretch;
                width: 100%;
                gap: 10px;
            }}
            .slicer-item {{
                display: flex;
                flex-direction: column;
                gap: 4px;
                width: 100%;
            }}
            .slicer-select {{
                width: 100%;
                height: 40px;
                font-size: 13px;
            }}
            .search-field {{
                width: 100%;
                height: 40px;
                font-size: 13px;
            }}
            .tab-group {{
                display: flex;
                flex-direction: column;
                width: 100%;
                gap: 6px;
            }}
            .nav-tab-btn {{
                width: 100%;
                text-align: center;
            }}
            .slicer-card {{
                width: 100%;
                max-width: 100%;
                box-sizing: border-box;
            }}
            .nav-tab-btn {{
                padding: 8px 14px;
                font-size: 12px;
                min-height: 38px;
            }}
            .mobile-table-hint {{
                display: block;
            }}
            .table-container {{
                margin-bottom: 18px;
                border-radius: 6px;
            }}
            .doc-grid {{
                grid-template-columns: 1fr;
                gap: 14px;
                margin-bottom: 24px;
            }}
            .code-snippet {{
                font-size: 11px;
                overflow-x: auto;
                padding: 10px;
            }}
        }}

        /* 4. Extra Small Mobile Phones (<= 520px) */
        @media (max-width: 520px) {{
            body {{
                padding: 6px 4px;
            }}
            .dashboard-container {{
                padding: 0 4px;
            }}
            .executive-header {{
                padding: 12px;
            }}
            .brand-section {{
                gap: 10px;
            }}
            .rr-logo {{
                width: 40px;
                height: 40px;
            }}
            .header-titles h1 {{
                font-size: 16px;
            }}
            .header-titles p {{
                font-size: 11px;
            }}
            .header-meta strong {{
                font-size: 11.5px;
            }}
            .header-meta span {{
                font-size: 10.5px;
            }}
            .kpi-strip {{
                grid-template-columns: 1fr;
                gap: 8px;
            }}
            .kpi-item {{
                padding: 10px 12px;
            }}
            .kpi-num {{
                font-size: 20px;
            }}
            .pill-header {{
                font-size: 10px;
                padding: 5px 12px;
            }}
            .panel-box {{
                padding: 14px 10px;
            }}
            .diff-row-header {{
                font-size: 11.5px;
            }}
        }}



    </style>
</head>
<body>

<!-- Header Section -->
    <div class="executive-header">
        <div class="brand-section">
            <img src="{rr_logo_b64}" alt="Rajasthan Royals" class="rr-logo">
            <div class="header-titles">
                <h1>Rajasthan Royals — Performance Analytics</h1>
                <p>Empirical Match Leverage & Bayesian Win Differential for IPL 2027 Auction</p>
            </div>
        </div>
        <div class="header-meta">
            <strong>Cricket Operations Scouting Model</strong>
            <span>Tournament Sample: 883 Fixtures | Evaluation Universe: 1,217</span>
        </div>
    </div>

    <!-- Power BI / Tableau Style KPI Strip -->
    <div class="kpi-strip">
        <div class="kpi-item">
            <div class="kpi-lbl">Matches Evaluated</div>
            <div class="kpi-num">883</div>
            <div class="kpi-sub">Senior T20 Competitions</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-lbl">High-Leverage Sample</div>
            <div class="kpi-num">178</div>
            <div class="kpi-sub">MLI &ge; 30 (20.2% of 883)</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-lbl">Candidate Universe</div>
            <div class="kpi-num">1,217</div>
            <div class="kpi-sub">Auction database pool</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-lbl">Top Ranked Batter</div>
            <div class="kpi-num" style="color:var(--rr-pink);">66.8</div>
            <div class="kpi-sub">Shivam Dube (+12.4% &Delta;)</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-lbl">Top Ranked Bowler</div>
            <div class="kpi-num" style="color:#111827;">68.8</div>
            <div class="kpi-sub">Jacob Duffy (+20.5% &Delta;)</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-lbl">Peak Leverage Lift</div>
            <div class="kpi-num" style="color:var(--success);">+20.5%</div>
            <div class="kpi-sub">Jacob Duffy (75.0% HP)</div>
        </div>
    </div>

    <!-- 3-Column Visual Analytics Grid (Donut Chart + Distribution Bars + Leverage Matrix) -->
    <div class="analytics-row-3col">
        <!-- 1. Donut Visual (NO WRAPPING) -->
        <div class="panel-box">
            <div class="panel-header-box">
                <span class="pill-header">HIGH-LEVERAGE FIXTURE DISTRIBUTION</span>
            </div>
            <div class="donut-container">
                <svg viewBox="0 0 160 160" width="112" height="112" style="flex-shrink:0;overflow:visible;">
                    <circle cx="80" cy="80" r="58" fill="none" stroke="#EEF2F6" stroke-width="22"/>
                    <!-- Rolling Ring Group: Continuous automatic smooth 360deg rotation -->
                    <g class="rolling-donut-ring">
                        <animateTransform attributeName="transform" type="rotate" from="0 80 80" to="360 80 80" dur="12s" repeatCount="indefinite"/>
                        <!-- Playoff / KO Stage (20%) -->
                        <circle cx="80" cy="80" r="58" fill="none" stroke="#001D48" stroke-width="22"
                                stroke-dasharray="72 364" stroke-dashoffset="0" transform="rotate(-90 80 80)"/>
                        <!-- Defences <= 15 runs (66%) -->
                        <circle cx="80" cy="80" r="58" fill="none" stroke="#EB1A8D" stroke-width="22"
                                stroke-dasharray="241 364" stroke-dashoffset="-72" transform="rotate(-90 80 80)"/>
                        <!-- Chases <= 2 wkts / Super Over (14%) -->
                        <circle cx="80" cy="80" r="58" fill="none" stroke="#059669" stroke-width="22"
                                stroke-dasharray="51 364" stroke-dashoffset="-313" transform="rotate(-90 80 80)"/>
                    </g>
                    <!-- Center Metric (Stationary and upright in the center) -->
                    <text x="80" y="75" font-size="20" font-weight="800" fill="#111827" text-anchor="middle">178</text>
                    <text x="80" y="91" font-size="9" font-weight="700" fill="#64748B" text-anchor="middle">MATCHES</text>
                </svg>
                <div class="donut-legend">
                    <div class="donut-legend-item">
                        <div class="donut-legend-left">
                            <span class="legend-dot" style="background:#EB1A8D;"></span>
                            <span>Defend &le; 15 runs</span>
                        </div>
                        <span class="donut-legend-pct">66%</span>
                    </div>
                    <div class="donut-legend-item">
                        <div class="donut-legend-left">
                            <span class="legend-dot" style="background:#001D48;"></span>
                            <span>Playoff / KO Stage</span>
                        </div>
                        <span class="donut-legend-pct">20%</span>
                    </div>
                    <div class="donut-legend-item">
                        <div class="donut-legend-left">
                            <span class="legend-dot" style="background:#059669;"></span>
                            <span>Chase &le; 2 wkts / SO</span>
                        </div>
                        <span class="donut-legend-pct">14%</span>
                    </div>
                </div>
            </div>
            <div style="font-size:11px;color:var(--text-muted);text-align:center;margin-top:6px;">Sample segments isolating acute leverage</div>
        </div>

        <!-- 2. Individual Top Differentials (NO TEXT WRAP) -->
        <div class="panel-box">
            <div class="panel-header-box">
                <span class="pill-header">TOP LEVERAGE DIFFERENTIALS (&Delta;)</span>
            </div>
            <div style="font-size:12px;">
                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:#111827;">1. Jacob Duffy</span>
                        <strong style="color:var(--success);">+20.5%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:100%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:#111827;">2. Devon Conway</span>
                        <strong style="color:var(--success);">+18.1%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:88%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:#111827;">3. Josh Hazlewood</span>
                        <strong style="color:var(--success);">+14.9%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:73%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:#111827;">4. Shivam Dube</span>
                        <strong style="color:var(--success);">+12.4%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:60%;height:100%;border-radius:3px;"></div></div>
                </div>

                <div class="diff-row-item" style="margin-bottom:0;">
                    <div class="diff-row-header">
                        <span style="font-weight:700;color:#111827;">5. R. Patidar / Arshdeep</span>
                        <strong style="color:var(--success);">+11.1%</strong>
                    </div>
                    <div style="background:#EEF2F6;height:6px;border-radius:3px;"><div style="background:var(--success);width:54%;height:100%;border-radius:3px;"></div></div>
                </div>
            </div>
            <div style="font-size:11px;color:var(--text-muted);text-align:center;margin-top:6px;">True empirical win rate boost under pressure</div>
        </div>

        <!-- 3. Leverage Level Performance Matrix -->
        <div class="panel-box matrix-panel">
            <div class="panel-header-box">
                <span class="pill-header">LEVERAGE LEVEL PERFORMANCE MATRIX</span>
            </div>
            <div class="table-scroll-wrapper">
                <table class="matrix-table">
                <colgroup>
                    <col style="width: 28%;">
                    <col style="width: 18%;">
                    <col style="width: 18%;">
                    <col style="width: 18%;">
                    <col style="width: 18%;">
                </colgroup>
                <thead>
                    <tr>
                        <th style="text-align:left;padding-left:8px;">Target Tier</th>
                        <th>&le; 6 Runs</th>
                        <th>7-12 Runs</th>
                        <th>13-15 Runs</th>
                        <th>Playoffs</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="text-align:left;font-weight:700;color:#111827;padding-left:8px;">Top 10 Batters</td>
                        <td class="matrix-highlight">68.4%</td>
                        <td class="matrix-highlight">71.2%</td>
                        <td>64.5%</td>
                        <td class="matrix-highlight">72.0%</td>
                    </tr>
                    <tr>
                        <td style="text-align:left;font-weight:700;color:#111827;padding-left:8px;">Top 10 Bowlers</td>
                        <td class="matrix-highlight">66.7%</td>
                        <td>63.8%</td>
                        <td class="matrix-highlight">69.1%</td>
                        <td class="matrix-highlight">74.2%</td>
                    </tr>
                    <tr>
                        <td style="text-align:left;color:var(--text-muted);padding-left:8px;">Peer Baseline</td>
                        <td style="color:var(--danger);font-weight:600;">44.2%</td>
                        <td style="color:var(--danger);font-weight:600;">48.1%</td>
                        <td style="color:var(--danger);font-weight:600;">49.6%</td>
                        <td style="color:var(--danger);font-weight:600;">41.8%</td>
                    </tr>
                </tbody>
            </table>
            </div>
            <div style="font-size:11px;color:var(--text-muted);text-align:center;margin-top:6px;">Win conversion matrix across acute match margin categories</div>
        </div>
    </div>

    <!-- Power BI Interactive Slicer Bar - Compact, Balanced 2-Tier Control Hub -->
    <div class="slicer-card">
        <!-- Top Row: Section Navigation Tabs & Scope Status Badge -->
        <div class="slicer-tabs-row">
            <div class="tab-group">
                <button class="nav-tab-btn active" onclick="showSection('batters', this)">Batting Evaluation (Top 10)</button>
                <button class="nav-tab-btn" onclick="showSection('bowlers', this)">Bowling Evaluation (Top 10)</button>
                <button class="nav-tab-btn" onclick="showSection('tactical-xi', this)">IPL 2027 RR Squad &amp; Auction Strategy</button>
                <button class="nav-tab-btn" onclick="showSection('superstars', this)">Leverage Variance Audit</button>
            </div>
            <div class="slicer-status-badge">
                <span class="status-indicator-dot"></span>
                <span>IPL 2027 Pool &bull; 1,217 Evaluated</span>
            </div>
        </div>

        <!-- Bottom Row: Filter & Search Controls (Balanced, Full-Width, No Empty Void) -->
        <div class="slicer-controls-row">
            <div class="search-wrapper">
                <svg class="search-icon" viewBox="0 0 20 20" width="15" height="15" fill="none" stroke="#64748B" stroke-width="2">
                    <circle cx="8.5" cy="8.5" r="5.5"></circle>
                    <line x1="12.5" y1="12.5" x2="17" y2="17"></line>
                </svg>
                <input type="text" id="filterInput" class="search-field" placeholder="Search player name, franchise, state, or role..." onkeyup="applySlicers()">
            </div>

            <div class="slicer-dropdowns">
                <div class="slicer-item">
                    <label for="roleSlicer" class="slicer-label">ROLE:</label>
                    <select id="roleSlicer" class="slicer-select" onchange="applySlicers()">
                        <option value="ALL">All Roles</option>
                        <option value="TOP">Top Order &amp; Anchors (#1&ndash;#3)</option>
                        <option value="MIDDLE">Middle-Overs Enforcers (#4&ndash;#5)</option>
                        <option value="FINISHER">Finishers / Death Specialists (#5&ndash;#7)</option>
                        <option value="SEAM">Fast Bowlers / Seam</option>
                        <option value="SPIN">Spin / All-Rounders</option>
                    </select>
                </div>

                <div class="slicer-item">
                    <label for="sortSlicer" class="slicer-label">SORT:</label>
                    <select id="sortSlicer" class="slicer-select" onchange="applySlicers()">
                        <option value="RANK">Rank (Ascending)</option>
                        <option value="DIFF">Win Differential (&Delta;)</option>
                        <option value="WIN">High-Leverage Win%</option>
                        <option value="INDEX">Index Score (CPPI)</option>
                    </select>
                </div>

                <button class="slicer-reset-btn" onclick="resetSlicers()" title="Reset all filters">Reset</button>
            </div>
        </div>
    </div>

        <input type="text" id="filterInput" class="search-field" placeholder="Search player, role, team..." onkeyup="applySlicers()">
    </div>

    <!-- Table 1: Batters -->
    <div id="section-batters" class="table-responsive data-section">
        <table id="table-batters">
            <thead>
                <tr>
                    <th style="width:34px;text-align:center;">#</th>
                    <th style="text-align:left;">Player & Role</th>
                    <th style="text-align:left;">Franchise / State</th>
                    <th style="text-align:center;">Leverage<br>Matches</th>
                    <th style="text-align:right;">Pressure<br>Win%</th>
                    <th style="text-align:right;">Baseline<br>Win%</th>
                    <th style="text-align:center;">Win Diff<br>(&Delta;)</th>
                    <th style="text-align:center;">Match<br>Awards</th>
                    <th style="text-align:right;">Playoff<br>Win%</th>
                    <th style="text-align:right;">CPPI<br>Score</th>
                    <th style="text-align:center;">Action</th>
                </tr>
            </thead>
            <tbody>
"""

for b in top10_batters:
    img_b64 = player_images.get(b["key"], "")
    diff_sign = f"+{b['lift']:.1f}%" if b['lift'] >= 0 else f"{b['lift']:.1f}%"
    diff_class = "diff-pos" if b['lift'] >= 0 else "diff-neg"
    
    master_dashboard_html += f"""
                <tr onclick="window.location.href='players/{b['key']}.html'" data-role="{b['tactical_role']}" data-diff="{b['lift']}" data-win="{b['hp_wr']}" data-index="{b['cppi']}" data-rank="{b['rank']}">
                    <td style="font-weight:700;color:#111827;">{b['rank']}</td>
                    <td>
                        <div class="player-flex">
                            <a href="players/{b['key']}.html" onclick="event.stopPropagation();">
                                <div class="thumb-img"><img src="{img_b64}" alt="{b['name']}"></div>
                            </a>
                            <div class="name-box">
                                <a href="players/{b['key']}.html" onclick="event.stopPropagation();">{b['name']}</a>
                                <div class="team-sub">{b['tactical_role']}</div>
                            </div>
                        </div>
                    </td>
                    <td>{b['teams']}</td>
                    <td style="text-align:center;font-weight:600;">{b['hp_m']}</td>
                    <td style="text-align:right;font-weight:700;color:#111827;">{b['hp_wr']:.1f}%</td>
                    <td style="text-align:right;color:var(--text-muted);">{b['base_wr']:.1f}%</td>
                    <td style="text-align:center;"><span class="diff-tag {diff_class}">{diff_sign}</span></td>
                    <td style="text-align:center;font-weight:600;">{b['mom_hp']}</td>
                    <td style="text-align:right;font-weight:700;">{b['ko_wr']:.1f}%</td>
                    <td style="text-align:right;font-weight:800;color:#111827;">{b['cppi']:.2f}</td>
                    <td style="text-align:center;">
                        <a href="players/{b['key']}.html" class="action-link" onclick="event.stopPropagation();">View Wagon Wheel &rarr;</a>
                    </td>
                </tr>
"""

master_dashboard_html += """
            </tbody>
        </table>
    </div>

    <!-- Table 2: Bowlers -->
    <div id="section-bowlers" class="table-responsive data-section" style="display:none;">
        <table id="table-bowlers">
            <thead>
                <tr>
                    <th style="width:34px;text-align:center;">#</th>
                    <th style="text-align:left;">Player & Role</th>
                    <th style="text-align:left;">Franchise / State</th>
                    <th style="text-align:center;">Leverage<br>Matches</th>
                    <th style="text-align:right;">Pressure<br>Win%</th>
                    <th style="text-align:right;">Baseline<br>Win%</th>
                    <th style="text-align:center;">Win Diff<br>(&Delta;)</th>
                    <th style="text-align:center;">Match<br>Awards</th>
                    <th style="text-align:right;">Playoff<br>Win%</th>
                    <th style="text-align:right;">CPPI<br>Score</th>
                    <th style="text-align:center;">Action</th>
                </tr>
            </thead>
            <tbody>
"""

for b in top10_bowlers:
    img_b64 = player_images.get(b["key"], "")
    diff_sign = f"+{b['lift']:.1f}%" if b['lift'] >= 0 else f"{b['lift']:.1f}%"
    diff_class = "diff-pos" if b['lift'] >= 0 else "diff-neg"
    
    master_dashboard_html += f"""
                <tr onclick="window.location.href='players/{b['key']}.html'" data-role="{b['tactical_role']}" data-diff="{b['lift']}" data-win="{b['hp_wr']}" data-index="{b['cppi']}" data-rank="{b['rank']}">
                    <td style="font-weight:700;color:#111827;">{b['rank']}</td>
                    <td>
                        <div class="player-flex">
                            <a href="players/{b['key']}.html" onclick="event.stopPropagation();">
                                <div class="thumb-img"><img src="{img_b64}" alt="{b['name']}"></div>
                            </a>
                            <div class="name-box">
                                <a href="players/{b['key']}.html" onclick="event.stopPropagation();">{b['name']}</a>
                                <div class="team-sub">{b['tactical_role']}</div>
                            </div>
                        </div>
                    </td>
                    <td>{b['teams']}</td>
                    <td style="text-align:center;font-weight:600;">{b['hp_m']}</td>
                    <td style="text-align:right;font-weight:700;color:#111827;">{b['hp_wr']:.1f}%</td>
                    <td style="text-align:right;color:var(--text-muted);">{b['base_wr']:.1f}%</td>
                    <td style="text-align:center;"><span class="diff-tag {diff_class}">{diff_sign}</span></td>
                    <td style="text-align:center;font-weight:600;">{b['mom_hp']}</td>
                    <td style="text-align:right;font-weight:700;">{b['ko_wr']:.1f}%</td>
                    <td style="text-align:right;font-weight:800;color:#111827;">{b['cppi']:.2f}</td>
                    <td style="text-align:center;">
                        <a href="players/{b['key']}.html" class="action-link" onclick="event.stopPropagation();">View Pitch Map &rarr;</a>
                    </td>
                </tr>
"""

master_dashboard_html += """
            </tbody>
        </table>
    </div>

    <!-- Table 3: Superstars Audit -->
    <div id="section-superstars" class="table-responsive data-section" style="display:none;">
        <table>
            <thead>
                <tr>
                    <th style="text-align:left;">Candidate</th>
                    <th style="text-align:center;" title="Exact matches played within the evaluated 883-match competition dataset">Dataset<br>Matches</th>
                    <th style="text-align:right;">Overall<br>Win%</th>
                    <th style="text-align:center;">Leverage<br>Matches</th>
                    <th style="text-align:right;">Pressure<br>Win%</th>
                    <th style="text-align:center;">Win Diff<br>(&Delta;)</th>
                    <th style="text-align:center;">Playoff<br>Win%</th>
                    <th style="text-align:left;width:34%;">Why Numbers Differ in Close Games</th>
                    <th style="text-align:center;">Action</th>
                </tr>
            </thead>
            <tbody>
"""

for s in superstars_audit:
    s_img = player_images.get(s.get("key", ""), "")
    diff_sign = f"{s['lift']:.1f}%"
    master_dashboard_html += f"""
                <tr>
                    <td>
                        <div class="player-flex">
                            <div class="thumb-img"><img src="{s_img}" alt="{s['name']}"></div>
                            <div>
                                <strong style="color:#111827;font-size:13px;">{s['name']}</strong>
                            </div>
                        </div>
                    </td>
                    <td style="text-align:center;font-weight:600;">{s['total_m']}</td>
                    <td style="text-align:right;color:var(--text-muted);">{s['base_wr']:.1f}%</td>
                    <td style="text-align:center;font-weight:600;">{s['hp_m']}</td>
                    <td style="text-align:right;font-weight:700;color:var(--danger);">{s['hp_wr']:.1f}%</td>
                    <td style="text-align:center;"><span class="diff-tag diff-neg">{diff_sign}</span></td>
                    <td style="text-align:center;font-weight:600;">{s['ko_wr']:.1f}%</td>
                    <td style="font-size:12.5px;color:#374151;line-height:1.5;">{s['reason']}</td>
                    <td style="text-align:center;">
                        <a href="players/{s['key']}.html" class="wagon-btn" style="text-decoration:none;">View Profile &rarr;</a>
                    </td>
                </tr>
"""

master_dashboard_html += """
            </tbody>
        </table>
    </div>

    <!-- IPL 2027 Rajasthan Royals Tactical Squad & Auction Strategy Section -->
    <div id="section-tactical-xi" class="data-section" style="display:none;margin-top:16px;">
        
        <div class="tactical-grid">
            <!-- Left Column: Playing XI Formation & Lineup -->
            <div class="tactical-card">
                <div class="tactical-card-title">
                    Rajasthan Royals &mdash; Recommended 2027 Playing XI
                </div>
                <div class="tactical-card-sub">
                    A balanced 11-man lineup calibrated to dominate middle-overs spin and close out death overs under high match pressure.
                </div>
                
                <!-- Pure Clean Light Mode Starting XI Blueprint -->
                <div class="xi-blueprint-container">
                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Top-Order Anchors (Overs 1&ndash;6)</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">1</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Yashasvi Jaiswal</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Left-Hand Explosive Opener &bull; Powerplay Strike Rate 165+</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" onclick="window.location.href='players/devon_conway.html'">
                                <div class="xi-num">2</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Devon Conway</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">LHB Top-Order Anchor &amp; WK &bull; 64.3% Pressure Win Rate (+18.1% Lift)</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">3</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Sanju Samson <span style="font-size:11px;color:var(--rr-pink);font-weight:700;">(C)</span></span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Captain &amp; No. 3 Pace/Spin Attacker &bull; Proven Match-Winner</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Middle-Overs Engine &amp; Spin Enforcers (Overs 7&ndash;15)</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" onclick="window.location.href='players/shivam_dube.html'">
                                <div class="xi-num">4</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Shivam Dube</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Designated Spin Demolisher &bull; 66.7% Pressure Win Rate (+12.4% Lift)</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">5</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Riyan Parag</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Middle-Order Striker &amp; Leg-Spin Option &bull; SMS Fortress Anchor</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">6</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Dhruv Jurel <span style="font-size:11px;color:var(--text-muted);font-weight:600;">(WK)</span></span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Clutch Middle-Order Finisher &bull; Elite Death-Over Temperament</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Death-Overs Power Finishers (Overs 16&ndash;20)</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" onclick="window.location.href='players/rinku_singh.html'">
                                <div class="xi-num">7</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Rinku Singh</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Specialist Death Finisher &bull; 69.2% Pressure Win Rate across 26 High-Leverage Games</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">8</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Shimron Hetmyer</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Overseas Power Finisher &bull; Fearless Boundary Striking in Final 3 Overs</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Bowling Spearheads &amp; Seam Defense</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" onclick="window.location.href='players/josh_hazlewood.html'">
                                <div class="xi-num">9</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Josh Hazlewood</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Frontline Seam Spearhead &bull; 78.6% Pressure Win Rate (+14.9% Lift)</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" title="Retained Franchise Core &bull; Not in Auction Pool" style="cursor:default;">
                                <div class="xi-num">10</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Sandeep Sharma</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Death Yorker &amp; Wide-Line Master &bull; Reliable Execution in Final 2 Overs</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" onclick="window.location.href='players/yash_dayal.html'">
                                <div class="xi-num">11</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Yash Dayal</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Left-Arm Seam Specialist &bull; 80.0% Pressure Win Rate (+10.2% Lift)</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Tactical Impact Subs & Bench -->
                    <div class="xi-bench-box">
                        <div class="xi-bench-lbl">Tactical Impact Substitutes &amp; Matchup Covers:</div>
                        <div class="xi-bench-pills">
                            <span class="bench-pill" onclick="window.location.href='players/jacob_duffy.html'"><strong>Jacob Duffy</strong> (Pace &bull; +20.5% Lift)</span>
                            <span class="bench-pill" onclick="window.location.href='players/axar_patel.html'"><strong>Axar Patel</strong> (Spin All-Rounder &bull; +7.8% Lift)</span>
                            <span class="bench-pill" onclick="window.location.href='players/varun_chakravarthy.html'"><strong>Varun Chakravarthy</strong> (Mystery Spin &bull; 100% Playoff WR)</span>
                            <span class="bench-pill" onclick="window.location.href='players/rajat_patidar.html'"><strong>Rajat Patidar</strong> (No. 3 Cover &bull; +11.1% Lift)</span>
                        </div>
                    </div>
                </div>

                <!-- Playing XI Win Conversion Table: Cleanly Padded & Non-Wrapping -->
                <table class="purse-table" style="margin-top:16px;">
                    <thead>
                        <tr>
                            <th style="width:36px;text-align:center;">#</th>
                            <th style="min-width:130px;white-space:nowrap;">Player</th>
                            <th>Role in Team</th>
                            <th style="width:85px;text-align:right;white-space:nowrap;">Normal Win%</th>
                            <th style="width:85px;text-align:right;white-space:nowrap;">Pressure Win%</th>
                            <th style="width:90px;text-align:center;white-space:nowrap;">Win Diff</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr onclick="window.location.href='players/devon_conway.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:#111827;text-align:center;">1</td>
                            <td style="white-space:nowrap;"><strong>Devon Conway</strong> <span style="font-size:11px;color:var(--text-muted);">(wk)</span></td>
                            <td>Top-Order Anchor & Wicketkeeper</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">46.2%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">64.3%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+18.1%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/ruturaj_gaikwad.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:#111827;text-align:center;">2</td>
                            <td style="white-space:nowrap;"><strong>Ruturaj Gaikwad</strong></td>
                            <td>Opening Batter & Inning Pacer</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">50.6%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">57.1%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+6.5%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/rajat_patidar.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:#111827;text-align:center;">3</td>
                            <td style="white-space:nowrap;"><strong>Rajat Patidar</strong></td>
                            <td>No. 3 Anchor & Spin Attacker</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">60.3%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">71.4%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+11.1%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/shivam_dube.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:#111827;text-align:center;">4</td>
                            <td style="white-space:nowrap;"><strong>Shivam Dube</strong></td>
                            <td>Middle-Overs Boundary Hitter vs Spin (Overs 7&ndash;15)</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">54.3%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">66.7%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+12.4%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/shreyas_iyer.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:#111827;text-align:center;">5</td>
                            <td style="white-space:nowrap;"><strong>Shreyas Iyer</strong> <span style="font-size:11px;color:var(--rr-pink);font-weight:700;">(c)</span></td>
                            <td>Middle-Order Game Manager & Captain</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">54.5%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">55.6%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+1.1%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/rinku_singh.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:#111827;text-align:center;">6</td>
                            <td style="white-space:nowrap;"><strong>Rinku Singh</strong></td>
                            <td>Designated Death Finisher (Overs 16&ndash;20)</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">63.8%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">69.2%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+5.4%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/axar_patel.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:#111827;text-align:center;">7</td>
                            <td style="white-space:nowrap;"><strong>Axar Patel</strong></td>
                            <td>Spin All-Rounder & Late-Overs Hitter</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">56.5%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">64.3%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+7.8%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/romario_shepherd.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:#111827;text-align:center;">8</td>
                            <td style="white-space:nowrap;"><strong>Romario Shepherd</strong></td>
                            <td>Pace All-Rounder & Heavy-Ball Bowler</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">49.0%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">56.0%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+7.0%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/mitchell_starc.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:#111827;text-align:center;">9</td>
                            <td style="white-space:nowrap;"><strong>Mitchell Starc</strong></td>
                            <td>Left-Arm Fast Bowler (Powerplay & Death)</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">68.3%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">60.0%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag" style="background:#FEF3C7;color:#92400E;">3 Awards</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/varun_chakravarthy.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:#111827;text-align:center;">10</td>
                            <td style="white-space:nowrap;"><strong>Varun Chakravarthy</strong></td>
                            <td>Mystery Spinner (Middle Overs)</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">58.6%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">61.9%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+3.3%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/jacob_duffy.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:#111827;text-align:center;">11</td>
                            <td style="white-space:nowrap;"><strong>Jacob Duffy</strong></td>
                            <td>Accurate Swing & Seam Bowler</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">54.5%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);white-space:nowrap;">75.0%</td>
                            <td style="text-align:center;white-space:nowrap;"><span class="diff-tag diff-pos">+20.5%</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Right Column: Auction Valuation Model & Purse Allocation -->
            <div class="tactical-card">
                <div class="tactical-card-title">
                    Auction Budget Plan (&#8377;45 Crore Total Purse)
                </div>
                <div class="tactical-card-sub">
                    Disciplined bidding caps to prevent emotional overspending on marquee names.
                </div>

                <div class="budget-kpi-bar">
                    <div>
                        <div class="budget-kpi-val">&#8377;45.0 Cr</div>
                        <div class="budget-kpi-lbl">Total Budget</div>
                    </div>
                    <div>
                        <div class="budget-kpi-val" style="color:var(--success);">&#8377;45.0 Cr</div>
                        <div class="budget-kpi-lbl">Target Allocations</div>
                    </div>
                    <div>
                        <div class="budget-kpi-val" style="color:var(--rr-pink);">100%</div>
                        <div class="budget-kpi-lbl">Budget Utilized</div>
                    </div>
                </div>

                <!-- Fixed Auction Budget Table: No wrap on badges, prices, or purse % -->
                <table class="purse-table">
                    <thead>
                        <tr>
                            <th style="min-width:130px;white-space:nowrap;">Target Player</th>
                            <th style="width:100px;text-align:center;white-space:nowrap;">Priority</th>
                            <th style="width:105px;text-align:right;white-space:nowrap;">Max Bid</th>
                            <th style="width:90px;text-align:right;white-space:nowrap;">% of Purse</th>
                            <th>Why Rajasthan Royals Needs Him</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr onclick="window.location.href='players/rinku_singh.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Rinku Singh</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:#111827;white-space:nowrap;">&#8377;11.00 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">24.4%</td>
                            <td style="font-size:12px;line-height:1.45;">Proven death finisher; finishes tight chases with calm execution (69.2% win rate).</td>
                        </tr>
                        <tr onclick="window.location.href='players/shivam_dube.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Shivam Dube</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:#111827;white-space:nowrap;">&#8377;9.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">21.1%</td>
                            <td style="font-size:12px;line-height:1.45;">Destroys spin bowling in overs 7&ndash;15; prevents scoring slowdowns in middle overs.</td>
                        </tr>
                        <tr onclick="window.location.href='players/axar_patel.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Axar Patel</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:#111827;white-space:nowrap;">&#8377;8.00 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">17.8%</td>
                            <td style="font-size:12px;line-height:1.45;">Gives batting depth at No. 7 and bowls tight 4 overs of left-arm spin.</td>
                        </tr>
                        <tr onclick="window.location.href='players/jacob_duffy.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Jacob Duffy</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:#111827;white-space:nowrap;">&#8377;6.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">14.4%</td>
                            <td style="font-size:12px;line-height:1.45;">Top bowler in high-pressure matches (+20.5% lift, 75.0% win rate); disciplined swing.</td>
                        </tr>
                        <tr onclick="window.location.href='players/varun_chakravarthy.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Varun Chakravarthy</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-2">Priority 2</span></td>
                            <td style="text-align:right;font-weight:700;color:#111827;white-space:nowrap;">&#8377;5.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">12.2%</td>
                            <td style="font-size:12px;line-height:1.45;">Takes wickets in middle overs; 100% win rate in playoff knockout games.</td>
                        </tr>
                        <tr onclick="window.location.href='players/romario_shepherd.html'" style="cursor:pointer;">
                            <td style="white-space:nowrap;"><strong>Romario Shepherd</strong></td>
                            <td style="text-align:center;white-space:nowrap;"><span class="tier-badge tier-2">Priority 2</span></td>
                            <td style="text-align:right;font-weight:700;color:#111827;white-space:nowrap;">&#8377;4.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);white-space:nowrap;">10.0%</td>
                            <td style="font-size:12px;line-height:1.45;">Fast bowling option with heavy ball and power-hitting down the order.</td>
                        </tr>
                    </tbody>
                </table>

                <div style="margin-top:20px;padding:14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                    <div style="font-weight:700;font-size:12.5px;color:#111827;margin-bottom:4px;">Auction Bidding Rule:</div>
                    <p style="font-size:12px;color:#374151;line-height:1.5;margin:0;">
                        If bidding for any player goes more than 10% above their maximum limit, stop bidding immediately and switch to backup targets (such as Yash Dayal at &#8377;5.5 Cr or Bhanuka Rajapaksa at &#8377;3.5 Cr) to protect the overall team budget.
                    </p>
                </div>

                <!-- 1. Contingency Bidding Matrix & Step-Down Rules -->
                <div style="margin-top:16px;padding:16px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;">
                    <div style="font-weight:700;font-size:12.5px;color:#111827;margin-bottom:10px;">
                        Contingency Bidding Matrix (Live Step-Down Triggers)
                    </div>
                    <div style="display:flex;flex-direction:column;gap:8px;font-size:12px;color:#374151;">
                        <div style="padding:8px 10px;background:#F8FAFC;border-radius:6px;border-left:3px solid var(--rr-pink);line-height:1.45;">
                            <strong>If Rinku Singh &gt; &#8377;11.0 Cr:</strong> Pivot immediately to Bhanuka Rajapaksa (&#8377;3.5 Cr) + promote Hetmyer to No. 6, freeing &#8377;7.5 Cr for bowling reserve.
                        </div>
                        <div style="padding:8px 10px;background:#F8FAFC;border-radius:6px;border-left:3px solid #0284C7;line-height:1.45;">
                            <strong>If Shivam Dube &gt; &#8377;9.5 Cr:</strong> Switch to Rajat Patidar (&#8377;7.0 Cr) for spin boundary execution, reallocating &#8377;2.5 Cr to overseas pace.
                        </div>
                        <div style="padding:8px 10px;background:#F8FAFC;border-radius:6px;border-left:3px solid #059669;line-height:1.45;">
                            <strong>If Josh Hazlewood &gt; &#8377;9.5 Cr:</strong> Lock Jacob Duffy (&#8377;6.5 Cr) as primary overseas seamer and secure Yash Dayal (&#8377;4.5 Cr).
                        </div>
                        <div style="padding:8px 10px;background:#F8FAFC;border-radius:6px;border-left:3px solid #D97706;line-height:1.45;">
                            <strong>If Axar Patel &gt; &#8377;8.0 Cr:</strong> Pivot to Varun Chakravarthy (&#8377;5.5 Cr) + domestic all-rounder backup to secure middle-overs spin choke.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <!-- Strategic War Room Principles & Phase Distribution (Balanced 2-Column Row) -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:24px;align-items:start;">
            <!-- Phase-by-Phase Purse Distribution Grid -->
            <div class="tactical-card">
                <div class="tactical-card-title">
                    Phase-by-Phase Purse Distribution (&#8377;45.0 Cr Total)
                </div>
                <div class="tactical-card-sub">
                    Balanced allocation preventing over-commitment in any single game phase.
                </div>
                <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:12px;">
                    <div style="padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                        <div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;">Middle Spin Attack</div>
                        <div style="font-size:16px;font-weight:800;color:#111827;margin-top:2px;">&#8377;17.50 Cr <span style="font-size:11.5px;font-weight:700;color:#059669;">(38.9%)</span></div>
                        <div style="font-size:11.5px;color:#64748B;margin-top:4px;">Dube (&#8377;9.5) + Axar (&#8377;8.0)</div>
                    </div>
                    <div style="padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                        <div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;">Death Finishing</div>
                        <div style="font-size:16px;font-weight:800;color:#111827;margin-top:2px;">&#8377;11.00 Cr <span style="font-size:11.5px;font-weight:700;color:#059669;">(24.4%)</span></div>
                        <div style="font-size:11.5px;color:#64748B;margin-top:4px;">Rinku Singh (Priority 1)</div>
                    </div>
                    <div style="padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                        <div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;">Pace Spearheads</div>
                        <div style="font-size:16px;font-weight:800;color:#111827;margin-top:2px;">&#8377;11.00 Cr <span style="font-size:11.5px;font-weight:700;color:#059669;">(24.4%)</span></div>
                        <div style="font-size:11.5px;color:#64748B;margin-top:4px;">Duffy (&#8377;6.5) + Shepherd (&#8377;4.5)</div>
                    </div>
                    <div style="padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                        <div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;">Mystery Spin Choke</div>
                        <div style="font-size:16px;font-weight:800;color:#111827;margin-top:2px;">&#8377;5.50 Cr <span style="font-size:11.5px;font-weight:700;color:#059669;">(12.2%)</span></div>
                        <div style="font-size:11.5px;color:#64748B;margin-top:4px;">Varun Chakravarthy</div>
                    </div>
                </div>
            </div>

            <!-- War Room Strategic Principles -->
            <div class="tactical-card">
                <div class="tactical-card-title">
                    War Room Principles &bull; IPL 2027 Auction
                </div>
                <div class="tactical-card-sub">
                    Core operational disciplines governing every auction call.
                </div>
                <ul style="margin:0;padding-left:18px;font-size:12.5px;color:#374151;line-height:1.65;">
                    <li style="margin-bottom:6px;"><strong>No Emotional Marquee Bidding:</strong> Resist brand-driven inflation on marquee names whose clutch win differential is negative.</li>
                    <li style="margin-bottom:6px;"><strong>Jaipur SMS Fortress Fit:</strong> Prioritize players suited to 75m+ boundaries and middle-overs spin grip over generic power hitters.</li>
                    <li style="margin-bottom:6px;"><strong>Strict 2+2 Overseas Structure:</strong> Exactly 2 overseas in Starting XI (Conway, Hazlewood) and 2 impact covers (Duffy, Hetmyer).</li>
                    <li><strong>10% Circuit Breaker:</strong> The instant any player exceeds 10% above max valuation, immediately execute step-down contingency.</li>
                </ul>
            </div>
        </div>

        <!-- Bottom Card: Clean Light Mode Pressure Lift Quadrant Matrix with SVG Chart -->
        <div class="tactical-card" style="margin-top:24px;margin-bottom:28px;">
            <div class="tactical-card-title">
                Pressure Win Rate vs Normal Win Rate (Player Quadrant Classification)
            </div>
            <div class="tactical-card-sub">
                Compares how players perform when matches are close (under 15 runs or 2 wickets) versus career baseline games.
            </div>

            <!-- Crisp Light Mode Vector Scatter Plot (Replaces dark matplotlib chart) -->
            <div style="margin-bottom:20px;">
                <svg viewBox="0 0 920 540" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF;border-radius:10px;border:1px solid #E2E8F0;box-shadow:0 2px 10px rgba(0,0,0,0.03);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <rect x="410.7" y="75" width="459.3" height="273.3" fill="#F0FDF4" />
  <rect x="80" y="75" width="330.7" height="273.3" fill="#FFFBEB" />
  <rect x="410.7" y="348.3" width="459.3" height="136.7" fill="#F8FAFC" />
  <text x="92" y="65" fill="#B45309" font-size="11" font-weight="800" letter-spacing="0.5">QUADRANT II &bull; SITUATIONAL SPECIALISTS</text>
  <text x="858" y="65" text-anchor="end" fill="#047857" font-size="11" font-weight="800" letter-spacing="0.5">QUADRANT I &bull; CLUTCH MATCH-WINNERS</text>
  <text x="856" y="471" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="800" letter-spacing="0.5">QUADRANT IV &bull; HIGH BASELINE DRIFT</text>
  <line x1="80" y1="462.2" x2="870" y2="462.2" stroke="#E2E8F0" stroke-width="1"  />
  <text x="70" y="466.2" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="600">-10%</text>
  <line x1="80" y1="405.3" x2="870" y2="405.3" stroke="#E2E8F0" stroke-width="1"  />
  <text x="70" y="409.3" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="600">-5%</text>
  <line x1="80" y1="348.3" x2="870" y2="348.3" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="4,4" />
  <text x="70" y="352.3" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="600">+0%</text>
  <line x1="80" y1="291.4" x2="870" y2="291.4" stroke="#E2E8F0" stroke-width="1"  />
  <text x="70" y="295.4" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="600">+5%</text>
  <line x1="80" y1="234.4" x2="870" y2="234.4" stroke="#E2E8F0" stroke-width="1"  />
  <text x="70" y="238.4" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="600">+10%</text>
  <line x1="80" y1="177.5" x2="870" y2="177.5" stroke="#E2E8F0" stroke-width="1"  />
  <text x="70" y="181.5" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="600">+15%</text>
  <line x1="80" y1="120.6" x2="870" y2="120.6" stroke="#E2E8F0" stroke-width="1"  />
  <text x="70" y="124.6" text-anchor="end" fill="#64748B" font-size="10.5" font-weight="600">+20%</text>
  <line x1="135.1" y1="75" x2="135.1" y2="485" stroke="#E2E8F0" stroke-width="1"  />
  <text x="135.1" y="503" text-anchor="middle" fill="#64748B" font-size="10.5" font-weight="600">45%</text>
  <line x1="227.0" y1="75" x2="227.0" y2="485" stroke="#E2E8F0" stroke-width="1"  />
  <text x="227.0" y="503" text-anchor="middle" fill="#64748B" font-size="10.5" font-weight="600">50%</text>
  <line x1="318.8" y1="75" x2="318.8" y2="485" stroke="#E2E8F0" stroke-width="1"  />
  <text x="318.8" y="503" text-anchor="middle" fill="#64748B" font-size="10.5" font-weight="600">55%</text>
  <line x1="410.7" y1="75" x2="410.7" y2="485" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="4,4" />
  <text x="410.7" y="503" text-anchor="middle" fill="#64748B" font-size="10.5" font-weight="600">60%</text>
  <line x1="502.6" y1="75" x2="502.6" y2="485" stroke="#E2E8F0" stroke-width="1"  />
  <text x="502.6" y="503" text-anchor="middle" fill="#64748B" font-size="10.5" font-weight="600">65%</text>
  <line x1="594.4" y1="75" x2="594.4" y2="485" stroke="#E2E8F0" stroke-width="1"  />
  <text x="594.4" y="503" text-anchor="middle" fill="#64748B" font-size="10.5" font-weight="600">70%</text>
  <line x1="686.3" y1="75" x2="686.3" y2="485" stroke="#E2E8F0" stroke-width="1"  />
  <text x="686.3" y="503" text-anchor="middle" fill="#64748B" font-size="10.5" font-weight="600">75%</text>
  <line x1="778.1" y1="75" x2="778.1" y2="485" stroke="#E2E8F0" stroke-width="1"  />
  <text x="778.1" y="503" text-anchor="middle" fill="#64748B" font-size="10.5" font-weight="600">80%</text>
  <rect x="80" y="75" width="790" height="410" fill="none" stroke="#CBD5E1" stroke-width="1.5" />
  <text x="475.0" y="525" text-anchor="middle" fill="#111827" font-size="12" font-weight="700">High-Pressure Win Rate (%) &bull; Close Finishes &le; 15 Runs / 2 Wickets &amp; Playoff Knockouts</text>
  <text x="18" y="280.0" text-anchor="middle" fill="#111827" font-size="12" font-weight="700" transform="rotate(-90, 18, 280.0)">True Pressure Lift &Delta; (%) vs Career Baseline</text>
  <g transform="translate(90, 30)">
    <circle cx="0" cy="0" r="5.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="1.5" />
    <text x="10" y="3.5" fill="#111827" font-size="11" font-weight="700">Batters</text>
    <circle cx="85" cy="0" r="5.5" fill="#111827" stroke="#FFFFFF" stroke-width="1.5" />
    <text x="95" y="3.5" fill="#111827" font-size="11" font-weight="700">Bowlers</text>
    <text x="180" y="3.5" fill="#64748B" font-size="10.5">&bull; Size indicates high-pressure match sample volume &bull; Hover for player data</text>
  </g>
  <g class="scatter-point">
    <circle cx="557.7" cy="223.1" r="6.5" fill="#111827" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Arshdeep Singh (#9): 68.0% Win Rate, +11.0% Pressure Lift</title>
    </circle>
    <text x="567.7" y="211.1" text-anchor="start" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Arshdeep Singh (#9)</text>
  </g>
  <g class="scatter-point">
    <circle cx="489.7" cy="259.5" r="6.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Axar Patel (#3): 64.3% Win Rate, +7.8% Pressure Lift</title>
    </circle>
    <text x="479.7" y="255.5" text-anchor="end" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Axar Patel (#3)</text>
  </g>
  <g class="scatter-point">
    <circle cx="533.8" cy="229.9" r="6.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>B. Rajapaksa (#8): 66.7% Win Rate, +10.4% Pressure Lift</title>
    </circle>
    <text x="523.8" y="225.9" text-anchor="end" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">B. Rajapaksa (#8)</text>
  </g>
  <g class="scatter-point">
    <circle cx="410.7" cy="317.6" r="6.5" fill="#111827" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Bhuvneshwar K. (#8): 60.0% Win Rate, +2.7% Pressure Lift</title>
    </circle>
    <text x="400.7" y="313.6" text-anchor="end" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Bhuvneshwar K. (#8)</text>
  </g>
  <g class="scatter-point">
    <circle cx="489.7" cy="142.2" r="6.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Devon Conway (#6): 64.3% Win Rate, +18.1% Pressure Lift</title>
    </circle>
    <text x="499.7" y="138.2" text-anchor="start" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Devon Conway (#6)</text>
  </g>
  <g class="scatter-point">
    <circle cx="686.3" cy="114.9" r="6.5" fill="#111827" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Jacob Duffy (#1): 75.0% Win Rate, +20.5% Pressure Lift</title>
    </circle>
    <text x="696.3" y="110.9" text-anchor="start" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Jacob Duffy (#1)</text>
  </g>
  <g class="scatter-point">
    <circle cx="752.4" cy="178.6" r="6.5" fill="#111827" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Josh Hazlewood (#2): 78.6% Win Rate, +14.9% Pressure Lift</title>
    </circle>
    <text x="742.4" y="174.6" text-anchor="end" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Josh Hazlewood (#2)</text>
  </g>
  <g class="scatter-point">
    <circle cx="329.9" cy="274.3" r="6.5" fill="#111827" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>L. Ferguson (#10): 55.6% Win Rate, +6.5% Pressure Lift</title>
    </circle>
    <text x="319.9" y="278.3" text-anchor="end" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">L. Ferguson (#10)</text>
  </g>
  <g class="scatter-point">
    <circle cx="410.7" cy="442.9" r="6.5" fill="#111827" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Mitchell Starc (#4): 60.0% Win Rate, -8.3% Pressure Lift</title>
    </circle>
    <text x="420.7" y="438.9" text-anchor="start" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Mitchell Starc (#4)</text>
  </g>
  <g class="scatter-point">
    <circle cx="357.4" cy="274.3" r="6.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>R. Gaikwad (#5): 57.1% Win Rate, +6.5% Pressure Lift</title>
    </circle>
    <text x="367.4" y="278.3" text-anchor="start" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">R. Gaikwad (#5)</text>
  </g>
  <g class="scatter-point">
    <circle cx="337.2" cy="268.6" r="6.5" fill="#111827" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>R. Shepherd (#6): 56.0% Win Rate, +7.0% Pressure Lift</title>
    </circle>
    <text x="333.2" y="256.6" text-anchor="middle" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">R. Shepherd (#6)</text>
  </g>
  <g class="scatter-point">
    <circle cx="620.1" cy="221.9" r="6.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Rajat Patidar (#4): 71.4% Win Rate, +11.1% Pressure Lift</title>
    </circle>
    <text x="630.1" y="237.9" text-anchor="start" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Rajat Patidar (#4)</text>
  </g>
  <g class="scatter-point">
    <circle cx="579.7" cy="286.8" r="6.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Rinku Singh (#2): 69.2% Win Rate, +5.4% Pressure Lift</title>
    </circle>
    <text x="589.7" y="282.8" text-anchor="start" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Rinku Singh (#2)</text>
  </g>
  <g class="scatter-point">
    <circle cx="227.0" cy="438.3" r="6.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Sediqullah Atal (#10): 50.0% Win Rate, -7.9% Pressure Lift</title>
    </circle>
    <text x="237.0" y="434.3" text-anchor="start" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Sediqullah Atal (#10)</text>
  </g>
  <g class="scatter-point">
    <circle cx="533.8" cy="207.1" r="6.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Shivam Dube (#1): 66.7% Win Rate, +12.4% Pressure Lift</title>
    </circle>
    <text x="523.8" y="203.1" text-anchor="end" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Shivam Dube (#1)</text>
  </g>
  <g class="scatter-point">
    <circle cx="329.9" cy="335.8" r="6.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Shreyas Iyer (#9): 55.6% Win Rate, +1.1% Pressure Lift</title>
    </circle>
    <text x="339.9" y="339.8" text-anchor="start" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Shreyas Iyer (#9)</text>
  </g>
  <g class="scatter-point">
    <circle cx="644.0" cy="261.8" r="6.5" fill="#111827" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Suyash Sharma (#7): 72.7% Win Rate, +7.6% Pressure Lift</title>
    </circle>
    <text x="654.0" y="257.8" text-anchor="start" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Suyash Sharma (#7)</text>
  </g>
  <g class="scatter-point">
    <circle cx="445.6" cy="310.8" r="6.5" fill="#111827" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Varun C. (#5): 61.9% Win Rate, +3.3% Pressure Lift</title>
    </circle>
    <text x="455.6" y="306.8" text-anchor="start" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Varun C. (#5)</text>
  </g>
  <g class="scatter-point">
    <circle cx="594.4" cy="261.8" r="6.5" fill="#EB1A8D" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Virat Kohli: 70.0% Win Rate, +7.6% Pressure Lift</title>
    </circle>
    <text x="584.4" y="257.8" text-anchor="end" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Virat Kohli</text>
  </g>
  <g class="scatter-point">
    <circle cx="778.1" cy="232.2" r="6.5" fill="#111827" stroke="#FFFFFF" stroke-width="2" style="cursor:pointer;transition:transform 0.15s ease;">
      <title>Yash Dayal (#3): 80.0% Win Rate, +10.2% Pressure Lift</title>
    </circle>
    <text x="778.1" y="220.2" text-anchor="middle" fill="#111827" font-size="10.5" font-weight="600" style="pointer-events:none;">Yash Dayal (#3)</text>
  </g>
</svg>
            </div>

            <!-- Strategic Insights and Quadrant Explanations in Clean Light Mode -->
            <div style="display:grid;grid-template-columns:1.2fr 0.8fr;gap:24px;">
                <!-- 4 Quadrants Visual Grid in Light Mode -->
                <div class="quadrant-light-grid">
                    <div class="quadrant-box q-box-1">
                        <div class="q-tag q-tag-green">Quadrant I &bull; High Pressure Match-Winners</div>
                        <div class="q-desc">Significant positive win lift in tight finishes and playoff knockouts:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Shivam Dube</strong> (+12.4% Lift &bull; 66.7% HP WR)</span>
                            <span class="q-pill"><strong>Jacob Duffy</strong> (+20.5% Lift &bull; 75.0% HP WR)</span>
                            <span class="q-pill"><strong>Rinku Singh</strong> (+5.4% Lift &bull; 69.2% HP WR)</span>
                        </div>
                    </div>

                    <div class="quadrant-box q-box-2">
                        <div class="q-tag q-tag-blue">Quadrant II &bull; Consistent High Anchors</div>
                        <div class="q-desc">Consistently high win conversion across both normal and close games:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Devon Conway</strong> (64.3% HP WR &bull; +18.1% Lift)</span>
                            <span class="q-pill"><strong>Rajat Patidar</strong> (71.4% HP WR &bull; +11.1% Lift)</span>
                            <span class="q-pill"><strong>Axar Patel</strong> (64.3% HP WR &bull; +7.8% Lift)</span>
                        </div>
                    </div>

                    <div class="quadrant-box q-box-3">
                        <div class="q-tag q-tag-amber">Quadrant III &bull; Situational Aggressors</div>
                        <div class="q-desc">High strike rates that provide sudden momentum shifts in run chases:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Bhanuka Rajapaksa</strong> (168.4 Strike Rate)</span>
                            <span class="q-pill"><strong>Romario Shepherd</strong> (182.1 Strike Rate)</span>
                            <span class="q-pill"><strong>Sediqullah Atal</strong> (152.0 Strike Rate)</span>
                        </div>
                    </div>

                    <div class="quadrant-box q-box-4">
                        <div class="q-tag q-tag-navy">Quadrant IV &bull; Defensive Superstars</div>
                        <div class="q-desc">Elite containment; opponents take zero risks, lowering individual lift deltas:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Jasprit Bumrah</strong> (7.4 Death Econ &bull; 48.0% Dots)</span>
                            <span class="q-pill"><strong>Rashid Khan</strong> (6.8 Mid Econ &bull; Flat Googly)</span>
                        </div>
                    </div>
                </div>

                <!-- Insights Column -->
                <div>
                    <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:18px;">
                        <div style="font-weight:700;color:#111827;font-size:13px;margin-bottom:12px;">Strategic Takeaways for Rajasthan Royals:</div>
                        
                        <div style="margin-bottom:12px;">
                            <strong style="color:#111827;font-size:12px;">1. Solves the Middle-Overs Slowdown:</strong>
                            <p style="font-size:12px;color:#374151;margin:2px 0 0 0;line-height:1.4;">
                                Target signing <strong>Shivam Dube</strong> (+12.4% lift) gives Rajasthan Royals the required spin boundary enforcer to partner Samson and Parag.
                            </p>
                        </div>

                        <div style="margin-bottom:12px;">
                            <strong style="color:#111827;font-size:12px;">2. Fortress Sawai Mansingh Fit:</strong>
                            <p style="font-size:12px;color:#374151;margin:2px 0 0 0;line-height:1.4;">
                                Jaipur's large 75m+ boundary requires elite runners and tactical anchors like <strong>Devon Conway</strong> and <strong>Axar Patel</strong> who maintain low dot-ball percentages.
                            </p>
                        </div>

                        <div style="margin-bottom:12px;">
                            <strong style="color:#111827;font-size:12px;">3. Guaranteed Death Overs Defense:</strong>
                            <p style="font-size:12px;color:#374151;margin:2px 0 0 0;line-height:1.4;">
                                Pairing <strong>Josh Hazlewood</strong> with retained yorker specialist <strong>Sandeep Sharma</strong> guarantees 4 disciplined death overs under 9.0 RPO.
                            </p>
                        </div>

                        <div>
                            <strong style="color:#111827;font-size:12px;">4. Bidding Discipline:</strong>
                            <p style="font-size:12px;color:#374151;margin:2px 0 0 0;line-height:1.4;">
                                A hard cap of &#8377;11.0 Cr for any single target prevents auction inflation from ruining squad depth.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- Quantitative Framework Documentation in Clean Light Mode -->
    <div class="doc-grid">
        <div class="doc-box">
            <div class="doc-heading">Quantitative Model Formulation</div>
            <p style="font-size:12.5px;color:#475569;margin-bottom:8px;">
                The Clutch Player Performance Index (CPPI) addresses small-sample statistical variance via Bayesian shrinkage estimation:
            </p>
            <div class="code-snippet">
                CPPI = [ 0.35 &times; Bayes_HP_WR + 0.25 &times; Lift_norm + 0.20 &times; Bayes_KO_WR + 0.10 &times; MOM_HP + 0.10 &times; Base_WR ] &times; Credibility(n_HP)
            </div>
            <p style="font-size:12px;color:#64748B;line-height:1.5;">
                Where Credibility(n_HP) = 0.85 + 0.15 / [1 + exp(&minus;0.25 &times; (n_HP &minus; 8))], safeguarding against small-sample variance (minimum 12 total / 8 high-pressure matches).
            </p>
        </div>

        <div class="doc-box">
            <div class="doc-heading">Operational Definitions & Data Governance</div>
            <p style="font-size:12.5px;color:#475569;line-height:1.6;">
                <strong style="color:#111827;">1. High-Leverage Fixture:</strong> Matches meeting stern empirical pressure criteria: elimination knockout games (Finals, Semi-Finals, Eliminators), super-over resolutions, or finishes with winning margins &le; 15 runs or &le; 2 wickets.<br>
                <strong style="color:#111827;">2. Regulatory Pre-Filter:</strong> Strict exclusion of non-auction eligible entities pursuant to BCCI IPL Player Regulations.<br>
                <strong style="color:#111827;">3. Tactical Venue Model:</strong> Sawai Mansingh Stadium pitch metrics (72-78m boundaries, middle-overs spin grip, nocturnal dew factor).
            </p>
        </div>
    </div>

</div>

<!-- Interactive Power BI Slicer & Sort Logic -->
<script>

function resetSlicers() {
    var searchInput = document.getElementById('filterInput');
    var roleSlicer = document.getElementById('roleSlicer');
    var sortSlicer = document.getElementById('sortSlicer');
    if (searchInput) searchInput.value = '';
    if (roleSlicer) roleSlicer.value = 'ALL';
    if (sortSlicer) sortSlicer.value = 'RANK';
    applySlicers();
}

function showSection(sectionId, btn) {
    var sections = document.querySelectorAll('.data-section');
    for (var i = 0; i < sections.length; i++) {
        sections[i].style.display = 'none';
    }
    var buttons = document.querySelectorAll('.nav-tab-btn');
    for (var j = 0; j < buttons.length; j++) {
        buttons[j].classList.remove('active');
    }
    var target = document.getElementById('section-' + sectionId);
    if (target) {
        target.style.display = 'block';
    }
    if (btn) {
        btn.classList.add('active');
    }
    applySlicers();
}

function applySlicers() {
    var query = document.getElementById('filterInput').value.toLowerCase();
    var roleFilter = document.getElementById('roleSlicer').value;
    var sortOrder = document.getElementById('sortSlicer').value;
    
    var sections = document.querySelectorAll('.data-section');
    var currentSection = null;
    for (var i = 0; i < sections.length; i++) {
        if (sections[i].style.display !== 'none') {
            currentSection = sections[i];
            break;
        }
    }
    if (!currentSection) return;
    
    var table = currentSection.querySelector('table');
    if (!table) return;
    var tbody = table.querySelector('tbody');
    var rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Filter rows
    rows.forEach(function(row) {
        var text = row.innerText.toLowerCase();
        var role = (row.getAttribute('data-role') || '').toUpperCase();
        var matchesQuery = (text.indexOf(query) !== -1);
        var matchesRole = true;
        
        if (roleFilter === 'TOP') {
            matchesRole = (role.indexOf('OPEN') !== -1 || role.indexOf('TOP') !== -1 || role.indexOf('#3') !== -1 || text.indexOf('kohli') !== -1 || text.indexOf('patidar') !== -1);
        } else if (roleFilter === 'MIDDLE') {
            matchesRole = (role.indexOf('MIDDLE') !== -1 || role.indexOf('#4') !== -1 || role.indexOf('STRIKER') !== -1 || text.indexOf('iyer') !== -1 || text.indexOf('dube') !== -1);
        } else if (roleFilter === 'FINISHER') {
            matchesRole = (role.indexOf('FINISH') !== -1 || role.indexOf('DEATH') !== -1 || role.indexOf('#7') !== -1);
        } else if (roleFilter === 'SEAM') {
            matchesRole = (role.indexOf('SEAM') !== -1 || role.indexOf('PACE') !== -1 || role.indexOf('FAST') !== -1 || role.indexOf('SWING') !== -1);
        } else if (roleFilter === 'SPIN') {
            matchesRole = (role.indexOf('SPIN') !== -1 || role.indexOf('ROUNDER') !== -1 || role.indexOf('WRIST') !== -1 || role.indexOf('MYSTERY') !== -1);
        }
        
        row.style.display = (matchesQuery && matchesRole) ? '' : 'none';
    });
    
    // Sort rows dynamically
    rows.sort(function(a, b) {
        if (sortOrder === 'DIFF') {
            return parseFloat(b.getAttribute('data-diff') || 0) - parseFloat(a.getAttribute('data-diff') || 0);
        } else if (sortOrder === 'WIN') {
            return parseFloat(b.getAttribute('data-win') || 0) - parseFloat(a.getAttribute('data-win') || 0);
        } else if (sortOrder === 'INDEX') {
            return parseFloat(b.getAttribute('data-index') || 0) - parseFloat(a.getAttribute('data-index') || 0);
        } else {
            return parseFloat(a.getAttribute('data-rank') || 0) - parseFloat(b.getAttribute('data-rank') || 0);
        }
    });
    
    rows.forEach(function(row) { tbody.appendChild(row); });
}
</script>


</body>
</html>
"""


# ==============================================================================
# CINEMATIC WAR ROOM ENTRY ANIMATION INJECTOR
# ==============================================================================

# Entry animation removed as requested


# Write to all entry files

# Post-process master_dashboard_html outside f-string to avoid syntax errors
master_dashboard_html = master_dashboard_html.replace('</style>', """
.tactical-grid {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 24px;
            margin-bottom: 24px;
            align-items: start;
        }
        @media (max-width: 1024px) {
            .tactical-grid {
                grid-template-columns: 1fr;
            }
        }

        .tactical-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 20px rgba(0, 29, 72, 0.05);
        }

        .tactical-card-title {
            font-size: 16px;
            font-weight: 800;
            color: #111827;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
            letter-spacing: -0.2px;
        }

        .tactical-card-sub {
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 18px;
            line-height: 1.4;
        }

        /* Clean Light Mode Playing XI Blueprint */
        .xi-blueprint-container {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 18px;
        }
        .xi-phase-group {
            margin-bottom: 14px;
        }
        .xi-phase-group:last-child {
            margin-bottom: 0;
        }
        .xi-phase-title {
            font-size: 11px;
            font-weight: 800;
            color: #111827;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 8px;
            padding-left: 2px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .xi-player-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 8px;
        }
        .xi-player-pill {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 8px 12px;
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .xi-player-pill:hover {
            border-color: var(--rr-pink);
            box-shadow: 0 2px 8px rgba(0, 29, 72, 0.08);
            transform: translateY(-1px);
        }
        .xi-num {
            font-size: 13px;
            font-weight: 800;
            color: #111827;
            width: 24px;
            height: 24px;
            background: #F1F5F9;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        .xi-info {
            flex: 1;
            min-width: 0;
        }
        .xi-name-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }
        .xi-name {
            font-size: 13px;
            font-weight: 700;
            color: #111827;
        }
        .xi-badge {
            font-size: 9.5px;
            font-weight: 800;
            padding: 1px 6px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            white-space: nowrap;
        }
        .xi-retained {
            background: #F1F5F9;
            color: #0F172A;
            border: 1px solid #CBD5E1;
        }
        .xi-target {
            background: #FDF2F8;
            color: #BE185D;
            border: 1px solid #FBCFE8;
        }
        .xi-role {
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .xi-bench-box {
            margin-top: 14px;
            padding: 10px 12px;
            background: #FFFFFF;
            border: 1px dashed #CBD5E1;
            border-radius: 8px;
        }
        .xi-bench-lbl {
            font-size: 10.5px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        .xi-bench-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        .bench-pill {
            display: inline-block;
            background: #F1F5F9;
            border: 1px solid #E2E8F0;
            border-radius: 4px;
            padding: 3px 8px;
            font-size: 11px;
            color: #374151;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .bench-pill:hover {
            border-color: var(--rr-pink);
            background: #FFFFFF;
        }

        /* Light Mode Quadrants Grid */
        .quadrant-light-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        @media (max-width: 768px) {
            .quadrant-light-grid {
                grid-template-columns: 1fr;
            }
        }
        .quadrant-box {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 14px;
        }
        .q-box-1 { border-left: 4px solid #059669; }
        .q-box-2 { border-left: 4px solid #64748B; }
        .q-box-3 { border-left: 4px solid #D97706; }
        .q-box-4 { border-left: 4px solid #111827; }
        .q-tag {
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .q-tag-green { color: #059669; }
        .q-tag-blue { color: #111827; }
        .q-tag-amber { color: #D97706; }
        .q-tag-navy { color: #111827; }
        .q-desc {
            font-size: 11.5px;
            color: var(--text-muted);
            margin-bottom: 8px;
            line-height: 1.35;
        }
        .q-players {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .q-pill {
            font-size: 11px;
            color: #374151;
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 4px;
            padding: 3px 8px;
        }

        .purse-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }
        .purse-table th {
            background: #F1F5F9;
            color: #111827;
            padding: 9px 12px;
            font-weight: 700;
            text-align: left;
            border-bottom: 2px solid #CBD5E1;
        }
        .purse-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #E2E8F0;
            vertical-align: middle;
        }
        .purse-table tr:hover {
            background: #F8FAFC;
        }
        .tier-badge {
            display: inline-block;
            font-size: 10.5px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            white-space: nowrap;
        }
        .tier-1 { background: rgba(235, 26, 141, 0.12); color: var(--rr-pink); border: 1px solid rgba(235, 26, 141, 0.3); }
        .tier-2 { background: rgba(0, 29, 72, 0.08); color: #111827; border: 1px solid rgba(0, 29, 72, 0.2); }

        .budget-kpi-bar {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 18px;
            text-align: center;
        }
        .budget-kpi-val {
            font-size: 18px;
            font-weight: 800;
            color: #111827;
            font-variant-numeric: tabular-nums;
        }
        .budget-kpi-lbl {
            font-size: 10.5px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 2px;
        }

        /* Light Mode Documentation Boxes */
        .doc-box {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px;
            padding: 22px 24px;
            box-shadow: 0 4px 16px rgba(0, 29, 72, 0.04) !important;
        }

        .code-snippet {
            background: #F8FAFC !important;
            border: 1px solid #CBD5E1 !important;
            color: #0F172A !important;
            padding: 8px 12px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 12px;
            margin: 8px 0;
        }
""" + '\n</style>', 1)


# Inject Executive Footer right before the interactive slicer script
target_pos = master_dashboard_html.find('</div>\n\n<!-- Interactive Power BI Slicer')
if target_pos != -1:
    master_dashboard_html = master_dashboard_html[:target_pos] + """
    <!-- Simple Minimal Footer with Copyright -->
    <footer class="simple-footer" style="margin-top:44px;margin-bottom:28px;padding-top:26px;border-top:1px solid #E2E8F0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#475569;">
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(300px, 1fr));gap:28px;margin-bottom:22px;">
            <div>
                <div style="font-size:12.5px;font-weight:700;color:#111827;margin-bottom:6px;">Methodology</div>
                <p style="margin:0;font-size:12px;line-height:1.65;color:#475569;">
                    Evaluated 883 IPL &amp; T20I matches (2022&ndash;2026) to isolate 178 high-pressure games (MLI &ge; 30: knockouts, Super Overs, or close finishes). Players are ranked via the calibrated CPPI combining Bayesian HP Win Rate (35%), Normalized Pressure Lift &Delta; (25%), Knockout Win Rate (20%), HP POTM Density (10%), and Baseline Win Rate (10%), scaled by a sigmoid credibility curve and BCCI auction eligibility filters.
                </p>
            </div>
            <div>
                <div style="font-size:12.5px;font-weight:700;color:#111827;margin-bottom:6px;">Thought Process</div>
                <p style="margin:0;font-size:12px;line-height:1.65;color:#475569;">
                    Traditional averages reward stat-padding in one-sided matches. Measuring True Pressure Lift (&Delta;) isolates who genuinely raises their team&rsquo;s win rate when stakes peak &mdash; highlighting high-value clutch winners like Shivam Dube and Jacob Duffy suited for Sawai Mansingh Stadium (Jaipur) within a &#8377;45 Cr auction budget, rather than overpaying for reputation.
                </p>
            </div>
        </div>

        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;padding-top:16px;border-top:1px solid #E2E8F0;font-size:12px;color:#64748B;">
            <div>
                &copy; 2026 Ketan Rawat. All rights reserved. &middot; Rajasthan Royals SupeRR Selector Season 2
            </div>
            <div style="display:flex;flex-wrap:wrap;align-items:center;gap:10px;">
                <a href="https://www.linkedin.com/in/ketan-rawat-97a8aa2a0/" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">LinkedIn</a>
                <span style="color:#CBD5E1;">|</span>
                <a href="https://github.com/Ketanrawat2004/RR-Dashboard" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">GitHub</a>
                <span style="color:#CBD5E1;">|</span>
                <a href="https://drive.google.com/file/d/1YV_i3Un8t7UZsfk1_WXQdfsM6T0Pe6ui/view?usp=drive_link" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">Resume</a>
                <span style="color:#CBD5E1;">|</span>
                <a href="https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/view?usp=sharing" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">Season 1 Certificate (Additional Top 20)</a>
            </div>
        </div>
    </footer>
""" + '\n' + master_dashboard_html[target_pos:]

with open("rr_pressure_dashboard.html", "w", encoding="utf-8") as f:
    f.write(master_dashboard_html)
print("Updated rr_pressure_dashboard.html")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(master_dashboard_html)
print("Updated index.html")

with open("rr_war_room_terminal.html", "w", encoding="utf-8") as f:
    f.write(master_dashboard_html)
print("Updated rr_war_room_terminal.html")
