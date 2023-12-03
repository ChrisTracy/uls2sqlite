#!/bin/bash

# Create the archives directory if it doesn't exist
mkdir -p ../archives

# Assuming weekly_db_urls.txt is now in the config folder
config_folder="../config"
url_file="$config_folder/weekly_db_urls.txt"

for url in $(cat "$url_file"); do
    # Extract the filename from the URL
    filename=$(basename "$url")

    # Download the file to the archives sub-directory using curl
    curl -s -S -L --progress-bar "$url" -o "../archives/$filename"

    # Sleep for a random time between 30 seconds and 120 seconds (2 minutes)
    sleep $((30 + RANDOM % 91))
done

# Process Zip Files after all downloads are completed
./process_zip_files.sh

