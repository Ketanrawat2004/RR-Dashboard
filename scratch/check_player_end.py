with open('fix_dashboard_and_wagon.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx_end_p = text.find('</div>\n</body>\n</html>\n"""\n    return html')
if idx_end_p == -1:
    # search for return html in generate_player_page
    idx_ret = text.find('</body>\n</html>')
    print(text[idx_ret-400:idx_ret+100])
else:
    print(text[idx_end_p-300:idx_end_p+100])

