# Description: This script modifies the schema of a table in the database.
import sqlite3

# Connect to the SQLite database
db_file = "flights.sqlite"
connection = sqlite3.connect(db_file)
cursor = connection.cursor()


# Step 1: Create the new table with the updated schema
cursor.execute("""
CREATE TABLE IF NOT EXISTS aircrafts_new (
    code TEXT PRIMARY KEY,
    layout TEXT,
    row_number INTEGER
);
""")
print("New table 'aircrafts_new' created with updated schema.")

# Step 2: Copy data from the old table to the new table
try:
    cursor.execute("""
    INSERT INTO aircrafts_new (code, row_number)
    SELECT code, rows FROM aircrafts;
    """)
    print("Data copied from 'aircrafts' to 'aircrafts_new'.")
except sqlite3.IntegrityError as e:
    print(f"Error copying data: {e}")
    connection.rollback()
    connection.close()
    exit()

# Step 3: Drop the oldtable
cursor.execute("DROP TABLE aircrafts;")
print("Old table 'aircrafts' dropped.")

# Step 4: Rename the new table
cursor.execute("ALTER TABLE aircrafts_new RENAME TO aircrafts;")
print("Table 'aircrafts_new' renamed to 'aircrafts'.")

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Schema updated: 'aircrafts' table modified successfully.")
