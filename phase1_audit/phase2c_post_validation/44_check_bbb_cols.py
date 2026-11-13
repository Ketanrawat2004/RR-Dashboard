import pandas as pd

bbb = pd.read_csv("ball_by_ball.csv", nrows=5)
print(list(bbb.columns))

