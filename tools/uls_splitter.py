#!/usr/bin/env python

import argparse
from modules import uls

# Define command-line argument parser
parser = argparse.ArgumentParser(description="Splits combined ULS files")
# Argument for import/input file
parser.add_argument(
    "-i",
    "--in_file",
    metavar="<filename>",
    type=str,
    help="Valid ULS pipe-delimited file to import",
)

args = parser.parse_args()

"""
The combined files seem to be in windows-1252 encoding, so we'll use that
as the default
"""
file_encoding = "windows-1252"

definitions_file = uls.find_definitions_file()

valid_record_types = uls.validate_record_types(definitions_file, file_encoding)

file_type = uls.check_type(args.in_file, valid_record_types, file_encoding)

if file_type == "individual":
    print("individual")
elif file_type == "combined":
    uls.splitter(
        args.in_file, valid_record_types, delimiter="|", file_encoding="windows-1252"
    )
    print("combined")
else:
    raise Exception("No valid record types found")
