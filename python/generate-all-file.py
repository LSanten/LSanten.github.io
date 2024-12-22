import os
import re

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the _mms-md folder relative to the script directory
folder_path = os.path.join(script_dir, '../_mms-md')
output_file = os.path.join(script_dir, '../_mms-md/ALL.md')

# Function to extract the first title from a markdown file
def extract_first_title(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r'^#\s+(.*)', line)
            if match:
                return match.group(1)
    return "No Title"

# Collect all markdown files in the folder
md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
md_files.sort(key=lambda f: f.lower())  # Sort files alphabetically, case insensitive

# Generate the output content
output_content = ""
for md_file in md_files:
    file_path = os.path.join(folder_path, md_file)
    title = extract_first_title(file_path)
    filename = os.path.splitext(md_file)[0]
    output_content += f"- [[{filename}]] - {title}\n"

# Write the output content to the all.md file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(output_content)
    file.write("\n\n#excludeFromGraph (to filter out write -tag:)")  # Add this line to append the tag at the end

print(f"PYTHON: Generated {output_file} with the list of markdown files and their first titles.")

