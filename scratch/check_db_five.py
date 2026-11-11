import json

with open('players_db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print("Keys in players_db.json:", len(db))
five = ['jasprit_bumrah', 'mohammed_siraj', 'rashid_khan', 'heinrich_klaasen', 'rohit_sharma']
for k in five:
    if k in db:
        print(f"{k}: exists in db! Keys: {list(db[k].keys())}")
    else:
        print(f"{k}: NOT IN DB")

