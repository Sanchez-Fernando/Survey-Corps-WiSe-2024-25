import tkinter as tk
import db_queries

class App(tk.Tk):
    """
    The main application class that initializes the Tkinter window and manages different pages.

    Methods:
        __init__(): Initializes the main application window.
        show_page(page_class): Switches to the specified page.
        set_user_info(user_info2): Sets or updates the logged in user info.
        get_user_info(): Gets the logged in user info.
    """
    def __init__(self):
        super().__init__()
        
        self.title("Multi-Page App")
        self.geometry("430x330")

        # Container to hold all frames (pages)
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionary to store all pages
        self.pages = {}

        # Dictionary to store user information
        self.user_info = {}

        # Initialize and show the main menu
        self.show_page(WelcomeMenu)

    def show_page(self, page_class):
        """
        Switch to the specified page.

        Args:
            page_class (class): The class of the page to be displayed.
        """
        # All pages are created anew each time we use show_page, it doesnt matter since we have user_info
        if (page_class not in self.pages) or (page_class != WelcomeMenu):
            # If the page doesn't exist, create it
            page = page_class(self.container, self)
            self.pages[page_class] = page
            page.pack(fill="both", expand=True)
        
        # Show the requested page and hide others
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_class].pack(fill="both", expand=True)

    def set_user_info(self, user_info2):
        """
        Sets or updates the logged in user info.

        Args:
            user_info2 (dict): The dictionary containing the user information.
        """
        self.user_info = user_info2

    def get_user_info(self):
        """
        Gets the logged in user info.

        Returns:
            The dictionary containing the user information.
        """
        return self.user_info

# Welcome Menu Page
class WelcomeMenu(tk.Frame):
    """
    The welcome menu page class that displays the welcome menu options.

    Methods:
        __init__(parent, controller): Initializes the welcome menu page.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Super flights", font=("Arial", 16)).pack(pady=20)

        # "Login" Button
        tk.Button(self, text="Login", command=lambda: controller.show_page(LoginPage)).pack(pady=10)

        #TODO: add register functionality
        
        # "Exit" Button
        tk.Button(self, text="Exit", command=self.exit_with_message).pack(pady=10)

    # Thank you message and exit with timeout
    def exit_with_message(self):
        tk.Label(self, text="Thank you for using Super flights!", font=("Arial", 12)).pack(pady=10)
        self.after(2000, self.controller.quit)  # 2-second timeout before quitting

        

# Login Page
class LoginPage(tk.Frame):
    """
    The login page class that allows users to enter their username and password.

    Methods:
        __init__(parent, controller): Initializes the login page.
        login(): Handles the login logic.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
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

        # Back Button
        tk.Button(self, text="Back to Welcome Menu", command=lambda: controller.show_page(WelcomeMenu)).pack(pady=10)

        # Error message label
        self.error_message = tk.Label(self, text="", fg="red")
        self.error_message.pack(pady=5)

    def login(self):
        """
        Handles the login logic by retrieving the username and password entered by the user and verifying they are in a users row. 
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
            #self.username_entry.delete(0, tk.END)
            #self.password_entry.delete(0, tk.END)
            #self.error_message.config(text="")
            self.controller.show_page(MainMenu)
            
        else:
            self.error_message.config(text="Wrong username or password")




# My Account Page
class MyAccountPage(tk.Frame):
    """
    The my account page class that displays the user's account information.

    Methods:
        __init__(parent, controller): Initializes the my account page.
        show_info(): Displays the user's account information.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="My Account", font=("Arial", 16)).pack(pady=20)

        # Account information
        self.show_info()

        # Back Button
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_page(MainMenu)).pack(pady=10)

        # Back Button
        tk.Button(self, text="Log out", command=lambda: (controller.show_page(WelcomeMenu))).pack(pady=10)

    def show_info(self):
        user = self.controller.get_user_info()
        if user:
            tk.Label(self, text=f"Full name: {user['name']}").pack(pady=5)
            tk.Label(self, text=f"Username: {user['username']}").pack(pady=5)
            tk.Label(self, text=f"Password: {user['password']}").pack(pady=5)


