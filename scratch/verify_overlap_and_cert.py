for fpath in ["index.html", "rr_war_room_terminal.html", "rr_pressure_dashboard.html", "players/jasprit_bumrah.html", "players/shivam_dube.html"]:
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()
    has_view_cert = "View Certificate" in c or "certDrawer" in c
    has_copy = "&copy; 2026 Ketan Rawat" in c
    if "players/" not in fpath:
        has_margin = "margin-top: 28px;" in c and ".data-section {" in c
        has_bottom_card_mb = "margin-top:24px;margin-bottom:28px;" in c
    else:
        has_margin = True
        has_bottom_card_mb = True
    print(f"{fpath:30s} | NoViewCert: {not has_view_cert} | Copyright: {has_copy} | SpacingOK: {has_margin and has_bottom_card_mb}")

