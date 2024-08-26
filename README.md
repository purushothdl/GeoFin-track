# GeoFin-Track: Role-Based Geographic Data Management

This project is a web application built with Streamlit, Python's popular framework for building interactive web apps. It provides user and admin functionalities to manage database tables using SQLite3. The application features a login page that differentiates user roles and directs users to appropriate pages based on their roles. Admins can manage all tables, while regular users have restricted access to specific functionalities.

## Project Overview
The web application has the following components:

1. **Login Page**: Users are prompted to enter a username, password, and role (Admin or User). Based on the provided credentials, users are redirected to the appropriate page:

- Admin Page: Admins can manage all three tables.
- User Page: Users can manage only the Country_Details table and view only the countries in the regions allotted to them by the admin.


2. **Admin Page**: Admins can perform CRUD (Create, Read, Update, Delete) operations on three tables:

- Region_Limits
- Country_Details
- Users

3. **User Page**: Users can perform CRUD operations on the Country_Details table only. They are restricted to viewing and managing countries that fall within the regions assigned to them by the admin.

## Modules Used
- sqlite3: For database interactions.
- pandas: For handling data in tabular form.
- time: For managing time-related operations.
- streamlit: For building the web interface.

## Setup and Installation

 #### 1. Prerequisites
Ensure you have Python 3.7 or higher installed. You also need to install the required Python modules using pip.
```
- pip install streamlit pandas sqlite3
```
  

#### 2. Project Structure
The project directory contains the following key files and directories:

- `loginpy.py`: The main script that runs the Streamlit application and handles user authentication and page routing.
  
- `database/`: Directory containing the SQLite database files and  table-specific functions.
  
- `pages/`: Directory with different Streamlit pages based on user roles:
  - `admin_page.py`: Page for Admins to manage `Region_Limits`, `Country_Details`, and `Users` tables.
  - `user_page.py`: Page for Users to manage the `Country_Details` table and view countries within their assigned regions.
  
- `.streamlit/`: Directory for modifying the fonts and color of the streamlit page.

#### 3. Running the Application
* Navigate to the Project Directory

* Open your terminal or command prompt and navigate to the directory containing loginpy.py.

* Run the Streamlit App

* Use the following command to start the Streamlit app:
```
- streamlit run login.py
```

#### 4. Access the Web Application

After running the command, Streamlit will start a local server. Open your web browser and go to http://localhost:8501 to access the application.

## Usage
### Login Page
* Enter Credentials: Input your username, password, and role (Admin or User) to log in.
    * Admins: Will be redirected to the Admin Page.
    * Users: Will be redirected to the User Page.

## Admin Page
* Manage Tables: Admins have full access to the following tables:
    
    * Region_Limits: Add, update, delete, or view records.
    * Country_Details: Add, update, delete, or view records.
    * Users: Add, update, delete, or view user records.

## User Page
* Manage Country Details: Users can:
    * Add: New entries to the Country_Details table.
    * Update: Existing entries in the Country_Details table.
    * Delete: Entries from the Country_Details table.
    * View: Only countries within the regions assigned to them by an admin.