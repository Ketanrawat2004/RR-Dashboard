import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

sections = re.findall(r'<div[^>]*class=["\'][^"\']*data-section[^"\']*["\'][^>]*id=["\'](.*?)["\']', text)
print("Data sections:", sections)

tables = re.findall(r'<table[^>]*id=["\'](.*?)["\']', text)
print("Tables:", tables)

ths = re.findall(r'<th[^>]*>(.*?)</th>', text)
clean_ths = [re.sub(r'<[^>]+>', '', t).strip() for t in ths]
print(f"Total ths found: {len(clean_ths)}")
print("First 30 table headers:", clean_ths[:30])

# Cards / Metrics
cards = re.findall(r'<div[^>]*class=["\'][^"\']*stat-card[^"\']*["\']', text)
print(f"Stat cards count: {len(cards)}")

