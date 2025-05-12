#!/bin/bash

# Script to comment out image references in Markdown files
# This will allow Docusaurus to run without errors

# Create the image directory if it doesn't exist
mkdir -p static/img/docs

# Create a single placeholder image
echo "Creating placeholder image..."
convert -size 300x200 xc:lightblue -gravity center -pointsize 20 -annotate 0 "Placeholder Image" static/img/docs/placeholder.png

# Find all Markdown files and process them
find docs -name "*.md" | while read file; do
  echo "Processing $file..."
  # Replace image references with commented versions
  sed -i 's/!\[.*\](\/img\/docs\/.*\.png)/<!-- Image temporarily removed -->/' "$file"
done

echo "Done! All image references have been commented out."
