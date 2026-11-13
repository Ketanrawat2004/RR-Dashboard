import os
import re
import pandas as pd

ROOT = r"C:\RR NEW"
STEP4_DIR = os.path.join(ROOT, "phase1_audit", "step4_jury_harmonization")
IMG_DIR = os.path.join(ROOT, "player_images")

def to_key(name):
    # Normalize slug
    k = re.sub(r"[^a-zA-Z0-9]+", "_", name.strip()).strip("_").lower()
    return k

def get_initials(name):
    clean = re.sub(r"[^a-zA-Z\s]", "", name).strip()
    parts = clean.split()
    if len(parts) == 0:
        return "RR"
    elif len(parts) == 1:
        return parts[0][:2].upper()
    else:
        return (parts[0][0] + parts[-1][0]).upper()

def make_svg_content(initials):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <defs>
    <linearGradient id="rrGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EB1A8D"/>
      <stop offset="100%" stop-color="#001D48"/>
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="96" fill="url(#rrGrad)" stroke="#FFFFFF" stroke-width="4"/>
  <text x="100" y="125" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="72" font-weight="800" fill="#FFFFFF">{initials}</text>
</svg>"""

def main():
    bat_csv = pd.read_csv(os.path.join(STEP4_DIR, "FINAL_BATTER_RANKINGS.csv"))
    bowl_csv = pd.read_csv(os.path.join(STEP4_DIR, "FINAL_BOWLER_RANKINGS_COMPOSITE.csv"))

    all_players = set()
    for _, r in bat_csv.iterrows():
        all_players.add((r["player_id"], r["player_name"]))
    for _, r in bowl_csv.iterrows():
        all_players.add((r["player_id"], r["player_name"]))

    print(f"Total unique qualified players across both disciplines: {len(all_players)}")

    existing_pngs = set([f.replace(".png", "") for f in os.listdir(IMG_DIR) if f.endswith(".png")])
    print(f"Existing PNG images in player_images/: {len(existing_pngs)}")

    svgs_created = 0
    pngs_preserved = 0

    for pid, name in sorted(all_players, key=lambda x: x[1]):
        key = to_key(name)
        png_path = os.path.join(IMG_DIR, f"{key}.png")
        svg_path = os.path.join(IMG_DIR, f"{key}.svg")

        if os.path.exists(png_path):
            pngs_preserved += 1
        else:
            # Generate SVG
            initials = get_initials(name)
            svg_content = make_svg_content(initials)
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
            svgs_created += 1

    print(f"\nSVG Generation Complete:")
    print(f"  Existing official PNG headshots preserved (untouched): {pngs_preserved}")
    print(f"  New offline SVG monogram badges created: {svgs_created}")

if __name__ == "__main__":
    main()

