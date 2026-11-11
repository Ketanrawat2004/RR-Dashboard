with open("scratch/test_final_check_3.py", "r", encoding="utf-8") as f:
    text = f.read()

# Change Rinku Singh dy to 16
text = text.replace('{"name": "Rinku Singh (#2)", "wr": 69.2, "lift": 5.4, "cat": "Batter", "dx": 12, "dy": 4, "anchor": "start"},',
                    '{"name": "Rinku Singh (#2)", "wr": 69.2, "lift": 5.4, "cat": "Batter", "dx": 12, "dy": 16, "anchor": "start"},')

with open("scratch/test_final_check_3.py", "w", encoding="utf-8") as f:
    f.write(text)

import subprocess
res = subprocess.run(["python", "scratch/test_final_check_3.py"], capture_output=True, text=True)
print(res.stdout)

