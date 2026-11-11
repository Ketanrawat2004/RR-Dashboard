for fpath in ["index.html", "rr_war_room_terminal.html", "rr_pressure_dashboard.html", "players/jasprit_bumrah.html", "players/shivam_dube.html"]:
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()
    has_simple = 'class="simple-footer"' in c
    has_copy = '&copy; 2026 Ketan Rawat. All rights reserved.' in c
    has_links = all(u in c for u in [
        "https://www.linkedin.com/in/ketan-rawat-97a8aa2a0/",
        "https://github.com/Ketanrawat2004",
        "https://drive.google.com/file/d/1YV_i3Un8t7UZsfk1_WXQdfsM6T0Pe6ui/view?usp=drive_link",
        "https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/view?usp=sharing",
        "https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/preview"
    ])
    print(f"{fpath:30s} | SimpleFooter: {has_simple} | Copyright: {has_copy} | AllLinks: {has_links}")

