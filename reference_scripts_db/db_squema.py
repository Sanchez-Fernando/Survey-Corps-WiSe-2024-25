# Description: This script lists all tables in the SQLite database and the schema for each table.
import sqlite3
import os

# Get the absolute path to the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_dir, '../MainApp/flights.sqlite')

# Connect to the SQLite database
connection = sqlite3.connect(db_path)

# Create a cursor object
cursor = connection.cursor()

# Query to list all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(f"  - {table[0]}")

# Query the schema for each table
print("\nSchema of each table:")
for table in tables:
    table_name = table[0]
    print(f"\nSchema for '{table_name}':")
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    for column in columns:
        print(f"  - Column: {column[1]}, Type: {column[2]}, Primary Key: {column[5]}")

# Close the connection
connection.close()
