#!/bin/bash

# Check if GNU Parallel is installed
if command -v parallel > /dev/null 2>&1; then
    USE_PARALLEL=true
else
    USE_PARALLEL=false
    echo "GNU Parallel not found. Falling back to sequential processing."
fi

process_dat() {
    zipfile="$1"
    datfile="$2"
    tempdir="$3"
    
    # Assuming zipfile is the variable containing the path to the ZIP file, e.g., "archives/l_coast.zip"
    zipfile_basename=$(basename "$zipfile" .zip) # Extracts "l_coast" from "archives/l_coast.zip"
    sqlite_filename="${zipfile_basename}.sqlite" # Constructs "l_coast.sqlite"

    # Process the .DAT file to append data to the .sqlite file
    python3 uls2sqlite.py -i "$datfile" -o "$tempdir/$sqlite_filename" --encoding=utf-8

    # Remove the processed DAT file
    rm "$datfile"
}

process_zip() {
    zipfile="$1"

    # Create a temporary directory for this zipfile
    tempdir=$(mktemp -d)

    # Extract .DAT files from the ZIP file into the temporary directory
    unzip -j "$zipfile" -d "$tempdir" '*.dat'
    
    if [ $? -ne 0 ]; then
        echo "Failed to extract from $zipfile"
        return
    fi
    
    # Prepare the DAT files for processing
    python3 ./ready_dat_files.py "$tempdir"
    
    if [ $? -ne 0 ]; then
        echo "Failed to prepare .DAT files for processing"
        return
    fi

    # Process .DAT files sequentially
    for datfile in "$tempdir"/*.dat; do
        process_dat "$zipfile" "$datfile" "$tempdir"
    done

    # Move the .sqlite file to the databases directory
    mv "$tempdir"/*.sqlite /databases/

    # Remove the temporary directory
    rm -r "$tempdir"
}

export -f process_dat
export -f process_zip

# Ensure the databases directory exists
mkdir -p databases

#
# If using GNU Parallel, it will spawn a "job" per available CPU core.
# This can consume a great deal of system memory. If you are at all 
# resource constrained, it is recommended to run this sequentially.
#

if $USE_PARALLEL; then
    # Use GNU Parallel to process ZIP files in parallel
    ls ./archives/*.zip | parallel process_zip
else
    # Sequential processing
    for zipfile in ./archives/*.zip; do
        process_zip "$zipfile"
    done
fi

./swap_db.sh
