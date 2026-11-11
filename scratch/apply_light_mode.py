# Script to rewrite section-tactical-xi and related styles in fix_dashboard_and_wagon.py
import re

with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Target start of section-tactical-xi to end of doc-grid
start_target = '    <!-- IPL 2027 Rajasthan Royals Tactical Squad & Auction Strategy Section -->'
end_target = '<!-- Interactive Power BI Slicer & Sort Logic -->'

start_idx = content.find(start_target)
end_idx = content.find(end_target)

if start_idx == -1 or end_idx == -1:
    print(f"Error: indices not found. start={start_idx}, end={end_idx}")
    exit(1)

new_section_html = """    <!-- IPL 2027 Rajasthan Royals Tactical Squad & Auction Strategy Section -->
    <div id="section-tactical-xi" class="data-section" style="display:none;margin-top:16px;">
        
        <div class="tactical-grid">
            <!-- Left Column: Playing XI Formation & Lineup -->
            <div class="tactical-card">
                <div class="tactical-card-title">
                    Rajasthan Royals &mdash; Recommended 2027 Playing XI
                </div>
                <div class="tactical-card-sub">
                    A balanced 11-man lineup calibrated to dominate middle-overs spin and close out death overs under high match pressure.
                </div>
                
                <!-- Pure Clean Light Mode Starting XI Blueprint -->
                <div class="xi-blueprint-container">
                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Top-Order Anchors (Overs 1&ndash;6)</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" onclick="window.location.href='players/yashasvi_jaiswal.html'">
                                <div class="xi-num">1</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Yashasvi Jaiswal</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Left-Hand Explosive Opener &bull; Powerplay Strike Rate 165+</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" onclick="window.location.href='players/devon_conway.html'">
                                <div class="xi-num">2</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Devon Conway</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">LHB Top-Order Anchor &amp; WK &bull; 64.3% Pressure Win Rate (+18.1% Lift)</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" onclick="window.location.href='players/sanju_samson.html'">
                                <div class="xi-num">3</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Sanju Samson <span style="font-size:11px;color:var(--rr-pink);font-weight:700;">(C)</span></span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Captain &amp; No. 3 Pace/Spin Attacker &bull; Proven Match-Winner</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Middle-Overs Engine &amp; Spin Enforcers (Overs 7&ndash;15)</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" onclick="window.location.href='players/shivam_dube.html'">
                                <div class="xi-num">4</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Shivam Dube</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Designated Spin Demolisher &bull; 66.7% Pressure Win Rate (+12.4% Lift)</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" onclick="window.location.href='players/riyan_parag.html'">
                                <div class="xi-num">5</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Riyan Parag</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Middle-Order Striker &amp; Leg-Spin Option &bull; SMS Fortress Anchor</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" onclick="window.location.href='players/dhruv_jurel.html'">
                                <div class="xi-num">6</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Dhruv Jurel <span style="font-size:11px;color:var(--text-muted);font-weight:600;">(WK)</span></span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Clutch Middle-Order Finisher &bull; Elite Death-Over Temperament</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Death-Overs Power Finishers (Overs 16&ndash;20)</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" onclick="window.location.href='players/rinku_singh.html'">
                                <div class="xi-num">7</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Rinku Singh</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Specialist Death Finisher &bull; 69.2% Pressure Win Rate across 26 High-Leverage Games</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" onclick="window.location.href='players/shimron_hetmyer.html'">
                                <div class="xi-num">8</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Shimron Hetmyer</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Overseas Power Finisher &bull; Fearless Boundary Striking in Final 3 Overs</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="xi-phase-group">
                        <div class="xi-phase-title">Bowling Spearheads &amp; Seam Defense</div>
                        <div class="xi-player-grid">
                            <div class="xi-player-pill" onclick="window.location.href='players/josh_hazlewood.html'">
                                <div class="xi-num">9</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Josh Hazlewood</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Frontline Seam Spearhead &bull; 78.6% Pressure Win Rate (+14.9% Lift)</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" onclick="window.location.href='players/sandeep_sharma.html'">
                                <div class="xi-num">10</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Sandeep Sharma</span>
                                        <span class="xi-badge xi-retained">Retained Core</span>
                                    </div>
                                    <div class="xi-role">Death Yorker &amp; Wide-Line Master &bull; Reliable Execution in Final 2 Overs</div>
                                </div>
                            </div>

                            <div class="xi-player-pill" onclick="window.location.href='players/yash_dayal.html'">
                                <div class="xi-num">11</div>
                                <div class="xi-info">
                                    <div class="xi-name-row">
                                        <span class="xi-name">Yash Dayal</span>
                                        <span class="xi-badge xi-target">Auction Target</span>
                                    </div>
                                    <div class="xi-role">Left-Arm Seam Specialist &bull; 80.0% Pressure Win Rate (+10.2% Lift)</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Tactical Impact Subs & Bench -->
                    <div class="xi-bench-box">
                        <div class="xi-bench-lbl">Tactical Impact Substitutes &amp; Matchup Covers:</div>
                        <div class="xi-bench-pills">
                            <span class="bench-pill" onclick="window.location.href='players/jacob_duffy.html'"><strong>Jacob Duffy</strong> (Pace &bull; +20.5% Lift)</span>
                            <span class="bench-pill" onclick="window.location.href='players/axar_patel.html'"><strong>Axar Patel</strong> (Spin All-Rounder &bull; +7.8% Lift)</span>
                            <span class="bench-pill" onclick="window.location.href='players/varun_chakravarthy.html'"><strong>Varun Chakravarthy</strong> (Mystery Spin &bull; 100% Playoff WR)</span>
                            <span class="bench-pill" onclick="window.location.href='players/rajat_patidar.html'"><strong>Rajat Patidar</strong> (No. 3 Cover &bull; +11.1% Lift)</span>
                        </div>
                    </div>
                </div>

                <!-- Playing XI Win Conversion Table -->
                <table class="purse-table" style="margin-top:16px;">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Player</th>
                            <th>Role in Team</th>
                            <th style="text-align:right;">Normal Win%</th>
                            <th style="text-align:right;">Pressure Win%</th>
                            <th style="text-align:center;">Win Difference</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr onclick="window.location.href='players/devon_conway.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);">1</td>
                            <td><strong>Devon Conway</strong> <span style="font-size:11px;color:var(--text-muted);">(wk)</span></td>
                            <td>Top-Order Anchor & Wicketkeeper</td>
                            <td style="text-align:right;color:var(--text-muted);">46.2%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);">64.3%</td>
                            <td style="text-align:center;"><span class="diff-tag diff-pos">+18.1%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/ruturaj_gaikwad.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);">2</td>
                            <td><strong>Ruturaj Gaikwad</strong></td>
                            <td>Opening Batter & Inning Pacer</td>
                            <td style="text-align:right;color:var(--text-muted);">50.6%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);">57.1%</td>
                            <td style="text-align:center;"><span class="diff-tag diff-pos">+6.5%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/rajat_patidar.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);">3</td>
                            <td><strong>Rajat Patidar</strong></td>
                            <td>No. 3 Anchor & Spin Attacker</td>
                            <td style="text-align:right;color:var(--text-muted);">60.3%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);">71.4%</td>
                            <td style="text-align:center;"><span class="diff-tag diff-pos">+11.1%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/shivam_dube.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);">4</td>
                            <td><strong>Shivam Dube</strong></td>
                            <td>Middle-Overs Boundary Hitter vs Spin (Overs 7&ndash;15)</td>
                            <td style="text-align:right;color:var(--text-muted);">54.3%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);">66.7%</td>
                            <td style="text-align:center;"><span class="diff-tag diff-pos">+12.4%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/shreyas_iyer.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);">5</td>
                            <td><strong>Shreyas Iyer</strong> <span style="font-size:11px;color:var(--rr-pink);font-weight:700;">(c)</span></td>
                            <td>Middle-Order Game Manager & Captain</td>
                            <td style="text-align:right;color:var(--text-muted);">54.5%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);">55.6%</td>
                            <td style="text-align:center;"><span class="diff-tag diff-pos">+1.1%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/rinku_singh.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);">6</td>
                            <td><strong>Rinku Singh</strong></td>
                            <td>Designated Death Finisher (Overs 16&ndash;20)</td>
                            <td style="text-align:right;color:var(--text-muted);">63.8%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);">69.2%</td>
                            <td style="text-align:center;"><span class="diff-tag diff-pos">+5.4%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/axar_patel.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);">7</td>
                            <td><strong>Axar Patel</strong></td>
                            <td>Spin All-Rounder & Late-Overs Hitter</td>
                            <td style="text-align:right;color:var(--text-muted);">56.5%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);">64.3%</td>
                            <td style="text-align:center;"><span class="diff-tag diff-pos">+7.8%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/romario_shepherd.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);">8</td>
                            <td><strong>Romario Shepherd</strong></td>
                            <td>Pace All-Rounder & Heavy-Ball Bowler</td>
                            <td style="text-align:right;color:var(--text-muted);">49.0%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);">56.0%</td>
                            <td style="text-align:center;"><span class="diff-tag diff-pos">+7.0%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/mitchell_starc.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);">9</td>
                            <td><strong>Mitchell Starc</strong></td>
                            <td>Left-Arm Fast Bowler (Powerplay & Death)</td>
                            <td style="text-align:right;color:var(--text-muted);">68.3%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);">60.0%</td>
                            <td style="text-align:center;"><span class="diff-tag" style="background:#FEF3C7;color:#92400E;">3 Awards</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/varun_chakravarthy.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);">10</td>
                            <td><strong>Varun Chakravarthy</strong></td>
                            <td>Mystery Spinner (Middle Overs)</td>
                            <td style="text-align:right;color:var(--text-muted);">58.6%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);">61.9%</td>
                            <td style="text-align:center;"><span class="diff-tag diff-pos">+3.3%</span></td>
                        </tr>
                        <tr onclick="window.location.href='players/jacob_duffy.html'" style="cursor:pointer;">
                            <td style="font-weight:700;color:var(--rr-navy);">11</td>
                            <td><strong>Jacob Duffy</strong></td>
                            <td>Accurate Swing & Seam Bowler</td>
                            <td style="text-align:right;color:var(--text-muted);">54.5%</td>
                            <td style="text-align:right;font-weight:700;color:var(--success);">75.0%</td>
                            <td style="text-align:center;"><span class="diff-tag diff-pos">+20.5%</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Right Column: Auction Valuation Model & Purse Allocation -->
            <div class="tactical-card">
                <div class="tactical-card-title">
                    Auction Budget Plan (&#8377;45 Crore Total Purse)
                </div>
                <div class="tactical-card-sub">
                    Disciplined bidding caps to prevent emotional overspending on marquee names.
                </div>

                <div class="budget-kpi-bar">
                    <div>
                        <div class="budget-kpi-val">&#8377;45.0 Cr</div>
                        <div class="budget-kpi-lbl">Total Budget</div>
                    </div>
                    <div>
                        <div class="budget-kpi-val" style="color:var(--success);">&#8377;45.0 Cr</div>
                        <div class="budget-kpi-lbl">Target Allocations</div>
                    </div>
                    <div>
                        <div class="budget-kpi-val" style="color:var(--rr-pink);">100%</div>
                        <div class="budget-kpi-lbl">Budget Utilized</div>
                    </div>
                </div>

                <table class="purse-table">
                    <thead>
                        <tr>
                            <th>Target Player</th>
                            <th>Priority</th>
                            <th style="text-align:right;">Max Bid</th>
                            <th style="text-align:right;">% of Purse</th>
                            <th>Why Rajasthan Royals Needs Him</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr onclick="window.location.href='players/rinku_singh.html'" style="cursor:pointer;">
                            <td><strong>Rinku Singh</strong></td>
                            <td><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);">&#8377;11.00 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);">24.4%</td>
                            <td style="font-size:12px;">Proven death finisher; finishes tight chases with calm execution (69.2% win rate).</td>
                        </tr>
                        <tr onclick="window.location.href='players/shivam_dube.html'" style="cursor:pointer;">
                            <td><strong>Shivam Dube</strong></td>
                            <td><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);">&#8377;9.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);">21.1%</td>
                            <td style="font-size:12px;">Destroys spin bowling in overs 7&ndash;15; prevents scoring slowdowns in middle overs.</td>
                        </tr>
                        <tr onclick="window.location.href='players/axar_patel.html'" style="cursor:pointer;">
                            <td><strong>Axar Patel</strong></td>
                            <td><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);">&#8377;8.00 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);">17.8%</td>
                            <td style="font-size:12px;">Gives batting depth at No. 7 and bowls tight 4 overs of left-arm spin.</td>
                        </tr>
                        <tr onclick="window.location.href='players/jacob_duffy.html'" style="cursor:pointer;">
                            <td><strong>Jacob Duffy</strong></td>
                            <td><span class="tier-badge tier-1">Priority 1</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);">&#8377;6.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);">14.4%</td>
                            <td style="font-size:12px;">Top bowler in high-pressure matches (+20.5% lift, 75.0% win rate); disciplined swing.</td>
                        </tr>
                        <tr onclick="window.location.href='players/varun_chakravarthy.html'" style="cursor:pointer;">
                            <td><strong>Varun Chakravarthy</strong></td>
                            <td><span class="tier-badge tier-2">Priority 2</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);">&#8377;5.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);">12.2%</td>
                            <td style="font-size:12px;">Takes wickets in middle overs; 100% win rate in playoff knockout games.</td>
                        </tr>
                        <tr onclick="window.location.href='players/romario_shepherd.html'" style="cursor:pointer;">
                            <td><strong>Romario Shepherd</strong></td>
                            <td><span class="tier-badge tier-2">Priority 2</span></td>
                            <td style="text-align:right;font-weight:700;color:var(--rr-navy);">&#8377;4.50 Cr</td>
                            <td style="text-align:right;color:var(--text-muted);">10.0%</td>
                            <td style="font-size:12px;">Fast bowling option with heavy ball and power-hitting down the order.</td>
                        </tr>
                    </tbody>
                </table>

                <div style="margin-top:20px;padding:14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;">
                    <div style="font-weight:700;font-size:12.5px;color:var(--rr-navy);margin-bottom:4px;">Auction Bidding Rule:</div>
                    <p style="font-size:12px;color:var(--text-main);line-height:1.5;margin:0;">
                        If bidding for any player goes more than 10% above their maximum limit, stop bidding immediately and switch to backup targets (such as Yash Dayal at &#8377;5.5 Cr or Bhanuka Rajapaksa at &#8377;3.5 Cr) to protect the overall team budget.
                    </p>
                </div>
            </div>
        </div>

        <!-- Bottom Card: Clean Light Mode Pressure Lift Quadrant Matrix -->
        <div class="tactical-card" style="margin-top:24px;">
            <div class="tactical-card-title">
                Pressure Win Rate vs Normal Win Rate (Player Quadrant Classification)
            </div>
            <div class="tactical-card-sub">
                Separates authentic match-deciding performers from baseline franchise strength across all players evaluated.
            </div>

            <div style="display:grid;grid-template-columns:1.2fr 0.8fr;gap:24px;">
                <!-- 4 Quadrants Visual Grid in Light Mode -->
                <div class="quadrant-light-grid">
                    <div class="quadrant-box q-box-1">
                        <div class="q-tag q-tag-green">Quadrant I &bull; High Pressure Match-Winners</div>
                        <div class="q-desc">Significant positive win lift in tight finishes and playoff knockouts:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Shivam Dube</strong> (+12.4% Lift)</span>
                            <span class="q-pill"><strong>Jacob Duffy</strong> (+20.5% Lift)</span>
                            <span class="q-pill"><strong>Rinku Singh</strong> (+5.4% Lift)</span>
                        </div>
                    </div>

                    <div class="quadrant-box q-box-2">
                        <div class="q-tag q-tag-blue">Quadrant II &bull; Consistent High Anchors</div>
                        <div class="q-desc">Consistently high win conversion across both normal and close games:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Devon Conway</strong> (64.3% HP WR)</span>
                            <span class="q-pill"><strong>Rajat Patidar</strong> (71.4% HP WR)</span>
                            <span class="q-pill"><strong>Axar Patel</strong> (64.3% HP WR)</span>
                        </div>
                    </div>

                    <div class="quadrant-box q-box-3">
                        <div class="q-tag q-tag-amber">Quadrant III &bull; Situational Aggressors</div>
                        <div class="q-desc">High strike rates that provide sudden momentum shifts in run chases:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Bhanuka Rajapaksa</strong> (168.4 SR)</span>
                            <span class="q-pill"><strong>Romario Shepherd</strong> (182.1 SR)</span>
                            <span class="q-pill"><strong>Sediqullah Atal</strong> (152.0 SR)</span>
                        </div>
                    </div>

                    <div class="quadrant-box q-box-4">
                        <div class="q-tag q-tag-navy">Quadrant IV &bull; Defensive Superstars</div>
                        <div class="q-desc">Elite containment; opponents take zero risks, lowering their individual win-lift delta:</div>
                        <div class="q-players">
                            <span class="q-pill"><strong>Jasprit Bumrah</strong> (7.4 Death Econ)</span>
                            <span class="q-pill"><strong>Rashid Khan</strong> (6.8 Mid Econ)</span>
                        </div>
                    </div>
                </div>

                <!-- Insights Column -->
                <div>
                    <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:18px;">
                        <div style="font-weight:700;color:var(--rr-navy);font-size:13px;margin-bottom:12px;">Strategic Takeaways for Rajasthan Royals:</div>
                        
                        <div style="margin-bottom:12px;">
                            <strong style="color:var(--rr-navy);font-size:12px;">1. Solves the Middle-Overs Slowdown:</strong>
                            <p style="font-size:12px;color:var(--text-main);margin:2px 0 0 0;line-height:1.4;">
                                Target signing <strong>Shivam Dube</strong> (+12.4% lift) gives Rajasthan Royals the required spin boundary enforcer to partner Samson and Parag.
                            </p>
                        </div>

                        <div style="margin-bottom:12px;">
                            <strong style="color:var(--rr-navy);font-size:12px;">2. Fortress Sawai Mansingh Fit:</strong>
                            <p style="font-size:12px;color:var(--text-main);margin:2px 0 0 0;line-height:1.4;">
                                Jaipur's large 75m+ boundary requires elite runners and tactical anchors like <strong>Devon Conway</strong> and <strong>Axar Patel</strong> who maintain low dot-ball percentages.
                            </p>
                        </div>

                        <div style="margin-bottom:12px;">
                            <strong style="color:var(--rr-navy);font-size:12px;">3. Guaranteed Death Overs Defense:</strong>
                            <p style="font-size:12px;color:var(--text-main);margin:2px 0 0 0;line-height:1.4;">
                                Pairing <strong>Josh Hazlewood</strong> with retained yorker specialist <strong>Sandeep Sharma</strong> guarantees 4 disciplined death overs under 9.0 RPO.
                            </p>
                        </div>

                        <div>
                            <strong style="color:var(--rr-navy);font-size:12px;">4. Bidding Discipline:</strong>
                            <p style="font-size:12px;color:var(--text-main);margin:2px 0 0 0;line-height:1.4;">
                                A hard cap of &#8377;11.0 Cr for any single target prevents auction inflation from ruining squad depth.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- Quantitative Framework Documentation in Clean Light Mode -->
    <div class="doc-grid">
        <div class="doc-box">
            <div class="doc-heading">Quantitative Model Formulation</div>
            <p style="font-size:12.5px;color:#475569;margin-bottom:8px;">
                The Clutch Player Performance Index (CPPI) addresses small-sample statistical variance via Bayesian shrinkage estimation:
            </p>
            <div class="code-snippet">
                CPPI = [ 0.35 &times; WR_hp + 0.15 &times; WR_base + 0.20 &times; &Delta; + 0.15 &times; MOM_hp + 0.15 &times; WR_ko ] &times; Saturation
            </div>
            <p style="font-size:12px;color:#64748B;line-height:1.5;">
                Where Saturation = min(1.0, Matches_hp / 10.0), guaranteeing that candidates with insufficient high-leverage samples are penalised in final ranking calculations.
            </p>
        </div>

        <div class="doc-box">
            <div class="doc-heading">Operational Definitions & Data Governance</div>
            <p style="font-size:12.5px;color:#475569;line-height:1.6;">
                <strong style="color:var(--rr-navy);">1. High-Leverage Fixture:</strong> Matches meeting stern empirical pressure criteria: elimination knockout games (Finals, Semi-Finals, Eliminators), super-over resolutions, or finishes with winning margins &le; 15 runs or &le; 2 wickets.<br>
                <strong style="color:var(--rr-navy);">2. Regulatory Pre-Filter:</strong> Strict exclusion of non-auction eligible entities pursuant to BCCI IPL Player Regulations.<br>
                <strong style="color:var(--rr-navy);">3. Tactical Venue Model:</strong> Sawai Mansingh Stadium pitch metrics (72-78m boundaries, middle-overs spin grip, nocturnal dew factor).
            </p>
        </div>
    </div>

</div>

"""

