# Description: Self explanatory.
import sqlite3

# Connect to the SQLite database
db_file = "flights.sqlite"
connection = sqlite3.connect(db_file)
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
