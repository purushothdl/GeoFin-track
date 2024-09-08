import streamlit as st
from login import get_name
import base64
import time

st.set_page_config(page_title="Dashboard", page_icon=":material/dashboard:")
st.title(f"Welcome back,  {get_name()}")


# Function to encode image as base64 (for sidebar)
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# Dashboard icon and caption for sidebar using html and css
local_image_path = "images/user/dashboard.webp"  # Adjust this path as necessary
image_base64 = image_to_base64(local_image_path)

html_img = f"""
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{image_base64}" style = "width: 50%; padding-bottom: 12px;" />
        
    </div>
"""
st.sidebar.markdown(html_img, unsafe_allow_html=True)

html_string_dboard = """
    <div style="
        background-color: #E1EBEE; 
        text-align: center;  
        padding: 5px; 
        border-radius: 10px;
        margin-bottom: 270px;
    ">
        <p style="margin: 0; font-size: 18px; font-weight: bold; color: black;">
            Dashboard
        </p>
    </div>
"""
st.sidebar.markdown(html_string_dboard, unsafe_allow_html=True)


# Logout functionality
if st.sidebar.button("Logout", type = 'primary', use_container_width = True):
    st.session_state.logged_in_admin = False
    st.toast("Logging out...", icon = "🔄")
    time.sleep(2)
    
    hide_sidebar_js = """
        <script>
        const sidebar = window.parent.document.querySelector('section[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.style.display = 'none';
        }
        </script>
    """
    st.components.v1.html(hide_sidebar_js, height=0, width=0)
    time.sleep(1)
    st.rerun()


# Enabling the sidebar using javascript (as it was disabled during logout)
enable_sidebar_js = """
<script>
const sidebar = window.parent.document.querySelector('section[data-testid="stSidebar"]');
if (sidebar) {
    sidebar.style.display = 'block';
}
</script>
    """
st.components.v1.html(enable_sidebar_js, height=0, width=0)



# Streamlit start 
st.header('**Admin actions**')
def main_dashboard():

    with st.container():
        col1, col2 = st.columns(2)
        
        # Loads Manage Users page
        with col1:
            with st.form(key = 'user'):
                st.markdown("### **Add New User**")
                st.write("Create a new use account with specific roles and permissions.")
                add_user = st.form_submit_button('Manage Users', type = 'primary')

                if add_user:
                    st.switch_page('pages/admin/user_management.py')
                
        # Loads Manage Regions page
        with col2:
            with st.form(key = 'regions'):
                st.write("### **Manage Regions**")
                st.write("Add or update regions for better localization of services.")
                manage_regions = st.form_submit_button('Manage Regions', type = 'primary')

                if manage_regions:
                    st.switch_page('pages/admin/region_management.py')

    # Loads Manage countries page
    with st.form(key = 'countries'):
        st.markdown("### **Manage Countries**")
        st.write("Add new countries to the database or manage existing country information.")
        manage_countries = st.form_submit_button('Manage Countries', type = 'primary')

        if manage_countries:
            st.switch_page('pages/admin/country_management.py')

main_dashboard()