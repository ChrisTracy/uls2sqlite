#!/bin/bash

# Set the path to the folder
folder_path="/databases"

# Check if the folder exists
if [ ! -d "$folder_path" ]; then
    echo "Error: Folder $folder_path not found."
    exit 1
fi

# Look for the random sqlite file exists
random_sqlite=$(find "$folder_path" -maxdepth 1 -type f -name "*.sqlite" ! -name "db.sqlite" | head -n 1)
    
# Check if the random file exists and its size is at least 700MB
if [ -n "$random_sqlite" ] && [ "$(stat -c%s "$random_sqlite")" -ge 700000000 ]; then

    db_sqlite="$folder_path/db.sqlite"
    
    # Get today's date in the format YYYY-MM-DD
    today_date=$(date +"%Y-%m-%d")
    
    # Rename the random file to db.sqlite
    mv "$db_sqlite" "$folder_path/$today_date.sqlite"
    mv "$random_sqlite" "$folder_path/db.sqlite"
    echo "Random sqlite file renamed to db.sqlite."
    
    # Create the archive subfolder if it doesn't exist
    archive_folder="$folder_path/archive"
    mkdir -p "$archive_folder"

    # Move the renamed db.sqlite to archive
    mv "$folder_path/$today_date.sqlite" "$archive_folder/"
    echo "Renamed db.sqlite moved to archive as $today_date.sqlite."
    exit 0
else
    echo "Error: No valid random sqlite file found or its size is less than 700MB."
    exit 1
fi
