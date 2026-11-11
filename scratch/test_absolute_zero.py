def test_absolute_zero():
    W, H = 900, 520
    ML, MR, MT, MB = 80, 60, 50, 55
    plot_w = W - ML - MR
    plot_h = H - MT - MB

    x_min, x_max = 42.0, 85.0
    y_min, y_max = -12.0, 24.0

    def to_x(wr):
        return ML + (wr - x_min) / (x_max - x_min) * plot_w

    def to_y(lift):
        return MT + (y_max - lift) / (y_max - y_min) * plot_h

    players = [
        {"name": "Jacob Duffy (#1)", "wr": 75.0, "lift": 20.5, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Devon Conway (#6)", "wr": 64.3, "lift": 18.1, "cat": "Batter", "dx": 0, "dy": -12, "anchor": "middle"},
        {"name": "Josh Hazlewood (#2)", "wr": 78.6, "lift": 14.9, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Yash Dayal (#3)", "wr": 80.0, "lift": 10.2, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Shivam Dube (#1)", "wr": 66.7, "lift": 12.4, "cat": "Batter", "dx": -12, "dy": -4, "anchor": "end"},
        {"name": "Rajat Patidar (#4)", "wr": 71.4, "lift": 11.1, "cat": "Batter", "dx": 0, "dy": -12, "anchor": "middle"},
        {"name": "Arshdeep Singh (#9)", "wr": 68.0, "lift": 11.0, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "B. Rajapaksa (#8)", "wr": 66.7, "lift": 10.4, "cat": "Batter", "dx": -12, "dy": -4, "anchor": "end"},
        {"name": "Virat Kohli", "wr": 70.0, "lift": 7.6, "cat": "Batter", "dx": 12, "dy": -4, "anchor": "start"},
        {"name": "Rinku Singh (#2)", "wr": 69.2, "lift": 5.4, "cat": "Batter", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Suyash Sharma (#7)", "wr": 72.7, "lift": 7.6, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Axar Patel (#3)", "wr": 64.3, "lift": 7.8, "cat": "Batter", "dx": 0, "dy": 16, "anchor": "middle"},
        {"name": "R. Gaikwad (#5)", "wr": 57.1, "lift": 6.5, "cat": "Batter", "dx": -12, "dy": 4, "anchor": "end"},
        {"name": "R. Shepherd (#6)", "wr": 56.0, "lift": 7.0, "cat": "Bowler", "dx": -12, "dy": -8, "anchor": "end"},
        {"name": "L. Ferguson (#10)", "wr": 55.6, "lift": 6.5, "cat": "Bowler", "dx": -12, "dy": 16, "anchor": "end"},
        {"name": "Varun C. (#5)", "wr": 61.9, "lift": 3.3, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Bhuvneshwar K. (#8)", "wr": 60.0, "lift": 2.7, "cat": "Bowler", "dx": -12, "dy": -6, "anchor": "end"},
        {"name": "Shreyas Iyer (#9)", "wr": 55.6, "lift": 1.1, "cat": "Batter", "dx": -12, "dy": 4, "anchor": "end"},
        {"name": "Mitchell Starc (#4)", "wr": 60.0, "lift": -8.3, "cat": "Bowler", "dx": 12, "dy": 4, "anchor": "start"},
        {"name": "Sediqullah Atal (#10)", "wr": 50.0, "lift": -7.9, "cat": "Batter", "dx": 12, "dy": 4, "anchor": "start"},
    ]

    boxes = []
    char_w = 6.2
    line_h = 12

    for p in players:
        cx = to_x(p['wr'])
        cy = to_y(p['lift'])
        tx = cx + p['dx']
        ty = cy + p['dy']
        tw = len(p['name']) * char_w
        if p['anchor'] == 'middle':
            bx1 = tx - tw/2
            bx2 = tx + tw/2
        elif p['anchor'] == 'end':
            bx1 = tx - tw
            bx2 = tx
        else: # start
            bx1 = tx
            bx2 = tx + tw
        by1 = ty - line_h
        by2 = ty + 2
        boxes.append((p['name'], (bx1, by1, bx2, by2), (cx, cy)))

    collisions = []
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            n1, (x1a, y1a, x1b, y1b), _ = boxes[i]
            n2, (x2a, y2a, x2b, y2b), _ = boxes[j]
            pad = 2
            if not (x1b + pad < x2a or x2b + pad < x1a or y1b + pad < y2a or y2b + pad < y1a):
                collisions.append((n1, n2))

    print(f"Total collisions detected: {len(collisions)}")
    if collisions:
        for c in collisions:
            print(f"  COLLISION: {c[0]} <---> {c[1]}")
    else:
        print("SUCCESS! ZERO COLLISIONS! 100% CLEAN AND READABLE!")

test_absolute_zero()

