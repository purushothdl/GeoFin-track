import streamlit as st

# Multiple pages navigation
def main_user():
    
    dashboard = st.Page(
    page = 'pages/user/dashboard_user.py',
    title = 'Dashboard',
    icon = ':material/dashboard:',
    default = True   
    )

    user_management = st.Page(
    page = 'pages/user/country_manage_user.py',
    title = 'Country Management',
    icon = ':material/globe_asia:'
    )

    pg = st.navigation(pages = [dashboard, user_management])
    pg.run()
    