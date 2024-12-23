import os
import re
import json

# Configuration
BASE_DIR = "/Users/lsanten/Documents/GitHub/LSanten.github.io/"
MARKDOWN_FOLDER = "_mms-md"
MEDIA_FOLDER = "_mms-md/media"
THUMBNAIL_FOLDER = "marble-thumbnails"
THUMBNAIL_URL_BASE = "https://leonsanten.info/marble-thumbnails"
ORIGINAL_IMAGE_URL_BASE = "https://leonsanten.info/marbles/media"
SIZE_LIMIT = 1_000_000  # Size limit in bytes (1 MB)

# Paths
MARKDOWN_FOLDER_PATH = os.path.join(BASE_DIR, MARKDOWN_FOLDER)
MEDIA_FOLDER_PATH = os.path.join(BASE_DIR, MEDIA_FOLDER)
THUMBNAIL_FOLDER_PATH = os.path.join(BASE_DIR, THUMBNAIL_FOLDER)
OUTPUT_FILE = os.path.join(THUMBNAIL_FOLDER_PATH, "image_mapping.json")

# Function to extract the first image reference from a Markdown file
def extract_first_image(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
        #print(f"Content of {markdown_file}:\n{content}")  # Debug the file content
    # Regex to find the first image reference: ![Alt text](media/image.png) or ![Alt text](http://...)
    matches = re.findall(r'!\[.*?\]\((.*?)\)', content)
    #print(f"Regex Matches for {markdown_file}: {matches}")
    return matches[0] if matches else None

# Function to create the image mapping
def create_image_mapping():
    mapping = {}
    os.makedirs(THUMBNAIL_FOLDER_PATH, exist_ok=True)  # Ensure the thumbnail folder exists

    for root, dirs, files in os.walk(MARKDOWN_FOLDER_PATH):
        for file in files:
            if file.endswith('.md'):  # Only process Markdown files
                #print(f"Found Markdown file: {file}")
                markdown_file = os.path.join(root, file)
                markdown_filename = os.path.splitext(file)[0]

                # Extract the first image reference
                first_image = extract_first_image(markdown_file)
                #print(f"Debug: First image for {file} is {first_image}")  # Check if first_image is found
                if first_image is None:
                    #print(f"Skipping {file}: No image found")
                    continue  # Skip this file
                #print(f"File: {file} - First Image Reference: {first_image}")
                if first_image:
                    if first_image.startswith('http://') or first_image.startswith('https://'):
                        print(f"External link detected for {file}: {first_image}")
                        # External link: Add directly to the mapping
                        mapping[markdown_filename] = first_image
                    else:
                        # Resolve local path relative to the Markdown file
                        image_path = os.path.normpath(os.path.join(os.path.dirname(markdown_file), first_image))
                        print(f"Resolved local image path for {file}: {image_path}")

                        if os.path.isfile(image_path):
                            print(f"Local Image Found: {image_path} - Size: {os.path.getsize(image_path)} bytes")
                            file_extension = os.path.splitext(first_image)[1]

                            if os.path.getsize(image_path) > SIZE_LIMIT:
                                # Image is larger than 1 MB; generate thumbnail URL
                                thumbnail_url = f"{THUMBNAIL_URL_BASE}/{markdown_filename}-thumb{file_extension}"
                                mapping[markdown_filename] = thumbnail_url
                            else:
                                # Image is small; use original URL
                                print(f"Local Image Not Found: {image_path}")
                                relative_path = os.path.relpath(image_path, MEDIA_FOLDER_PATH).replace(os.sep, '/')
                                original_url = f"{ORIGINAL_IMAGE_URL_BASE}/{relative_path}"
                                mapping[markdown_filename] = original_url
    return mapping

# Main execution
if __name__ == "__main__":
    image_mapping = create_image_mapping()
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(image_mapping, f, indent=4)

    print(f"Mapping file created at: {OUTPUT_FILE}")
