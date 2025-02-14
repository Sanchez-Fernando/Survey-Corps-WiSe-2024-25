"""
This module implements a multi-page Tkinter application for managing flight bookings,
user registration, and administrative flight management.
"""

import tkinter as tk
import db_queries
import os
import sys

from tkinter import messagebox
from stats import calculate_seat_availability, list_seat_availability, list_users_for_flight
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App(tk.Tk):
    """
    The main application class that initializes the Tkinter window and manages different pages.

    Methods:
        __init__(): Initializes the main application window.
        show_page(page_class): Switches to the specified page.
        show_previous_page(): Navigates back to the previous page.
        set_user_info(user_info2): Sets or updates the logged in user info.
        get_user_info(): Retrieves the logged in user info.
        on_close(): Cleans up resources and closes the application.
    """
    def __init__(self):
        super().__init__()
        
        self.title("Multi-Page App")
        self.geometry("600x600")

        # Container to hold all frames (pages)
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionary to store all pages
        self.pages = {}

        # Dictionary to store user information
        self.user_info = {}

        # List to track navigation history
        self.navigation_history = []

        # Initialize and show the main menu
        self.show_page(WelcomeMenu)

        # Bind the window close event to the cleanup method
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_page(self, page_class):
        """
        Switch to the specified page.

        Args:
            page_class (class): The class of the page to be displayed.
        """
        # Add the current page to navigation history if a page is already loaded
        if self.pages:
            self.navigation_history.append(self.current_page)

        # Create a new instance of the page if it doesn't exist (except for WelcomeMenu)
        if (page_class not in self.pages) or (page_class != WelcomeMenu):
            page = page_class(self.container, self)
            self.pages[page_class] = page
            page.pack(fill="both", expand=True)
        
        # Hide all other pages and display the selected page
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_class].pack(fill="both", expand=True)

        # Update the current page tracker
        self.current_page = page_class

    def show_previous_page(self):
        """
        Navigate back to the previous page in the navigation history.
        """
        if self.navigation_history:
            previous_page = self.navigation_history.pop()
            self.show_page(previous_page)

    def set_user_info(self, user_info2):
        """
        Set or update the logged in user information.

        Args:
            user_info2 (dict): A dictionary containing user details.
        """
        self.user_info = user_info2

    def get_user_info(self):
        """
        Retrieve the logged in user information.

        Returns:
            dict: The dictionary containing the user information.
        """
        return self.user_info

    def on_close(self):
        """
        Clean up resources and close the application.
        """
        # Close all matplotlib figures
        plt.close('all')
        # Destroy the Tkinter window
        self.destroy()
        # Terminate the Python process
        sys.exit()


