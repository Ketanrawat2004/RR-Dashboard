with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Check doc-box styles in index.html
doc_matches = re.findall(r'\.doc-box[^{]*\{[^}]*\}', text)
print("doc-box rules in index.html:")
for dm in doc_matches:
    print(" ", dm.replace('\n', ' '))

# Check doc-heading
head_matches = re.findall(r'\.doc-heading[^{]*\{[^}]*\}', text)
print("\ndoc-heading rules in index.html:")
for hm in head_matches:
    print(" ", hm.replace('\n', ' '))

# Check strategic takeaways snippet
idx = text.find('Strategic Takeaways')
if idx != -1:
    print("\nStrategic Takeaways preview:")
    print(text[idx-50:idx+400])

