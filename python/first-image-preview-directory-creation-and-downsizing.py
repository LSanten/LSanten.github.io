import os
import re
import json
from PIL import Image  # Ensure Pillow is installed: pip install pillow
from urllib.parse import unquote
from urllib.parse import quote

# Configuration
BASE_DIR = "/Users/lsanten/Documents/GitHub/LSanten.github.io/"
MARKDOWN_FOLDER = "_mms-md"
THUMBNAIL_FOLDER = "manual_files/marbles/mediathumbs"
THUMBNAIL_URL_BASE = "https://leonsanten.info/marbles/mediathumbs"
ORIGINAL_IMAGE_URL_BASE = "https://leonsanten.info/marbles/media"
SIZE_LIMIT = 1_000_000  # Size limit in bytes (1 MB)

# Paths
MARKDOWN_FOLDER_PATH = os.path.join(BASE_DIR, MARKDOWN_FOLDER)
THUMBNAIL_FOLDER_PATH = os.path.join(BASE_DIR, THUMBNAIL_FOLDER)
OUTPUT_FILE = os.path.join(THUMBNAIL_FOLDER_PATH, "image_mapping.json")

# Global counter for skipped files
skipped_count = 0

# Function to extract the first image reference from a Markdown file
def extract_first_image(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'!\[.*?\]\((.*?)\)', content)  # Regex for image links
    return matches[0] if matches else None

# Function to resize images (NEW FUNCTION)
def resize_image(input_path, output_path, size_limit=SIZE_LIMIT):
    """
    Resize the image to fit within the size limit while preserving aspect ratio.
    """
    with Image.open(input_path) as img:
        # Ensure compatibility with formats like PNG
        img = img.convert("RGB")
        quality = 95  # Start with high quality
        width, height = img.size

        # Iteratively reduce dimensions and quality
        while True:
            # Reduce dimensions proportionally
            new_width = int(width * 0.9)
            new_height = int(height * 0.9)
            # Use LANCZOS as the modern equivalent for high-quality resampling
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save the resized image with the current quality
            img_resized.save(output_path, format="JPEG", quality=quality, progressive=False)

            # Check the output file size
            current_size = os.path.getsize(output_path)
            print(f"Resizing {input_path}: New size: {current_size / 1_000_000:.2f} MB, Quality: {quality}, Dimensions: {new_width}x{new_height}")

            # Exit if the file size is within the limit
            if current_size <= size_limit:
                print(f"Successfully resized {input_path} to {output_path} below {size_limit / 1_000_000:.1f} MB.")
                return

            # Reduce quality for further compression
            quality -= 5
            width, height = new_width, new_height  # Update dimensions for next iteration

            # Stop if quality gets too low
            if quality <= 10:
                break

        # Raise an exception if unable to resize within the limit
        raise Exception(f"Unable to resize {input_path} below {size_limit / 1_000_000:.1f} MB.")

# Function to create the image mapping
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
                image_path = os.path.normpath(os.path.join(os.path.dirname(markdown_file), unquote(first_image)))

                if os.path.isfile(image_path):
                    file_size = os.path.getsize(image_path)

                    # Thumbnail path
                    resized_path = os.path.join(THUMBNAIL_FOLDER_PATH, f"{markdown_filename}-thumb.jpg")

                    # Check if resizing is necessary
                    if file_size > SIZE_LIMIT:
                        # Resize only if the original image is newer or thumbnail doesn't exist
                        if not os.path.exists(resized_path) or os.path.getmtime(image_path) > os.path.getmtime(resized_path):
                            print(f"Resizing {image_path} because it is newer or no resized version exists.")
                            resize_image(image_path, resized_path)  # Resize image to fit size limit
                        else:
                            # print(f"Skipping {image_path} as it has not been modified since the last resize.")
                            global skipped_count
                            skipped_count += 1  # Increment skipped counter
                        thumbnail_url = f"{THUMBNAIL_URL_BASE}/{quote(markdown_filename)}-thumb.jpg"
                        mapping[markdown_filename] = thumbnail_url
                    else:
                        # Use original URL for small images
                        original_url = f"{ORIGINAL_IMAGE_URL_BASE}/{quote(unquote(os.path.basename(first_image)))}"
                        mapping[markdown_filename] = original_url
    return mapping

# Function to print the skipped file count
def print_skipped_count():
    global skipped_count
    print(f"PTYHON: Total preview image skipped for resizing: {skipped_count}")


# Main execution
if __name__ == "__main__":
    image_mapping = create_image_mapping()
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(image_mapping, f, indent=4)

    print_skipped_count()

    print(f"PYTHON: Mapping file created at: {OUTPUT_FILE}")
