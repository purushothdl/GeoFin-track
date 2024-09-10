import streamlit as st
import time
import pandas as pd
import pydeck as pdk
from database.repositories.region_limits import get_entry, update_entry, get_all
from database.repositories.country_details import get_countries_from_region
import base64



st.set_page_config(page_title="Region Management", page_icon=":material/language:")
st.title('Region Management')


# Contains all the functions defined in this page

# Function to encode image as base64 (for sidebar)
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
    

# Scales the totallimitsUSD for marker size to represent regions
def min_max_scale(data, new_min=1, new_max=3):
    """
    Scales the input data to a specified range [new_min, new_max].

    Parameters:
    - data (list or array): Input data to be scaled.
    - new_min (int or float): The new minimum value for the scaled data (default is 1).
    - new_max (int or float): The new maximum value for the scaled data (default is 5).

    Returns:
    - list: Scaled data.
    """
    old_min = min(data)
    old_max = max(data)

    # Handle case where all values in data are the same
    if old_min == old_max:
        return [new_min] * len(data)

    # Apply min-max scaling formula
    scaled_data = [
        new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min)
        for value in data
    ]

    return scaled_data


# region icon and caption for sidebar using html and css
local_image_path = "images/admin/region.webp"  # Adjust this path as necessary
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
            Region Management
        </p>
    </div>
