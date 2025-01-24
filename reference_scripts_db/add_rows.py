# Description: Self explanatory.
import sqlite3
import os

# Get the absolute path to the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_dir, '../MainApp/flights.sqlite')

# Connect to the SQLite database"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Insert a row into a table
insert_query = """
INSERT INTO users (username, name, password, user_type)
VALUES (?, ?, ?, ?);
"""
data = ('weltgeist', 'Georg Wilhelm Friedrich Hegel', 11111115, 'regular')

try:
    cursor.execute(insert_query, data)
    connection.commit()  # Commit the transaction
    print("Row inserted successfully!")
except sqlite3.IntegrityError as e:
    print(f"Error inserting row: {e}")
finally:
    connection.close()
