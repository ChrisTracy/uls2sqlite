import os
import re
import csv
import tempfile

try:
    from sqlite_utils import Database
except ImportError:
    print("Please install sqlite-utils with: pip install sqlite-utils")
    exit(1)


def parse_definitions_file(definitions_file, encoding="utf-8"):
    """
    Parses SQL file and generates SQLite schema
    :param definitions_file: valid ULS definitions file
    :param encoding: file encoding
    :returns: SQLite schema
    """

    # Read valid ULS definitions file
    with open(definitions_file, "r", encoding=encoding) as f:
        sql_text = f.read()

    # Define regex patterns
    table_pattern = re.compile(r"create table (dbo\..*?)\n(.*?)\n\)", re.DOTALL)
    column_pattern = re.compile(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s.*$", re.MULTILINE)

    # Extract table definitions
    table_matches = table_pattern.findall(sql_text)

    # Build dictionary of table definitions
    table_definitions = {}
    for table_match in table_matches:
        table_name = table_match[0]
        column_definitions = column_pattern.findall(table_match[1])
        table_definitions[table_name] = column_definitions

    # Transform into SQLite schema definitions
    sqlite_schemas = {}
    for table_name, column_names in table_definitions.items():
        sqlite_schemas[table_name] = ", ".join(column_names)

    return sqlite_schemas


def get_record_types_from_table_names(table_names):
    """
    Returns a list of record types from a list of table names
    :param table_names: list of ULS record types
    :returns: list of record types
    """
    record_types = [table_name.split("_")[-1].upper() for table_name in table_names]

    return record_types


def add_definitions_to_file(filename, record_type, definitions, encoding="utf-8"):
    """
    Adds definitions as header to a file
    :param filename: file to add definitions header to
    :param record_type: ULS record type
    :param definitions: ULS definitions
    :param encoding: file encoding
    """

    # Generate file path
    file_path = filename

    # Split definitions into list
    headers = definitions.split(", ")

    # Check if file already exists
    if os.path.isfile(file_path):
        # Read existing data into a list
        with open(file_path, "r", encoding=encoding) as f:
            existing_data = f.readlines()

        # If the file only contains headers, return without overwriting
        if len(existing_data) <= 1:
            return

        # Write headers and existing data to a temporary list
        data_to_write = [headers]

        for line in existing_data:
            data_to_write.append(line.strip().split("|"))  # should set to var

        # Write the combined data back to the file
        with open(file_path, "w", newline="", encoding=encoding) as f:
            writer = csv.writer(f, delimiter="|")  # should set to var
            writer.writerows(data_to_write)
    else:
        # Write headers to new file
        with open(file_path, "w", newline="", encoding=encoding) as f:
            writer = csv.writer(f, delimiter="|")  # should set to var
            writer.writerow(headers)


def insert_csv_to_sqlite(
    db_name, table_name, csv_filename, delimiter="|", encoding="utf-8"
):
    """
    Inserts data from a CSV file into a SQLite database using the sqlite-utils Python module
    :param db_name: Database file name (e.g. test.db)
    :param table_name: SQLite database table name (the record type)
    :param csv_filename: CSV file to import to the SQLite database
    :param delimiter: Delimiter used for the file, default is pipe
    :param encoding: file encoding, default is utf-8
    """

    # Open the CSV file and read data
    with open(csv_filename, "r", encoding=encoding) as csv_file:
        reader = csv.reader(csv_file, delimiter=delimiter)
        data_list = list(reader)

    # Convert list of lists to list of dictionaries for insert_all function
    headers = data_list.pop(0)
    data_dicts = [dict(zip(headers, row)) for row in data_list]

    # Open the SQLite database
    db = Database(db_name)

    # Create the table if not exists and insert data
    table = db[table_name]
    table.insert_all(data_dicts)


def find_definitions_file():
    """
    Checks the definitions sub-directory for definitions file and returns path
    :returns: file path
    """
    search_path = os.path.join(os.getcwd(), "definitions")
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file.endswith(".txt"):
                return os.path.join(root, file)

    raise FileNotFoundError("No .txt file found in the 'definitions' directory")


def splitter(file, valid_record_types, delimiter="|", file_encoding="windows-1252"):
    """
    Takes a 'combined' type file and splits it into files according to the
    record type. For example, if a file contains records HD and AC, two files
    will be created and filled with only those record types.
    :param file: the file to split
    :param delimiter: delimiter to split on, defaults to pipe
    :param file_encoding: the file encoding, defaults to windows-1252
    :returns: Boolean
    """
    files = {}
    with open(file, "r", encoding=file_encoding) as in_file:
        for i, line in enumerate(in_file, start=1):
            fields = line.strip().split(delimiter)
            record_type = fields[0]

            # If the record type is not two letters, or not in valid record types, skip this line
            if (
                len(record_type) != 2
                or not record_type.isalpha()
                or record_type not in valid_record_types
            ):
                continue

            # If we haven't seen this record type before, open a new file
            if record_type not in files:
                # Create the "../temp" directory if it doesn't exist
                temp_path = os.path.join(".", "temp")
                if not os.path.exists(temp_path):
                    os.mkdir(temp_path)

                # Join the directory name with the filename
                filepath = os.path.join(temp_path, f"{record_type}.csv")

                # Open the file in the specified directory
                files[record_type] = open(filepath, "w", encoding=file_encoding)

            # Write the line to the appropriate file
            files[record_type].write(line)

    return files


def check_type(filename, valid_record_types, encoding="utf-8"):
    """
    Scans the file to determine what type of database is being used
    :param filename: the file to check
    :param valid_record_types: the valid ULS record types
    :param encoding: the file encoding
    :returns: type "individual" or "combined"
    """
    unique_values = set()

    with open(filename, "r", encoding=encoding) as file:
        for line in file:
            columns = line.strip().split("|")
            first_column = columns[0]

            # Check if the first column is one of the valid record types
            if first_column in valid_record_types:
                unique_values.add(first_column)

    if len(unique_values) == 1:
        return "individual"
    elif len(unique_values) > 1:
        return "combined"
    else:
        raise Exception("No valid lines found")


def validate_record_types(definitions_file, file_encoding):
    """
    Returns a list of valid record types
    :param definitions_file: the ULS definitions file
    :param file_encoding: the file encoding
    :returns: list of valid record types
    """
    sqlite_schemas = parse_definitions_file(definitions_file, file_encoding)
    valid_record_types = get_record_types_from_table_names(sqlite_schemas.keys())
    return valid_record_types


def export_file(filename, record_type, db_name, file_encoding="windows-1252"):
    """
    Processes a single pipe-delimited database file
    :param filename: the file to process
    :param record_type: the ULS record type
    :param db_name: the ULS database name (e.g. test.db)
    :param file_encoding: the file encoding
    """

    # temporary, this is redundant
    definitions_file = find_definitions_file()
    sqlite_schemas = parse_definitions_file(definitions_file, file_encoding)
    definitions = sqlite_schemas.get(
        f"dbo.PUBACC_{record_type}", "Record type not found"
    )

    # changed from 'definitions' to 'definitions_file'
    add_definitions_to_file(filename, record_type, definitions, file_encoding)
    insert_csv_to_sqlite(db_name, record_type, filename, "|", file_encoding)


def process_file(in_file, db_name, delimiter, file_encoding="windows-1252"):
    """
    Read in a pipe-delimited input file and identify valid lines, then write
    them to a temporary file which is then sent to the export_file() function
    for writing to DB
    :param in_file: the input file
    :param db_name: the ULS database name (e.g. test.db)
    :param delimiter: the delimiter to use
    :param file_encoding: the file encoding
    """

    record_type = os.path.splitext(os.path.basename(in_file))[0]
    definitions_file = find_definitions_file()
    valid_record_types = validate_record_types(definitions_file, file_encoding)

    with tempfile.NamedTemporaryFile(
        suffix=".csv", encoding=file_encoding, mode="w", delete=False
    ) as csv_file:
        with open(in_file, "r", encoding=file_encoding) as file:
            for line in file:
                columns = line.strip().split("|")
                first_column = columns[0]
                # Check if the first column is one of the valid record types
                if first_column in valid_record_types:
                    csv_file.write(line)
    export_file(csv_file.name, record_type, db_name, file_encoding)  # export to DB
    csv_file.close()  # close the file
    os.remove(csv_file.name)  # delete the temporary file
