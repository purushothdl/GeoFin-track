import streamlit as st
import os
import time
import pandas as pd

from database.repositories.users import(
    add_entry,
    get_entry, 
    get_by_email, 
    update_entry,
    update_by_mail,  
    delete_entry,
    delete_by_mail, 
    get_all, 
    get_next_id
)


st.set_page_config(page_title="User Management", page_icon=":material/account_circle:")
st.sidebar.header("User Management")
st.title('USER MANAGEMENT')
st.write('Add, Update or Delete users')


def main_user_management():

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.header("**Add User**")
            st.write("Add new users to the database. Click the dropdown menu to add new users to the database. ")
            st.write('\n')
            with st.expander('**Add New User Details**'):
                st.write('')
                with st.form(key = 'add_menu', border = False, clear_on_submit = True):     
                    id = get_next_id()
                    name = st.text_input('Name', key = 'name_ad')
                    options = ['admin', 'user']
                    role = st.selectbox('Select you role', options, key = 'role_ad')
                    email = st.text_input('Email', key = 'email_ad')
                    password = st.text_input('Password', key = 'password_ad')
                    region = st.multiselect(
                                "Accessed Regions",
                                ["Asia", "Africa", "North America", "South America", "Europe", "Australia"],
                                placeholder = 'choose from below')


                    submit = st.form_submit_button('**Add**')
                    

                    if submit:       
                            try:
                                outcome = add_entry(int(id), str(name), str(role), str(email), str(password), str(region))
                                if outcome is None:
                                    msg = st.toast('Adding user to the database...')
                                    time.sleep(1)
                                    msg.toast('Successfully added', icon = "✅")
                    
                                else:
                                    st.error(f"{outcome}")   
                            except Exception as e:
                                st.error(f"{e}")
                            

        with col2:
        
            st.header("**Update User**")
            st.write("Update existing users in the database by the User Email.")
            st.write('')
            with st.expander('**Enter the User Email**'):   
                
                mail = st.text_input('Email', placeholder = 'Press enter to view user')
                # st.divider()
                if mail != '':
                    data = get_by_email(mail)

                    if 'Error' not in data:
                       
                        # with st.popover('**Update User information**'):
                        #     # id = st.text_input('ID', data[0], key = 'id_up')
                        #     name = st.text_input('Name', data[1], key = 'name_up' )
                        #     options = ['admin', 'user']
                        #     index = options.index(data[2])
                        #     role = st.selectbox('Select you role', options, index = index, key = 'role_up')
                        #     email = st.text_input('Email', data[3], key = 'email_up')
                        #     password = st.text_input('Password', data[4], key = 'password_up')
                        #     region  = st.text_input('AccessedRegion', data[5], key = 'region_up')
                        #     submit = st.button('**Update**')   

                        with st.form('**Update User information**', clear_on_submit = True, border = False):
                            # id = st.text_input('ID', data[0], key = 'id_up')
                            st.markdown("<h3 style='text-align: center; margin-left: 18px; color: black; font-weight: bold;'>UPDATE USER</h3>", unsafe_allow_html=True)
                            name = st.text_input('Name', data[1], key = 'name_up' )
                            options = ['admin', 'user']
                            index = options.index(data[2])
                            role = st.selectbox('Select you role', options, index = index, key = 'role_up')
                            email = st.text_input('Email', data[3], key = 'email_up')
                            password = st.text_input('Password', data[4], key = 'password_up')
                            region  = st.text_input('AccessedRegion', data[5], key = 'region_up')
                            submit = st.form_submit_button('**Update**')    


                        if submit:
                                update_by_mail(name, role, email, password, region )
                                msg = st.toast(f"Updating user info...")
                                time.sleep(1)
                                msg.toast('User data updated', icon = '✅')
                                # time.sleep(2)
                                
                    else:
                        st.error(data)
                        #st.error(f"Error : User with Email {mail} not found")
                    
                            

    with st.container():
        col1, col2 = st.columns(2)

        with col1:

            st.header('**Get User**')
            st.write('Retrieve an existing user from the database using User Email.')
            with st.expander('**Enter the User Email**'):
                mail = st.text_input('Email', key = 'mail_get' ,placeholder = 'Press enter to view user')  
                
                
                # if get:
                #     entry = get_by_email(mail)
                    
                #     if 'Error' in entry:
                #         st.error(f"{entry}")
                    
                #     else:
                #         with st.popover('**Show User**'):
                #             data = pd.DataFrame(entry).values.reshape(1, -1)
                #             data = pd.DataFrame(data, columns = ['UserID', 'Name', 'Role', 'Email', 'Password', 'AccessedRegions'])
                #             st.dataframe(data, hide_index = True)
                if mail != '':
                    data = get_by_email(mail)
                    if 'Error' in data:
                        st.error(f"{data}")
                    else:
                        with st.popover('**Show User**'):
                            data = pd.DataFrame(data).values.reshape(1, -1)
                            data = pd.DataFrame(data, columns = ['UserID', 'Name', 'Role', 'Email', 'Password', 'AccessedRegions'])
                            st.dataframe(data, hide_index = True)   
                        
                    # close = st.button('**close**', key = 'close_get')
    
        with col2:

            st.header('**Delete User**')
            st.write('Delete the existing user from the database by the User Email.')
            with st.expander('**Enter the User Email**'):
                mail = st.text_input('Email', key = 'mail_del')
                delete = st.button('**Delete User**')

            if delete:
                outcome = delete_by_mail(mail)
                if outcome is None:
                    msg = st.toast('Deleting user from the database...')
                    time.sleep(1)
                    msg.toast('Successfully deleted', icon = "✅")
                if outcome != None:
                    st.error(outcome)


    with st.form(key = 'all'):
        
        st.markdown("## **Show all Users**")
        st.write('Displays all the users and their information present in the database.')
        all = st.form_submit_button('**Show All Users**')

        if all:

            entries = get_all()
            data = pd.DataFrame(entries, columns = ['UserID', 'Name', 'Role', 'Email', 'Password', 'AccessedRegions'] )
            data = data.sort_values(by = 'UserID', ascending = True)
            st.dataframe(data, hide_index = True, width = 700 )

            with st.container():

                col1, col2, col3, col4, col5 = st.columns(5)
                with col3:
                    st.form_submit_button('**close**')

main_user_management()
