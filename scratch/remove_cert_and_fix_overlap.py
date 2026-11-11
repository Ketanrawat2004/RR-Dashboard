import re

with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Replace footer with ultra-clean version WITHOUT View Certificate / certDrawer
CLEAN_FOOTER_HTML = """    <!-- Simple Minimal Footer with Copyright -->
    <footer class="simple-footer" style="margin-top:44px;margin-bottom:28px;padding-top:26px;border-top:1px solid #E2E8F0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#475569;">
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(300px, 1fr));gap:28px;margin-bottom:22px;">
            <div>
                <div style="font-size:12.5px;font-weight:700;color:#111827;margin-bottom:6px;">Methodology</div>
                <p style="margin:0;font-size:12px;line-height:1.65;color:#475569;">
                    Evaluated 883 IPL &amp; T20I matches (2022&ndash;2026) to filter 174 high-pressure games (knockouts, Super Overs, or finishes within 15 runs / 2 wickets). Players are ranked via a Bayesian CPPI score combining High-Pressure Win Rate (35%), True Pressure Lift &Delta; (20%), Baseline Win Rate (15%), High-Pressure POTM Awards (15%), and Knockout Win Rate (15%), scaled by a minimum sample saturation curve and BCCI auction eligibility filters.
                </p>
            </div>
            <div>
                <div style="font-size:12.5px;font-weight:700;color:#111827;margin-bottom:6px;">Thought Process</div>
                <p style="margin:0;font-size:12px;line-height:1.65;color:#475569;">
                    Traditional averages reward stat-padding in one-sided matches. Measuring True Pressure Lift (&Delta;) isolates who genuinely raises their team&rsquo;s win rate when stakes peak &mdash; highlighting high-value clutch winners like Shivam Dube and Jacob Duffy suited for Sawai Mansingh Stadium (Jaipur) within a &#8377;45 Cr auction budget, rather than overpaying for reputation.
                </p>
            </div>
        </div>

        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;padding-top:16px;border-top:1px solid #E2E8F0;font-size:12px;color:#64748B;">
            <div>
                &copy; 2026 Ketan Rawat. All rights reserved. &middot; Rajasthan Royals SupeRR Selector Season 2
            </div>
            <div style="display:flex;flex-wrap:wrap;align-items:center;gap:10px;">
                <a href="https://www.linkedin.com/in/ketan-rawat-97a8aa2a0/" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">LinkedIn</a>
                <span style="color:#CBD5E1;">|</span>
                <a href="https://github.com/Ketanrawat2004" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">GitHub</a>
                <span style="color:#CBD5E1;">|</span>
                <a href="https://drive.google.com/file/d/1YV_i3Un8t7UZsfk1_WXQdfsM6T0Pe6ui/view?usp=drive_link" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">Resume</a>
                <span style="color:#CBD5E1;">|</span>
                <a href="https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/view?usp=sharing" target="_blank" rel="noopener noreferrer" style="color:#111827;text-decoration:none;font-weight:600;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">Season 1 Certificate (Top 20)</a>
            </div>
        </div>
    </footer>"""

pattern = re.compile(r'    <!-- Simple Minimal Footer with Copyright -->[\s\S]*?</footer>')
matches = list(pattern.finditer(text))
print(f"Found {len(matches)} footer blocks to update")
assert len(matches) == 2, f"Expected 2 footer blocks, found {len(matches)}"
text = pattern.sub(lambda m: CLEAN_FOOTER_HTML, text)

# 2. Fix overlapping .doc-grid vs card above it: add margin-top: 28px to .doc-grid and margin-bottom: 24px to .data-section and bottom tactical-card
old_doc_grid_css = """        .doc-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }"""

new_doc_grid_css = """        .data-section {
            margin-bottom: 28px;
        }
        .doc-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 28px;
            margin-bottom: 24px;
        }"""

if old_doc_grid_css in text:
    text = text.replace(old_doc_grid_css, new_doc_grid_css)
    print("✓ Updated .doc-grid and added .data-section margin-bottom")
else:
    print("Warning: old_doc_grid_css not matched identically, updating via replace on master_dashboard_html CSS")

# Also ensure Bottom Card inside section-tactical-xi has margin-bottom: 24px
old_bottom_card = '<!-- Bottom Card: Clean Light Mode Pressure Lift Quadrant Matrix with SVG Chart -->\n        <div class="tactical-card" style="margin-top:24px;">'
new_bottom_card = '<!-- Bottom Card: Clean Light Mode Pressure Lift Quadrant Matrix with SVG Chart -->\n        <div class="tactical-card" style="margin-top:24px;margin-bottom:28px;">'
if old_bottom_card in text:
    text = text.replace(old_bottom_card, new_bottom_card)
    print("✓ Added margin-bottom:28px to Bottom Card")

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(text)

print("✓ Saved fix_dashboard_and_wagon.py successfully!")

