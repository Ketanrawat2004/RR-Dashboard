import re

with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update superstars_audit data to exact dataset counts
replacements = [
    ('"name": "Jasprit Bumrah",\n        "key": "jasprit_bumrah",\n        "teams": "India, Mumbai Indians, Gujarat",\n        "role_desc": "Premier Fast Bowler & Death Specialist",\n        "total_m": 56,\n        "base_wr": 52.0,',
     '"name": "Jasprit Bumrah",\n        "key": "jasprit_bumrah",\n        "teams": "India, Mumbai Indians, Gujarat",\n        "role_desc": "Premier Fast Bowler & Death Specialist",\n        "total_m": 77,\n        "base_wr": 51.9,'),
    ('"name": "Mohammed Siraj",\n        "key": "mohammed_siraj",\n        "teams": "India, Royal Challengers Bengaluru, Hyderabad",\n        "role_desc": "Pace Strike Bowler",\n        "total_m": 67,\n        "base_wr": 55.4,',
     '"name": "Mohammed Siraj",\n        "key": "mohammed_siraj",\n        "teams": "India, Royal Challengers Bengaluru, Hyderabad",\n        "role_desc": "Pace Strike Bowler",\n        "total_m": 83,\n        "base_wr": 55.4,'),
    ('"name": "Rashid Khan",\n        "key": "rashid_khan",\n        "teams": "Afghanistan, Gujarat Titans, Sunrisers Hyderabad",\n        "role_desc": "Leg-Spin Mystery Bowler",\n        "total_m": 122,\n        "base_wr": 62.0,\n        "hp_m": 22,\n        "hp_wr": 63.6,\n        "lift": 1.6,',
     '"name": "Rashid Khan",\n        "key": "rashid_khan",\n        "teams": "Afghanistan, Gujarat Titans, Sunrisers Hyderabad",\n        "role_desc": "Leg-Spin Mystery Bowler",\n        "total_m": 122,\n        "base_wr": 57.4,\n        "hp_m": 26,\n        "hp_wr": 38.5,\n        "lift": -18.9,'),
    ('"name": "Heinrich Klaasen",\n        "key": "heinrich_klaasen",\n        "teams": "South Africa, Sunrisers Hyderabad, Titans",\n        "role_desc": "Middle-Overs Spin Enforcer & Wicketkeeper",\n        "total_m": 68,\n        "base_wr": 54.4,\n        "hp_m": 16,\n        "hp_wr": 50.0,\n        "lift": -4.4,',
     '"name": "Heinrich Klaasen",\n        "key": "heinrich_klaasen",\n        "teams": "South Africa, Sunrisers Hyderabad, Titans",\n        "role_desc": "Middle-Overs Spin Enforcer & Wicketkeeper",\n        "total_m": 76,\n        "base_wr": 48.7,\n        "hp_m": 15,\n        "hp_wr": 40.0,\n        "lift": -8.7,'),
    ('"name": "Rohit Sharma",\n        "key": "rohit_sharma",\n        "teams": "India, Mumbai Indians, Deccan Chargers",\n        "role_desc": "Top-Order Opening Batter & Powerplay Attacker",\n        "total_m": 95,\n        "base_wr": 56.8,\n        "hp_m": 24,\n        "hp_wr": 50.0,\n        "lift": -6.8,',
     '"name": "Rohit Sharma",\n        "key": "rohit_sharma",\n        "teams": "India, Mumbai Indians, Deccan Chargers",\n        "role_desc": "Top-Order Opening Batter & Powerplay Attacker",\n        "total_m": 92,\n        "base_wr": 51.1,\n        "hp_m": 19,\n        "hp_wr": 47.4,\n        "lift": -3.7,')
]

for old, new in replacements:
    if old in code:
        code = code.replace(old, new, 1)
        print("Updated superstar metrics!")
    else:
        print("WARNING: Could not find exact block, checking with regex...")

# 2. Update the table header in Table 3: Superstars Audit
old_header = '<th style="text-align:center;">Career<br>Matches</th>'
new_header = '<th style="text-align:center;" title="Exact matches played within the evaluated 883-match competition dataset">Dataset<br>Matches</th>'
if old_header in code:
    code = code.replace(old_header, new_header, 1)
    print("Updated table header to Dataset Matches!")

# 3. Add the War Room Auction Strategy content to fill the empty Right Column
old_rule_block = r'''                <div style="margin-top:20px;padding:14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                    <div style="font-weight:700;font-size:12.5px;color:#111827;margin-bottom:4px;">Auction Bidding Rule:</div>
                    <p style="font-size:12px;color:#374151;line-height:1.5;margin:0;">
                        If bidding for any player goes more than 10% above their maximum limit, stop bidding immediately and switch to backup targets (such as Yash Dayal at &#8377;5.5 Cr or Bhanuka Rajapaksa at &#8377;3.5 Cr) to protect the overall team budget.
                    </p>
                </div>
            </div>'''

