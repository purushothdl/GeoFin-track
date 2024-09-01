import streamlit as st
import time
import pandas as pd
import pydeck as pdk
from database.repositories.country_details import add_entry, get_next_count_id, get_countries_from_region, get_entry, update_entry, delete_entry
from pages.admin.all_countries import all_countries

st.set_page_config(page_title="Country Management", page_icon=":material/south_america:")
st.sidebar.header('Country Management')

st.title('Country Management')
st.write('Add, Update or Delete countries.')

def get_country_name(region:str):
    vals = get_countries_from_region(region)
    countries = [country[2] for country in vals]
    return countries

def avail_countries(region):
    all = all_countries[region]
    present = get_country_name(region)
    for country in present:
         if country in all:
              all.remove(country)
    return all


with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("**Add Country**")
            st.write("Add new countries to the database. Click the dropdown menu to add new country info. ")
            st.write('\n')
            with st.expander('**Add New Country Details**'):
                
                st.write('')   
                count_id = get_next_count_id()
                region = st.selectbox("**Region**", ["Asia", "Africa", "North America", "South America", "Europe", "Oceania"], key='region_ip')
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


        with col2:

            st.header("**Update Country**")
            st.write("Update existing country information in the database.")
            st.write('')
            with st.expander('**Update Country Info**'):               
                
                region = st.selectbox('Region', options = ["Asia", "Africa", "North America", "South America", "Europe", "Oceania"], placeholder = 'Enter region')
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

    with col1:
        st.header('**Get Country Details**')
        st.write('Retrieve an existing Country and its info from the database.')
        with st.expander('**Enter the Country Details**'):
            region = st.selectbox('**Region**', options = ["Asia", "Africa", "North America", "South America", "Europe", "Oceania"], placeholder = 'Enter region')
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
            
    with col2:

            st.header('**Delete Country**')
            st.write('Delete the existing country and its details from the database.')
            with st.expander('**Enter the Country Details**'):
                
                region = st.selectbox('**Region**', options = ["Asia", "Africa", "North America", "South America", "Europe", "Oceania"], 
                                      placeholder = 'Enter region', key = 'region_del')
                count_name = st.selectbox('**Country**', options = get_country_name(region), key = 'count_del')
                delete = st.button('**Delete**', use_container_width = True)

                if delete:
                    outcome = delete_entry(count_name)
                    
                    if outcome is None:
                        msg = st.toast('Deleting country from the database...')
                        time.sleep(1)
                        msg.toast('Successfully deleted', icon = "✅")
                    
                    else:
                        st.error(outcome)

st.write('')
st.info("To view information about all the countries present in a region head over to region management.")


df = pd.read_csv('pages/user/countries.csv')

def get_lat_lon(country_name):
    # Filter the DataFrame for the country
    result = df[df['Country'] == country_name.title()]
    if not result.empty:
        location = result.iloc[0]
        return location['Latitude'], location['Longitude']
    return None, None


def region_map(region:str):
    
    all_countries = get_country_name(region)

    data = {
    'Country': [],
    'Latitude': [],
    'Longitude': []
    }

    for country in all_countries:
        lat, lon = get_lat_lon(country)
        if lat is not None and lon is not None:
            data['Country'].append(country)
            data['Latitude'].append(lat)
            data['Longitude'].append(lon)
        else:
            print(f"Skipping {country} due to missing coordinates.")

    df = pd.DataFrame(data)

    if not df.empty:
        # Create a Pydeck Layer
        layer = pdk.Layer(
            'ScatterplotLayer',
            df,
            get_position=['Longitude', 'Latitude'],
            get_fill_color=[255, 0, 0, 140],  # Red color with some transparency
            get_radius=50000,  # Radius in meters
            pickable=True
        )

        text_layer = pdk.Layer(
            'TextLayer',
            df,
            get_position=['Longitude', 'Latitude'],
            get_text='Country',
            get_size=24,
            get_color=[0, 0, 0, 255],  # Black color for text
            get_angle=0,
            get_text_anchor='middle'
        )
        
        # Create a Pydeck View
        view_state = pdk.ViewState(
            latitude=df['Latitude'].mean(),
            longitude=df['Longitude'].mean(),
            zoom=2,
            pitch=0
        )

        # Create the deck
        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{Country}"}
        )

        # Streamlit App
        st.subheader(region)
        st.pydeck_chart(deck)
        st.caption('The above map represents the countries that are presently accessed by the user.')
    else:
        st.write("No valid data available to display on the map.")


st.write('')
st.header("Accessed Countries")
tabs = st.tabs(["Asia", "Africa", "North America", "South America", "Europe", "Oceania"])

with tabs[0]:
    region_map("Asia")

with tabs[1]:
    region_map("Africa")

with tabs[2]:
    region_map("North America")

with tabs[3]:
    region_map("South America")

with tabs[4]:
    region_map("Europe")

with tabs[5]:
    region_map("Oceania")