# Perform replacement of the tactical and doc section
content = content[:start_idx] + new_section_html + content[end_idx:]

# 2. Update CSS in fix_dashboard_and_wagon.py
new_css = """
        .tactical-grid {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 24px;
            margin-bottom: 24px;
        }
        @media (max-width: 1024px) {
            .tactical-grid {
                grid-template-columns: 1fr;
            }
        }

        .tactical-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 20px rgba(0, 29, 72, 0.05);
        }

        .tactical-card-title {
            font-size: 16px;
            font-weight: 800;
            color: var(--rr-navy);
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
            letter-spacing: -0.2px;
        }

        .tactical-card-sub {
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 18px;
            line-height: 1.4;
        }

        /* Clean Light Mode Playing XI Blueprint */
        .xi-blueprint-container {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 18px;
        }
        .xi-phase-group {
            margin-bottom: 14px;
        }
        .xi-phase-group:last-child {
            margin-bottom: 0;
        }
        .xi-phase-title {
            font-size: 11px;
            font-weight: 800;
            color: var(--rr-navy);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 8px;
            padding-left: 2px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .xi-player-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 8px;
        }
        .xi-player-pill {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 8px 12px;
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .xi-player-pill:hover {
            border-color: var(--rr-pink);
            box-shadow: 0 2px 8px rgba(0, 29, 72, 0.08);
            transform: translateY(-1px);
        }
        .xi-num {
            font-size: 13px;
            font-weight: 800;
            color: var(--rr-navy);
            width: 24px;
            height: 24px;
            background: #F1F5F9;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        .xi-info {
            flex: 1;
            min-width: 0;
        }
        .xi-name-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }
        .xi-name {
            font-size: 13px;
            font-weight: 700;
            color: var(--rr-navy);
        }
        .xi-badge {
            font-size: 9.5px;
            font-weight: 800;
            padding: 1px 6px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            white-space: nowrap;
        }
        .xi-retained {
            background: #EFF6FF;
            color: #1E40AF;
            border: 1px solid #BFDBFE;
        }
        .xi-target {
            background: #FDF2F8;
            color: #BE185D;
            border: 1px solid #FBCFE8;
        }
        .xi-role {
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .xi-bench-box {
            margin-top: 14px;
            padding: 10px 12px;
            background: #FFFFFF;
            border: 1px dashed #CBD5E1;
            border-radius: 8px;
        }
        .xi-bench-lbl {
            font-size: 10.5px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        .xi-bench-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        .bench-pill {
            display: inline-block;
            background: #F1F5F9;
            border: 1px solid #E2E8F0;
            border-radius: 4px;
            padding: 3px 8px;
            font-size: 11px;
            color: var(--text-main);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .bench-pill:hover {
            border-color: var(--rr-pink);
            background: #FFFFFF;
        }

        /* Light Mode Quadrants Grid */
        .quadrant-light-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        @media (max-width: 768px) {
            .quadrant-light-grid {
                grid-template-columns: 1fr;
            }
        }
        .quadrant-box {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 14px;
        }
        .q-box-1 { border-left: 4px solid #059669; }
        .q-box-2 { border-left: 4px solid #0284C7; }
        .q-box-3 { border-left: 4px solid #D97706; }
        .q-box-4 { border-left: 4px solid #001D48; }
        .q-tag {
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .q-tag-green { color: #059669; }
        .q-tag-blue { color: #0284C7; }
        .q-tag-amber { color: #D97706; }
        .q-tag-navy { color: #001D48; }
        .q-desc {
            font-size: 11.5px;
            color: var(--text-muted);
            margin-bottom: 8px;
            line-height: 1.35;
        }
        .q-players {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .q-pill {
            font-size: 11px;
            color: var(--text-main);
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 4px;
            padding: 3px 8px;
        }

        .purse-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }
        .purse-table th {
            background: #F1F5F9;
            color: var(--rr-navy);
            padding: 9px 12px;
            font-weight: 700;
            text-align: left;
            border-bottom: 2px solid #CBD5E1;
        }
        .purse-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #E2E8F0;
            vertical-align: middle;
        }
        .purse-table tr:hover {
            background: #F8FAFC;
        }
        .tier-badge {
            display: inline-block;
            font-size: 10px;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .tier-1 { background: rgba(235, 26, 141, 0.12); color: var(--rr-pink); border: 1px solid rgba(235, 26, 141, 0.3); }
        .tier-2 { background: rgba(0, 29, 72, 0.08); color: var(--rr-navy); border: 1px solid rgba(0, 29, 72, 0.2); }

        .budget-kpi-bar {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 18px;
            text-align: center;
        }
        .budget-kpi-val {
            font-size: 18px;
            font-weight: 800;
            color: var(--rr-navy);
            font-variant-numeric: tabular-nums;
        }
        .budget-kpi-lbl {
            font-size: 10.5px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 2px;
        }

        /* Light Mode Documentation Boxes */
        .doc-box {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px;
            padding: 22px 24px;
            box-shadow: 0 4px 16px rgba(0, 29, 72, 0.04) !important;
        }
        .doc-heading {
            color: var(--rr-navy) !important;
            font-size: 14px;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .code-snippet {
            background: #F8FAFC !important;
            border: 1px solid #CBD5E1 !important;
            color: #0F172A !important;
            padding: 8px 12px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 12px;
            margin: 8px 0;
        }
"""

# Replace the injected CSS at the end of fix_dashboard_and_wagon.py
css_start = content.find('.tactical-grid {')
if css_start != -1:
    css_end = content.find('""" + \'\\n</style>\', 1)', css_start)
    if css_end != -1:
        content = content[:css_start] + new_css.strip() + '\n' + content[css_end:]

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated fix_dashboard_and_wagon.py!")

