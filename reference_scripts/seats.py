import sqlite3
import time

# Function to load users dynamically from a database
def load_users_from_db(db_connection):
    users = {}
    cursor = db_connection.cursor()
    cursor.execute("SELECT userID, name, username, password, role FROM users")
    rows = cursor.fetchall()
    for row in rows:
        user_id, name, username, password, role = row
        users[username] = {"userID": user_id, "name": name, "password": password, "role": role}
    return users

# Function to load the seating chart dynamically from the database
def load_seating_chart_from_db(db_connection):
    seats = {}
    cursor = db_connection.cursor()
    cursor.execute("SELECT row, seat, status FROM seats")
    rows = cursor.fetchall()
    for row in rows:
        row_number, seat, status = row
        if row_number not in seats:
            seats[row_number] = {}
        seats[row_number][seat] = status
    return seats

# Function to display the seat map
def display_seats(seats):
    print("Seat Map:")
    for row in seats:
        left_section = " ".join([seat if seats[row][seat] == 'Available' else 'X' for seat in ['A', 'B', 'C']])
        right_section = " ".join([seat if seats[row][seat] == 'Available' else 'X' for seat in ['D', 'E', 'F']])
        print(f"Row {row}: {left_section} |   | {right_section}")

# Function to handle login
def login(users_db):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users_db and users_db[username]["password"] == password:
        print(f"Welcome, {users_db[username]['name']}!")
        return users_db[username]
    else:
        print("Invalid username or password!")
        return None

# Function to reserve a seat
def reserve_seat(seats, seat_id, user):
    row = int(seat_id[0])  # Row number (e.g., '4A' -> row=4)
    seat = seat_id[1].upper()  # Seat letter (e.g., '4A' -> seat='A')

    # Check if the seat is already reserved
    if seats[row][seat] == 'Reserved':
        print(f"Error: Seat {seat_id} is already reserved.")
        return

    # Confirm reservation
    confirmation = input(f"Are you sure you want to reserve seat {seat_id}? (yes/no): ").lower()
    if confirmation == "yes":
        seats[row][seat] = 'Reserved'
        print(f"Seat {seat_id} reserved successfully.")
    else:
        print(f"Reservation for seat {seat_id} canceled.")

# Function to cancel a reservation (only for admin)
def cancel_seat(seats, seat_id, user):
    if user['role'] != 'admin':
        print("Error: Only admin can cancel reservations.")
        return
    
    row = int(seat_id[0])  # Row number (e.g., '4A' -> row=4)
    seat = seat_id[1].upper()  # Seat letter (e.g., '4A' -> seat='A')

    # Check if the seat is already available
    if seats[row][seat] == 'Available':
        print(f"Error: Seat {seat_id} is already available.")
        return

    # Confirm cancellation
    confirmation = input(f"Are you sure you want to cancel the reservation for seat {seat_id}? (yes/no): ").lower()
    if confirmation == "yes":
        seats[row][seat] = 'Available'
        print(f"Reservation for seat {seat_id} canceled successfully.")
    else:
        print(f"Cancellation for seat {seat_id} canceled.")

# Main function to simulate the system behavior
def main():
    print("Welcome to the Airline Seat Reservation System!")

    # Set up SQLite database connection (adjust as needed for your environment)
    db_connection = sqlite3.connect('airline_reservation_system.db')
    
    # Load users and seats from the database
    users_db = load_users_from_db(db_connection)
    seats_db = load_seating_chart_from_db(db_connection)

    # User login
    user = None
    while user is None:
        user = login(users_db)

    # Main menu loop
    while True:
        print("\nMain Menu:")
        print("1. Display Seat Map")
        print("2. Reserve Seat")
        print("3. Cancel Reservation (Admin only)")
        print("4. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_seats(seats_db)
        elif choice == '2':
            seat_id = input("Enter seat number to reserve (e.g., 4A): ")
            reserve_seat(seats_db, seat_id, user)
        elif choice == '3' and user['role'] == 'admin':
            seat_id = input("Enter seat number to cancel (e.g., 4A): ")
            cancel_seat(seats_db, seat_id, user)
        elif choice == '4':
            print("Logging out...")
            time.sleep(2)  # Simulate a short timeout before logout
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
