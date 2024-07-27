#!/bin/bash

# Ensure you are in the project root
cd /Users/lsanten/Documents/GitHub/LSanten.github.io

# Build the Jekyll site
jekyll build --destination docs

# Copy manual files into docs
cp -r manual_files/* docs/

# Commit and push to the repository
git add docs
git commit -m "Deploying site with manual files"
git push origin main


# Execute by running 
# ./build_and_deploy.sh
