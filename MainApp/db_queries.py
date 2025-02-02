import sqlite3
import os

# Get the absolute path to the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_dir, 'flights.sqlite')

def gimme_tuples(table, columns='*', identifier=None):
    """
    Requests all rows from a table in the database.
    
    :param table: The name of the table to query.
    :param columns='*': The columns to select from the table. Default is all columns.
    :param identifier=None: A dictionary with the column names and values to filter the rows.
    """
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if identifier is not None:
        where_clause = "AND ".join([f"{col} = ?" for col in identifier.keys()])
        query = f"SELECT {columns} FROM {table} WHERE {where_clause};"
        cursor.execute(query, tuple(identifier.values()))
    else:
        query = f"SELECT {columns} FROM {table};"
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

def update_row(table, old_values, new_values):
    
    if old_values is not None and new_values is not None:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        where_clause = "AND ".join([f"{col} = ?" for col in old_values.keys()])
        set_clause = ", ".join([f"{col} = ?" for col in new_values.keys()])

        # Combine parameters: SET values first, THEN WHERE values
        params = tuple(list(new_values.values()) + list(old_values.values()))

        # Build the query
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause};"

        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True
    return False

def insert_row(table, values):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    columns = ', '.join(values.keys())
    placeholders = ', '.join(['?'] * len(values))

    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"

    cursor.execute(query, tuple(values.values()))
    conn.commit()
    conn.close()

def delete_row(table, values):
    pass
