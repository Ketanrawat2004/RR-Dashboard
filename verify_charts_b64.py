import os
import base64

with open("pressure_output/chart_02_pressure_lift_quadrants.png", "rb") as f:
    q_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

with open("pressure_output/chart_03_rr_tactical_xi.png", "rb") as f:
    t_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

print("Quad b64 len:", len(q_b64))
print("Tactical b64 len:", len(t_b64))

