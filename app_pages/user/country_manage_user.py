import streamlit as st
import time
import pandas as pd
from database.repositories.country_details import add_entry, get_next_count_id, get_countries_from_region, get_entry, update_entry, delete_entry
from app_pages.admin.all_countries import all_countries
from app_pages.user.dashboard_user import get_user_continents
import base64



st.set_page_config(page_title="Country Management", page_icon=":material/south_america:")


## All the defined functions in this page

# Function to encode image as base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# Returns all the countries in a given region in a list 
def get_country_name(region:str):
    vals = get_countries_from_region(region)
    countries = [country[2] for country in vals]
    return countries


# Returns all the countries that are not present in the database for a given region
def avail_countries(region):
    all = all_countries[region]
    present = get_country_name(region)
    for country in present:
         if country in all:
              all.remove(country)
    return all



# Sidebar icon for country management and caption using html and css

local_image_path = "images/user/country.webp"  # Adjust this path as necessary
image_base64 = image_to_base64(local_image_path)

html_img = f"""
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{image_base64}" style = "width: 50%; padding-bottom: 12px;" />
        
    </div>
"""
st.sidebar.markdown(html_img, unsafe_allow_html=True)

html_string_cty_mng = """
    <div style="
        background-color: #E1EBEE; 
        text-align: center;  
        padding: 10px; 
        border-radius: 10px;
    ">
        <p style="margin: 0; font-size: 18px; font-weight: bold; color: black;">
            Country Management
        </p>
    </div>
"""
st.sidebar.markdown(html_string_cty_mng, unsafe_allow_html=True)



# Streamlit start

st.title('Country Management')
st.write('Add, Update or Delete countries.')


with st.container():
        col1, col2 = st.columns(2)
        
        # Adds new country in the database
        with col1:
            
            st.markdown(
                """
                <h3 style="font-family: Arial, sans-serif; color: #00b33c  ; text-align: left;">
                    Add Country
                </h3>
                """,
            unsafe_allow_html=True)
            


            st.write("Add new countries to the database. Click the dropdown menu to add new country info. ")
            st.write('\n')
            with st.expander('**Add New Country Details**'):
                
                st.write('')   
                count_id = get_next_count_id()
                region = st.selectbox("**Region**", get_user_continents(), key='region_ip')
                mapping = {'Asia' : 1, 'Africa' : 2, 'North America' : 3, 'South America' : 4, 'Europe' : 5, 'Oceania' : 6}
                region_id = mapping[region]
                countries = all_countries.get(region, [])

                country = st.selectbox("**Country**", options = avail_countries(region), key='country_ip')
                gfi_limit = st.text_input("**GFILimit**", key='gfi_ip')
                gfi_insitute = st.text_input("**GFIInstitute**", key='gfi_inst')
                trade_limits = st.text_input("**TradeLimits**", key='trade_limits')
                trade_os = st.text_input("**TradeOS**", key='trade_os')
                treasury_limits = st.text_input("**TreasuryLimits**", key='treasury_limits')
                treasury_os = st.text_input("**TreasuryOS**", key='treasury_os')
                total_limit = st.text_input("**TotalLimit**", key='total_limit')
                total_os_limit = st.text_input("**TotalOSLimit**", key='os_limit')
                submit = st.button('**Add**', use_container_width = True)
                    
                if submit:
                    try:
                        outcome = add_entry( count_id, region_id, country, gfi_limit, gfi_insitute, trade_limits,
                                                trade_os, treasury_limits, treasury_os, total_limit, total_os_limit )
                        if outcome is None:
                            msg = st.toast(f'Adding {country} to the {region}...')
                            time.sleep(1)
                            msg.toast('Successfully added', icon = "✅")
            
                        else:
                            st.error(f"{outcome}")   
                    except Exception as e:
                        st.error(f"{e}")


        # Updates existing country info
        with col2:

            st.markdown(
                """
                <h3 style="font-family: Arial, sans-serif; color: #4747d1  ; text-align: left;">
                    Update Country
                </h3>
                """,
            unsafe_allow_html=True)


            st.write("Update existing country information in the database.")
            st.write('')
            with st.expander('**Update Country Info**'):               
                
                region = st.selectbox('Region', options = get_user_continents(), placeholder = 'Enter region')
                country = st.selectbox('Country', options = get_country_name(region), key = 'country_up')
                data = get_entry(country)
                gfi_limit = st.text_input("**GFILimit**", data[3], key='gfi_up')
                gfi_insitute = st.text_input("**GFIInstitute**", data[4], key='gfi_inst_up')
                trade_limits = st.text_input("**TradeLimits**", data[5], key='trade_limits_up')
                trade_os = st.text_input("**TradeOS**", data[6], key='trade_os_up')
                treasury_limits = st.text_input("**TreasuryLimits**", data[7], key='treasury_limits_up')
                treasury_os = st.text_input("**TreasuryOS**", data[8], key='treasury_os_up')
                total_limit = st.text_input("**TotalLimit**", data[9], key='total_limit_up')
                total_os_limit = st.text_input("**TotalOSLimit**", data[10], key='os_limit_up')
                update = st.button('**Update**', use_container_width = True)

                if update:
                    entry = update_entry(country, gfi_limit, gfi_insitute, trade_limits, trade_os, treasury_limits, treasury_os,
                                        total_limit, total_os_limit)
                    if entry == None:
                        msg = st.toast(f"Updating country info")
                        time.sleep(1)
                        msg.toast('Country data updated', icon = '✅')
                        time.sleep(2)
                    
                    else:
                        st.error(entry)


with st.container():
    col1, col2 = st.columns(2)

    # Retrieve country details from the database
    with col1:

        st.markdown(
        """
        <h3 style="font-family: Arial, sans-serif; color: #e68a00  ; text-align: left;">
            Get Country Details
        </h3>
        """,
        unsafe_allow_html=True)

        st.write('Retrieve an existing Country and its info from the database.')
        with st.expander('**Enter the Country Details**'):
            region = st.selectbox('**Region**', options = get_user_continents(), placeholder = 'Enter region')
            count_name = st.selectbox('**Country**', options = get_country_name(region))
            data = get_entry(count_name)
            

            if 'Error' in data:
                st.error(f"{data}")

            else:
                with st.popover('**view country**', use_container_width = True):
                    data = pd.DataFrame(data).values.reshape(1, -1)
                    data = pd.DataFrame(data, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                                                         'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'])
                    st.dataframe(data, hide_index = True)

    st.write('')
    st.write('')

    # Deletes a country from the database
    with col2:
            st.markdown(
            """
            <h3 style="font-family: Arial, sans-serif; color: #A80000  ; text-align: left;">
                Delete Country
            </h3>
            """,
            unsafe_allow_html=True)

            st.write('Delete the existing country and its details from the database.')
            with st.expander('**Enter the Country Details**'):
                region = st.selectbox('**Region**', options = get_user_continents())
                count_name = st.selectbox('**Country**', options = get_country_name(region), key = 'count_del')
                delete = st.button('**Delete**', use_container_width = True)

                if delete:
                    outcome = delete_entry(count_name)
                    
                    if outcome is None:
                        msg = st.toast('Deleting country from the database...')
                        time.sleep(1)
                        msg.toast('Successfully deleted', icon = "✅")
                        time.sleep(2)
                        st.rerun()
                    
                    else:
                        st.error(outcome)
