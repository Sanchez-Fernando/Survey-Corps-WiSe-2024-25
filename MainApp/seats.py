import sqlite3
import time


def load_users_from_db(db_connection):
    """
   This Function is to load users dynamically from a database.
   fetchall() : After executing the query, all resulting rows will be fetched.
   db_connection is a connection to the data base that holds the user data.
   cursor: executes SQL queries on the database.
   users = {}: creates an empty dictionary that will later be filled with user data loaded from the database.

    """
    users = {}
    cursor = db_connection.cursor()
    cursor.execute("SELECT userID, name, username, password, role FROM users")   # executes the SQL SELECT Statement 
    rows = cursor.fetchall()               
    for row in rows:                       # processes each row 
        user_id, name, username, password, role = row
        users[username] = {"userID": user_id, "name": name, "password": password, "role": role}   # stores in dictionnary calles 'users'
    return users


def load_seating_chart_from_db(db_connection):
    """
   Function to load the seating chart dynamically from the database.
   cursor.execute() : A SQL query is executed to retrieve the row, seat, and status columns from the seats table.
   seats: is a dictionary used to store the seat data.

    """
    seats = {}
    cursor = db_connection.cursor()
    cursor.execute("SELECT row, seat, status FROM seats")
    rows = cursor.fetchall()     
    for row in rows:              # processes each row 
        row_number, seat, status = row    # and unpacks the data into row_number, seat and status.
        if row_number not in seats:
            seats[row_number] = {}
        seats[row_number][seat] = status    #  the values are dictionaries representing individual seats (A, B, C, D, E, F), with each seat's status as its value.
    return seats


def display_seats(seats):
    """
    # Function to display the seat map ( print).
    The seats are divided into two sections displays it accordingly. 
    "X" is shown for reserved seats, while the actual seat label is shown for available seats.


    """
    print("Seat Map:")
    for row in seats:           # The function loops through each row in the seats dictionary        
        left_section = " ".join([seat if seats[row][seat] == 'Available' else 'X' for seat in ['A', 'B', 'C']])
        right_section = " ".join([seat if seats[row][seat] == 'Available' else 'X' for seat in ['D', 'E', 'F']])
        print(f"Row {row}: {left_section} |   | {right_section}")

def reserve_seat(seats, seat_id, user):
    """
    Function to reserve a seat.
    Checks if the seat is already reserved
    Confirms reservation. If the seat is available, the function asks the user to confirm the reservation.
    Cancels a reservation (only for admin).
    Checks if a seat is available.

    """
    row = int(seat_id[0])  # Row number ('4A' -> row=4)
    seat = seat_id[1].upper()  # Seat letter ('4A' -> seat='A')
    
    if seats[row][seat] == 'Reserved':
        print(f"Error: Seat {seat_id} is already reserved.")
        return
    
    confirmation = input(f"Are you sure you want to reserve seat {seat_id}? (yes/no): ").lower()
    if confirmation == "yes":
        seats[row][seat] = 'Reserved'
        print(f"Seat {seat_id} reserved successfully.")
    else:
        print(f"Reservation for seat {seat_id} canceled.")
        
def cancel_seat(seats, seat_id, user):
    if user['role'] != 'admin':          #if not admin: error
        print("Error: Only admin can cancel reservations.")
        return
    
    row = int(seat_id[0])  # Row number ('4A' -> row=4)
    seat = seat_id[1].upper()  # Seat letter ('4A' -> seat='A')

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

def login(users_db):
    """
    Inputs for user's Login.
    Checks if all inputs are right.

    """
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users_db and users_db[username]["password"] == password:
        print(f"Welcome {users_db[username]['name']}!")
        return users_db[username]
    else:
        print("Invalid username or password. Please try again.")
        return None
    
def main():
    """
    Main function to simulate the system behavior
    Connects with the database.
    Loads users and seats from database.
    Login Process. 
    When logged in: Many options for the user.


    """
    print("Welcome to the Airline Seat Reservation System!")

    # Set up SQLite database connection
    db_connection = sqlite3.connect('airline_reservation_system.db')
    
    # Load users and seats from the database
    users_db = load_users_from_db(db_connection)
    seats_db = load_seating_chart_from_db(db_connection)
    
    # Benutzeranmeldung
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
