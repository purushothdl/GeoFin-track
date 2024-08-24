# All user related features should be available to the user

# This is a test user page

import streamlit as st

def user_page():
    st.title(f"Welcome, {st.session_state.username}!")
    st.write("You are an User.")
    st.write("You can view the financial details of various countries and their regions.")