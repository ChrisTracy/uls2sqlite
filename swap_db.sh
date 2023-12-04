#!/bin/bash

# Set the path to the folder
folder_path="/databases"

# Get today's date in the format YYYY-MM-DD
today_date=$(date +"%Y-%m-%d")

# Check if the folder exists
if [ ! -d "$folder_path" ]; then
    echo "Error: Folder $folder_path not found."
    exit 1
fi

# Check if the db.sqlite file exists and its size is at least 700MB
db_sqlite="$folder_path/db.sqlite"
random_sqlite=$(find "$folder_path" -maxdepth 1 -type f -name "*.sqlite" ! -name "db.sqlite" | head -n 1)

if [ -f "$db_sqlite" ] && [ "$(stat -c%s "$db_sqlite")" -ge 700000000 ]; then
    # Rename db.sqlite to [todays_date].sqlite
    mv "$db_sqlite" "$folder_path/$today_date.sqlite"
    
    # Check if the random file exists and its size is at least 700MB
    if [ -n "$random_sqlite" ] && [ "$(stat -c%s "$random_sqlite")" -ge 700000000 ]; then
        # Rename the random file to db.sqlite
        mv "$random_sqlite" "$folder_path/db.sqlite"
        echo "Random sqlite file renamed to db.sqlite."
        
        # Create the archive subfolder if it doesn't exist
        archive_folder="$folder_path/archive"
        mkdir -p "$archive_folder"

        # Move the renamed db.sqlite to archive
        mv "$folder_path/$today_date.sqlite" "$archive_folder/"
        echo "Renamed db.sqlite moved to archive as $today_date.sqlite."
    else
        echo "Error: No valid random sqlite file found or its size is less than 700MB."
        exit 1
    fi
    
    echo "Files renamed successfully."
else
    echo "Error: db.sqlite does not exist or its size is less than 700MB."
    exit 1
fi
