# Description: Use this script for simple queries.
import sqlite3

# Path to the SQLite file (same folder as the script)
db_file = 'flights.sqlite'  # Replace with your SQLite file name

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Define your SQL query (e.g., selecting two columns)
query = "SELECT DISTINCT * FROM aircrafts;"

# Execute the query
cursor.execute(query)

# Fetch and print the results
rows = cursor.fetchall()

#i = 0 # Counter for the number of displayed rows
for row in rows:
    print(row)
    #if i == 100:
        #break
    #i += 1

# Close the connection
conn.close()

# TODO: crear una tabla con los asientos reservados de los vuelos, usando el esquema de chatGPT