import os
import subprocess
import csv

# Define the directories
script_dir = os.path.dirname(os.path.abspath(__file__))
markdown_dir = os.path.join(script_dir, '../_mms-md/')
csv_output_path = os.path.join(script_dir, '../CSVs/marbleMetaData.csv')

def get_file_metadata(file_path):
    """
    Retrieve creation and modification dates for a file using mdls on macOS.
    """
    creation_date, last_modified_date = None, None

    try:
        # Use mdls to retrieve metadata
        mdls_output = subprocess.run(
            ["mdls", "-name", "kMDItemFSCreationDate", "-name", "kMDItemFSContentChangeDate", file_path],
            capture_output=True, text=True, check=True
        )
        for line in mdls_output.stdout.splitlines():
            if "kMDItemFSCreationDate" in line:
                creation_date = line.split("=")[1].strip()
            elif "kMDItemFSContentChangeDate" in line:
                last_modified_date = line.split("=")[1].strip()
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving metadata for {file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return creation_date, last_modified_date

def process_markdown_files():
    """
    Process all markdown files in the specified directory, retrieve metadata,
    and save it to a CSV file starting at A1.
    """
    if not os.path.exists(markdown_dir):
        print(f"Markdown directory not found: {markdown_dir}")
        return

    metadata_list = []

    # Scan markdown files
    for file_name in os.listdir(markdown_dir):
        if file_name.endswith('.md'):
            file_path = os.path.join(markdown_dir, file_name)
            creation_date, last_modified_date = get_file_metadata(file_path)

            # Extract relative path and marble ID
            relative_path = os.path.relpath(file_path, start=os.path.dirname(csv_output_path))
            marble_id = os.path.splitext(file_name)[0]  # Filename without extension

            metadata_list.append({
                "marble_ID": marble_id,
                "relative_path": relative_path,
                "created": creation_date,
                "last_updated": last_modified_date
            })

    # Write metadata to CSV starting at A1
    with open(csv_output_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["marble_ID", "relative_path", "created", "last_updated"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # Write headers at A1
        writer.writerows(metadata_list)  # Write metadata rows

    print(f"Metadata CSV created at: {csv_output_path}, starting at A1.")

# Run the processing function
process_markdown_files()
