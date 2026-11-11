import json

W, H = 900, 520
ML, MR, MT, MB = 80, 60, 65, 55
plot_w = W - ML - MR
plot_h = H - MT - MB
x_min, x_max = 42.0, 85.0
y_min, y_max = -12.0, 24.0

def to_x(wr): return ML + (wr - x_min) / (x_max - x_min) * plot_w
def to_y(lift): return MT + (y_max - lift) / (y_max - y_min) * plot_h

players = [
    {"name": "Jacob Duffy (#1)", "wr": 75.0, "lift": 20.5, "cat": "Bowler"},
    {"name": "Devon Conway (#6)", "wr": 64.3, "lift": 18.1, "cat": "Batter"},
    {"name": "Josh Hazlewood (#2)", "wr": 78.6, "lift": 14.9, "cat": "Bowler"},
    {"name": "Yash Dayal (#3)", "wr": 80.0, "lift": 10.2, "cat": "Bowler"},
    {"name": "Shivam Dube (#1)", "wr": 66.7, "lift": 12.4, "cat": "Batter"},
    {"name": "Rajat Patidar (#4)", "wr": 71.4, "lift": 11.1, "cat": "Batter"},
    {"name": "Arshdeep Singh (#9)", "wr": 68.0, "lift": 11.0, "cat": "Bowler"},
    {"name": "B. Rajapaksa (#8)", "wr": 66.7, "lift": 10.4, "cat": "Batter"},
    {"name": "Virat Kohli", "wr": 70.0, "lift": 7.6, "cat": "Batter"},
    {"name": "Rinku Singh (#2)", "wr": 69.2, "lift": 5.4, "cat": "Batter"},
    {"name": "Suyash Sharma (#7)", "wr": 72.7, "lift": 7.6, "cat": "Bowler"},
    {"name": "Axar Patel (#3)", "wr": 64.3, "lift": 7.8, "cat": "Batter"},
    {"name": "R. Gaikwad (#5)", "wr": 57.1, "lift": 6.5, "cat": "Batter"},
    {"name": "R. Shepherd (#6)", "wr": 56.0, "lift": 7.0, "cat": "Bowler"},
    {"name": "L. Ferguson (#10)", "wr": 55.6, "lift": 6.5, "cat": "Bowler"},
    {"name": "Varun C. (#5)", "wr": 61.9, "lift": 3.3, "cat": "Bowler"},
    {"name": "Bhuvneshwar K. (#8)", "wr": 60.0, "lift": 2.7, "cat": "Bowler"},
    {"name": "Shreyas Iyer (#9)", "wr": 55.6, "lift": 1.1, "cat": "Batter"},
    {"name": "Mitchell Starc (#4)", "wr": 60.0, "lift": -8.3, "cat": "Bowler"},
    {"name": "Sediqullah Atal (#10)", "wr": 50.0, "lift": -7.9, "cat": "Batter"},
]

for p in players:
    p['cx'] = to_x(p['wr'])
    p['cy'] = to_y(p['lift'])

char_w = 6.2
line_h = 12

obstacles = [
    # Q2 header at top left
    ("Q2_HEAD", (ML + 10, MT + 6, ML + 10 + len("QUADRANT II • SITUATIONAL SPECIALISTS") * 6.5, MT + 24)),
    # Q1 header at top right
    ("Q1_HEAD", (W - MR - 12 - len("QUADRANT I • CLUTCH MATCH-WINNERS") * 6.5, MT + 6, W - MR - 12, MT + 24)),
    # Q4 header at bottom right
    ("Q4_HEAD", (W - MR - 12 - len("QUADRANT IV • HIGH BASELINE DRIFT") * 6.5, H - MB - 24, W - MR - 12, H - MB - 6)),
]

# Generate strictly valid candidate offsets where label clears its OWN dot with 9px margin
candidates = []
# Right side: dx in [10, 12, 14, 18], anchor='start'
for dx in [10, 12, 14, 16, 20]:
    for dy in [-16, -12, -8, -4, 4, 8, 12, 16]:
        candidates.append((dx, dy, 'start'))

# Left side: dx in [-10, -12, -14, -18], anchor='end'
for dx in [-10, -12, -14, -16, -20]:
    for dy in [-16, -12, -8, -4, 4, 8, 12, 16]:
        candidates.append((dx, dy, 'end'))

# Top / Bottom: anchor='middle'
for dx in [-5, 0, 5]:
    for dy in [-18, -14, -12, 16, 18, 22]:
        candidates.append((dx, dy, 'middle'))

# Sort candidates by distance from dot
candidates.sort(key=lambda c: c[0]**2 + c[1]**2)

def get_box(p, dx, dy, anchor):
    tx = p['cx'] + dx
    ty = p['cy'] + dy
    tw = len(p['name']) * char_w
    if anchor == 'middle':
        bx1 = tx - tw/2
        bx2 = tx + tw/2
    elif anchor == 'end':
        bx1 = tx - tw
        bx2 = tx
    else:
        bx1 = tx
        bx2 = tx + tw
    by1 = ty - line_h
    by2 = ty + 2
    return (bx1, by1, bx2, by2)

def collides(b1, b2, pad=3):
    return not (b1[2] + pad < b2[0] or b2[2] + pad < b1[0] or b1[3] + pad < b2[1] or b2[3] + pad < b1[1])

def covers_dot(box, cx, cy, r=8):
    return (box[0] - r <= cx <= box[2] + r) and (box[1] - r <= cy <= box[3] + r)

def out_of_bounds(box):
    return box[0] < ML + 4 or box[2] > W - MR - 4 or box[1] < MT + 2 or box[3] > H - MB - 2

# Filter viable candidates per player
player_candidates = {}
for p in players:
    valid = []
    for dx, dy, anchor in candidates:
        box = get_box(p, dx, dy, anchor)
        if out_of_bounds(box): continue
        if any(collides(box, obs[1], pad=4) for obs in obstacles): continue
        # Must not cover ANY player dot (including its own or others)
        if any(covers_dot(box, o['cx'], o['cy'], r=8) for o in players): continue
        valid.append((dx, dy, anchor, box))
    player_candidates[p['name']] = valid
    print(f"{p['name']:22}: {len(valid)} viable candidate positions")

# Sort players with fewest viable positions first (MRV heuristic)
players.sort(key=lambda p: len(player_candidates[p['name']]))

assignment = {}
def solve(idx):
    if idx == len(players):
        return True
    p = players[idx]
    for dx, dy, anchor, box in player_candidates[p['name']]:
        hit = False
        for prev_name, prev_box in assignment.items():
            if collides(box, prev_box, pad=3):
                hit = True
                break
        if not hit:
            assignment[p['name']] = box
            p['best_dx'] = dx
            p['best_dy'] = dy
            p['best_anchor'] = anchor
            if solve(idx + 1):
                return True
            del assignment[p['name']]
    return False

success = solve(0)
print("\nSOLVE SUCCESS:", success)
if success:
    print("\nOPTIMAL OFFSETS:")
    for p in sorted(players, key=lambda x: x['name']):
        print(f"    {{\"name\": \"{p['name']}\", \"wr\": {p['wr']}, \"lift\": {p['lift']}, \"cat\": \"{p['cat']}\", \"dx\": {p['best_dx']}, \"dy\": {p['best_dy']}, \"anchor\": \"{p['best_anchor']}\"}},")
