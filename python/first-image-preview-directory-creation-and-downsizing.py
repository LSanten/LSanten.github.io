import os
import re
import json

# Configuration
BASE_DIR = "/Users/lsanten/Documents/GitHub/LSanten.github.io/"
MARKDOWN_FOLDER = "_mms-md"
THUMBNAIL_FOLDER = "marble-thumbnails"
THUMBNAIL_URL_BASE = "https://leonsanten.info/marble-thumbnails"
ORIGINAL_IMAGE_URL_BASE = "https://leonsanten.info/marbles/media"
SIZE_LIMIT = 1_000_000  # Size limit in bytes (1 MB)

# Paths
MARKDOWN_FOLDER_PATH = os.path.join(BASE_DIR, MARKDOWN_FOLDER)
THUMBNAIL_FOLDER_PATH = os.path.join(BASE_DIR, THUMBNAIL_FOLDER)
OUTPUT_FILE = os.path.join(THUMBNAIL_FOLDER_PATH, "image_mapping.json")

# Function to extract the first image reference from a Markdown file
def extract_first_image(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'!\[.*?\]\((.*?)\)', content)  # Regex for image links
    return matches[0] if matches else None

# Function to create the image mapping
def create_image_mapping():
    mapping = {}
    os.makedirs(THUMBNAIL_FOLDER_PATH, exist_ok=True)  # Ensure the thumbnail folder exists

    for root, dirs, files in os.walk(MARKDOWN_FOLDER_PATH):
        for file in files:
            if file.endswith('.md'):  # Only process Markdown files
                markdown_file = os.path.join(root, file)
                markdown_filename = os.path.splitext(file)[0]

                # Extract the first image reference
                first_image = extract_first_image(markdown_file)
                if not first_image:
                    continue

                # Handle external links
                if first_image.startswith('http://') or first_image.startswith('https://'):
                    mapping[markdown_filename] = first_image
                    continue

                # Resolve local path relative to the Markdown file
                image_path = os.path.normpath(os.path.join(os.path.dirname(markdown_file), first_image))

                if os.path.isfile(image_path):
                    file_size = os.path.getsize(image_path)

                    if file_size > SIZE_LIMIT:
                        # Use thumbnail URL for large images
                        thumbnail_url = f"{THUMBNAIL_URL_BASE}/{markdown_filename}-thumb{os.path.splitext(first_image)[1]}"
                        mapping[markdown_filename] = thumbnail_url
                    else:
                        # Use original URL for small images
                        original_url = f"{ORIGINAL_IMAGE_URL_BASE}/{os.path.basename(first_image)}"
                        mapping[markdown_filename] = original_url
    return mapping

# Main execution
if __name__ == "__main__":
    image_mapping = create_image_mapping()
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(image_mapping, f, indent=4)

    print(f"Mapping file created at: {OUTPUT_FILE}")
