import os
import subprocess
import yaml
from datetime import datetime, timezone

# Folder containing markdown files
markdown_folder = "/Users/lsanten/Documents/GitHub/LSanten.github.io/_mms-md"

# Required fields and their default values
REQUIRED_FIELDS = {
    "date_created": "calculate",  # Calculate from file creation date if missing
    "date_lastchanged": "calculate",  # Calculate from file last modification date if missing
    "show_date_lastchanged_updatedauto": "YES, NO, NO"
}

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

def ensure_yaml_frontmatter(file_path):
    """
    Ensure the YAML front matter of a markdown file contains the required fields.
    Automatically update files with 'null' dates using file system metadata.
    """
    try:
        # Read the file content
        with open(file_path, "r") as f:
            content = f.read()

        # Parse the YAML front matter and body
        if content.startswith("---"):
            parts = content.split("---", 2)
            frontmatter = yaml.safe_load(parts[1]) if len(parts) > 2 else {}
            body = parts[2].lstrip() if len(parts) > 2 else ""
        else:
            frontmatter = {}
            body = content.strip()

        # Retrieve dates from front matter
        creation_date = frontmatter.get("date_created")
        modified_date = frontmatter.get("date_lastchanged")

        # Check for 'null' dates and update from file metadata if needed
        if creation_date == "null" or creation_date is None or modified_date == "null" or modified_date is None:
            print(f"Updating file with null dates: {file_path}")

            # Retrieve file creation/modification dates using mdls
            file_creation_date, file_modified_date = get_file_dates(file_path)
            file_creation_date = convert_to_local_time(file_creation_date) if file_creation_date else None
            file_modified_date = convert_to_local_time(file_modified_date) if file_modified_date else None

            # Update the front matter fields with retrieved dates
            if creation_date == "null" or creation_date is None:
                frontmatter["date_created"] = file_creation_date
            if modified_date == "null" or modified_date is None:
                frontmatter["date_lastchanged"] = file_modified_date

        # Add or update other required fields
        for field, default_value in REQUIRED_FIELDS.items():
            if field not in frontmatter or frontmatter[field] == "null":
                if field == "date_created":
                    frontmatter[field] = creation_date
                elif field == "date_lastchanged":
                    frontmatter[field] = modified_date
                else:
                    frontmatter[field] = default_value

        # Reconstruct the content with updated YAML front matter
        yaml_content = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True).strip()
        updated_content = f"---\n{yaml_content}\n---\n{body}"

        # Write the updated content only if changes were made
        if content.strip() != updated_content.strip():
            print(f"Writing updated content to: {file_path}")
            with open(file_path, "w") as f:
                f.write(updated_content)

    except Exception as e:
        print(f"Error ensuring YAML front matter for {file_path}: {e}")





def main():
    # Process markdown files
    for filename in os.listdir(markdown_folder):
        if filename.endswith(".md"):
            file_path = os.path.join(markdown_folder, filename)
            ensure_yaml_frontmatter(file_path)

if __name__ == "__main__":
    main()
