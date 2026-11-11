import re

with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Ensure NO 'kami' anywhere in fix_dashboard_and_wagon.py
text = re.sub(r'\(Kami\s*/\s*Shortcoming\)', '(Strategic Assessment)', text, flags=re.IGNORECASE)
text = re.sub(r'Kami\s*/\s*Shortcoming', 'Strategic Assessment', text, flags=re.IGNORECASE)
text = re.sub(r'\bKami\b', 'Shortcoming', text, flags=re.IGNORECASE)

# 2. Make sure .tactical-grid has align-items: start;
text = re.sub(
    r'\.tactical-grid\s*\{[^}]+\}',
    """.tactical-grid {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 24px;
            margin-bottom: 24px;
            align-items: start;
        }""",
    text
)

# 3. Check section-tactical-xi in fix_dashboard_and_wagon.py
# Move Phase-by-Phase and War Room Principles into a balanced 2-column grid right after .tactical-grid
# First find where the right column ends in tactical-grid
old_right_end = """                <!-- 2. Phase-by-Phase Purse Distribution Grid -->
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
            </div>
        </div>"""

new_right_end = """            </div>
        </div>

        <!-- Strategic War Room Principles & Phase Distribution (Balanced 2-Column Row) -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:24px;align-items:start;">
            <!-- Phase-by-Phase Purse Distribution Grid -->
            <div class="tactical-card">
                <div class="tactical-card-title">
                    Phase-by-Phase Purse Distribution (&#8377;45.0 Cr Total)
                </div>
                <div class="tactical-card-sub">
                    Balanced allocation preventing over-commitment in any single game phase.
                </div>
                <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:12px;">
                    <div style="padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                        <div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;">Middle Spin Attack</div>
                        <div style="font-size:16px;font-weight:800;color:#111827;margin-top:2px;">&#8377;17.50 Cr <span style="font-size:11.5px;font-weight:700;color:#059669;">(38.9%)</span></div>
                        <div style="font-size:11.5px;color:#64748B;margin-top:4px;">Dube (&#8377;9.5) + Axar (&#8377;8.0)</div>
                    </div>
                    <div style="padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                        <div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;">Death Finishing</div>
                        <div style="font-size:16px;font-weight:800;color:#111827;margin-top:2px;">&#8377;11.00 Cr <span style="font-size:11.5px;font-weight:700;color:#059669;">(24.4%)</span></div>
                        <div style="font-size:11.5px;color:#64748B;margin-top:4px;">Rinku Singh (Priority 1)</div>
                    </div>
                    <div style="padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                        <div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;">Pace Spearheads</div>
                        <div style="font-size:16px;font-weight:800;color:#111827;margin-top:2px;">&#8377;11.00 Cr <span style="font-size:11.5px;font-weight:700;color:#059669;">(24.4%)</span></div>
                        <div style="font-size:11.5px;color:#64748B;margin-top:4px;">Duffy (&#8377;6.5) + Shepherd (&#8377;4.5)</div>
                    </div>
                    <div style="padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                        <div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;">Mystery Spin Choke</div>
                        <div style="font-size:16px;font-weight:800;color:#111827;margin-top:2px;">&#8377;5.50 Cr <span style="font-size:11.5px;font-weight:700;color:#059669;">(12.2%)</span></div>
                        <div style="font-size:11.5px;color:#64748B;margin-top:4px;">Varun Chakravarthy</div>
                    </div>
                </div>
            </div>

            <!-- War Room Strategic Principles -->
            <div class="tactical-card">
                <div class="tactical-card-title">
                    War Room Principles &bull; IPL 2027 Auction
                </div>
                <div class="tactical-card-sub">
                    Core operational disciplines governing every auction call.
                </div>
                <ul style="margin:0;padding-left:18px;font-size:12.5px;color:#374151;line-height:1.65;">
                    <li style="margin-bottom:6px;"><strong>No Emotional Marquee Bidding:</strong> Resist brand-driven inflation on marquee names whose clutch win differential is negative.</li>
                    <li style="margin-bottom:6px;"><strong>Jaipur SMS Fortress Fit:</strong> Prioritize players suited to 75m+ boundaries and middle-overs spin grip over generic power hitters.</li>
                    <li style="margin-bottom:6px;"><strong>Strict 2+2 Overseas Structure:</strong> Exactly 2 overseas in Starting XI (Conway, Hazlewood) and 2 impact covers (Duffy, Hetmyer).</li>
                    <li><strong>10% Circuit Breaker:</strong> The instant any player exceeds 10% above max valuation, immediately execute step-down contingency.</li>
                </ul>
            </div>
        </div>"""

if old_right_end in text:
    text = text.replace(old_right_end, new_right_end)
    print("✓ Successfully restructured right column into balanced 2-column middle row!")
else:
    print("old_right_end not found exactly, searching with normalized whitespace")
    # let's try replacing based on comments
    pos_phase = text.find('<!-- 2. Phase-by-Phase Purse')
    pos_end_tactical = text.find('</div>\n        </div>\n\n        <!-- Bottom Card:', pos_phase)
    if pos_phase != -1 and pos_end_tactical != -1:
        text = text[:pos_phase] + new_right_end + text[pos_end_tactical+len('</div>\n        </div>'):]
        print("✓ Successfully spliced new layout!")

with open('fix_dashboard_and_wagon.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved fix_dashboard_and_wagon.py")

