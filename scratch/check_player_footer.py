with open("players/jasprit_bumrah.html", "r", encoding="utf-8") as f:
    c = f.read()
p = c.find('class="analyst-footer"')
print(c[p-150:p+60])
pe = c.find('</footer>', p)
print('---END---')
print(c[pe-40:pe+80])

