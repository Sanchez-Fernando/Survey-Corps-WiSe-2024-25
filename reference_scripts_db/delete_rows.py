# DONT run this script
import sqlite3
import os

# Get the absolute path to the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_dir, '../MainApp/flights.sqlite')

# Specify the condition for deletion
condition = {'flight_number': 'AA123', 'departure_date': '2024-12-25'}

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Construct the WHERE clause
where_clause = " AND ".join([f"{col} = ?" for col in condition.keys()])
query = f"DELETE FROM ;"

# Execute the query with the values
cursor.execute(query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Rows deleted successfully.")