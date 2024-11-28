import os
import subprocess
import csv

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '../CSVs/marbleMetaData.csv')
older_folder = '/Users/lsanten/Documents/GitHub/LSanten.github.io2/_mms-md'

print("Script started...")

print(f"CSV Path: {csv_path}")
print(f"Older Folder: {older_folder}")

print(f"Testing access to CSV: {os.path.exists(csv_path)}")
print(f"Testing access to older folder: {os.path.exists(older_folder)}")

def get_creation_date(file_path):
    """
    Retrieve creation date for a file using mdls on macOS.
    """
    try:
        mdls_output = subprocess.run(
            ["mdls", "-name", "kMDItemFSCreationDate", file_path],
            capture_output=True, text=True, check=True
        )
        for line in mdls_output.stdout.splitlines():
            if "kMDItemFSCreationDate" in line:
                return line.split("=")[1].strip()
    except Exception as e:
        print(f"Error retrieving creation date for {file_path}: {e}")
    return None

def update_csv_with_older_files():
    """
    Updates an existing CSV by comparing it with markdown files from an older folder.
    If an older creation date is found, updates the entry. Adds new entries for files not present.
    """
    rows = []
    fieldnames = []

    # Load the existing CSV data
    with open(csv_path, 'r', newline='', encoding='utf-8') as csv_file:
        data_reader = csv.DictReader(csv_file)
        rows = list(data_reader)
        fieldnames = data_reader.fieldnames
        print(f"Total rows read from CSV: {len(rows)}")
        print(f"Fieldnames: {fieldnames}")

    # Ensure the `found_in_older_1` column exists
    if 'found_in_older_1' not in fieldnames:
        fieldnames.append('found_in_older_1')

    # Track which IDs are already in the CSV
    existing_ids = {row['marble_ID'] for row in rows}
    print(f"Existing marble_IDs in CSV: {existing_ids}")

    # Scan the older folder
    older_files = [f for f in os.listdir(older_folder) if f.endswith('.md')]
    print(f"Markdown files in the older folder: {older_files}")

    for file_name in older_files:
        marble_id = os.path.splitext(file_name)[0]
        older_file_path = os.path.join(older_folder, file_name)
        older_creation_date = get_creation_date(older_file_path)
        print(f"Processing file: {file_name}, marble_ID: {marble_id}, creation date: {older_creation_date}")

        if marble_id in existing_ids:
            # Compare and update if necessary
            for row in rows:
                if row['marble_ID'] == marble_id:
                    current_creation_date = row['created']
                    if older_creation_date and older_creation_date < current_creation_date:
                        row['created'] = older_creation_date
                        row['found_in_older_1'] = 'YES'
                        print(f"Updated {marble_id}: created date changed to {older_creation_date}")
                    break
        else:
            # Add new entry for missing files
            rows.append({
                'marble_ID': marble_id,
                'relative_path': os.path.relpath(older_file_path, start=os.path.dirname(csv_path)),
                'created': older_creation_date,
                'last_updated': '',  # Leave blank as we don't have this info for new entries
                'found_in_older_1': 'NEW'
            })
            print(f"Added new entry for {marble_id} with creation date {older_creation_date}")

    # Save the updated CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV updated successfully: {csv_path}")

try:
    update_csv_with_older_files()
except Exception as e:
    print(f"Error: {e}")
