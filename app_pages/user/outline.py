import streamlit as st

# Multiple pages navigation for user
def main_user():
    
    dashboard = st.Page(
    page = 'app_pages/user/dashboard_user.py',
    title = 'Dashboard',
    icon = ':material/dashboard:',
    default = True   
    )

    user_management = st.Page(
    page = 'app_pages/user/country_manage_user.py',
    title = 'Country Management',
    icon = ':material/globe_asia:'
    )

    pg = st.navigation(pages = [dashboard, user_management])
    pg.run()
    