import streamlit as st
import time
import pandas as pd
from database.repositories.region_limits import get_entry, update_entry, get_all
from database.repositories.country_details import get_countries_from_region

st.set_page_config(page_title="Region Management", page_icon=":material/language:")
st.sidebar.header("Region Management")
st.title('Region Management')
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
                st.info(continent, icon = "◾")

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

st.info('To add new countries or remove them from a region head over to country management.')

st.write('')
st.header('**Region Limits**')
entries = get_all()
data = pd.DataFrame(entries, columns = ['RegionID', 'RegionName', 'TotalLimitsUSD', 'TotalOutstandingUSD'] )
data = data.sort_values(by = 'RegionID', ascending = True)
st.dataframe(data, hide_index = True, width = 700)