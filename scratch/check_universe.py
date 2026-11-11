import csv

with open("pressure_output/audit_match_pressure_scores.csv", encoding="utf-8") as f:
    hp = [r for r in csv.DictReader(f) if r["is_high_pressure"] == "True"]

print("HP count:", len(hp))
# Exclusive priority: Knockout/Stage>=20, Defend runs <= 15, Chase wkts <= 2 / Super Over
ko_matches = [r for r in hp if int(float(r["knockout_score"])) > 0 or r["stage_label"] in ("Final", "Semi-Final", "Qualifier/Eliminator", "Super 4")]
non_ko_run = [r for r in hp if r not in ko_matches and "run" in r["close_label"]]
non_ko_wkt = [r for r in hp if r not in ko_matches and r not in non_ko_run]
print(f"Mutually exclusive in {len(hp)} HP: KO/Stage={len(ko_matches)} ({len(ko_matches)/len(hp)*100:.1f}%), League<=15runs={len(non_ko_run)} ({len(non_ko_run)/len(hp)*100:.1f}%), League<=2wkts/SuperOver={len(non_ko_wkt)} ({len(non_ko_wkt)/len(hp)*100:.1f}%)")

for fn in ["pressure_output/audit_all_players_ranked.csv", "season2_data/player_master.csv"]:
    try:
        with open(fn, encoding="utf-8") as f:
            print(fn, "rows:", len(list(csv.DictReader(f))))
    except Exception as e:
        print(fn, "err:", e)

