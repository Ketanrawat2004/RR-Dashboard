with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('player_html = f"""')
print("player_html starts at:", idx)
print(text[idx:idx+800])

