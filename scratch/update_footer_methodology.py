import re

NEW_FOOTER_HTML = """    <!-- Executive Analyst Footer: Methodology, Thought Process & Verified Credentials -->
    <footer class="analyst-footer" style="margin-top:36px;margin-bottom:24px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:26px 30px;box-shadow:0 4px 20px rgba(0,29,72,0.04);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
        
        <!-- Top Row: Methodology & Analyst Thought Process -->
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));gap:20px;margin-bottom:22px;padding-bottom:22px;border-bottom:1px solid #E2E8F0;">
            <!-- Column 1: Methodology -->
            <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:18px 20px;">
                <div style="font-size:12px;font-weight:800;color:#111827;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid #E2E8F0;">
                    1. Selection Methodology &amp; Scoring Model
                </div>
                <div style="font-size:12.5px;color:#374151;line-height:1.6;">
                    <p style="margin:0 0 8px 0;">
                        <strong style="color:#111827;">Pressure Match Definition:</strong> Evaluated 883 IPL &amp; T20I fixtures (2022&ndash;2026). Only 174 matches qualified as high-pressure: tournament knockouts (Finals, Semi-Finals, Playoffs), Super Overs, or close finishes (&le;15 runs or &le;2 wickets).
                    </p>
                    <p style="margin:0 0 8px 0;">
                        <strong style="color:#111827;">CPPI Formula:</strong> Combines High-Pressure Win Rate (35%), True Pressure Lift &Delta; (20%), Career Baseline Win Rate (15%), High-Pressure POTM Awards (15%), and Knockout Win Rate (15%).
                    </p>
                    <p style="margin:0;">
                        <strong style="color:#111827;">Fair Sample Protection:</strong> Multiplied by a saturation factor min(1.0, HP Matches / 10) so players with small sample sizes cannot rank artificially high, alongside strict BCCI IPL eligibility and role separation.
                    </p>
                </div>
            </div>

            <!-- Column 2: Analyst Thought Process -->
            <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:18px 20px;">
                <div style="font-size:12px;font-weight:800;color:#111827;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid #E2E8F0;">
                    2. My Thought Process &amp; Auction Logic
                </div>
                <div style="font-size:12.5px;color:#374151;line-height:1.6;">
                    <p style="margin:0 0 8px 0;">
                        <strong style="color:#111827;">Look Beyond Reputation &amp; Averages:</strong> Standard batting averages and total wickets reward comfortable runs in one-sided games. At an IPL auction, paying &ge;15 Cr for fame often hurts squad balance when matches get tight.
                    </p>
                    <p style="margin:0 0 8px 0;">
                        <strong style="color:#111827;">Measure Who Lifts the Team (&Delta;):</strong> My core goal was to see whose win rate rises under stress compared to normal games. That explains why Shivam Dube (+12.4%) and Jacob Duffy (+20.5%) outrank superstars whose lift turns negative when opponents tactically play them out or exploit death-over variance.
                    </p>
                    <p style="margin:0;">
                        <strong style="color:#111827;">Built for Sawai Mansingh Stadium:</strong> Analytics only win trophies when fit to team needs. Every selection addresses RR&rsquo;s Jaipur priorities: hitting middle-overs spin across 75m boundaries (Overs 7&ndash;15) and executing disciplined seam in night dew within a &#8377;45 Cr budget.
                    </p>
                </div>
            </div>
        </div>

        <!-- Middle Row: Author Bio & Identity -->
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:16px;padding-bottom:18px;margin-bottom:18px;border-bottom:1px solid #F1F5F9;">
            <div>
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                    <span style="display:inline-block;width:9px;height:9px;background:var(--rr-pink, #E91E8C);border-radius:50%;"></span>
                    <h3 style="margin:0;font-size:16.5px;font-weight:800;color:#111827;letter-spacing:0.2px;">Ketan Rawat</h3>
                    <span style="font-size:11px;font-weight:700;color:#059669;background:#ECFDF5;border:1px solid #A7F3D0;padding:2px 8px;border-radius:12px;">SupeRR Selector Season 1 &bull; Top 20 Finalist</span>
                </div>
                <div style="font-size:12px;color:#64748B;line-height:1.5;">
                    Principal Quantitative Analyst &bull; Rajasthan Royals SupeRR Selector Strategy Architecture
                </div>
            </div>
            <div style="font-size:11.5px;color:#94A3B8;text-align:right;">
                BCCI IPL 2027 Mega-Auction Model &bull; 883 Fixtures Calibrated
            </div>
        </div>

        <!-- Bottom Row: Credentials & Portfolio Grid -->
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(230px, 1fr));gap:12px;">
            <!-- LinkedIn Profile -->
            <a href="https://www.linkedin.com/in/ketan-rawat-97a8aa2a0/" target="_blank" rel="noopener noreferrer" 
               style="display:flex;align-items:center;gap:12px;padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;text-decoration:none;transition:all 0.15s ease;"
               onmouseover="this.style.borderColor='var(--rr-pink, #E91E8C)';this.style.transform='translateY(-1px)';this.style.boxShadow='0 3px 10px rgba(0,0,0,0.05)';"
               onmouseout="this.style.borderColor='#E2E8F0';this.style.transform='none';this.style.boxShadow='none';">
                <div style="width:34px;height:34px;border-radius:8px;background:#0A66C2;display:flex;align-items:center;justify-content:center;color:#FFFFFF;flex-shrink:0;">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.2V10.9H6.46M7.83 6.2a1.66 1.66 0 0 0-1.66 1.66c0 .92.74 1.66 1.66 1.66.92 0 1.66-.74 1.66-1.66 0-.92-.74-1.66-1.66-1.66Z"/></svg>
                </div>
                <div style="min-width:0;">
                    <div style="font-size:12.5px;font-weight:700;color:#111827;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">LinkedIn Profile</div>
                    <div style="font-size:11px;color:#64748B;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">ketan-rawat-97a8aa2a0</div>
                </div>
            </a>

            <!-- GitHub Profile -->
            <a href="https://github.com/Ketanrawat2004" target="_blank" rel="noopener noreferrer"
               style="display:flex;align-items:center;gap:12px;padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;text-decoration:none;transition:all 0.15s ease;"
               onmouseover="this.style.borderColor='var(--rr-pink, #E91E8C)';this.style.transform='translateY(-1px)';this.style.boxShadow='0 3px 10px rgba(0,0,0,0.05)';"
               onmouseout="this.style.borderColor='#E2E8F0';this.style.transform='none';this.style.boxShadow='none';">
                <div style="width:34px;height:34px;border-radius:8px;background:#24292F;display:flex;align-items:center;justify-content:center;color:#FFFFFF;flex-shrink:0;">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2Z"/></svg>
                </div>
                <div style="min-width:0;">
                    <div style="font-size:12.5px;font-weight:700;color:#111827;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">GitHub Repository</div>
                    <div style="font-size:11px;color:#64748B;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">@Ketanrawat2004</div>
                </div>
            </a>

            <!-- Resume (Google Drive) -->
            <a href="https://drive.google.com/file/d/1YV_i3Un8t7UZsfk1_WXQdfsM6T0Pe6ui/view?usp=drive_link" target="_blank" rel="noopener noreferrer"
               style="display:flex;align-items:center;gap:12px;padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;text-decoration:none;transition:all 0.15s ease;"
               onmouseover="this.style.borderColor='var(--rr-pink, #E91E8C)';this.style.transform='translateY(-1px)';this.style.boxShadow='0 3px 10px rgba(0,0,0,0.05)';"
               onmouseout="this.style.borderColor='#E2E8F0';this.style.transform='none';this.style.boxShadow='none';">
                <div style="width:34px;height:34px;border-radius:8px;background:#DC2626;display:flex;align-items:center;justify-content:center;color:#FFFFFF;flex-shrink:0;">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                </div>
                <div style="min-width:0;">
                    <div style="font-size:12.5px;font-weight:700;color:#111827;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">Curriculum Vitae</div>
                    <div style="font-size:11px;color:#64748B;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">Ketan Rawat &bull; Resume (PDF)</div>
                </div>
            </a>

            <!-- SupeRR Selector Season 1 Certificate -->
            <div style="display:flex;align-items:center;gap:6px;">
                <a href="https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/view?usp=sharing" target="_blank" rel="noopener noreferrer"
                   style="flex:1;display:flex;align-items:center;gap:12px;padding:12px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;text-decoration:none;transition:all 0.15s ease;"
                   onmouseover="this.style.borderColor='var(--rr-pink, #E91E8C)';this.style.transform='translateY(-1px)';this.style.boxShadow='0 3px 10px rgba(0,0,0,0.05)';"
                   onmouseout="this.style.borderColor='#E2E8F0';this.style.transform='none';this.style.boxShadow='none';">
                    <div style="width:34px;height:34px;border-radius:8px;background:#D97706;display:flex;align-items:center;justify-content:center;color:#FFFFFF;flex-shrink:0;">
                        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2"><circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline></svg>
                    </div>
                    <div style="min-width:0;">
                        <div style="font-size:12.5px;font-weight:700;color:#111827;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">Season 1 Certificate</div>
                        <div style="font-size:11px;color:#64748B;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">Unstop Top 20 Additional</div>
                    </div>
                </a>
                <button onclick="toggleCertDrawer()" title="Toggle Inline Preview" 
                        style="height:46px;padding:0 12px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;cursor:pointer;font-size:11px;font-weight:700;color:#374151;display:flex;align-items:center;gap:5px;transition:all 0.15s ease;"
                        onmouseover="this.style.borderColor='var(--rr-pink, #E91E8C)';this.style.background='#F8FAFC';"
                        onmouseout="this.style.borderColor='#E2E8F0';this.style.background='#FFFFFF';">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                    Preview
                </button>
            </div>
        </div>

        <!-- Collapsible Inline Certificate Embed Drawer -->
        <div id="certDrawer" style="display:none;margin-top:16px;padding-top:16px;border-top:1px solid #E2E8F0;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span style="font-size:12.5px;font-weight:700;color:#111827;">
                    Rajasthan Royals SupeRR Selector Season 1 &bull; Certificate of Excellence (Top 20 Additional Finalist)
                </span>
                <a href="https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/view?usp=sharing" target="_blank" rel="noopener noreferrer" style="font-size:11.5px;font-weight:700;color:#111827;text-decoration:none;">
                    Open in Full Tab &rarr;
                </a>
            </div>
            <div style="width:100%;height:480px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;overflow:hidden;">
                <iframe src="https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/preview" width="100%" height="100%" style="border:none;" allow="autoplay"></iframe>
            </div>
        </div>

        <script>
        function toggleCertDrawer() {
            var d = document.getElementById('certDrawer');
            if (d.style.display === 'none' || d.style.display === '') {
                d.style.display = 'block';
            } else {
                d.style.display = 'none';
            }
        }
        </script>
    </footer>"""

with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

pattern = re.compile(r'    <!-- Executive Analyst Footer & Verified Credentials -->[\s\S]*?</footer>')
matches = list(pattern.finditer(text))
print(f"Found {len(matches)} footer blocks to replace")
assert len(matches) == 2, f"Expected 2 footer blocks, found {len(matches)}"

text_new = pattern.sub(lambda m: NEW_FOOTER_HTML, text)

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(text_new)

print("✓ Updated both footer blocks in fix_dashboard_and_wagon.py cleanly!")

