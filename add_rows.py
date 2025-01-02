import sqlite3

# Connect to the SQLite database
db_file = "flights.sqlite"
connection = sqlite3.connect(db_file)

# Create a cursor object
cursor = connection.cursor()

# Rows to insert into the aircrafts table
bookings_data = [] # TODO: Add the rows, you will obviously not do this by hand

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
