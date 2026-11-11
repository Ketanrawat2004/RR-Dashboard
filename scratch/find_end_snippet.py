with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('.doc-box {{')
# Look for the end of this block
snippet_idx = text.find('.code-snippet {{', idx1)
end_snippet_idx = text.find('}}', snippet_idx) + 2

print("EXACT BLOCK FROM idx1 to end_snippet_idx:")
print(text[idx1:end_snippet_idx])

