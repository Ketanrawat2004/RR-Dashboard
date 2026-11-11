with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    code = f.read()

# Update Klaasen total_m to 76
code = code.replace('"name": "Heinrich Klaasen",\n        "key": "heinrich_klaasen",\n        "teams": "South Africa, Sunrisers Hyderabad, Titans",\n        "role_desc": "Middle-Overs Spin Enforcer & Wicketkeeper",\n        "total_m": 68,',
                    '"name": "Heinrich Klaasen",\n        "key": "heinrich_klaasen",\n        "teams": "South Africa, Sunrisers Hyderabad, Titans",\n        "role_desc": "Middle-Overs Spin Enforcer & Wicketkeeper",\n        "total_m": 76,', 1)

# Update Rohit total_m to 92
code = code.replace('"name": "Rohit Sharma",\n        "key": "rohit_sharma",\n        "teams": "India, Mumbai Indians, Deccan Chargers",\n        "role_desc": "Top-Order Opening Batter & Powerplay Attacker",\n        "total_m": 95,',
                    '"name": "Rohit Sharma",\n        "key": "rohit_sharma",\n        "teams": "India, Mumbai Indians, Deccan Chargers",\n        "role_desc": "Top-Order Opening Batter & Powerplay Attacker",\n        "total_m": 92,', 1)

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated Klaasen (76) and Rohit (92) matches in fix_dashboard_and_wagon.py!")

