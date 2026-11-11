with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('</div>\n    </div>\n\n    <!-- Main Navigation')
if idx == -1:
    idx = text.find('class="kpi-container"')
print(text[idx-200:idx+300])
