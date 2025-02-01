import sqlite3
import os

# Get the absolute path to the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_dir, '../MainApp/flights.sqlite')

# Parameters for the update
flight_id = 1  # The ID of the flight to update
new_values = {
    "booker": "angel31"
}

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Construct the SET clause
set_clause = ", ".join([f"{col} = ?" for col in new_values.keys()])
query = f"UPDATE bookings SET booker = 'emmaW' WHERE flight = 33010 AND seat_number = '11D';"

# Execute the query with the values
cursor.execute(query)
conn.commit()
conn.close()

print(f"Flight with ID {flight_id} has been updated.")