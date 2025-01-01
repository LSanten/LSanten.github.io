import os
import subprocess
import yaml
from datetime import datetime, timezone
import csv

# Paths
csv_file = "/Users/lsanten/Documents/GitHub/LSanten.github.io/CSVs/marbleMetaData_updated.csv"
markdown_folder = "/Users/lsanten/Documents/GitHub/LSanten.github.io/_mms-md"

def convert_to_local_time(utc_time_str):
    """
    Convert UTC time string to local time and return only the date (YYYY-MM-DD).
    """
    try:
        # Parse the UTC time string
        utc_time = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S +0000")
        # Convert to local time
        local_time = utc_time.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return local_time.strftime("%Y-%m-%d")  # Return only the date part
    except Exception as e:
        print(f"Error converting time: {e}")
        return None  # Return None if conversion fails


def get_file_dates(file_path):
    """
    Retrieve creation and modification dates for a file using mdls on macOS.
    """
    try:
        mdls_output = subprocess.run(
            ["mdls", "-name", "kMDItemFSCreationDate", "-name", "kMDItemFSContentChangeDate", file_path],
            capture_output=True, text=True, check=True
        )
        creation_date, modified_date = None, None
        for line in mdls_output.stdout.splitlines():
            if "kMDItemFSCreationDate" in line:
                creation_date = line.split("=")[1].strip()
            elif "kMDItemFSContentChangeDate" in line:
                modified_date = line.split("=")[1].strip()
        return creation_date, modified_date
    except Exception as e:
        print(f"Error retrieving dates for {file_path}: {e}")
    return None, None

def update_yaml_frontmatter(file_path, metadata):
    """
    Update the YAML front matter of a markdown file.
    Ensure no extra line break after the YAML front matter.
    """
    try:
        with open(file_path, "r") as f:
            content = f.read()
        
        # Check if front matter exists
        if content.startswith("---"):
            parts = content.split("---", 2)
            frontmatter = yaml.safe_load(parts[1]) if len(parts) > 2 else {}
            body = parts[2].lstrip() if len(parts) > 2 else ""
        else:
            frontmatter = {}
            body = content.strip()

        # Update or add required fields
        frontmatter["date_created"] = metadata.get("date_created")
        frontmatter["date_lastchanged"] = metadata.get("date_lastchanged")
        frontmatter["show_date_lastchanged_updatedauto"] = "YES, NO, NO"
        
        # Reconstruct the YAML front matter and ensure no trailing blank lines
        yaml_content = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True).strip()
        updated_content = f"---\n{yaml_content}\n---\n{body}"

        # Write back the updated content
        with open(file_path, "w") as f:
            f.write(updated_content)

    except Exception as e:
        print(f"Error updating YAML front matter for {file_path}: {e}")



def main():
    # Load CSV data
    csv_data = {}
    with open(csv_file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_data[row["marble_ID"]] = {
                "date_created": row["created"],
                "date_lastchanged": row["last_updated"]
            }
    
    # Process markdown files
    for filename in os.listdir(markdown_folder):
        if filename.endswith(".md"):
            file_path = os.path.join(markdown_folder, filename)
            file_id = os.path.splitext(filename)[0]
            
            if file_id in csv_data:
                # Use data from CSV
                metadata = csv_data[file_id]
            else:
                # Use file dates and convert to local time
                creation_date, modified_date = get_file_dates(file_path)
                metadata = {
                    "date_created": convert_to_local_time(creation_date) if creation_date else None,
                    "date_lastchanged": convert_to_local_time(modified_date) if modified_date else None
                }
            
            # Update YAML front matter
            update_yaml_frontmatter(file_path, metadata)

if __name__ == "__main__":
    main()
