import re
import pandas as pd

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Extract bowlers from index.html
m_bowl = re.search(r'<table id="table-bowlers">[\s\S]*?<\/tbody>', html)
bowl_rows = re.findall(r'<tr[^>]*>[\s\S]*?<\/tr>', m_bowl.group(0))

comp_rows = [r for r in bowl_rows if "bowler-row-composite" in r]
rpae_rows = [r for r in bowl_rows if "bowler-row-rpae" in r]

print(f"Composite rows in HTML: {len(comp_rows)}")
print(f"RPAE rows in HTML: {len(rpae_rows)}")

# Load Step 4 CSVs
df_step4_comp = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_COMPOSITE.csv")
df_step4_rpae = pd.read_csv("phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv")

def parse_bowler_rows(rows):
    res = []
    for r in rows:
        tds = [re.sub(r'<[^>]*>', '', td).strip() for td in re.findall(r'<td\b[^>]*>([\s\S]*?)<\/td>', r)]
        m_name = re.search(r'<div class="name-box">\s*<(?:a|span)[^>]*>([^<]+)<\/(?:a|span)>', r)
        name = m_name.group(1).strip() if m_name else ""
        res.append({
            "rank": int(tds[0]),
            "name": name,
            "lev_balls": int(tds[3]),
            "col8": tds[7],
            "score": tds[9]
        })
    return pd.DataFrame(res)

df_html_comp = parse_bowler_rows(comp_rows)
df_html_rpae = parse_bowler_rows(rpae_rows)

print("\n=== COMPOSITE BOWLER COMPARISON: HTML vs STEP 4 CSV ===")
mismatches_comp = 0
for _, r_csv in df_step4_comp.iterrows():
    name = r_csv["player_name"]
    csv_p_b = int(r_csv["pressure_b"])
    
    sub = df_html_comp[df_html_comp["name"] == name]
    if sub.empty:
        print(f"MISSING in HTML: {name}")
        mismatches_comp += 1
    else:
        h_row = sub.iloc[0]
        h_p_b = h_row["lev_balls"]
        if h_p_b != csv_p_b:
            print(f"MISMATCH {name}: HTML(p={h_p_b}) vs CSV(p={csv_p_b})")
            mismatches_comp += 1

print(f"Total Composite Bowlers checked: {len(df_step4_comp)}, Mismatches: {mismatches_comp}")

print("\n=== RPAE BOWLER COMPARISON: HTML vs STEP 4 CSV ===")
mismatches_rpae = 0
for _, r_csv in df_step4_rpae.iterrows():
    name = r_csv["player_name"]
    csv_p_b = int(r_csv["pressure_b"])
    csv_c_b = int(r_csv["career_b"])
    
    sub = df_html_rpae[df_html_rpae["name"] == name]
    if sub.empty:
        print(f"MISSING in HTML: {name}")
        mismatches_rpae += 1
    else:
        h_row = sub.iloc[0]
        h_p_b = h_row["lev_balls"]
        h_c_b = int(h_row["col8"].replace(",", ""))
        if h_p_b != csv_p_b or h_c_b != csv_c_b:
            print(f"MISMATCH {name}: HTML(p={h_p_b}, c={h_c_b}) vs CSV(p={csv_p_b}, c={csv_c_b})")
            mismatches_rpae += 1

print(f"Total RPAE Bowlers checked: {len(df_step4_rpae)}, Mismatches: {mismatches_rpae}")

