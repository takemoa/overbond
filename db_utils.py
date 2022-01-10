import logging
import sqlite3

from config import *


# Set up a local sql lite 3 database
# If the database does not exist one is created based on the configuration values
# Also dynamically creates the required table and indexes (if they are not created
def setup_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        logging.info(f"Database created and successfully connected to: {DB_NAME}")

        cursor.execute("select sqlite_version();")
        record = cursor.fetchall()
        logging.info(f"SQLite Database Version is: {record}")
        cursor.close()

        try:
            create_bond_table(conn)
        except sqlite3.Error as error:
            logging.error("Error while creating sqlite table", error)
            # In case of any exception close the connection and return null
            conn.close()
            conn = None

        return conn

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)


# Create bonds table and indexes if they do not already exist not exist
def create_bond_table(conn):
    # Dynamically create the SQL
    sql_table = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}( \n'
    sql_pk = '\tPRIMARY KEY ('
    sql_indexes = []
    first_pk = True

    for col_name, field_config in DATA_CONFIG.items():
        sql_table += f'  {col_name}'

        col_type = field_config['type']
        if col_type == 'int':
            sql_table += ' INTEGER'
        elif col_type == 'float':
            sql_table += ' REAL'
        elif col_type == 'date':
            sql_table += ' DATETIME'
        else:
            sql_table += ' TEXT'

        # Is colum a primary key?
        if field_config.get('pk'):
            if first_pk:
                sql_pk += col_name
                first_pk = False
            else:
                sql_pk += f', {col_name}'
        # Is column not null
        if field_config.get('notnull'):
            sql_table += ' NOT NULL'
        # Is it indexable
        if field_config.get('index'):
            sql_indexes.append(f'CREATE INDEX IF NOT EXISTS {TABLE_NAME}_{col_name}_index ON {TABLE_NAME}({col_name})')
        sql_table += ',\n'

    sql_table += sql_pk
    sql_table += ')\n)'

    logging.debug(f'SQL CREATE TABLE: \n{sql_table}')
    logging.debug(f'SQL CREATE INDEX: \n{sql_indexes}')

    # Execute create table and index statements
    cursor = conn.cursor()
    cursor.execute(sql_table)
    for sql_index in sql_indexes:
        cursor.execute(sql_index)
    conn.commit()

    # GET THE NUMBER OF RECORDS IN THE TABLE
    cursor.execute(f'SELECT COUNT(*) FROM {TABLE_NAME}')
    logging.info(f'{TABLE_NAME} table is setup - {cursor.fetchone()} existing records')

    cursor.close()


# Global variables used in insert_records
cols = ','.join(DATA_CONFIG.keys())
vals_qm = ','.join('?' * len(DATA_CONFIG))
# The insert SQL command
insert_sql = f'INSERT INTO {TABLE_NAME}\n  ({cols}) \n VALUES({vals_qm})'


# Insert new records in the bonds table only if the records do not already exist
def insert_records(conn, source_records):
    if not source_records:
        return 0  # nothing to insert

    logging.debug(f'SQL INSERT:\n {insert_sql}')

    count = 0
    cursor = conn.cursor()
    for source_record in source_records:
        # binding values for the insert sql
        record_values = [source_record.get(k) for k in DATA_CONFIG.keys()]
        # Do Insert the record
        try:
            cursor.execute(insert_sql, record_values)
            count += 1
            logging.debug(f"Successfully inserted:\n {record_values}")
        except sqlite3.Error as error:
            if str(error).startswith('UNIQUE constraint failed'):
                logging.debug(f'Record already exists: {record_values}')
            else:
                logging.warning(f'Error while inserting record {error}')

    # Commit at the end and close the cursor
    conn.commit()
    cursor.close()

    logging.info(f'- {count} records')
    return count


# Safe close the connection
def close_db(conn):
    if conn:
        conn.close()
