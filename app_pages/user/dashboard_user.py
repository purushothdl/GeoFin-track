import streamlit as st
from login import get_name
from database.repositories.users import get_by_email
import pandas as pd
from database.repositories.country_details import  get_countries_from_region, get_entry
import pydeck as pdk
import time
import base64


#st.set_page_config(page_title="Dashboard", page_icon=":material/dashboard:")


### All the defined functions in this page

# Function to encode image as base64 (for sidebar)
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# Gives coordinates of the countries stored in csv file
df = pd.read_csv('app_pages/user/countries.csv')
def get_lat_lon(country_name):
    # Filter the DataFrame for the country
    result = df[df['Country'] == country_name.title()]
    if not result.empty:
        location = result.iloc[0]
        return location['Latitude'], location['Longitude']
    return None, None


# The below two functions are extensions of one another. Returns the regions accessed by the current logged in user
# in string and list format respectively.
def get_user_regions():
    data = get_by_email(st.session_state.email)
    return str(data[-1][1:-1])

def get_user_continents():
    vals = get_user_regions().split(',')
    vals = [country.replace('"','').strip() for country in vals]
    return vals


# Returns all the country names from a given region
def get_country_name(region:str):
    vals = get_countries_from_region(region)
    countries = [country[2] for country in vals]
    return countries


# Returns the list of countries present in the region
def total_countries():
    total = []
    for c in get_user_continents():
        total += get_country_name(c)
    return total


# Welcome message for the user
welcome = f"Welcome Back, {get_name()}"
html_string_dboard = f"""
    <div style="
        background-color: #d4f1f4; 
        text-align: center;  
        padding: 1px;
        border: 1px solid black; 
        border-radius: 10px;
    ">
        <h3 style=" font-size: 40px; font-weight: bold; color: black;">
            {welcome}
        </h3>
    </div>
"""
st.markdown(html_string_dboard, unsafe_allow_html=True)


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
        margin-bottom: 200px;
    ">
        <p style="margin: 0; font-size: 18px; font-weight: bold; color: black;">
            Dashboard
        </p>
    </div>
"""
st.sidebar.markdown(html_string_dboard, unsafe_allow_html=True)


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


# Logout functionality
if st.sidebar.button("Logout", type = 'primary', use_container_width = True):
    st.session_state.logged_in_user = False
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


# Streamlit program start
st.header('**User actions**')
def main_dashboard():

    with st.container():
        col1, col2 = st.columns(2, gap = 'small')
        
        with col1:
            with st.form(key = 'Country'):
                st.markdown("### **Add New Country**")
                st.write("Click the below button to head over to manage countries section.")
                add_user = st.form_submit_button('Manage Countries', type = 'primary')

                if add_user:
                    st.switch_page('app_pages/user/country_manage_user.py')

        
        with col2:
            with st.form(key = 'regions'):
                st.write("### **Accessed Regions**")
                st.write("Click the below button to view your assigned regions.")
                assign_regions = st.form_submit_button('View Regions', type = 'primary')

            if assign_regions:
                with st.expander("Accessed Regions", expanded=True):
                    for continent in get_user_continents():
                        st.info(continent )
                    st.button("Close", on_click=lambda: st.expander("Form Submitted", expanded=False), type = 'secondary', use_container_width = True)

        st.write('')


    # Pydeck map to display countries in accessed regions
    all_countries = total_countries()

    data = {
    'Country': [],
    'Latitude': [],
    'Longitude': [],
    'tl_limits': [],
    'tl_os_limits': []
    }

    for country in all_countries:
        lat, lon = get_lat_lon(country)
        if lat is not None and lon is not None:
            data['Country'].append(country)
            data['Latitude'].append(lat)
            data['Longitude'].append(lon)
            data['tl_limits'].append(get_entry(country)[-2])
            data['tl_os_limits'].append(get_entry(country)[-1])
        else:
            print(f"Skipping {country} due to missing coordinates.")
    
    # Convert total_limits and total_os_limits into Billions
    data['tl_limits'] = [round(int(val)/(10**9), 3)  for val in data['tl_limits']]
    data['tl_os_limits'] = [round(int(val)/(10**9),3) for val in data['tl_os_limits']]
    
    df = pd.DataFrame(data)

    if not df.empty:
        # Create a Pydeck Layer
        layer = pdk.Layer(
            'ScatterplotLayer',
            df,
            get_position=['Longitude', 'Latitude'],
            get_fill_color=[255, 0, 0, 200],  # Red color with some transparency
            get_radius=80000,  # Radius in meters
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
            tooltip={"text": "{Country}\n TotalLimitUSD: {tl_limits} Billion\n TotalOSLimitUSD: {tl_os_limits} Billion"}
        )

        # Streamlit App
        st.header('**Accessed Countries**')
        st.pydeck_chart(deck)
        st.caption('The above map represents the countries that are presently accessed by the user.')
    else:
        st.write("No valid data available to display on the map.")

    st.write('')
    st.write('')

    # Tabs for different regions to display country details in dataframe
    [Asia_Pacific, Africa, North_America, South_America, Europe, Oceania] = st.tabs(['Asia', 'Africa', 'North America', 'South America', 'Europe', 'Oceania'])
    
    all_continents = get_user_continents()

    with Asia_Pacific:
        if 'Asia' in all_continents:
            st.subheader('Asia')
            entries = get_countries_from_region('Asia')
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

        with Oceania:
            if 'Oceania' in all_continents:
                st.subheader('Oceania')
                entries = get_countries_from_region('Oceania')
                data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                        'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
                data = data.sort_values(by = 'CountryID', ascending = True)
                st.dataframe(data, hide_index = True, width = 700 )

            else:
                st.info('This region is currently not accessible by you. Contact administrator for further info.')
        
main_dashboard()

