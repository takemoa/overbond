import argparse
import logging
import os.path

from log_utils import *
from db_utils import *
from parse_utils import parse_record

# Main entry point into this application
if __name__ == '__main__':

    setup_logging()

    # 1. Parse the command line arguments, at least the file path should be provided
    parser = argparse.ArgumentParser(description='Parse the file given as argument and store database into a local '
                                                 'SQL database')
    parser.add_argument('input_file_path', metavar='input_file', type=str,
                        help='The path (absolute or relative to current directory) of the input raw file')
    # input_file_path = '_data/XICE_Bond_Close2.tip'
    args = parser.parse_args()

    # 2. Check that file exist
    if not os.path.isfile(args.input_file_path):
        logging.error(f'Invalid file: {args.input_file_path}')
        exit(1)

    # 3. parse and insert records
    conn = None

    try:
        # 3.1 Parse the file record by record, each record has exactly 10 lines
        with open(args.input_file_path) as f:
            records_count = 0

            # a. Setup database - called only one time
            conn = setup_db()
            if not conn:
                exit(2)  # Unable to create a database connection

            logging.info(f'Processing file {args.input_file_path}')

            source_records = []
            # b. Parse one record (10 rows) into a record dictionary
            source_record = parse_record(f)

            while source_record:
                # Process records in batches
                source_records.append(source_record)
                if len(source_records) >= INSERT_BATCH_SIZE:
                    # c. Now insert the batch intor the database table
                    records_count += insert_records(conn, source_records)
                    source_records.clear()

                # Read next record - if end of file the source_record will be None
                source_record = parse_record(f)

            # insert the remaining source records
            records_count += insert_records(conn, source_records)
            logging.info(f'Successfully inserted {records_count} records')

    finally:
        # Make sure the database connection is closed
        close_db(conn)
