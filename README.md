# Survey Corps Python Project

## Description
The (default) project implements a seat reservation system for an airplane consisting of:
- A database for data storage
- A frontend
- A computing backend implemented in Python
## Functionalities

### Data Sources and Retrieval
We extract information from [this](https://www.kaggle.com/datasets/saadharoon27/airlines-dataset) dataset, more specifically from the "flights" table. 
We also extract the number of seats and its distribution from the "aircrafts_data" table; this information is fetched externally (using the model name).
### Data Storage and Handling
The data gets manipulated and stored using the sqlite3 library for python.
### User Management
There is a login system with two types of accounts: customers and administrators. The customer can book a reservation upon confirmation which he can also cancel. The admin additionally has access to functions such as canceling any reservation, managing flights or viewing statistics. You can create an account on the Welcome Menu.
### Interface
The desktop application utilizes tkinter. It features a tab-based interface, allowing users to access various functionalities conveniently.
### Statistical Analysis
The statistics of the specific flight information will be visualized in a pie chart through Matplotlib (admin only).
This information can be saved into a text file.

## Installation and Usage
Clone this Repository.
This application runs on Python.
Sample admin account: 
- Username: angel31
- Password: 54321

## Group Details
- Group name: Survey Corps
- Group Code: G10
- Group repository: https://github.com/Sanchez-Fernando/Survey-Corps-WiSe-2024-25.git
- Tutor responsible:  Ole Hänies
- Group team leader: Fernando Sanchez
- Group members: Fernando Sanchez, Ahmad Dekmak, Andre Duong

## Acknowledgments
- Fernando: Database, Login & Register, MyAccount, Interface.
- Andre: Statistics, Help Page
- Ahmad: MyBookings, Reservations
