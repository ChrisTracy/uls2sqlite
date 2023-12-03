#!/bin/bash

# Check if the database filename is provided
if [ -z "$1" ]; then
  echo "Please provide the database filename as the first argument."
  exit 1
fi

# Store the provided database filename
db_filename="$1"

# Loop through all .CSV files in the "temp" sub-directory
for csv_file in ./temp/*.csv; do
  # Run the Python command with the current CSV file as an input and the provided database filename as an output
  python3 uls2sqlite.py -i "$csv_file" -o "$db_filename" --encoding=windows-1252
  rm $csv_file # Remove the CSV file that has been processed and is no longer needed
done
