# Description: Use this script for simple queries.
import sqlite3

# Path to the SQLite file (same folder as the script)
db_file = 'flights.sqlite'  

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Define your SQL query (e.g., selecting two columns)
query = "SELECT * FROM users"
#query = "UPDATE users SET user_type = 'regular' WHERE username = 'emmaW' or username = 'weltgeist';"

# Execute the query
cursor.execute(query)

# Fetch and print the results
rows = cursor.fetchall()


for row in rows:
    print(row)
    #query = f"UPDATE aircrafts SET layout = 'ABC| |DEF' WHERE code = '321';"

# Close the connection
#conn.commit() # For updates
conn.close()