class WelcomeMenu(tk.Frame):
    """
    The welcome menu page that displays initial options for the user.

    Methods:
        __init__(parent, controller): Initializes the welcome menu page.
        exit_with_message(): Displays a thank-you message and exits the application.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Help Button in the upper right corner
        help_frame = tk.Frame(self)
        help_frame.pack(anchor="ne", padx=10, pady=10)
        tk.Button(help_frame, text="Help", command=lambda: controller.show_page(HelpPage)).pack()

        # Title of the application
        tk.Label(self, text="Super flights", font=("Arial", 16)).pack(pady=20)

        # "Login" Button
        tk.Button(self, text="Login", command=lambda: controller.show_page(LoginPage)).pack(pady=10)

        # "Register" Button
        tk.Button(self, text="Create an account", command=lambda: controller.show_page(RegisterPage)).pack(pady=10)
        
        # "Exit" Button
        tk.Button(self, text="Exit", command=self.exit_with_message).pack(pady=10)

    def exit_with_message(self):
        """
        Display a thank-you message and exit the application after a short delay.
        """
        tk.Label(self, text="Thank you for using Super flights!", font=("Arial", 12)).pack(pady=10)
        self.after(2000, self.controller.quit)  # 2-second timeout before quitting


class LoginPage(tk.Frame):
    """
    The login page that allows users to enter their credentials to access their account.

    Methods:
        __init__(parent, controller): Initializes the login page.
        login(): Processes the login attempt and verifies credentials.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Help Button in the upper right corner
        help_frame = tk.Frame(self)
        help_frame.pack(anchor="ne", padx=10, pady=10)
        tk.Button(help_frame, text="Help", command=lambda: controller.show_page(HelpPage)).pack()

        # Page Title
        tk.Label(self, text="Login", font=("Arial", 16)).pack(pady=20)

        # Username field
        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        # Password field
        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        tk.Button(self, text="Login", command=self.login).pack(pady=10)

        # Back Button to return to the Welcome Menu
        tk.Button(self, text="Back to Welcome Menu", command=lambda: controller.show_page(WelcomeMenu)).pack(pady=10)

        # Label to display error messages
        self.error_message = tk.Label(self, text="", fg="red")
        self.error_message.pack(pady=5)

    def login(self):
        """
        Process the login by validating the username and numeric password,
        then verifying the credentials against the database.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            password = int(password)
        except ValueError:
            self.error_message.config(text="Password must be a number.")
            return

        user = {"username": username, "password": password}
        
        if db_queries.is_in_table("users", user):
            full_user_info_tuple = db_queries.gimme_tuples("users", identifier=user)
            user["name"] = full_user_info_tuple[0][1]
            user["user_type"] = full_user_info_tuple[0][3]

            self.controller.set_user_info(user)
            self.controller.show_page(MainMenu)
            
        else:
            self.error_message.config(text="Wrong username or password")


class RegisterPage(tk.Frame):
    """
    The registration page that allows new users to create an account.

    Methods:
        __init__(parent, controller): Initializes the registration page.
        register(user_type): Validates input and registers a new user of the specified type.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Help Button in the upper right corner
        help_frame = tk.Frame(self)
        help_frame.pack(anchor="ne", padx=10, pady=10)
        tk.Button(help_frame, text="Help", command=lambda: controller.show_page(HelpPage)).pack()

        # Page Title
        tk.Label(self, text="Create account", font=("Arial", 16)).pack(pady=20)

        # Full name field
        tk.Label(self, text="Full name:").pack(pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        # Username field
        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        # Password field
        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Repeat Password field
        tk.Label(self, text="Repeat Password:").pack(pady=5)
        self.password_entry2 = tk.Entry(self, show="*")
        self.password_entry2.pack(pady=5)

        # Register Button for regular user
        tk.Button(self, text="Register as user", command=lambda: self.register(user_type="regular")).pack(pady=10)

        # Register Button for admin user
        tk.Button(self, text="Register as admin", command=lambda: self.register(user_type="admin")).pack(pady=10)

        # Back Button to return to the Welcome Menu
        tk.Button(self, text="Back to Welcome Menu", command=lambda: controller.show_page(WelcomeMenu)).pack(pady=10)

        # Label to display error messages
        self.error_message = tk.Label(self, text="", fg="red")
        self.error_message.pack(pady=5)

    def register(self, user_type):
        """
        Validate the registration form and create a new user if all inputs are correct.

        Args:
            user_type (str): The type of user account to register (e.g., "regular" or "admin").
        """
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        password2 = self.password_entry2.get()
        
        if not name or not username or not password or not password2:
            self.error_message.config(text="Please fill in all the fields.")
            return
        try:
            password = int(password)
            password2 = int(password2)
        except ValueError:
            self.error_message.config(text="Password must be a number.")
            return
        
        if password != password2:
            self.error_message.config(text="Passwords do not match.")
            return
        
        user = {"name": name, "username": username, "password": password, "user_type": user_type}
        
        if db_queries.is_in_table("users", {"username": user["username"]}):
            messagebox.showerror("Error", "Username already exists, try another one.")
        else:
            db_queries.insert_row("users", user)
            messagebox.showinfo("Info", "User created successfully. Please log in.")
            self.controller.show_page(WelcomeMenu)


class MyAccountPage(tk.Frame):
    """
    The account page that displays the logged-in user's account information.

    Methods:
        __init__(parent, controller): Initializes the account page.
        show_info(): Displays user account details.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Help Button and Return button in the upper right corner
        help_frame = tk.Frame(self)
        help_frame.pack(anchor="ne", padx=10, pady=10)
        tk.Button(help_frame, text="Return", command=lambda: controller.show_page(MainMenu)).pack(side="left", padx=5)
        tk.Button(help_frame, text="Help", command=lambda: controller.show_page(HelpPage)).pack(side="left", padx=5)

        # Page Title
        tk.Label(self, text="My Account", font=("Arial", 16)).pack(pady=20)

        # Display the account information
        self.show_info()

        # Back Button to return to the Main Menu
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_page(MainMenu)).pack(pady=10)

        # Log out Button to return to the Welcome Menu
        tk.Button(self, text="Log out", command=lambda: (controller.show_page(WelcomeMenu))).pack(pady=10)

    def show_info(self):
        """
        Retrieve and display the current user's account information.
        """
        user = self.controller.get_user_info()
        if user:
            tk.Label(self, text=f"Full name: {user['name']}").pack(pady=5)
            tk.Label(self, text=f"Username: {user['username']}").pack(pady=5)
            tk.Label(self, text=f"Password: {user['password']}").pack(pady=5)
            tk.Label(self, text=f"Status: {user['user_type']}").pack(pady=5)


class MainMenu(tk.Frame):
    """
    The main menu page that provides navigation to various functionalities such as booking flights,
    viewing bookings, and accessing account and admin options.

    Methods:
        __init__(parent, controller): Initializes the main menu page.
        search_display_flight(): Searches for a flight and displays its seat layout.
        book_seat(entry, flight_id): Processes the booking of a selected seat.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Upper left button frame for navigation options
        button_frame = tk.Frame(self)
        button_frame.pack(anchor="ne", padx=10, pady=10)

        # Display admin-only buttons if the user is an admin
        user_info = controller.get_user_info()
        if user_info["user_type"] == "admin":
            tk.Button(button_frame, text="Stats", command=lambda: controller.show_page(Stats)).pack(side="left", padx=5)
            tk.Button(button_frame, text="Manage Flights", command=lambda: controller.show_page(ManageFlights)).pack(side="left", padx=5)

        tk.Button(button_frame, text="My Bookings", command=lambda: controller.show_page(MyBookings)).pack(side="left", padx=5)
        tk.Button(button_frame, text="My Account", command=lambda: controller.show_page(MyAccountPage)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Log Off", command=lambda: controller.show_page(WelcomeMenu)).pack(side="left", padx=5)

        # Search field frame in the center for flight booking
        search_frame = tk.Frame(self)
        search_frame.pack(expand=True, pady=10, anchor="n")

        # Help Button
        tk.Button(button_frame, text="Help", command=lambda: controller.show_page(HelpPage)).pack(side="left", padx=5)

        tk.Label(search_frame, text="Book Flight\nSearch Flight by ID:").pack(pady=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(pady=5)
        tk.Button(search_frame, text="Search", command=self.search_display_flight).pack(pady=5)
        
    def search_display_flight(self):
        """
        Search for a flight using the flight ID provided by the user, then display the seat layout
        along with booking options.
        """
        flight_id = self.search_entry.get()

        if db_queries.is_in_table("flights", {"flight_id": flight_id}):
            # Retrieve flight, aircraft, and booking information from the database
            flight_info = db_queries.gimme_tuples("flights", identifier={"flight_id": flight_id})
            aircraft_info = db_queries.gimme_tuples("aircrafts", identifier={"code": flight_info[0][1]})
            booking_info = db_queries.gimme_tuples("bookings", identifier={"flight": flight_id})
            
            # Build the string representation of the flight's seat layout
            seat_representation = aircraft_info[0][1].replace("| |", "|   |")
            flight_representation = ["     " + seat_representation + "\n"]
            rows = aircraft_info[0][2]

            for i in range(rows):
                if i+1 < 10:
                    flight_representation += ["\n" + str(i+1) + "    " + seat_representation]
                else:
                    flight_representation += ["\n" + str(i+1) + "  " + seat_representation]
                
            # Replace seat characters with 'X' if the seat is booked
            booked_seats = [booking[1] for booking in booking_info if booking[2] is not None]
            for seat in booked_seats:
                flight_representation[int(seat[:-1])] = flight_representation[int(seat[:-1])].replace(seat[-1], "X")

            single_string_representation = "".join(flight_representation)
                
            # Create a frame to display the seat layout and booking input
            display_frame = tk.Frame(self)
            display_frame.pack(expand=True, pady=10, anchor="n")
            tk.Label(display_frame, text=f"Seat Layout Representation for Flight no {flight_id}\n X represents a reserved seat \n |   | represents an aisle").pack(pady=5)
            tk.Label(display_frame, anchor = "n", text=single_string_representation).pack(pady=5)

            tk.Label(display_frame, text="Enter the seat number you want to book:").pack(pady=5, anchor="n")
            book_seat_entry = tk.Entry(display_frame)
            book_seat_entry.pack(pady=5, anchor="n")
            tk.Button(display_frame, text="Book", command=lambda: self.book_seat(entry=book_seat_entry, flight_id=flight_id)).pack(pady=5, anchor="n")

        else:
            messagebox.showerror("Error", "Flight not found, please try again.")

    def book_seat(self, entry, flight_id):
        """
        Attempt to book a seat for the specified flight based on user input.

        Args:
            entry (tk.Entry): The entry widget containing the seat number.
            flight_id (str): The ID of the flight for which the seat is being booked.
        """
        booking_info_dictionary = {"seat_number": entry.get(),
                                    "flight": flight_id,
                                    }
        if db_queries.is_in_table("bookings", booking_info_dictionary):
            seat_info = db_queries.gimme_tuples("bookings", identifier=booking_info_dictionary)

            if seat_info[0][2] is None:
                booker_username ={"booker" : self.controller.get_user_info()["username"]}
                db_queries.update_row("bookings", old_values=booking_info_dictionary, new_values=booker_username)
                messagebox.showinfo("Info", "Booking succesful")

                self.controller.show_page(EmptyPage)
                self.controller.show_page(MainMenu)
            else:
                messagebox.showerror("Error", "The selected seat already booked, please choose another one.")

        else:
            messagebox.showerror("Error", "Invalid seat number, try again.")


class Stats(tk.Frame):
    """
    Admin-only statistics page that displays seat availability and user booking data for a flight.

    Methods:
        __init__(parent, controller): Initializes the stats page.
        search_flight(): Fetches and displays statistics for the given flight.
        show_pie_chart(seat_data): Displays a pie chart for reserved vs. available seats.
        save_statistics_to_file(): Saves the current flight statistics to a text file.
        clear_stats_frame(): Clears previous statistics from the display.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Upper left button frame for navigation
        button_frame = tk.Frame(self)
        button_frame.pack(anchor="ne", padx=10, pady=10)

        tk.Button(button_frame, text="Return", command=lambda: controller.show_page(MainMenu)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Log Off", command=lambda: controller.show_page(WelcomeMenu)).pack(side="left", padx=5)

        # Help Button for assistance
        tk.Button(button_frame, text="Help", command=lambda: controller.show_page(HelpPage)).pack(side="left", padx=5)

        # Search field frame for flight statistics
        search_frame = tk.Frame(self)
        search_frame.pack(expand=True, pady=10, anchor="n")

        tk.Label(search_frame, text="Show Stats\nSearch Flight by ID:").pack(pady=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(pady=5)
        tk.Button(search_frame, text="Search", command=self.search_flight).pack(pady=5)

        # Button to save statistics to a text file
        tk.Button(search_frame, text="Save Statistics to File", command=self.save_statistics_to_file).pack(pady=5)

        # Frame to display statistics
        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame for the pie chart display
        self.chart_frame = tk.Frame(self.stats_frame)
        self.chart_frame.pack(fill="both", expand=True, pady=10)

        # Variables to store current flight statistics
        self.current_flight_id = None
        self.seat_data = None
        self.seat_list_data = None
        self.user_data = None

    def search_flight(self):
        """
        Fetch and display statistics for the entered flight ID, including seat availability,
        reserved seats, and user booking details.
        """
        flight_id = self.search_entry.get()
        if not flight_id:
            messagebox.showerror("Error", "Please enter a flight ID.")
            return
        
        current_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(current_dir, 'flights.sqlite')

        # Fetch seat availability data
        seat_data, error = calculate_seat_availability(flight_id, db_path)
        if error:
            messagebox.showerror("Error", error)
            return

        # Fetch seat list data
        seat_list_data, error = list_seat_availability(flight_id, db_path)
        if error:
            messagebox.showerror("Error", error)
            return

        # Fetch user booking data
        user_data, error = list_users_for_flight(flight_id, db_path)
        if error:
            messagebox.showerror("Error", error)
            return

        # Store the current flight ID and related statistics
        self.current_flight_id = flight_id
        self.seat_data = seat_data
        self.seat_list_data = seat_list_data
        self.user_data = user_data

        # Clear any previous statistics from the frame
        self.clear_stats_frame()

        # Display seat availability details
        tk.Label(self.stats_frame, text="Seat Availability", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.stats_frame, text=f"Total Seats: {seat_data['total_seats']}").pack(pady=2)
        tk.Label(self.stats_frame, text=f"Reserved Seats: {seat_data['reserved_seats']} ({seat_data['reserved_percentage']:.2f}%)").pack(pady=2)
        tk.Label(self.stats_frame, text=f"Available Seats: {seat_data['available_seats']} ({seat_data['available_percentage']:.2f}%)").pack(pady=2)

        # Display reserved seats list
        tk.Label(self.stats_frame, text="Reserved Seats", font=("Arial", 14)).pack(pady=5)
        reserved_seats_text = tk.Text(self.stats_frame, height=5, width=100)
        reserved_seats_text.pack(pady=2)
        reserved_seats_text.insert(tk.END, ", ".join(seat_list_data['reserved_seats']))
        reserved_seats_text.config(state=tk.DISABLED)

        # Display available seats list
        tk.Label(self.stats_frame, text="Available Seats", font=("Arial", 14)).pack(pady=5)
        available_seats_text = tk.Text(self.stats_frame, height=5, width=100)
        available_seats_text.pack(pady=2)
        available_seats_text.insert(tk.END, ", ".join(seat_list_data['available_seats']))
        available_seats_text.config(state=tk.DISABLED)

        # Display user details along with their booked seats
        tk.Label(self.stats_frame, text="Users and their Booked Seats", font=("Arial", 14)).pack(pady=5)
        users_text = tk.Text(self.stats_frame, height=10, width=100)
        users_text.pack(pady=2)
        for user in user_data:
            users_text.insert(tk.END, f"Username: {user[0]}, Name: {user[1]}, User Type: {user[2]}, Booked Seats: {user[3]}\n")
        users_text.config(state=tk.DISABLED)

        # Display a pie chart showing reserved vs. available seats
        self.show_pie_chart(seat_data)

    def show_pie_chart(self, seat_data):
        """
        Display a pie chart representing the distribution of reserved and available seats.

        Args:
            seat_data (dict): Dictionary containing seat availability statistics.
        """
        # Clear any existing chart widgets from the frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Create a pie chart using matplotlib
        fig, ax = plt.subplots()
        labels = ['Reserved Seats', 'Available Seats']
        sizes = [seat_data['reserved_seats'], seat_data['available_seats']]
        colors = ['red', 'green']
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Ensure the pie chart is circular

        # Embed the matplotlib figure in the Tkinter interface
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def save_statistics_to_file(self):
        """
        Save the current flight statistics to a text file.
        """
        if not self.current_flight_id:
            messagebox.showerror("Error", "No flight statistics to save. Please search for a flight first.")
            return

        file_path = f"flight_{self.current_flight_id}_statistics.txt"

        try:
            with open(file_path, 'w') as file:
                file.write(f"Flight Details for Flight {self.current_flight_id}\n")
                file.write("=================\n\n")

                # Write seat availability data to file
                file.write("Seat Availability:\n")
                file.write(f"Total Seats: {self.seat_data['total_seats']}\n")
                file.write(f"Reserved Seats: {self.seat_data['reserved_seats']} ({self.seat_data['reserved_percentage']:.2f}%)\n")
                file.write(f"Available Seats: {self.seat_data['available_seats']} ({self.seat_data['available_percentage']:.2f}%)\n\n")

                # Write reserved and available seats information to file
                file.write("Reserved Seats:\n")
                file.write(", ".join(self.seat_list_data['reserved_seats']) + "\n\n")

                file.write("Available Seats:\n")
                file.write(", ".join(self.seat_list_data['available_seats']) + "\n\n")

                # Write user booking details to file
                file.write("Users:\n")
                for user in self.user_data:
                    file.write(f"Username: {user[0]}, Name: {user[1]}, User Type: {user[2]}, Booked Seats: {user[3]}\n")

            messagebox.showinfo("Success", f"Statistics saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save statistics: {e}")

    def clear_stats_frame(self):
        """
        Clear all widgets from the statistics frame except for the chart frame.
        """
        for widget in self.stats_frame.winfo_children():
            if widget != self.chart_frame:
                widget.destroy()


class ManageFlights(tk.Frame):
    """
    Admin-only page to add new aircraft templates and flights to the database.

    Methods:
        __init__(parent, controller): Initializes the Manage Flights page.
        clear_options_frame(): Clears all widgets from the options frame.
        aircraft_addition(): Displays the UI for adding a new aircraft.
        flight_addition(): Displays the UI for adding a new flight.
        add_aircraft(): Validates input and adds a new aircraft to the database.
        add_flight(): Validates input and adds a new flight to the database.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Upper left button frame for navigation
        button_frame = tk.Frame(self)
        button_frame.pack(anchor="ne", padx=10, pady=10)
        
        tk.Button(button_frame, text="Return", command=lambda: controller.show_page(MainMenu)).pack(side=tk.LEFT, padx=5)

        # Help Button for assistance
        tk.Button(button_frame, text="Help", command=lambda: controller.show_page(HelpPage)).pack(side=tk.LEFT, padx=5)

        # Action frame in the center for add/remove operations
        action_frame = tk.Frame(self)
        action_frame.pack(expand=True, pady=10, anchor="n")

        tk.Label(action_frame, text="Add to the database").pack(pady=5)

        # Frame to hold side-by-side buttons for adding aircraft or flight
        button_frame = tk.Frame(action_frame)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Add aircraft", command=self.aircraft_addition).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Add flight", command=self.flight_addition).pack(side=tk.LEFT, padx=5)

        # Options frame where additional widgets are displayed
        self.options_frame = tk.Frame(action_frame)
        self.options_frame.pack(anchor="n", padx=10, pady=10)

    def clear_options_frame(self):
        """
        Clear all widgets from the options frame.
        """
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def aircraft_addition(self):
        """
        Display the user interface components for adding a new aircraft.
        """
        self.clear_options_frame()
    
        # Title label for aircraft addition
        tk.Label(self.options_frame, text="Add aircraft:").pack(pady=5)

        # Frame to hold labels for aircraft code, layout, and number of rows
        top_frame = tk.Frame(self.options_frame)
        top_frame.pack(pady=5)

        self.code = tk.Label(top_frame, text="Enter aircraft code:")
        self.code.pack(side=tk.LEFT, padx=5)

        self.layout = tk.Label(top_frame, text="Enter aircraft layout:\n e.g. 'ABC| |DEF'")
        self.layout.pack(side=tk.LEFT, padx=5)

        self.rows = tk.Label(top_frame, text="Enter number of rows:")
        self.rows.pack(side=tk.LEFT, padx=5)

        # Frame to hold entry fields corresponding to the above labels
        middle_frame = tk.Frame(self.options_frame)
        middle_frame.pack(pady=5)

        self.aircraft_code = tk.Entry(middle_frame)
        self.aircraft_code.pack(side=tk.LEFT, padx=5)

        self.aircraft_layout = tk.Entry(middle_frame)
        self.aircraft_layout.pack(side=tk.LEFT, padx=5)

        self.row_number = tk.Entry(middle_frame)
        self.row_number.pack(side=tk.LEFT, padx=5)

        # Button to trigger aircraft addition
        tk.Button(self.options_frame, text="Add", command=self.add_aircraft).pack(pady=5)

    def flight_addition(self):
        """
        Display the user interface components for adding a new flight.
        """
        self.clear_options_frame()

        # Frame to hold labels for flight ID and associated aircraft code
        top_frame = tk.Frame(self.options_frame)
        top_frame.pack(pady=5)

        self.flightid = tk.Label(top_frame, text="                  Enter new Flight ID:")
        self.flightid.pack(side=tk.LEFT, padx=5)

        self.aircraftc = tk.Label(top_frame, text="Enter new aircraft code for the flight:")
        self.aircraftc.pack(side=tk.LEFT, padx=5)

        # Frame to hold entry fields for flight ID and aircraft code
        middle_frame = tk.Frame(self.options_frame)
        middle_frame.pack(pady=5)

        self.flight_id = tk.Entry(middle_frame)
        self.flight_id.pack(side=tk.LEFT, padx=5)

        self.aircraft_code = tk.Entry(middle_frame)
        self.aircraft_code.pack(side=tk.LEFT, padx=5)
       
        # Button to trigger flight addition
        tk.Button(self.options_frame, text="Add", command=self.add_flight).pack(pady=5)

    def add_aircraft(self):
        """
        Validate input data and add a new aircraft record to the database.
        """
        code = self.aircraft_code.get()
        layout = self.aircraft_layout.get()
        rows = self.row_number.get()

        if not code or not layout or not rows:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if db_queries.is_in_table("aircrafts", {"code": code}):
            messagebox.showerror("Error", "Aircraft code already exists.")
            return
        
        if len(code) != 3:
            messagebox.showerror("Error", "Invalid aircraft code. Please enter the 3-letter IATA-code.")
            return
        
        if ("|" not in layout) or ("||" in layout):
            messagebox.showerror("Error", "Invalid layout format. Please follow the example.")
            return
        
        for a in layout:
            if a not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ| ":
                messagebox.showerror("Error", "Invalid layout format. Please follow the example.")
                return
        
        for c in code:
            if c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":	
                messagebox.showerror("Error", "Invalid aircraft code. Please enter the 3-letter IATA-code.")
                return
        
        aircraft = {"code": code, "layout": layout, "row_number": rows}

        db_queries.insert_row("aircrafts", aircraft)
        messagebox.showinfo("Success", "Aircraft added successfully to the database.")

    def add_flight(self):
        """
        Validate input data and add a new flight record to the database. Also updates the bookings table.
        """
        id = self.flight_id.get()
        code = self.aircraft_code.get()

        if not id or not code:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if db_queries.is_in_table("flights", {"flight_id": id}):    
            messagebox.showerror("Error", "Flight already exists.")
            return
        
        if not db_queries.is_in_table("aircrafts", {"code": code}):    
            messagebox.showerror("Error", f"No such aircraft '{code}' exists.")
            return
        
        db_queries.insert_row("flights", {"flight_id": id, "aircraft_code": code})
        db_queries.add_rows_to_bookings(id, code)
        messagebox.showinfo("Success", "Flight added successfully to the database.")


class MyBookings(tk.Frame):
    """
    The bookings page that displays the current user's bookings and allows cancellation.

    Methods:
        __init__(parent, controller): Initializes the bookings page.
        load_bookings(): Loads and displays the user's current bookings.
        show_booking_page(): Navigates back to the flight search interface.
        cancel_booking(booking): Cancels the specified booking.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Help and Return Buttons in the upper right corner
        help_frame = tk.Frame(self)
        help_frame.pack(anchor="ne", padx=10, pady=10)
        tk.Button(help_frame, text="Return", command=self.show_booking_page).pack(side="left", padx=5)
        tk.Button(help_frame, text="Help", command=lambda: controller.show_page(HelpPage)).pack(side="left", padx=5)

        # Page Title
        tk.Label(self, text="My Bookings", font=("Arial", 16)).pack(pady=20)

        # Frame to display booking information
        self.booking_frame = tk.Frame(self)
        self.booking_frame.pack(fill="both", expand=True, pady=10)

        # Load and display current bookings
        self.load_bookings()

    def load_bookings(self):
        """
        Retrieve the user's bookings from the database and display them in the booking frame.
        """
        user_info = self.controller.get_user_info()
        username = user_info['username']

        # Fetch current bookings for the user
        current_bookings = db_queries.gimme_tuples("bookings", identifier={"booker": username})

        # Clear the previous booking display
        for widget in self.booking_frame.winfo_children():
            widget.destroy()

        if current_bookings:
            # Display a title for the bookings list
            tk.Label(self.booking_frame, text=f"{username}'s Current Bookings", font=("Arial", 14)).pack(pady=10)

            # Display each booking with an option to cancel
            for booking in current_bookings:
                flight_id = booking[0]
                seat_number = booking[1]
                tk.Label(self.booking_frame, text=f"Flight ID: {flight_id}, Seat: {seat_number}").pack(pady=5)

                # Button to cancel the booking
                cancel_button = tk.Button(self.booking_frame, text="Cancel Booking", 
                                          command=lambda b=booking: self.cancel_booking(b))
                cancel_button.pack(pady=5)
        else:
            # Inform the user if there are no bookings
            tk.Label(self.booking_frame, text="You currently have no bookings.").pack(pady=10)

    def show_booking_page(self):
        """
        Navigate back to the flight search interface to allow the user to book a new flight.
        """
        self.controller.show_page(MainMenu)

    def cancel_booking(self, booking):
        """
        Cancel the specified booking and update the database accordingly.

        Args:
            booking (tuple): A tuple containing booking details (flight_id, seat_number, etc.).
        """
        flight_id = booking[0]
        seat_number = booking[1]

        # Update the booking in the database to remove the user's booking
        booking_info = {"flight": flight_id, "seat_number": seat_number}
        new_booker = {"booker": None}
        db_queries.update_row("bookings", old_values=booking_info, new_values=new_booker)

        # Notify the user and refresh the bookings list
        messagebox.showinfo("Booking Canceled", f"Your booking for Flight {flight_id}, Seat {seat_number} has been canceled.")
        self.load_bookings()


class HelpPage(tk.Frame):
    """
    The help page that provides instructions on how to use the application.

    Methods:
        __init__(parent, controller): Initializes the help page.
        return_to_previous_page(): Returns to the previous page.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Page Title
        tk.Label(self, text="Help", font=("Arial", 16)).pack(pady=20)
        
        # Help instructions text
        help_text = """
        Welcome to Super Flights!

        Here's how to use the application:
        1. [ LOGIN ]: Enter your username and password to access your account.
        2. [ REGISTER ]: Create a user account to use the application, or an admin account for additional features.
        3. [ MAIN MENU ]: After logging in, you can book flights, view your bookings, or access admin features.
        4. [ MY BOOKINGS ]: Book or cancel seats from your desired flight.
        5. [ STATS (ADMIN ONLY) ]: View statistics for flights, including seat availability and user details.
        6. [ MANAGE FLIGHTS (ADMIN ONLY) ]: Add or remove flights and aircraft from the database.
        7. [ MY ACCOUNT ]: View your account information.
        8. [ HELP ]: Access this page for instructions on how to use the application.
        """

        tk.Label(self, text=help_text, justify=tk.LEFT).pack(pady=10, padx=10)

        # Return Button to go back to the previous page
        tk.Button(self, text="Return", command=self.return_to_previous_page).pack(pady=10)

    def return_to_previous_page(self):
        """
        Return to the page that was displayed before the help page.
        """
        self.controller.show_previous_page()


class EmptyPage(tk.Frame):
    """
    An empty page used as a temporary placeholder or refresher.
    
    Methods:
        __init__(parent, controller): Initializes the empty page.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


# Run the application if this module is executed directly
if __name__ == "__main__":
    app = App()
    app.mainloop()
