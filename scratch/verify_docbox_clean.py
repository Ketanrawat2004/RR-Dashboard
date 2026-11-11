with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("File length:", len(text))

doc_matches = re.findall(r'\.doc-box[^{]*\{[^}]*\}', text)
print("\n.doc-box rules:")
for dm in doc_matches:
    print(" ", dm.replace('\n', ' '))

head_matches = re.findall(r'\.doc-heading[^{]*\{[^}]*\}', text)
print("\n.doc-heading rules:")
for hm in head_matches:
    print(" ", hm.replace('\n', ' '))

# Check if any ::before or ::after exists on doc-box
print("\n::before on doc-box:", ".doc-box::before" in text)
print("::after on doc-box:", ".doc-box::after" in text)

# Check the HTML markup of the documentation section at the bottom
idx = text.find('class="doc-grid"')
if idx != -1:
    print("\nDoc-grid markup preview:")
    print(text[idx:idx+1000])

