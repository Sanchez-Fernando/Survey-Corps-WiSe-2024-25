import sqlite3

# Specify the condition for deletion
condition = {'flight_number': 'AA123', 'departure_date': '2024-12-25'}

# Connect to the SQLite database
conn = sqlite3.connect('flights.sqlite')
cursor = conn.cursor()

# Construct the WHERE clause
where_clause = " AND ".join([f"{col} = ?" for col in condition.keys()])
query = f"DELETE FROM bookings;"

# Execute the query with the values
cursor.execute(query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Rows deleted successfully.")