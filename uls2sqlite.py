#!/usr/bin/env python

import argparse
import os
import tempfile
from modules import uls

# Define command-line argument parser
parser = argparse.ArgumentParser(description="Example program with -file option")
# Argument for import/input file
parser.add_argument(
    "-i",
    "--in_file",
    metavar="<filename>",
    type=str,
    help="Valid FCC ULS pipe-delimited file to import",
)
# Argument for export file
parser.add_argument(
    "-o",
    "--out_file",
    metavar="<filename>",
    type=str,
    help="SQLite database file to export data to",
)
# Argument to change the file encoding
parser.add_argument(
    "-e",
    "--encoding",
    help="File encoding",
)

args = parser.parse_args()

file_encoding = "utf-8"  # "windows-1252" and "utf-8" have been observed

if args.encoding:
    file_encoding = args.encoding

db_name = args.out_file
delimiter = "|"

# Process the ULS file and export it to an SQLite database file
if args.in_file:
    uls.process_file(args.in_file, db_name, delimiter, file_encoding)
