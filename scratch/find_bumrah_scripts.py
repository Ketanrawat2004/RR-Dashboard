import glob

for f in glob.glob('*.py') + glob.glob('scratch/*.py'):
    with open(f, 'r', encoding='utf-8') as fh:
        s = fh.read()
        if 'jasprit_bumrah' in s:
            print("jasprit_bumrah found in:", f)

