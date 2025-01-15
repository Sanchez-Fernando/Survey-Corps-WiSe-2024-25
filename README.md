# Survey Corps Python Project

## Description
We will be working on the default project. This will be a desktop application acting as a seat reservation site for flights.  
## Functionalities

### Data Sources and Retrieval
We will extract information from [this](https://www.kaggle.com/datasets/saadharoon27/airlines-dataset) dataset, more specifically from the "flights" table where we can use flight_id as a primary key. 
We also plan to get the number of seats and its distribution from the "aircrafts_data" table; this information would be fetched externally (using the model name).
### Data Storage and Handling
The data will be manipulated and stored using the sqlite3 library for python.
### User Management
There is a login system with two types of accounts: customers and administrators. The admin has access to certain functions through higher privileges such as canceling any reservation or viewing statistics (more to be determined later). The database contains userID, name, user_name and a password. The customer can book a reservation upon confirmation which he can also cancel.
### Interface
A desktop application is planned to be developed using PyQt. The application will feature a tab-based interface, allowing users to access various functionalities conveniently. The planned tabs and their functionalities are as follows:
-	Reservation and Booking Tab: This tab will enable users to reserve and book seats.
-	Booking History Tab: Users can view their past bookings in this section.
-	Statistics Tab: This tab will display various statistics.
-	User Management Tab (Optional): This tab will be available exclusively to admin users.
-	Help Page Tab: A dedicated tab to describe the functionality of the application

### Statistical Analysis
The mandatory statistics will be available:

- Number and percentage of available seats
- Number and percentage of reserved seats
- List of available seats 
- List of seats that are not available
- Number of users in the system with their information, except for their password

Plus seat prices and cashflow. 
These statistics will have also a graphical representation.

### Visualizations
Mathplotlib will be used for the visualization of charts and graphics.
## Installation and Usage
This is to be explained later.

## Group Details
- Group name: Survey Corps
- Group Code: G10
- Group repository: https://github.com/Sanchez-Fernando/Survey-Corps-WiSe-2024-25.git
- Tutor responsible:  Ole Hänies
- Group team leader: Fernando Sanchez
- Group members: Fernando Sanchez, Ahmad Dekmak, Andre Duong

Contributions are to be stated later.
## Acknowlegdments
This section will be progressively filled out the more we work on the project.
