#!/bin/bash

# Ensure you are in the project root
cd /Users/lsanten/Documents/GitHub/LSanten.github.io

# Run python scripts to scan _mms-md folder

python3 python/generate-all-file.py # Generate file called ALL.md that contains a list of all .md files in the folder
python3 python/add-headers.py # Add headers with template = default settings if it doesn't exist (needs to be after the generate-all-file)
python3 python/add-title-subtitle_frontmatter.py # Add title and subtitle to YAML and update changes


# Build the Jekyll site
jekyll build --destination docs

# Copy manual files into docs
cp -r manual_files/* docs/

# Add magic symbol to internal links
python3 python/add-magic-symbol.py # Add headers with template settings if it doesn't exist (needs to be after the generate-all-file)

# Commit and push to the repository
#git add docs
#git commit -m "Deploying site with manual files"
#git push origin main


# Execute by running 
# ./build_and_deploy.sh
