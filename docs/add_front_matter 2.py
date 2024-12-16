import os

def add_front_matter_to_md_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if not content.startswith("---"):
                title = os.path.splitext(filename)[0].replace("-", " ").capitalize()
                front_matter = f"---\nlayout: default\ntitle: \"{title}\"\n---\n\n"
                new_content = front_matter + content
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Added front matter to {filename}")
            else:
                print(f"{filename} already has front matter")

directory = '_marbles-md'  # Change this to your directory containing .md files
add_front_matter_to_md_files(directory)

