import os
import re

# Define colors
old_color_pattern = re.compile(r"#6445ff", re.IGNORECASE)
new_color = "#00695d"

# Get current directory
current_dir = os.getcwd()
# Loop through files in current directory
for filename in os.listdir(current_dir):
    if filename.endswith(".svg"):
        filepath = os.path.join(current_dir, filename)

        # Read file
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace color if found
        if re.search(old_color_pattern, content):
            updated = re.sub(old_color_pattern, new_color, content)

            # Optional: backup original
            with open(filepath + ".bak", "w", encoding="utf-8") as backup:
                backup.write(content)

            # Write updated content
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated)

            print(f"✅ Updated color in: {filename}")
        else:
            print(f"⚪ No color match found in: {filename}")