# Main Menu Page, all functionalities can be accessed from here
class MainMenu(tk.Frame):
    """
    The main menu page class that displays the main menu options and enables booking flights.

    Methods:
        __init__(parent, controller): Initializes the main menu page.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        #tk.Label(self, text="Super flights", font=("Arial", 16)).pack(pady=20)

        # Upper left buttons
        button_frame = tk.Frame(self)
        button_frame.pack(anchor="ne", padx=10, pady=10)

        # Admin-only buttons
        user_info = controller.get_user_info()
        if user_info["user_type"] == "admin":
            tk.Button(button_frame, text="Stats", command=lambda: controller.show_page(Stats)).pack(side="left", padx=5)
            tk.Button(button_frame, text="Manage Flights", command=lambda: controller.show_page(ManageFlights)).pack(side="left", padx=5)

        tk.Button(button_frame, text="My Bookings").pack(side="left", padx=5)
        tk.Button(button_frame, text="My Account", command=lambda: controller.show_page(MyAccountPage)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Log Off", command=lambda: controller.show_page(WelcomeMenu)).pack(side="left", padx=5)

        # Search field in the center
        search_frame = tk.Frame(self)
        search_frame.pack(expand=True, pady=10, anchor="n")

        tk.Label(search_frame, text="Book Flight\nSearch Flight by ID:").pack(pady=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(pady=5)
        tk.Button(search_frame, text="Search", command=self.search_flight).pack(pady=5)


    #TODO: add search, display and book functionality
    # Placeholder for search functionality
    def search_flight(self):
        flight_id = self.search_entry.get()
        # Implement the search functionality here
        print(f"Searching for flight ID: {flight_id}")


class Stats(tk.Frame):
    """
    Admin only statistics page class that displays stats for each individual flight.

    Methods:
        __init__(parent, controller): Initializes the stats page.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Upper left buttons
        button_frame = tk.Frame(self)
        button_frame.pack(anchor="ne", padx=10, pady=10)
        
        tk.Button(button_frame, text="Return", command=lambda: controller.show_page(MainMenu)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Log Off", command=lambda: controller.show_page(WelcomeMenu)).pack(side="left", padx=5)

        # Search field in the center
        search_frame = tk.Frame(self)
        search_frame.pack(expand=True, pady=10, anchor="n")

        tk.Label(search_frame, text="Show Stats\nSearch Flight by ID:").pack(pady=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(pady=5)
        tk.Button(search_frame, text="Search", command=self.search_flight).pack(pady=5)

    #TODO: add stats functionality
    # Placeholder for search functionality
    def search_flight(self):
        flight_id = self.search_entry.get()
        # Implement the search functionality here
        print(f"Searching for flight ID: {flight_id}")

        

class ManageFlights(tk.Frame):
    """
    Admin only page to create new templates for aircrafts and to add flights to the database.

    Methods:
        __init__(parent, controller): Initializes the stats page.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Upper left buttons
        button_frame = tk.Frame(self)
        button_frame.pack(anchor="ne", padx=10, pady=10)
        
        tk.Button(button_frame, text="Return", command=lambda: controller.show_page(MainMenu)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Log Off", command=lambda: controller.show_page(WelcomeMenu)).pack(side="left", padx=5)

        # action field in the center
        action_frame = tk.Frame(self)
        action_frame.pack(expand=True, pady=10, anchor="n")

        tk.Label(action_frame, text="Add to/Remove from the database").pack(pady=5)

        # Create a frame to hold the buttons
        button_frame = tk.Frame(action_frame)
        button_frame.pack(pady=5)

        # Add buttons side by side
        tk.Button(button_frame, text="Add aircraft", command=self.aircraft_options).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Add/Remove flight", command=self.flight_options).pack(side=tk.LEFT, padx=5)

        # Frame to either add or remove aircrafts or flights
        self.options_frame = tk.Frame(action_frame)
        self.options_frame.pack(anchor="n", padx=10, pady=10)

    #TODO: add functionalities to all these functions add aircrafts and flights 
    # and potentially change names to not match those on the database

    def clear_options_frame(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def aircraft_options(self):
        self.clear_options_frame()
    
        # Center widget above all others
        tk.Label(self.options_frame, text="Add aircraft:").pack(pady=5)

        # Frame to hold the three widgets side by side
        top_frame = tk.Frame(self.options_frame)
        top_frame.pack(pady=5)

        self.code = tk.Label(top_frame, text="Enter aircraft code:")
        self.code.pack(side=tk.LEFT, padx=5)

        self.layout = tk.Label(top_frame, text="Enter aircraft layout:\n e.g. 'ABC| |DEF'")
        self.layout.pack(side=tk.LEFT, padx=5)

        self.rows = tk.Label(top_frame, text="Enter number of rows:")
        self.rows.pack(side=tk.LEFT, padx=5)

        # Frame to hold the next three widgets side by side
        middle_frame = tk.Frame(self.options_frame)
        middle_frame.pack(pady=5)

        self.aircraft_code = tk.Entry(middle_frame)
        self.aircraft_code.pack(side=tk.LEFT, padx=5)

        self.aircraft_layout = tk.Entry(middle_frame)
        self.aircraft_layout.pack(side=tk.LEFT, padx=5)

        self.row_number = tk.Entry(middle_frame)
        self.row_number.pack(side=tk.LEFT, padx=5)

        # Widget at the bottom
        tk.Button(self.options_frame, text="Add").pack(pady=5)

    #TODO: finish design
    def flight_options(self):
        self.clear_options_frame()
        tk.Label(self.options_frame, text="Search Flight by ID:").pack(pady=5)
        self.search_entry = tk.Entry(self.options_frame)
        self.search_entry.pack(pady=5)
        tk.Button(self.options_frame, text="Search").pack(pady=5)

#TODO: add booking and cancellation functionalities
class MyBookings(tk.Frame):
    """
    Bookings page that displays user's bookings and allows cancellation.

    Methods:
        __init__(parent, controller): Initializes the Bookings page.
    """
    pass


# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
