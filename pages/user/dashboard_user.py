import streamlit as st
from login import get_name
from database.repositories.users import get_by_email
import pandas as pd
from database.repositories.country_details import  get_countries_from_region
import pydeck as pdk



st.set_page_config(page_title="Dashboard", page_icon=":material/dashboard:")
st.sidebar.header('Dashboard')
st.title(f"Hello,  {get_name()}")
st.header('**User actions**')

df = pd.read_csv('pages/user/countries.csv')

def get_lat_lon(country_name):
    # Filter the DataFrame for the country
    result = df[df['Country'] == country_name.title()]
    if not result.empty:
        location = result.iloc[0]
        return location['Latitude'], location['Longitude']
    return None, None


def get_country_name(region):
    vals = get_countries_from_region(region)
    countries = [country[2] for country in vals ]
    return countries

def get_user_regions():
    data = get_by_email(st.session_state.email)
    return str(data[-1][1:-1])


def get_user_continents():
    vals = get_user_regions().split(',')
    vals = [country.replace('"','').strip() for country in vals]
    return vals

def total_countries():
    total = []
    for c in get_user_continents():
        total += get_country_name(c)
    return total


def main_dashboard():

    with st.container():
        
        col1, col2 = st.columns(2, gap = 'small')
        
        with col1:
            with st.form(key = 'Country'):
                st.markdown("### **Add New Country**")
                st.write("Click the below button to head over to manage countries section.")
                add_user = st.form_submit_button('Manage Countries', type = 'primary')

                if add_user:
                    st.switch_page('pages/user/country_manage_user.py')
                
        
        with col2:
            with st.form(key = 'regions'):
                st.write("### **Accessed Regions**")
                st.write("Click the below button to view your assigned regions.")
                assign_regions = st.form_submit_button('View Regions', type = 'primary')

            if assign_regions:
                with st.expander("Accessed Regions", expanded=True):
                    for continent in get_user_continents():
                        st.info(continent, icon = "◾" )
                    st.button("Close", on_click=lambda: st.expander("Form Submitted", expanded=False), type = 'primary')

        st.write('')

    # with st.container():

    #     col1, col2 = st.columns(2)

    #     with col1:
    #         with st.form(key = 'countries'):
    #             st.markdown("### **Manage Countries**")
    #             st.write("Add new countries or manage existing country information.")
    #             manage_countries = st.form_submit_button('Manage Countries', type = 'primary')

    #     with col2:
    #         with st.form(key = 'logs'):
    #             st.markdown("### **User Logs**")
    #             st.write("Review user activity logs for security and auditing purposes")
    #             user_logs = st.form_submit_button('View Logs', type = 'primary')


    all_countries = total_countries()

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
        st.header('**Accessed Countries**')
        st.pydeck_chart(deck)
        st.caption('The above map represents the countries that are presently accessed by the user.')
    else:
        st.write("No valid data available to display on the map.")


    # mapping = {'Asia-Pacific' : 1, 'Africa' : 2, 'North America' : 3, 'South America' : 4, 'Europe' : 5, 'Australia' : 6}

    st.write('')
    st.write('')
    [Asia_Pacific, Africa, North_America, South_America, Europe, Australia] = st.tabs(['Asia-Pacific', 'Africa', 'North America', 'South America', 'Europe', 'Australia'])
    
    all_continents = get_user_continents()

    with Asia_Pacific:
        if 'Asia-Pacific' in all_continents:
            st.subheader('Asia-Pacific')
            entries = get_countries_from_region('Asia-Pacific')
            data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                    'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
            data = data.sort_values(by = 'CountryID', ascending = True)
            st.dataframe(data, hide_index = True, width = 700 )

        else:
            st.info('This region is currently not accessible by you. Contact administrator for further info.')

    with Africa:
        if 'Africa' in all_continents:
            st.subheader('Africa')
            entries = get_countries_from_region('Africa')
            data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                    'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
            data = data.sort_values(by = 'CountryID', ascending = True)
            st.dataframe(data, hide_index = True, width = 700 )

        else:
            st.info('This region is currently not accessible by you. Contact administrator for further info.')    
    
        with North_America:
            if 'North America' in all_continents:
                st.subheader('North America')
                entries = get_countries_from_region('North America')
                data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                        'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
                data = data.sort_values(by = 'CountryID', ascending = True)
                st.dataframe(data, hide_index = True, width = 700 )

            else:
                st.info('This region is currently not accessible by you. Contact administrator for further info.')    

        with South_America:
            if 'South America' in all_continents:
                st.subheader('South America')
                entries = get_countries_from_region('South America')
                data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                        'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
                data = data.sort_values(by = 'CountryID', ascending = True)
                st.dataframe(data, hide_index = True, width = 700 )

            else:
                st.info('This region is currently not accessible by you. Contact administrator for further info.')
       
        with Europe:
            if 'Europe' in all_continents:
                st.subheader('Europe')
                entries = get_countries_from_region('Europe')
                data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                        'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
                data = data.sort_values(by = 'CountryID', ascending = True)
                st.dataframe(data, hide_index = True, width = 700 )

            else:
                st.info('This region is currently not accessible by you. Contact administrator for further info.')

        with Australia:
            if 'Australia' in all_continents:
                st.subheader('Australia')
                entries = get_countries_from_region('Australia')
                data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                        'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
                data = data.sort_values(by = 'CountryID', ascending = True)
                st.dataframe(data, hide_index = True, width = 700 )

            else:
                st.info('This region is currently not accessible by you. Contact administrator for further info.')
        
main_dashboard()

