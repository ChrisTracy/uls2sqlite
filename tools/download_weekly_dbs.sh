#!/bin/bash

# Create the archives directory if it doesn't exist
mkdir -p ../archives

for url in $(cat weekly_db_urls.txt); do
    # Extract the filename from the URL
    filename=$(basename "$url")

    # Download the file to the archives sub-directory using curl
    # -s: Silent mode, don't show progress or error messages
    # -S: Show error messages if an error occurs
    # -L: Follow redirects
    # -o: Specify output file
    # --progress-bar: Show download progress
    curl -s -S -L --progress-bar "$url" -o "../archives/$filename"

    # Sleep for a random time between 30 seconds and 120 seconds (2 minutes)
    sleep $((30 + RANDOM % 91))
done
