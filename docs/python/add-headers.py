import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the _mms-md folder relative to the script directory
folder_path = os.path.join(script_dir, '../_mms-md')

# Define the front matter to be added
front_matter = "---\nlayout: default\n---\n"
front_matter_beginning = "---\nlayout:"

# Function to check and add front matter to a markdown file
def add_front_matter(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        if not content.startswith(front_matter_beginning):
            print(f"Adding front matter to {file_path}")
            file.seek(0, 0)
            file.write(front_matter + content)

# Collect all markdown files in the folder
md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]

# Add front matter to each file if it's missing
for md_file in md_files:
    file_path = os.path.join(folder_path, md_file)
    add_front_matter(file_path)

print(f"Processed all markdown files in {folder_path} for missing front matter.")
