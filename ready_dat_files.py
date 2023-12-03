'''
This small script can be used to prep .DAT files for use with the ULS2SQLite tool. It will convert all .DAT filenames to upper-case, and
convert the file extensions to lower-case.
'''

import os
import argparse

parser = argparse.ArgumentParser(description='Process .DAT files in the specified directory.')
parser.add_argument('directory', type=str, help='The directory to process .DAT files in.')
    
args = parser.parse_args()

for filename in os.listdir(args.directory):
    if filename.endswith('.DAT') or filename.endswith('.dat'):
        base, ext = os.path.splitext(filename)
        new_name = base.upper() + ext.lower()
        os.rename(os.path.join(args.directory, filename), os.path.join(args.directory, new_name))
