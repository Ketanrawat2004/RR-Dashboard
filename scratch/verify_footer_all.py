import re

urls = [
    "https://www.linkedin.com/in/ketan-rawat-97a8aa2a0/",
    "https://github.com/Ketanrawat2004",
    "https://drive.google.com/file/d/1YV_i3Un8t7UZsfk1_WXQdfsM6T0Pe6ui/view?usp=drive_link",
    "https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/view?usp=sharing",
    "https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/preview"
]

for fpath in ["index.html", "rr_war_room_terminal.html", "rr_pressure_dashboard.html", "players/jasprit_bumrah.html", "players/shivam_dube.html"]:
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()
    has_footer = 'class="analyst-footer"' in c
    all_urls = all(u in c for u in urls)
    print(f"{fpath:30s} | Footer: {has_footer} | All 5 URLs (incl. embed): {all_urls}")

# Also check placement inside index.html
with open("index.html", "r", encoding="utf-8") as f:
    idx_c = f.read()
pos_f = idx_c.find('<footer class="analyst-footer"')
print("\n=== Context around footer start in index.html ===")
print(idx_c[pos_f-120:pos_f+80])
pos_fe = idx_c.find('</footer>', pos_f)
print("\n=== Context around footer end in index.html ===")
print(idx_c[pos_fe-40:pos_fe+100])

