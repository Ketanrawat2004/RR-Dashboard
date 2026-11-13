import pandas as pd
import re

df1 = pd.read_csv('phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_COMPOSITE.csv')
print('Bowl Comp columns:', df1.columns.tolist()[:10])
df2 = pd.read_csv('phase1_audit/step4_jury_harmonization/FINAL_BOWLER_RANKINGS_RAE.csv')
print('Bowl RAE columns:', df2.columns.tolist()[:10])

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx1 = html.find('id="batters"')
print('batters pos:', idx1)
print(html[idx1:idx1+400])

idx2 = html.find('id="bowlers"')
print('bowlers pos:', idx2)
print(html[idx2:idx2+400])

