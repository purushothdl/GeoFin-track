# create a login page for admin and user
# login page should have a email, password, role and login button
# in the users table add role as it is required to differentiate between admin and user
# if the role is admin then the user should be redirected to the admin page
# if the role is user then the user should be redirected to the user page

import streamlit as st
import sqlite3
import os
import base64
from app_pages.admin.outline import main_admin
from app_pages.user.outline import main_user
from database.repositories.users import get_by_email

script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, 'database', 'databasefile.db')
db_path = os.path.abspath(db_path)

def authenticate_user(email, password, role):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Users WHERE
        Email = ? AND 
        Role = ? AND
        Password = ?""",
        (email, role, password))
    entry = cursor.fetchone()
    conn.close()

    if entry:
        return True
    else:
        return False

# Function to encode image as base64 (for sidebar)
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()    


def login_page():
    
    
    # Create a form to handle submission
    with st.container():
        col1, col2 = st.columns(2)

        with col2:
            
            local_image_path = "images/logos/fintrack.webp"  # Adjust this path as necessary
            image_base64 = image_to_base64(local_image_path)

            html_img = f"""
                <div style="text-align: center; width: 100%; height: 100%;">
                    <img src="data:image/jpeg;base64,{image_base64}" style="width: 100%; 
                    margin-top: 50px; margin-left: 30px; height: auto; max-width: 100%; max-height: 100%;" />
                </div>
            """
            st.markdown(html_img, unsafe_allow_html=True)



        with col1:
            with st.form('login_form'):
                with st.container():
                    st.markdown("<h1 style='text-align: center; margin-left: 18px; color: black;'>GeoFinTrack</h1>", unsafe_allow_html=True)
                    email = st.text_input('**Email**', placeholder = 'Enter you email' )
                    password = st.text_input('**Password**', type = 'password', placeholder = '******************')
                    options = ['admin', 'user']
                    role = st.selectbox('**Select role**', options)

                    st.session_state.email = email
                    st.write('')
                    with st.container():
                        col1, col2= st.columns(2)    
                        with col1:
                            login_button = st.form_submit_button("**Login**", type = 'primary')

                        with col2:
                            st.markdown("""
                                <h6 style = '
                                    text-align: center; 
                                    margin-top: 9px;
                                    margin-left: 0px;
                                    font-weight: bold; 
                                    color: rgb(10, 107, 254);'>
                                        Forgot Password?
                                </h6>""", unsafe_allow_html=True)
        
                    if login_button and role == 'admin' :
                        if authenticate_user(email, password, role):
                            st.session_state.logged_in_admin = True
                            st.session_state.email = email
                            st.rerun()
                        else:
                            st.error("Invalid email or password")

                    if login_button and role == 'user':
                        if authenticate_user(email, password, role):
                            st.session_state.logged_in_user = True
                            st.session_state.email = email
                            st.rerun()
                        else:
                            st.error("Invalid email or password")

        st.markdown("""
                <h6 style='
                    text-size-adjut: none;
                    display: block;
                    font-size: 14px;
                    margin-right: 0px;
                    margin-left: 50px; 
                    color: #808080;'>
                        ©2024 GeoFinTrack. All rights reserved.
                </h6>""", unsafe_allow_html=True)
        



def get_name():
    data = get_by_email(st.session_state.email)
    return data[1]


def main():
    if 'logged_in_admin' not in st.session_state:
        st.session_state.logged_in_admin = False

    if 'logged_in_user' not in st.session_state:
        st.session_state.logged_in_user = False

    if st.session_state.logged_in_admin:
        main_admin()
    
    elif st.session_state.logged_in_user:
        main_user()

    else:
        login_page()

if __name__ == "__main__":
    main()
