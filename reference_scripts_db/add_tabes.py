# IMPORTANT: Dont run this script, it was used to create the tables in the database, this is only for reference.
import sqlite3
import os

# Get the absolute path to the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_dir, '../MainApp/flights.sqlite')

# Connect to the SQLite database (or create a new one)
connection = sqlite3.connect(db_path)

# Create a cursor object
cursor = connection.cursor()

# SQL commands to create tables
create_tables_sql = [
    """
    CREATE TABLE IF NOT EXISTS flights (
        flight_id INTEGER PRIMARY KEY,
        aircraft_code TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS aircrafts (
        code TEXT PRIMARY KEY,
        columns INTEGER NOT NULL,
        rows INTEGER NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS users (
        username INTEGER PRIMARY KEY,
        password INTEGER NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS bookings_new (
        flight INTEGER NOT NULL,
        seat_number TEXT NOT NULL,
        booker TEXT,
        PRIMARY KEY (flight, seat_number),
        FOREIGN KEY (flight) REFERENCES flights(flight_id),
        FOREIGN KEY (booker) REFERENCES users(username)
    );
    """
]

# Execute each SQL command to create tables
for sql in create_tables_sql:
    cursor.execute(sql)

# Commit the changes and close the connection
connection.commit()
connection.close()

print(f"Database 'flights.sqlite' with all tables has been created!")
