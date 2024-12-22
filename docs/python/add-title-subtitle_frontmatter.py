import os
import yaml

# Define the folder containing the markdown files
script_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(script_dir, '../_mms-md')

# Function to extract title and subtitle based on strict rules
def extract_title_and_subtitle(content):
    lines = content.splitlines()
    title = None
    subtitle = None

    # Find the first non-blank line
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:  # Skip blank lines
            continue

        # If the first non-blank line is a title
        if line.startswith('# '):
            title = line[2:].strip()
            # Check if the next line is a subtitle
            if i + 1 < len(lines) and lines[i + 1].startswith('## '):
                subtitle = lines[i + 1][3:].strip()
        break  # Stop after the first non-blank line

    return title, subtitle

# Function to ensure no blank line between YAML and the first heading
def remove_extra_space(content):
    lines = content.splitlines()
    if lines and lines[0] == '':  # Check if the first line after YAML is blank
        return '\n'.join(lines[1:])
    return content

# Function to process a single markdown file
def process_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Check if the file has YAML front matter
    if content.startswith('---'):
        yaml_end = content.find('---', 3)
        if yaml_end == -1:
            raise ValueError(f"Malformed YAML in {file_path}")
        yaml_content = content[3:yaml_end].strip()
        markdown_content = content[yaml_end + 3:].lstrip()  # Remove leading blank lines
        front_matter = yaml.safe_load(yaml_content) or {}
    else:
        front_matter = {}
        markdown_content = content.strip()

    # Extract title and subtitle from the content
    title, subtitle = extract_title_and_subtitle(markdown_content)

    # Update title and subtitle in the front matter
    yaml_needs_update = False

    if title:
        if front_matter.get('title') != title:
            front_matter['title'] = title
            yaml_needs_update = True
    elif 'title' in front_matter:
        del front_matter['title']
        yaml_needs_update = True

    if subtitle:
        if front_matter.get('subtitle') != subtitle:
            front_matter['subtitle'] = subtitle
            yaml_needs_update = True
    elif 'subtitle' in front_matter:
        del front_matter['subtitle']
        yaml_needs_update = True

    if not yaml_needs_update:
        #print(f"File: {file_path}")
        #print("No changes needed.")
        return

    # Print proposed changes
    #print(f"\nFile: {file_path}")
    #print("Proposed YAML front matter:")
    #print(yaml.dump(front_matter, default_flow_style=False).strip())

    # Ensure no extra space between YAML and first heading
    markdown_content = remove_extra_space(markdown_content)

    with open(file_path, 'w', encoding='utf-8') as file:
        # Write updated YAML front matter
        file.write('---\n')
        file.write(yaml.dump(front_matter, default_flow_style=False).strip())
        file.write('\n---\n')
        # Write the markdown content directly after YAML
        file.write(markdown_content)
    #print(f"Changes applied to {file_path}")

# Function to process all markdown files in the folder
def process_all_markdown_files(folder_path):
    # Get all markdown files in the folder
    markdown_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]

    for md_file in markdown_files:
        file_path = os.path.join(folder_path, md_file)
        try:
            process_markdown_file(file_path)
        except Exception as e:
            print(f"Error processing file {file_path} for front matter: {e}")

# Process all markdown files in the folder
process_all_markdown_files(folder_path)
print(f"PYTHON: processed front matters")

