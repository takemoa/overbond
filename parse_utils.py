import logging

from datetime import datetime

from config import *


# Attempt to match a tag value to a field based on prefix and the record row
# It receives the tag value, a fields configuration dictionary (as setup in config) and the current row (0 based)
# in the record
# Returns field name and parsed value if a match or None otherwise
def match_value(value: str, fields_dict: dict, row: int):
    keys, values = [], []
    # Loop through the fields configuration
    for key, field in fields_dict.items():
        # check the row requirements
        req_rows = field.get('rows')
        if req_rows and row not in req_rows:
            # does not match the required row, go to the next value
            continue

        # Check if the prefix matches
        if value.startswith(field['prefix']):
            try:
                # extract the actual value
                _value = value[len(field['prefix']):]

                # Convert from string to the required datatype: date, float, int
                if field['type'] == 'date':
                    # parse date
                    _value = datetime.strptime(_value, '%Y%m%d')
                elif field['type'] == 'float':
                    # parse value into a number
                    _value = float(_value)
                elif field['type'] == 'int':
                    # parse value into a number
                    _value = int(_value)

                # Return the parsed value
                keys.append(key)
                values.append(_value)
            except Exception as e:
                logging.warning(f'Field {key} has unexpected value {value}', e)

    # No match was found
    return keys, values


# Parse a record composed of 10 rows from the file identified by a file pointer
# The required fields of the records are configured in config.DATA_CONFIG dictionary
def parse_record(fp):
    # Make a copy of the fields' config dictionary to remove from it as we go
    _fields_dict = DATA_CONFIG.copy()
    record_fields = {}

    # Each record has 10 lines
    logging.debug('Parsing a new record')
    for row_i in range(10):
        # read line by line
        line = fp.readline()
        if not line:
            # No more records
            return None

        # split into values, values are semicolon separated
        values = line.split(';')

        # Attempt to match each individual value against the configuration fields
        for value in values:
            field_keys, field_values = match_value(value, _fields_dict, row_i)
            for field_key, field_value in zip(field_keys, field_values):
                # we have a value match
                record_fields[field_key] = field_value
                # remove field from dictionary
                del _fields_dict[field_key]

        if not _fields_dict:
            # no more fields left to parse, exit for loop
            break

        logging.debug(f'- row {row_i}: {values}')

    logging.debug(f'- parsed fields:\n {record_fields}')
    logging.debug(f'- fields not found: {list(_fields_dict.keys())}')

    return record_fields
