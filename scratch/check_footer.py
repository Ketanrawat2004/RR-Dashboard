with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
idx = text.rfind('footer')
if idx != -1:
    print("Found footer at:", idx)
    print(text[idx-100:idx+600])
else:
    print("No footer found in index.html")
    print("End of index.html:")
    print(text[-1500:])

