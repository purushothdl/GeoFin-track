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

    pg = st.navigation(pages = [dashboard, user_management])
    pg.run()
    


if __name__ == "__main__":
    main_admin()