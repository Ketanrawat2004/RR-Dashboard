import pandas as pd
import glob

for f in ['demo_pack_TRUTH.csv', 'output/ranked_candidates.csv', 'pressure_output/clutch_player_rankings.csv']:
    try:
        df = pd.read_csv(f)
        print("Found:", f)
        print("Columns:", df.columns.tolist()[:10])
        for p in ['Bumrah', 'Siraj', 'Rashid', 'Klaasen', 'Rohit']:
            hit = df[df.apply(lambda row: row.astype(str).str.contains(p).any(), axis=1)]
            if len(hit) > 0:
                print(f"  Hit {p} in {f}:")
                for col in ['player_name', 'name', 'matches', 'total_matches', 'total_m', 'base_matches', 'hp_matches']:
                    if col in hit.columns:
                        print(f"    {col}: {hit[col].tolist()}")
    except Exception as e:
        pass

