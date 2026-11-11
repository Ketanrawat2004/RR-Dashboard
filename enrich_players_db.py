import json

with open("players_db.json", "r", encoding="utf-8") as f:
    players = json.load(f)

# Non-technical enhancements
takeaways = {
    "rajat_patidar": {
        "tagline": "Crushes spin in middle overs (71.4% win rate in tight finishes)",
        "superpower": "Destroys spin bowling between overs 7 and 15 without taking wild risks.",
        "why_not_famous": "Outperforms Virat Kohli and Rohit Sharma in pressure lift (+11.1% vs +7.6% and -3.7%). Did not crumble in IPL eliminators.",
        "rr_management_summary": "At Jaipur's Sawai Mansingh Stadium, the pitch slows down in the middle overs. Patidar attacks leg-spinners and left-arm spinners, freeing Riyan Parag and Jaiswal from pressure."
    },
    "rinku_singh": {
        "tagline": "Never lost an IPL playoff or knockout match (100% win rate)",
        "superpower": "Ice in his veins when required run rate crosses 12 runs per over.",
        "why_not_famous": "Big-name hitters like Heinrich Klaasen have high strike rates but lose 75% of playoff games. Rinku gets teams over the line 100% of the time.",
        "rr_management_summary": "Pairing Rinku with Dhruv Jurel and Shimron Hetmyer creates the most dependable overs 16–20 finishing trio in IPL history. RR will never throw away winning chases."
    },
    "devon_conway": {
        "tagline": "IPL Final Man of the Match (+18.1% clutch lift under pressure)",
        "superpower": "Anchors run chases on difficult tracks with zero dot-ball panic.",
        "why_not_famous": "Normal win rate is 46%, but in pressure games his team wins 64% of the time. Steps up when weather or revisions happen (IPL 2023 Final).",
        "rr_management_summary": "Provides world-class top-order stability and backup wicketkeeping, especially valuable when batting first under lights at Jaipur."
    },
    "sediqullah_atal": {
        "tagline": "2 Man of the Match awards in just 8 high-pressure appearances",
        "superpower": "Furious powerplay boundary hitting against international-quality pace.",
        "why_not_famous": "Costs less than 10% of a marquee opener's salary but wins matches off his own bat.",
        "rr_management_summary": "Low-cost, high-upside overseas backup opener who can exploit the 30-yard fielding restrictions at Jaipur."
    },
    "ruturaj_gaikwad": {
        "tagline": "100% playoff win rate; ice-cold chase pacing under rising run rate",
        "superpower": "Master of reading the match situation and finding boundaries without slogging.",
        "why_not_famous": "Far more consistent in playoffs than Shubman Gill (50% KO win rate) or KL Rahul (40% KO win rate).",
        "rr_management_summary": "High-IQ leader who can control the innings tempo, allowing young prodigy Vaibhav Sooryavanshi to play fearlessly."
    },
    "shivam_dube": {
        "tagline": "100% playoff win rate; destroys left-arm and leg-spin in middle overs",
        "superpower": "Hits balls into the top tier off lengths where other batters struggle to rotate strike.",
        "why_not_famous": "Massive +12.4% win rate boost when games are tight, compared to generic middle-order hitters.",
        "rr_management_summary": "Neutralizes opposition mystery spinners at Sawai Mansingh Stadium, making RR's home ground an offensive fortress."
    },
    "shreyas_iyer": {
        "tagline": "Championship-winning captain with 3 clutch Man-of-the-Match awards",
        "superpower": "Calm tactical leadership and counter-attacking when wickets fall early.",
        "why_not_famous": "Consistently outperforms Sanju Samson in knockout matches (60% KO win rate vs 37.5% for Samson).",
        "rr_management_summary": "Provides senior middle-order composure alongside Riyan Parag, guaranteeing RR doesn't panic in eliminator matches."
    },
    "virat_kohli": {
        "tagline": "70.0% win rate in 20 tight games; all-time master chase anchor",
        "superpower": "Relentless physical fitness, running between wickets, and deep chase execution.",
        "why_not_famous": "Ranked #8 only because younger stars (Patidar, Conway) show larger percentage jumps over baseline.",
        "rr_management_summary": "The ultimate benchmark for how to chase totals on large outfield grounds like Jaipur."
    },
    "axar_patel": {
        "tagline": "100% playoff win rate; crisis 47 in T20 World Cup Final",
        "superpower": "Rescues teams from top-order batting collapses while bowling 4 economical overs.",
        "why_not_famous": "Delivers more clutch batting output in high-stakes T20 matches than traditional all-rounders.",
        "rr_management_summary": "Provides batting depth down to #8 and guarantees 4 economical overs of spin, solving RR's team balance."
    },
    "bhanuka_rajapaksa": {
        "tagline": "100% knockout win rate; fearless left-hand boundary striker",
        "superpower": "Attacks from ball one against off-spin without needing 10 balls to settle.",
        "why_not_famous": "Legitimate, 100% auction-eligible foreign striker who outperforms expensive names in knockouts.",
        "rr_management_summary": "High-impact left-handed boundary option for tight middle-overs phases at an affordable price."
    },
    "mitchell_starc": {
        "tagline": "Man of the Match in both Qualifier 1 & Final; 100% playoff record",
        "superpower": "Unplayable fast inswinging yorkers that clean bowl top-order batters in finals.",
        "why_not_famous": "May look average in regular league games, but becomes an unstoppable match-winner in playoffs.",
        "rr_management_summary": "Guarantees wickets in big playoff matches. Pairs with Jofra Archer to intimidate opposition top orders."
    },
    "josh_hazlewood": {
        "tagline": "78.6% pressure win rate (+14.9% boost); robotic accuracy",
        "superpower": "Bowls the exact same hard length ball after ball, forcing mistimed pull shots.",
        "why_not_famous": "Dramatically beats Jasprit Bumrah in team pressure wins (78.6% vs 42.9%). Opponents can't safely defend against him.",
        "rr_management_summary": "The perfect fast bowling fit for Jaipur's true-bounce pitch. Shuts down scoring in powerplay and death overs."
    },
    "jacob_duffy": {
        "tagline": "Highest clutch lift (+20.5%) in the entire 883-match dataset",
        "superpower": "Hit-the-deck pace that takes unexpected wickets in high-scoring games.",
        "why_not_famous": "Costs a fraction of marquee fast bowlers but produces higher statistical clutch output.",
        "rr_management_summary": "Smart budget overseas pacer who gives RR world-class bench strength without blowing the purse."
    },
    "suyash_sharma": {
        "tagline": "Fast mystery leg-spin (72.7% win rate in tight games)",
        "superpower": "Rapid arm speed that deceives batters on length before they can commit to a shot.",
        "why_not_famous": "Much harder to hit for sixes in tight finishes than slow-flight leg-spinners like Chahal.",
        "rr_management_summary": "Forms an unreadable wrist-spin duo with Ravi Bishnoi, creating a 8-over middle-overs choke at SMS Stadium."
    },
    "lockie_ferguson": {
        "tagline": "150 kph express pace; 2 Man-of-the-Match awards in tight games",
        "superpower": "Pure velocity through the air that breaks established batting partnerships.",
        "why_not_famous": "Bowls maiden Super Overs and doesn't lose his radar under pressure.",
        "rr_management_summary": "Brings raw speed to support Archer, ensuring RR bowls 145kph+ across all phases of the innings."
    },
    "yash_dayal": {
        "tagline": "80.0% pressure win rate; famously defended final over vs CSK",
        "superpower": "Left-arm angle slanting across right-handers with pinpoint wide yorkers at the death.",
        "why_not_famous": "Tremendous mental toughness. Out-clutches Mohammed Siraj (80.0% win rate vs 38.9% for Siraj).",
        "rr_management_summary": "Fills RR's missing tactical piece: a world-class Indian left-arm pacer to bowl overs 18 and 20."
    },
    "romario_shepherd": {
        "tagline": "100% knockout win rate; heavy-ball bowler and power hitter",
        "superpower": "Hits the pitch hard to extract uncomfortable bounce and smashes 20-run final overs.",
        "why_not_famous": "Dual-threat all-rounder who wins matches with both ball and bat in tight finishes.",
        "rr_management_summary": "Gives RR tactical depth at #8, allowing the team to play an extra specialist bowler."
    },
    "varun_chakravarthy": {
        "tagline": "100% knockout win rate; mystery spin choke in middle overs",
        "superpower": "Multiple release points (carrom ball, leg-cutter) that freeze batters in close chases.",
        "why_not_famous": "Far more reliable in pressure games than Rashid Khan (61.9% pressure win rate vs 38.5% for Rashid).",
        "rr_management_summary": "Turns Sawai Mansingh Stadium into a spin fortress by suffocating opposition runs in overs 7–15."
    },
    "bhuvneshwar_kumar": {
        "tagline": "71.4% playoff win rate; calm knuckle-ball execution in death overs",
        "superpower": "Decades of high-pressure experience; robotic execution of wide yorkers and knuckle balls.",
        "why_not_famous": "Never panics or concedes extras under pressure, unlike younger, erratic pacers.",
        "rr_management_summary": "Veteran Indian seamer who can bowl tough powerplay overs (1 and 3) and mentor young pacers."
    },
    "arshdeep_singh": {
        "tagline": "68.0% pressure win rate (+11.1% boost); saves an overseas slot for RR",
        "superpower": "Pins right-handers with curling left-arm yorkers in the 19th and 20th overs.",
        "why_not_famous": "Replaces banned Pakistani pacers under BCCI rules; far superior to Siraj in death overs.",
        "rr_management_summary": "The ultimate strategic signing: gives RR elite death bowling WITHOUT wasting one of only 4 overseas slots!"
    }
}

for p in players:
    key = p["key"]
    if key in takeaways:
        p.update(takeaways[key])

with open("players_db.json", "w", encoding="utf-8") as f:
    json.dump(players, f, indent=2)

print("Enriched players_db.json with non-technical executive takeaways!")

