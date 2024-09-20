import os
import re

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the marbles folder
marbles_folder = os.path.join(script_dir, '../docs/marbles')

# Function to add the magic symbol to links in index files
def add_magic_symbol_to_links(folder_path):
    # Iterate through all files and subdirectories in the marbles folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Process only index.html files
            if file == 'index.html':
                file_path = os.path.join(root, file)
                # print(f'Processing: {file_path}')
                
                # Read the contents of the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Split content into non-header/footer and header/footer parts
                sections = re.split(r'(<header.*?</header>|<footer.*?</footer>)', content, flags=re.DOTALL)
                updated_sections = []
                
                for section in sections:
                    # Only add magic symbols to links in non-header/footer sections
                    if not (section.startswith('<header') or section.startswith('<footer')):
                        updated_section = re.sub(r'<a href="\.\./([^"]*?)">', r'🔮 <a href="../\1">', section)
                        updated_sections.append(updated_section)
                    else:
                        # Leave header/footer sections unchanged
                        updated_sections.append(section)
                
                # Recombine the sections
                updated_content = ''.join(updated_sections)
                
                # Write the updated content back to the file if changes were made
                if content != updated_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    # print('Updated:', file_path)

# Call the function with the path to the marbles folder
add_magic_symbol_to_links(marbles_folder)
print('PYTHON: Added marble symbols within html files')
