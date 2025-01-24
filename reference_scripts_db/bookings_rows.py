# This script was intended for general additions, but Ill keep it like this to show how I added all the rows in the bookings table.
import sqlite3
import os

# Get the absolute path to the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_dir, '../MainApp/flights.sqlite')

# Connect to the SQLite database
connection = sqlite3.connect(db_path)

# Create a cursor object
cursor = connection.cursor()


query = "SELECT * FROM flights;"

# Execute the query
cursor.execute(query)

# Fetch and print the results
rows = cursor.fetchall()

# Rows to insert into the aircrafts table
bookings_data = []

# Get the layout and row_number for each aircraft and create the bookings
for row in rows:
    flight_id, aircraft_code = row
    query = f"SELECT layout, row_number FROM aircrafts WHERE code = '{aircraft_code}';"
    cursor.execute(query)
    aircraft = cursor.fetchone()

    layout, row_number = aircraft
    layout = layout.replace("|", "")
    layout = layout.replace(" ", "")
    # Layout example: "ABC| |DEF", after replacing "|", " " -> "ABCDEF"

    for a in layout:
        for i in range(1, row_number+1):
            bookings_data.append((flight_id, f"{i}{a}", None))





# SQL command to insert data
insert_sql = """
INSERT INTO bookings (flight, seat_number, booker)
VALUES (?, ?, ?);
"""

# Insert each row
for booking in bookings_data:
    cursor.execute(insert_sql, booking)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Rows added to the 'booking' table!")
