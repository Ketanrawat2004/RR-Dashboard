import pandas as pd
import glob, os

files = glob.glob('season2_data/*.csv') + glob.glob('data/*.csv')
print("CSV files found:", files)

# Let's inspect playing_eleven.csv and matches.csv
if os.path.exists('season2_data/playing_eleven.csv'):
    pe = pd.read_csv('season2_data/playing_eleven.csv')
    print("playing_eleven shape:", pe.shape)
    print("Columns:", pe.columns.tolist())
    
    # Check player names
    names = ['Bumrah', 'Siraj', 'Rashid', 'Klaasen', 'Rohit']
    for n in names:
        matches = pe[pe['player_name'].str.contains(n, case=False, na=False)]
        unique_matches = matches['match_id'].nunique()
        print(f"Name search '{n}': unique match_ids in dataset = {unique_matches}")
        if len(matches) > 0:
            print("  Sample player names:", matches['player_name'].unique())

