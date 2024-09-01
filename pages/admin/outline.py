import streamlit as st

# Multiple pages navigation
def main_admin():
    
    dashboard = st.Page(
    page = 'pages/admin/dashboard.py',
    title = 'Dashboard',
    icon = ':material/dashboard:',
    default = True   
    )

    user_management = st.Page(
    page = 'pages/admin/user_management.py',
    title = 'User Management',
    icon = ':material/account_circle:'
    )

    region_management = st.Page(
    page = 'pages/admin/region_management.py',
    title = 'Region Management',
    icon = ':material/language:'
    )

    country_management = st.Page(
    page = 'pages/admin/country_management.py',
    title = 'country Management',
    icon = ':material/south_america:'
    )

    pg = st.navigation(pages = [dashboard, user_management, region_management, country_management])
    pg.run()
    