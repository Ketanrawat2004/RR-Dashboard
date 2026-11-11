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
    {"name": "Arshdeep Singh (#9)", "wr": 68.0, "lift": 11.0, "cat": "Bowler", "dx": 10, "dy": -12, "anchor": "start"},
    {"name": "Axar Patel (#3)", "wr": 64.3, "lift": 7.8, "cat": "Batter", "dx": -10, "dy": -4, "anchor": "end"},
    {"name": "B. Rajapaksa (#8)", "wr": 66.7, "lift": 10.4, "cat": "Batter", "dx": -10, "dy": -4, "anchor": "end"},
    {"name": "Bhuvneshwar K. (#8)", "wr": 60.0, "lift": 2.7, "cat": "Bowler", "dx": -10, "dy": -4, "anchor": "end"},
    {"name": "Devon Conway (#6)", "wr": 64.3, "lift": 18.1, "cat": "Batter", "dx": 10, "dy": -4, "anchor": "start"},
    {"name": "Jacob Duffy (#1)", "wr": 75.0, "lift": 20.5, "cat": "Bowler", "dx": 10, "dy": 4, "anchor": "start"},
    {"name": "Josh Hazlewood (#2)", "wr": 78.6, "lift": 14.9, "cat": "Bowler", "dx": -10, "dy": -4, "anchor": "end"},
    {"name": "L. Ferguson (#10)", "wr": 55.6, "lift": 6.5, "cat": "Bowler", "dx": -10, "dy": 4, "anchor": "end"},
    {"name": "Mitchell Starc (#4)", "wr": 60.0, "lift": -8.3, "cat": "Bowler", "dx": 10, "dy": -4, "anchor": "start"},
    {"name": "R. Gaikwad (#5)", "wr": 57.1, "lift": 6.5, "cat": "Batter", "dx": 10, "dy": 4, "anchor": "start"},
    {"name": "R. Shepherd (#6)", "wr": 56.0, "lift": 7.0, "cat": "Bowler", "dx": -10, "dy": -8, "anchor": "end"},
    {"name": "Rajat Patidar (#4)", "wr": 71.4, "lift": 11.1, "cat": "Batter", "dx": 10, "dy": 16, "anchor": "start"},
    {"name": "Rinku Singh (#2)", "wr": 69.2, "lift": 5.4, "cat": "Batter", "dx": 10, "dy": -4, "anchor": "start"},
    {"name": "Sediqullah Atal (#10)", "wr": 50.0, "lift": -7.9, "cat": "Batter", "dx": 10, "dy": -4, "anchor": "start"},
    {"name": "Shivam Dube (#1)", "wr": 66.7, "lift": 12.4, "cat": "Batter", "dx": -10, "dy": -4, "anchor": "end"},
    {"name": "Shreyas Iyer (#9)", "wr": 55.6, "lift": 1.1, "cat": "Batter", "dx": 10, "dy": 4, "anchor": "start"},
    {"name": "Suyash Sharma (#7)", "wr": 72.7, "lift": 7.6, "cat": "Bowler", "dx": 10, "dy": -4, "anchor": "start"},
    {"name": "Varun C. (#5)", "wr": 61.9, "lift": 3.3, "cat": "Bowler", "dx": 10, "dy": -4, "anchor": "start"},
    {"name": "Virat Kohli", "wr": 70.0, "lift": 7.6, "cat": "Batter", "dx": -10, "dy": -4, "anchor": "end"},
    {"name": "Yash Dayal (#3)", "wr": 80.0, "lift": 10.2, "cat": "Bowler", "dx": 0, "dy": -12, "anchor": "middle"},
]

for p in players:
    cx = to_x(p['wr'])
    cy = to_y(p['lift'])
    print(f"{p['name']:20}: dot=({cx:.1f}, {cy:.1f}), label=({cx+p['dx']:.1f}, {cy+p['dy']:.1f}) [{p['anchor']}]")

