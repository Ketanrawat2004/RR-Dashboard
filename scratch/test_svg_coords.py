import json

with open("players_db.json", "r", encoding="utf-8") as f:
    players = json.load(f)

# Plot dimensions: width=860, height=460, margins: left=65, right=35, top=45, bottom=50
W, H = 860, 460
ML, MR, MT, MB = 75, 40, 50, 55
plot_w = W - ML - MR
plot_h = H - MT - MB

# X range: 40 to 85 (hp_wr)
# Y range: -12 to +25 (lift)
x_min, x_max = 42.0, 85.0
y_min, y_max = -12.0, 24.0

def to_x(wr):
    return ML + (wr - x_min) / (x_max - x_min) * plot_w

def to_y(lift):
    return MT + (y_max - lift) / (y_max - y_min) * plot_h

print("Coordinate transform test:")
print(f"X range: {to_x(45):.1f} to {to_x(85):.1f}")
print(f"Y range: {to_y(24):.1f} (top) to {to_y(-12):.1f} (bottom)")
print(f"Zero lift Y: {to_y(0):.1f}")
print(f"Threshold 60% WR X: {to_x(60):.1f}")

for p in players:
    x = to_x(p['hp_wr'])
    y = to_y(p['lift'])
    print(f"{p['name']:20s} | WR: {p['hp_wr']:4.1f}% -> X={x:5.1f} | Lift: {p['lift']:+5.1f}% -> Y={y:5.1f} | Cat: {p['category']}")

