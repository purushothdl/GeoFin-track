# create a login page for admin and user
# login page should have a username, password, role and login button
# in the users table add role as it is required to differentiate between admin and user
# if the role is admin then the user should be redirected to the admin page
# if the role is user then the user should be redirected to the user page

import streamlit as st
import sqlite3
import os
from pages.admin.outline import main_admin
from user import user_page

script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, 'database', 'databasefile.db')
db_path = os.path.abspath(db_path)

def authenticate_user(username, password, role):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Users WHERE
        Name = ? AND 
        Role = ? AND
        Password = ?""",
        (username, role, password))
    entry = cursor.fetchone()
    conn.close()

    if entry:
        return True
    else:
        return False
    

def login_page():
    
    
    # Create a form to handle submission
    with st.form(key='login_form'):
        st.title('GEOFIN TRACK')
        # Display username, password and role inputs
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        options = ['admin', 'user']
        role = st.selectbox('Select you role', options)
        
        # Add login button
        login_button = st.form_submit_button("Login")

        if login_button and role == 'admin' :
            if authenticate_user(username, password, role):
                st.session_state.logged_in_admin = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password")

        if login_button and role == 'user':
            if authenticate_user(username, password, role):
                st.session_state.logged_in_user = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password")


def main():
    if 'logged_in_admin' not in st.session_state:
        st.session_state.logged_in_admin = False

    if 'logged_in_user' not in st.session_state:
        st.session_state.logged_in_user = False

    if st.session_state.logged_in_admin:
        main_admin()
    
    elif st.session_state.logged_in_user:
        user_page()

    else:
        login_page()

if __name__ == "__main__":
    main()
