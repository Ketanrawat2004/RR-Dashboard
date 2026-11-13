import re
import pandas as pd

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Extract batters from index.html
m_bat = re.search(r'<table id="table-batters">[\s\S]*?<\/tbody>', html)
bat_rows = re.findall(r'<tr[^>]*>[\s\S]*?<\/tr>', m_bat.group(0))[1:] # skip header

html_batters = []
for r in bat_rows:
    tds = [re.sub(r'<[^>]*>', '', td).strip() for td in re.findall(r'<td\b[^>]*>([\s\S]*?)<\/td>', r)]
    # tds[0] is rank, tds[1] is player/role, tds[3] is leverage deliveries, tds[7] is career balls
    m_name = re.search(r'<div class="name-box">\s*<(?:a|span)[^>]*>([^<]+)<\/(?:a|span)>', r)
    name = m_name.group(1).strip() if m_name else ""
    html_batters.append({
        "rank": int(tds[0]),
        "name": name,
        "lev_balls": int(tds[3]),
        "career_balls": int(tds[7].replace(",", ""))
    })

df_html_bat = pd.DataFrame(html_batters)

# Load Step 4 CSV
df_step4_bat = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BATTER_RANKINGS.csv")

print("=== BATTER COMPARISON: HTML vs STEP 4 CSV ===")
mismatches_bat = 0
for _, r_csv in df_step4_bat.iterrows():
    name = r_csv["player_name"]
    csv_p_bf = int(r_csv["pressure_bf"])
    csv_c_bf = int(r_csv["career_bf"])
    
    sub_html = df_html_bat[df_html_bat["name"] == name]
    if sub_html.empty:
        print(f"MISSING in HTML: {name}")
        mismatches_bat += 1
    else:
        h_row = sub_html.iloc[0]
        h_p_bf = h_row["lev_balls"]
        h_c_bf = h_row["career_balls"]
        if h_p_bf != csv_p_bf or h_c_bf != csv_c_bf:
            print(f"MISMATCH {name}: HTML(p={h_p_bf}, c={h_c_bf}) vs CSV(p={csv_p_bf}, c={csv_c_bf})")
            mismatches_bat += 1

print(f"Total Batters checked: {len(df_step4_bat)}, Mismatches: {mismatches_bat}")

