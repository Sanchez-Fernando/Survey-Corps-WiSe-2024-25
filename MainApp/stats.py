import sqlite3

def calculate_seat_availability(flight_id, db_path):
    """
    Calculate and output the number and percentage of available and reserved seats for a specific flight.

    :param flight_id: The ID of the flight to analyze.
    :param db_path: Path to the SQLite database file.
    :return: Dictionary with seat statistics or an error message.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Step 1: Get the aircraft code for the given flight
        cursor.execute("SELECT aircraft_code FROM flights WHERE flight_id = ?", (flight_id,))
        result = cursor.fetchone()

        if not result:
            return None, f"Flight ID {flight_id} not found."

        aircraft_code = result[0]

        # Step 2: Get the layout of the aircraft
        cursor.execute("SELECT layout FROM aircrafts WHERE code = ?", (aircraft_code,))
        result = cursor.fetchone()

        if not result:
            return None, f"Aircraft code {aircraft_code} not found."

        layout = result[0]

        # Step 3: Parse the layout to calculate the column length (number of seats per row)
        rows = layout.split('|')
        column_length = sum(len(row.strip()) for row in rows)

        # Step 4: Get the maximum number of rows for the aircraft
        cursor.execute("SELECT MAX(CAST(SUBSTR(seat_number, 1, LENGTH(seat_number) - 1) AS INTEGER)) AS max_row FROM bookings WHERE flight = ?", (flight_id,))
        max_row_result = cursor.fetchone()

        max_rows = max_row_result[0] if max_row_result and max_row_result[0] else 0

        # Step 5: Calculate the total number of seats
        total_seats = column_length * max_rows

        # Step 6: Get the number of reserved seats (where booker is NOT NULL)
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE flight = ? AND booker IS NOT NULL", (flight_id,))
        reserved_seats = cursor.fetchone()[0]

        # Step 7: Calculate the number of available seats
        available_seats = total_seats - reserved_seats

        # Step 8: Calculate percentages
        reserved_percentage = (reserved_seats / total_seats * 100) if total_seats > 0 else 0
        available_percentage = (available_seats / total_seats * 100) if total_seats > 0 else 0

        return {
            "total_seats": total_seats,
            "reserved_seats": reserved_seats,
            "available_seats": available_seats,
            "reserved_percentage": reserved_percentage,
            "available_percentage": available_percentage
        }, None

    except sqlite3.Error as e:
        return None, f"Database error: {e}"

    finally:
        conn.close()


def list_seat_availability(flight_id, db_path):
    """
    Outputs the list of available and reserved seats for a specific flight.

    :param flight_id: The ID of the flight to analyze.
    :param db_path: Path to the SQLite database file.
    :return: Dictionary with lists of reserved and available seats or an error message.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Step 1: Get the aircraft code and layout for the given flight
        cursor.execute("SELECT aircraft_code FROM flights WHERE flight_id = ?", (flight_id,))
        result = cursor.fetchone()

        if not result:
            return None, f"Flight ID {flight_id} not found."

        aircraft_code = result[0]

        cursor.execute("SELECT layout FROM aircrafts WHERE code = ?", (aircraft_code,))
        result = cursor.fetchone()

        if not result:
            return None, f"Aircraft code {aircraft_code} not found."

        layout = result[0]
        rows = layout.split('|')
        column_letters = ''.join(row.strip() for row in rows)

        # Step 2: Get the maximum number of rows for the aircraft
        cursor.execute("SELECT MAX(CAST(SUBSTR(seat_number, 1, LENGTH(seat_number) - 1) AS INTEGER)) AS max_row FROM bookings WHERE flight = ?", (flight_id,))
        max_row_result = cursor.fetchone()

        max_rows = max_row_result[0] if max_row_result and max_row_result[0] else 0

        # Generate all possible seats
        all_seats = [f"{row}{col}" for row in range(1, max_rows + 1) for col in column_letters]

        # Step 3: Get reserved seats (where booker is NOT NULL)
        cursor.execute("SELECT seat_number FROM bookings WHERE flight = ? AND booker IS NOT NULL", (flight_id,))
        reserved_seats = [row[0] for row in cursor.fetchall()]

        # Step 4: Calculate available seats
        available_seats = list(set(all_seats) - set(reserved_seats))

        return {
            "reserved_seats": sorted(reserved_seats),
            "available_seats": sorted(available_seats)
        }, None

    except sqlite3.Error as e:
        return None, f"Database error: {e}"

    finally:
        conn.close()


def list_users_for_flight(flight_id, db_path):
    """
    Outputs the number of users for a specific flight along with their details (username, name, user type, and booked seats).

    :param flight_id: The ID of the flight to analyze.
    :param db_path: Path to the SQLite database file.
    :return: List of user details or an error message.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Step 1: Get unique users who have bookings for the flight and their booked seats
        query = """
        SELECT DISTINCT u.username, u.name, u.user_type, GROUP_CONCAT(b.seat_number)
        FROM users u
        JOIN bookings b ON u.username = b.booker
        WHERE b.flight = ? AND b.booker IS NOT NULL
        GROUP BY u.username, u.name, u.user_type
        """
        cursor.execute(query, (flight_id,))
        users = cursor.fetchall()

        return users, None

    except sqlite3.Error as e:
        return None, f"Database error: {e}"

    finally:
        conn.close()
