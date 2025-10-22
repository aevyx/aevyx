import requests
import os
import re
from urllib.parse import unquote

urls = [
#   "https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white",
# more add
]


# Desired colors
BG_COLOR = "#00695d"    
TEXT_ICON_COLOR = "#FFFFFF"  

# Output folder
output_folder = "badges"
os.makedirs(output_folder, exist_ok=True)

# Regex patterns
bg_pattern = re.compile(r'(<rect[^>]*fill=")([^"]+)(")', re.IGNORECASE)
fill_stroke_pattern = re.compile(r'(fill|stroke)="([^"]+)"', re.IGNORECASE)
color_pattern_general = re.compile(r'(fill|stroke)="(#[a-fA-F0-9]{3,6})"', re.IGNORECASE)

# Store generated filenames for final markdown
badge_filenames = []

for idx, url in enumerate(urls, 1):
    print(f"Processing badge {idx}...")

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Failed to download: {url}")
            continue

        svg = response.text

        # Extract badge name
        raw_name = url.split("/badge/")[1].split("-")[0]
        badge_name = unquote(raw_name).replace("%20", "_").replace(" ", "_")

        # Replace background fill (first rect)
        svg, _ = bg_pattern.subn(rf'\1{BG_COLOR}\3', svg, count=1)

        # Find where first rect ends
        rect_end = svg.find("</rect>")
        before = svg[:rect_end]
        after = svg[rect_end:]

        # Set all other fills/strokes to white
        after = fill_stroke_pattern.sub(lambda m: f'{m.group(1)}="{TEXT_ICON_COLOR}"', after)

        tinted_svg = before + after

        # Final pass: Replace any remaining non-purple, non-white color to white
        def final_color_check(match):
            color = match.group(2).lower()
            if color not in [BG_COLOR.lower(), TEXT_ICON_COLOR.lower()]:
                return f'{match.group(1)}="{TEXT_ICON_COLOR}"'
            return match.group(0)

        tinted_svg = color_pattern_general.sub(final_color_check, tinted_svg)

        # Save output
        out_path = os.path.join(output_folder, f"{badge_name}.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(tinted_svg)

        badge_filenames.append(f"{badge_name}.svg")
        print(f"✅ Badge {idx} saved as {badge_name}.svg")

    except Exception as e:
        print(f"⚠️ Error with badge {idx}: {e}")

# Final Markdown Output
print("\n🎨 All badges processed. Add this to your GitHub Readme:\n")
for filename in badge_filenames:
    print(f'<img src="badges/{filename}" height="28"/> ', end="")

print("\n\n✅ Done! Only purple background and white text/icons guaranteed.")
