import subprocess

def get_file_dates(file_path):
    """
    Retrieve the actual creation and last modified dates for a file using mdls on macOS.
    """
    creation_date = None
    modified_date = None

    try:
        mdls_output = subprocess.run(
            ["mdls", "-name", "kMDItemContentCreationDate", "-name", "kMDItemFSContentChangeDate", file_path],
            capture_output=True, text=True, check=True
        )
        for line in mdls_output.stdout.splitlines():
            if "kMDItemContentCreationDate" in line:
                creation_date = line.split("=")[1].strip()
            elif "kMDItemFSContentChangeDate" in line:
                modified_date = line.split("=")[1].strip()
    except Exception as e:
        print(f"Error retrieving dates for {file_path}: {e}")
    
    return creation_date, modified_date

if __name__ == "__main__":
    file_path = "/Users/lsanten/Documents/GitHub/LSanten.github.io/_mms-md/PERSONAL-VALUE-SYSTEM.md"
    creation_date, modified_date = get_file_dates(file_path)

    if creation_date:
        print(f"Creation date for '{file_path}': {creation_date}")
    else:
        print(f"Could not retrieve creation date for '{file_path}'.")

    if modified_date:
        print(f"Last modified date for '{file_path}': {modified_date}")
    else:
        print(f"Could not retrieve last modified date for '{file_path}'.")
