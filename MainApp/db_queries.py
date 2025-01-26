import sqlite3
import os

# Get the absolute path to the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_dir, 'flights.sqlite')

#TODO: Modify to check for all keys and values in the dictionary, like is_in_table
def gimme_tuples(table, columns='*', identifier=None):
    """
    Requests all rows from a table in the database.
    
    :param table: The name of the table to query.
    :param columns='*': The columns to select from the table. Default is all columns.
    :param identifier=None: A dictionary with the column names and values to filter the rows.
    """
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = f"SELECT {columns} FROM {table};"
    if identifier is not None:
        query = f"SELECT {columns} FROM {table} WHERE username = '{identifier['username']}';"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return rows

def is_in_table(table, values):
    """
    Checks if a row with specific values exists in a table.

    :param values: A dictionary where keys are column names and values are the values to check.
    :param table: The name of the table to check.
    :return: True if the row exists, False otherwise.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Construct the WHERE clause
    where_clause = " AND ".join([f"{col} = ?" for col in values.keys()])
    query = f"SELECT 1 FROM {table} WHERE {where_clause} LIMIT 1;"

    # Execute the query with the values
    cursor.execute(query, tuple(values.values()))
    result = cursor.fetchone()

    conn.close()

    return result is not None

def update_row(table, values):
    pass

def delete_row(table, values):
    pass