new_expanded_right_col = r'''                <div style="margin-top:20px;padding:14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                    <div style="font-weight:700;font-size:12.5px;color:#111827;margin-bottom:4px;">Auction Bidding Rule:</div>
                    <p style="font-size:12px;color:#374151;line-height:1.5;margin:0;">
                        If bidding for any player goes more than 10% above their maximum limit, stop bidding immediately and switch to backup targets (such as Yash Dayal at &#8377;5.5 Cr or Bhanuka Rajapaksa at &#8377;3.5 Cr) to protect the overall team budget.
                    </p>
                </div>

                <!-- 1. Contingency Bidding Matrix & Step-Down Rules -->
                <div style="margin-top:16px;padding:16px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;">
                    <div style="font-weight:700;font-size:12.5px;color:#111827;margin-bottom:10px;">
                        Contingency Bidding Matrix (Live Step-Down Triggers)
                    </div>
                    <div style="display:flex;flex-direction:column;gap:8px;font-size:12px;color:#374151;">
                        <div style="padding:8px 10px;background:#F8FAFC;border-radius:6px;border-left:3px solid var(--rr-pink);line-height:1.45;">
                            <strong>If Rinku Singh &gt; &#8377;11.0 Cr:</strong> Pivot immediately to Bhanuka Rajapaksa (&#8377;3.5 Cr) + promote Hetmyer to No. 6, freeing &#8377;7.5 Cr for bowling reserve.
                        </div>
                        <div style="padding:8px 10px;background:#F8FAFC;border-radius:6px;border-left:3px solid #0284C7;line-height:1.45;">
                            <strong>If Shivam Dube &gt; &#8377;9.5 Cr:</strong> Switch to Rajat Patidar (&#8377;7.0 Cr) for spin boundary execution, reallocating &#8377;2.5 Cr to overseas pace.
                        </div>
                        <div style="padding:8px 10px;background:#F8FAFC;border-radius:6px;border-left:3px solid #059669;line-height:1.45;">
                            <strong>If Josh Hazlewood &gt; &#8377;9.5 Cr:</strong> Lock Jacob Duffy (&#8377;6.5 Cr) as primary overseas seamer and secure Yash Dayal (&#8377;4.5 Cr).
                        </div>
                        <div style="padding:8px 10px;background:#F8FAFC;border-radius:6px;border-left:3px solid #D97706;line-height:1.45;">
                            <strong>If Axar Patel &gt; &#8377;8.0 Cr:</strong> Pivot to Varun Chakravarthy (&#8377;5.5 Cr) + domestic all-rounder backup to secure middle-overs spin choke.
                        </div>
                    </div>
                </div>

                <!-- 2. Phase-by-Phase Purse Distribution Grid -->
                <div style="margin-top:16px;padding:16px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;">
                    <div style="font-weight:700;font-size:12.5px;color:#111827;margin-bottom:10px;">
                        Phase-by-Phase Purse Distribution (&#8377;45.0 Cr Total)
                    </div>
                    <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:10px;">
                        <div style="padding:10px 12px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:6px;">
                            <div style="font-size:10.5px;font-weight:700;color:#64748B;text-transform:uppercase;">Middle Spin Attack</div>
                            <div style="font-size:15px;font-weight:800;color:#111827;margin-top:2px;">&#8377;17.50 Cr <span style="font-size:11px;font-weight:600;color:#059669;">(38.9%)</span></div>
                            <div style="font-size:11px;color:#64748B;margin-top:2px;">Dube (&#8377;9.5) + Axar (&#8377;8.0)</div>
                        </div>
                        <div style="padding:10px 12px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:6px;">
                            <div style="font-size:10.5px;font-weight:700;color:#64748B;text-transform:uppercase;">Death Finishing</div>
                            <div style="font-size:15px;font-weight:800;color:#111827;margin-top:2px;">&#8377;11.00 Cr <span style="font-size:11px;font-weight:600;color:#059669;">(24.4%)</span></div>
                            <div style="font-size:11px;color:#64748B;margin-top:2px;">Rinku Singh (Priority 1)</div>
                        </div>
                        <div style="padding:10px 12px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:6px;">
                            <div style="font-size:10.5px;font-weight:700;color:#64748B;text-transform:uppercase;">Pace Spearheads</div>
                            <div style="font-size:15px;font-weight:800;color:#111827;margin-top:2px;">&#8377;11.00 Cr <span style="font-size:11px;font-weight:600;color:#059669;">(24.4%)</span></div>
                            <div style="font-size:11px;color:#64748B;margin-top:2px;">Duffy (&#8377;6.5) + Shepherd (&#8377;4.5)</div>
                        </div>
                        <div style="padding:10px 12px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:6px;">
                            <div style="font-size:10.5px;font-weight:700;color:#64748B;text-transform:uppercase;">Mystery Spin Choke</div>
                            <div style="font-size:15px;font-weight:800;color:#111827;margin-top:2px;">&#8377;5.50 Cr <span style="font-size:11px;font-weight:600;color:#059669;">(12.2%)</span></div>
                            <div style="font-size:11px;color:#64748B;margin-top:2px;">Varun Chakravarthy</div>
                        </div>
                    </div>
                </div>

                <!-- 3. War Room Strategic Principles -->
                <div style="margin-top:16px;padding:16px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                    <div style="font-weight:700;font-size:12.5px;color:#111827;margin-bottom:6px;">
                        War Room Principles &bull; IPL 2027 Auction
                    </div>
                    <ul style="margin:0;padding-left:16px;font-size:12px;color:#374151;line-height:1.55;">
                        <li><strong>No Emotional Marquee Bidding:</strong> Resist brand-driven inflation on marquee names whose clutch win differential is negative.</li>
                        <li><strong>Jaipur SMS Fortress Fit:</strong> Prioritize players suited to 75m+ boundaries and middle-overs spin grip over generic power hitters.</li>
                        <li><strong>Strict 2+2 Overseas Structure:</strong> Exactly 2 overseas in Starting XI (Conway, Hazlewood) and 2 impact covers (Duffy, Hetmyer).</li>
                        <li><strong>10% Circuit Breaker:</strong> The instant any player exceeds 10% above max valuation, immediately execute step-down contingency.</li>
                    </ul>
                </div>
            </div>'''

if old_rule_block in code:
    code = code.replace(old_rule_block, new_expanded_right_col, 1)
    print("SUCCESS: Expanded right column with Contingency Matrix, Phase Breakdown, and War Room Principles!")
else:
    print("ERROR: old_rule_block not found!")

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Saved updated fix_dashboard_and_wagon.py!")

