import streamlit as st
# import pandas as pd
# from database.repositories.country_details import  get_countries_from_region
# from pages.user.dashboard_user import get_user_regions


# def get_user_continents():
#     vals = get_user_regions().split(',')
#     vals = [country.replace('"','').strip() for country in vals]
#     return vals

# def get_country_name(region):
#     vals = get_countries_from_region(region)
#     countries = [country[2] for country in vals ]
#     return countries

# st.title('COUNTRY MANAGEMENT')

# with st.container():
#     col1, col2 = st.columns(2)

#     with col1:
#         st.header("**Add Country**")
#         st.write("Add new country to the database. Click the dropdown menu to add new country details to the database. ")
#         st.write('\n')
#         with st.expander('**Add New Country Details**'):
#                 st.write('')
#                 with st.form(key = 'add_menu', border = False, clear_on_submit = True):     
#                     id = get_next_id()
#                     name = st.text_input('Name', key = 'name_ad')
#                     options = ['admin', 'user']
#                     role = st.selectbox('Select you role', options, key = 'role_ad')
#                     email = st.text_input('Email', key = 'email_ad')
#                     password = st.text_input('Password', key = 'password_ad')
#                     region = st.multiselect(
#                                 "Accessed Regions",
#                                 ["Asia", "Africa", "North America", "South America", "Europe", "Australia"],
#                                 placeholder = 'choose from below')


#                     submit = st.form_submit_button('**Add**')
                    

#                     if submit:       
#                             try:
#                                 outcome = add_entry(int(id), str(name), str(role), str(email), str(password), str(region))
#                                 if outcome is None:
#                                     msg = st.toast('Adding user to the database...')
#                                     time.sleep(1)
#                                     msg.toast('Successfully added', icon = "✅")
                    
#                                 else:
#                                     st.error(f"{outcome}")   
#                             except Exception as e:
#                                 st.error(f"{e}")







#     with col2:
#         with st.form(key = 'update_country'):
#             st.header('Update Country')
#             st.write('Click below to update the existing country details.')
#             update = st.form_submit_button('**Update country**', type = 'primary')

st.info('Here goes Country management code.')