

# GeoFin-Track: Role-Based Geographic Data Management

GeoFin-Track is a web application built using Streamlit, a popular framework for creating interactive web apps in Python. The application provides both user and admin functionalities to manage geographic and financial data stored in SQLite3 tables. It features a login system that differentiates between user roles, directing them to appropriate pages based on their access level. Admins can manage all tables, while regular users have limited access to specific functionalities.

## Project Overview

The web application has the following components:

- **Login Page**: Users enter their username, password, and role (Admin or User). Based on their credentials, they are redirected to the appropriate page:
  - **Admin Page**: Full management of all tables.
  - **User Page**: Restricted to managing and viewing data within assigned regions.

### Functionalities

- **Admin Page**: Admins have full CRUD (Create, Read, Update, Delete) access to the following tables:
  - `Region_Limits`: Manage region-based financial limits.
  - `Country_Details`: Manage financial details for countries.
  - `Users`: Manage user accounts and their roles.
- **User Page**: Users have restricted CRUD access to the `Country_Details` table, limited to countries within their assigned regions by the admin.

## Modules Used

- `sqlite3`: For database operations.
- `pandas`: For data manipulation in tabular form.
- `time`: For handling time-related operations.
- `streamlit`: For building the web interface.

## Setup and Installation

### 1. Prerequisites

Ensure Python 3.7 or higher is installed. Install the required Python modules using pip:

```bash
pip install streamlit pandas sqlite3
```

### 2. Project Structure

- **`login.py`**: Main script for running the Streamlit application, handling user authentication and page routing.
- **`database/`**: Contains SQLite database files and functions for table management.
- **`app_pages/`**: Contains folders for different user roles:
  - **`1.admin/`**: Contains files specific to the Admin's functionality, such as managing `Region_Limits`, `Country_Details`, and `Users`.
  - **`2.user/`**: Contains files specific to the User's functionality, such as managing the `Country_Details` table within assigned regions.
- **`.streamlit/`**: Customizes the fonts and colors of the Streamlit app.

### 3. Running the Application

#### Step 1: Fork the Repository

1. Go to the <https://github.com/purushothdl/GeoFin-track>.
2. Click the "Fork" button in the upper right corner to create a copy of the repository in your own GitHub account.

#### Step 2: Clone the Forked Repository

1. Open your terminal or command prompt.
2. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/purushothdl/GeoFin-track.git
   ```

3. Navigate to the project directory:

   ```bash
   cd GeoFin-track
   ```

#### Step 3: Run the Streamlit Application

- Run the Streamlit app:

   ```bash
   streamlit run login.py
   ```

### 4. Access the Web Application

After running the above command, Streamlit will start a local server. Open your web browser and go to [http://localhost:8501](http://localhost:8501) to access the application.

## Usage

### Login Page

- **Enter Credentials**: Input your username, password, and role (Admin or User) to log in.
  - **Admins**: Redirected to the Admin Page.
  - **Users**: Redirected to the User Page.

### Admin Page

- **Manage Tables**:
  - **`Region_Limits`**: Add, update, delete, or view records.
  - **`Country_Details`**: Add, update, delete, or view records.
  - **`Users`**: Add, update, delete, or view user records.

### User Page

- **Manage Country Details**:
  - **Add**: New entries to the `Country_Details` table.
  - **Update**: Existing entries in the `Country_Details` table.
  - **Delete**: Entries from the `Country_Details` table.
  - **View**: Only countries within the regions assigned to them by an admin.


