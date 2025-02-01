# Description: Use this script for simple queries.
import sqlite3
import os

# Get the absolute path to the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_dir, '../MainApp/flights.sqlite')

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

user_data = ("Emma Woodhouse", "regular")
# Define your SQL query (e.g., selecting two columns)
query = f"SELECT * FROM bookings;"
#query = "UPDATE users SET user_type = 'regular' WHERE username = 'emmaW' or username = 'weltgeist';"

# Execute the query
cursor.execute(query) # (query, user_data)

# Fetch and print the results
rows = cursor.fetchall()


for row in rows:
    print(row)
    #query = f"UPDATE aircrafts SET layout = 'ABC| |DEF' WHERE code = '321';"

# Close the connection
#conn.commit() # For updates
conn.close()

