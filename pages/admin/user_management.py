import streamlit as st
import sqlite3
import os
import pandas as pd
from database.repositories.users import get_entry, update_entry, add_entry, delete_entry, get_all


# Get the path to the current databasefile
script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, '..', '..', 'database', 'databasefile.db')
db_path = os.path.abspath(db_path)


st.set_page_config(page_title="User Management", page_icon=":material/account_circle:")
st.sidebar.header("User Management")
st.title('USER MANAGEMENT')
st.write('Add, Update or Delete users')


def main_user_management():
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.header("**ADD USER**")
            st.write("Add new users to the database. Click the dropdown menu to add new users to the database. ")
            st.write('\n')
            with st.expander('**Add New User Details**'):
                 
                id = st.text_input('UserID', key = 'id_ad')
                name = st.text_input('Name', key = 'name_ad')
                options = ['admin', 'user']
                role = st.selectbox('Select you role', options, key = 'role_ad')
                email = st.text_input('Email', key = 'email_ad')
                password = st.text_input('Password', key = 'password_ad')
                region  = st.text_input('AccessedRegion', key = 'region_ad')
                submit = st.button('**Add**')
    
                if submit:       
                        outcome = add_entry(int(id), str(name), str(role), str(email), str(password), str(region))
                        if outcome is not None:
                            st.error(f"{outcome}")
                        st.rerun()
    
        with col2:
        
            st.header("**UPDATE USER**")
            st.write("Update existing users in the database by the UserID.")
            st.write('')
            with st.expander('**Enter the UserID**'):   
                id = st.text_input('UserID', key = 'update_id')
                
                if id != '':
                    data = get_entry(id)
                    if 'Error' not in data:
                        with st.popover('**Update User information**'):
                            name = st.text_input('Name', data[1], key = 'name_up' )
                            options = ['admin', 'user']
                            index = options.index(data[2])
                            role = st.selectbox('Select you role', options, index = index, key = 'role_up')
                            email = st.text_input('Email', data[3], key = 'email_up')
                            password = st.text_input('Password', data[4], key = 'password_up')
                            region  = st.text_input('AccessedRegion', data[5], key = 'region_up')
                            submit = st.button('**Update**')       
                        if submit:
                                update_entry(id, name, role, email, password, region )

                    else:
                        st.error(f"User with UserID {id} not found")
                    
                            

    with st.container():
        col1, col2 = st.columns(2)
  
        with col1:
            st.header('**GET USER**')
            st.write('Retrieve an existing user from the database using UserID.')
            with st.expander('**Enter the UserID**'):
                id = st.text_input('ID', key = 'id_get')
                get = st.button('**Get User**')
                if get:
                    entry = get_entry(id)
                    
                    if 'Error' in entry:
                        st.error(f"{entry}")
                    
                    else:
                        data = pd.DataFrame(entry).values.reshape(1, -1)
                        data = pd.DataFrame(data, columns = ['UserID', 'Name', 'Role', 'Email', 'Password', 'AccessedRegions'])
                        st.dataframe(data, hide_index = True)
                       
                        close = st.button('**close**', key = 'close_get')
        
        with col2:
            st.header('**DELETE USER**')
            st.write('Delete the existing user from the database by the UserID.')
            with st.expander('**Enter the UserID**'):
                id = st.text_input('ID', key = 'id_del')
                delete = st.button('**Delete User**')

            if delete:
                outcome = delete_entry(id)
                if outcome != None:
                    st.error(outcome)
    
    
    with st.form(key = 'all'):
        
        st.markdown("## **SHOW ALL USERS**")
        st.write('Displays all the users and their information present in the database.')
        all = st.form_submit_button('**Show All Users**')

        if all:

            entries = get_all()
            data = pd.DataFrame(entries, columns = ['UserID', 'Name', 'Role', 'Email', 'Password', 'AccessedRegions'] )
            data = data.sort_values(by = 'UserID', ascending = True)
            st.dataframe(data, hide_index = True)

            with st.container():
                col1, col2, col3, col4, col5 = st.columns(5)
                with col3:
                    st.form_submit_button('**close**')
main_user_management()