"""
st.sidebar.markdown(html_string_dboard, unsafe_allow_html=True)


# Streamlit start
st.write('View or Update regions.')
with st.container():
    col1, col2 = st.columns(2)

    # This column contains the view region resources
    with col1:
        st.header("**View Regions**")
        st.write("Displays all the different regions present in the database.")
        st.write('')
        with st.expander('**View all Regions**'):
            for continent in get_all():
                st.write('')
                st.info(continent[1])

    # This column contains the update region resources
    with col2:
    
        st.header("**Update Region**")
        st.write("Update existing Regions in the database by the region name.")
        st.write('')
        with st.expander('**Enter the Region Name**'):   
            options = ["Asia", "Africa", "North America", "South America", "Europe", "Oceania"] 
            region = st.selectbox('**RegionName**', options, key = 'region_up')

            if region != '':
                data = get_entry(region)

                if 'Error' not in data:
                    
                    with st.form('**Update Region information**', clear_on_submit = True, border = False):

                        st.markdown("<h3 style='text-align: center; margin-left: 18px; color: black; font-weight: bold;'>UPDATE REGION</h3>", unsafe_allow_html=True)
                        limits_usd = st.text_input('**TotalLimitsUSD**', data[2], key = 'limits_up')
                        outstanding_usd = st.text_input('**TotalOutstandingUSD**', data[3], key = 'outstading_up')
                        submit = st.form_submit_button('**Update**', use_container_width = True)

                        if submit:
                            entry = update_entry(region, limits_usd, outstanding_usd)
                            if entry == None:
                                msg = st.toast(f"Updating Region info...")
                                time.sleep(1)
                                msg.toast('Region data updated', icon = '✅')
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error(entry)

                else:
                        st.error(data)

st.write('')
st.write('')


# Financial details that are to be displayed when hovered
regions = ['Asia', 'Africa', 'Europe', 'North America', 'South America',  'Oceania']

total_limits = []
for region in regions:
     total_limits.append(get_entry(region)[2])

total_outstanding = []
for region in regions:
     total_outstanding.append(get_entry(region)[3])

limits_scaled = min_max_scale(total_limits, new_min=1, new_max=3)


# Displays PyDeck map to represent all the regions present
continents = {
    "Asia": [52.0479, 89, 500000*limits_scaled[0]],       
    "Africa": [11, 18, 500000*limits_scaled[1]],        
    "Europe": [51.5260, 10.2551, 500000*limits_scaled[2]],       
    "North America": [52.0902, -108.7129, 500000*limits_scaled[3]], 
    "South America": [-20.7832, -60.4915, 500000*limits_scaled[4]], 
    "Oceania": [-16.7350, 160.0194, 500000*limits_scaled[5]]      
}

total_limits = [round(int(val)/(10**9), 3)  for val in total_limits]
total_outstanding = [round(int(val)/(10**9), 3) for val in total_outstanding]

# Financial details about all regions
continent_info = {
    "Asia": {"TotalLimitsUSD": total_limits[0], "TotalOutstandingUSD": total_outstanding[0]},
    "Africa": {"TotalLimitsUSD": total_limits[1], "TotalOutstandingUSD": total_outstanding[1]},
    "Europe": {"TotalLimitsUSD": total_limits[2], "TotalOutstandingUSD": total_outstanding[2]},
    "North America": {"TotalLimitsUSD": total_limits[3], "TotalOutstandingUSD": total_outstanding[3]},
    "South America": {"TotalLimitsUSD": total_limits[4], "TotalOutstandingUSD": total_outstanding[4]},
    "Oceania": {"TotalLimitsUSD": total_limits[5], "TotalOutstandingUSD": total_outstanding[5]}
}

continent_data = [
    {"continent": name, "lat": coord[0], "lon": coord[1], "size": coord[2], **continent_info[name]}
    for name, coord in continents.items()
]

# Define the ScatterplotLayer
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=continent_data,
    get_position=["lon", "lat"],
    get_radius="size",
    get_fill_color=[200, 30, 0, 160],
    pickable=True,
    auto_highlight=True
)

# Define the TextLayer
text_layer = pdk.Layer(
    "TextLayer",
    data=continent_data,
    get_position=["lon", "lat"],
    get_text="continent",
    get_size=20,
    get_color=[255, 255, 255],
    get_angle=0,
    get_text_anchor="middle",
    get_alignment_baseline="center"
)

# Define the initial view state
view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=1,
    bearing=0,
    pitch=0
)

# Define the Deck
deck = pdk.Deck(
    layers=[scatter_layer, text_layer],
    initial_view_state=view_state,
    tooltip={
        "text": "{continent}\nTotalLimitsUSD: {TotalLimitsUSD} Billion \nTotalOutstandingUSD: {TotalOutstandingUSD} Billion"
    }
)

# Calling the map
st.title("Region info")
st.pydeck_chart(deck)
st.info("The above map covers all the regions and the size of the marker represents the relative TotalLimits of each region.", icon = "🔍")



# Display all the country financial details tab wise
st.write('')
st.write('')
[Asia, Africa, North_America, South_America, Europe, Oceania] = st.tabs(['Asia', 'Africa', 'North America', 'South America', 'Europe', 'Oceania'])


with Asia:
    st.subheader('Asia')
    entries = get_countries_from_region('Asia')
    
    if entries:
            data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                    'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
            data = data.sort_values(by = 'CountryID', ascending = True)
            st.dataframe(data, hide_index = True, width = 700)
    
    else:
        st.info('There are currently no countries in this region')

with Africa:
        st.subheader('Africa')
        entries = get_countries_from_region('Africa')
        
        if entries:
            data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                    'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
            data = data.sort_values(by = 'CountryID', ascending = True)
            st.dataframe(data, hide_index = True, width = 700)
        
        else:
             st.info('There are currently no countries in the region')

with North_America:
   
        st.subheader('North America')
        entries = get_countries_from_region('North America')
        
        if entries:
            data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                    'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
            data = data.sort_values(by = 'CountryID', ascending = True)
            st.dataframe(data, hide_index = True, width = 700)
        
        else:
            st.info('There are currently no countries in this region')

with South_America:
        st.subheader('South America')
        entries = get_countries_from_region('South America')
        
        if entries:
            data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                    'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
            data = data.sort_values(by = 'CountryID', ascending = True)
            st.dataframe(data, hide_index = True, width = 700)
        
        else:
            st.info('There are currently no countries in this region')

with Europe:
        st.subheader('Europe')
        entries = get_countries_from_region('Europe')
        
        if entries:
            data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                    'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
            data = data.sort_values(by = 'CountryID', ascending = True)
            st.dataframe(data, hide_index = True, width = 700)
        
        else:
            st.info('There are currently no countries in this region')


with Oceania:
        st.subheader('Oceania')
        entries = get_countries_from_region('Oceania')
        
        if entries:
            data = pd.DataFrame(entries, columns = ['CountryID', 'RegionID', 'CountryName', 'GFILimit', 'GFIInstitue', 'TradeLimits', 
                    'TradeOS', 'TreasuryLimits', 'TreasuryOS', 'TotalLimit', 'TotalOSLimit'] )
            data = data.sort_values(by = 'CountryID', ascending = True)
            st.dataframe(data, hide_index = True, width = 700)
        
        else:
            st.info('There are currently no countries in this region')

st.info(' To add new countries or remove them from a region head over to country management.', icon = "📝")


# Displays the region financial details in the dataframe
st.write('')
st.header('**Region Limits**')
entries = get_all()
data = pd.DataFrame(entries, columns = ['RegionID', 'RegionName', 'TotalLimitsUSD', 'TotalOutstandingUSD'] )
data = data.sort_values(by = 'RegionID', ascending = True)
st.dataframe(data, hide_index = True, width = 700)