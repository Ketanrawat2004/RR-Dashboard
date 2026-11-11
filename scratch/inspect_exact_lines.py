with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Line 2570 to 2595:")
for i in range(2569, 2595):
    l = lines[i]
    if 'data:image/png;base64' in l:
        print(f"{i+1}: [BASE64_IMAGE]")
    else:
        print(f"{i+1}: {l.rstrip()}")

print("\nLine 2780 to 2810:")
for i in range(2780, 2810):
    l = lines[i]
    if 'data:image/png;base64' in l:
        print(f"{i+1}: [BASE64_IMAGE]")
    else:
        print(f"{i+1}: {l.rstrip()}")

