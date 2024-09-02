import streamlit as st
from login import get_name

st.set_page_config(page_title="Dashboard", page_icon=":material/dashboard:")
st.sidebar.header('Dashboard')
st.title(f"Welcome back,  {get_name()}")
st.header('**Admin actions**')

def main_dashboard():

    with st.container():
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.form(key = 'user'):
                st.markdown("### **Add New User**")
                st.write("Create a new use account with specific roles and permissions.")
                add_user = st.form_submit_button('Manage Users', type = 'primary')

                if add_user:
                    st.switch_page('pages/admin/user_management.py')
                
        
        with col2:
            with st.form(key = 'regions'):
                st.write("### **Manage Regions**")
                st.write("Add or update regions for better localization of services.")
                manage_regions = st.form_submit_button('Manage Regions', type = 'primary')

                if manage_regions:
                    st.switch_page('pages/admin/region_management.py')

    with st.container():

        col1, col2 = st.columns(2)

        with col1:
            with st.form(key = 'countries'):
                st.markdown("### **Manage Countries**")
                st.write("Add new countries or manage existing country information.")
                manage_countries = st.form_submit_button('Manage Countries', type = 'primary')

                if manage_countries:
                    st.switch_page('pages/admin/country_management.py')

        with col2:
            with st.form(key = 'logs'):
                st.markdown("### **User Logs**")
                st.write("Review user activity logs for security and auditing purposes")
                user_logs = st.form_submit_button('View Logs', type = 'primary')
    
main_dashboard()