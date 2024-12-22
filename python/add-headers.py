import os
import yaml

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the _mms-md folder relative to the script directory
folder_path = os.path.join(script_dir, '../_mms-md')

# Function to check and add YAML front matter
def ensure_layout_front_matter(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        
        if content.startswith('---'):  # Check if YAML front matter exists
            yaml_end = content.find('---', 3)
            if yaml_end == -1:
                raise ValueError(f"Malformed YAML in {file_path}")
            
            # Parse the YAML block
            yaml_content = content[3:yaml_end].strip()
            front_matter = yaml.safe_load(yaml_content) or {}
            
            # Add 'layout: default' if not present
            if 'layout' not in front_matter:
                #print(f"Adding 'layout: default' to existing YAML in {file_path}")
                front_matter['layout'] = 'default'
                
                # Rewrite the file with updated YAML
                updated_yaml = yaml.dump(front_matter, default_flow_style=False).strip()
                file.seek(0)
                file.write(f"---\n{updated_yaml}\n---\n{content[yaml_end + 3:].strip()}\n")
                file.truncate()
        else:
            # No YAML front matter; add a new block
            #print(f"Adding new YAML front matter to {file_path}")
            front_matter = {"layout": "default"}
            updated_yaml = yaml.dump(front_matter, default_flow_style=False).strip()
            file.seek(0)
            file.write(f"---\n{updated_yaml}\n---\n\n{content}")
            file.truncate()

# Collect all markdown files in the folder
md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]

# Process each markdown file
for md_file in md_files:
    file_path = os.path.join(folder_path, md_file)
    ensure_layout_front_matter(file_path)

print(f"PYTHON: Processed all markdown files in {folder_path} for front matter.")
