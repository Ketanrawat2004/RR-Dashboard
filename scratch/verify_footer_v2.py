for fpath in ["index.html", "rr_war_room_terminal.html", "rr_pressure_dashboard.html", "players/jasprit_bumrah.html", "players/shivam_dube.html"]:
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()
    has_meth = "Selection Methodology &amp; Scoring Model" in c
    has_tp = "My Thought Process &amp; Auction Logic" in c
    has_cert = "https://drive.google.com/file/d/16QOHQMo1OzIbIaZD7xgYpnt25XGmDqfL/preview" in c
    print(f"{fpath:30s} | Meth: {has_meth} | ThoughtProcess: {has_tp} | CertEmbed: {has_cert}")

