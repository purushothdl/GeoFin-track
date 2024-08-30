# All the sql queries for the country_limits table will be defined here

import sqlite3
import os


# Get the path to the current databasefile
script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, '..', 'databasefile.db')
db_path = os.path.abspath(db_path)


# Adds an entry to the country_details table in the databasefile and then commits it (permanent)
def add_entry(
        CountryID:int, RegionID:int, CountryName:str, GFILimit:float, GFIInstitue:float, TradeLimits:float, 
        TradeOS:float, TreasuryLimits:float, TreasuryOS:float, TotalLimit:float, TotalOSLimit:float):
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO CountryDetails(
            CountryID, RegionID, CountryName, GFILimit, GFIInstitue, TradeLimits, 
            TradeOS, TreasuryLimits, TreasuryOS, TotalLimit, TotalOSLimit)
            
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            CountryID, RegionID, CountryName, GFILimit, GFIInstitue, TradeLimits, 
            TradeOS, TreasuryLimits, TreasuryOS, TotalLimit, TotalOSLimit))
        conn.commit()
        conn.close()
    
    except Exception as e:
        print({f"Error occured' : {e}"})


# Retreives an entry based on its CountryID
def get_entry(CountryID:int):
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM CountryDetails
            WHERE CountryID = ? """, (CountryID,))
        entry = cursor.fetchone()
        conn.close()

        if entry:
            return entry
        else:
            return {'Error' : f"Country with ID {CountryID} doesn't exist"}

    except Exception as e:
        print({'Error occured' : f"{e}"})


# Updates the entry in the country_details table with its CountryID and commits it
def update_entry(
        CountryID:int, RegionID:int, CountryName:str, GFILimit:float, GFIInstitue:float, TradeLimits:float, 
        TradeOS:float, TreasuryLimits:float, TreasuryOS:float, TotalLimit:float, TotalOSLimit:float):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CountryDetails WHERE CountryID = ?", (CountryID,))
    entry = cursor.fetchone()
    
    if entry:
        
        try:
            cursor.execute("""
                UPDATE CountryDetails
                SET RegionID = ?, 
                    CountryName = ?, 
                    GFILimit = ?, 
                    GFIInstitue = ?, 
                    TradeLimits = ?, 
                    TradeOS = ?, 
                    TreasuryLimits = ?, 
                    TreasuryOS = ?, 
                    TotalLimit = ?, 
                    TotalOSLimit = ?
                WHERE CountryID = ?""",
                (RegionID, CountryName, GFILimit, GFIInstitue, TradeLimits, 
                TradeOS, TreasuryLimits, TreasuryOS, TotalLimit, TotalOSLimit, CountryID,))
            conn.commit()
            conn.close()
        
        except Exception as e:
            print({'Error occured' : f"{e}"})

    else:
        print({'Error' : f"Country with ID {CountryID} doesn't exist"})
            

# Removes an entry based on its CountryID and commits it
def delete_entry(CountryID:int):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CountryDetails WHERE CountryID = ?", (CountryID,))
    entry = cursor.fetchone()
    
    if entry:        
            
            try:
                cursor.execute("""
                    DELETE FROM CountryDetails
                    WHERE CountryID = ? """, (CountryID,))
                conn.commit()
                conn.close()

            except Exception as e:
                print({'Error occured' : f"{e}"})

    else:
        print({'Error' : f"Country with ID {CountryID} doesn't exist"})
    

# Returns all the entries present in the country_details table
def get_all():
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM CountryDetails""")
        data = cursor.fetchall()
        conn.close()
        for entry in data:
            print(entry)

    except Exception as e:
        print({'Error occured' : f"{e}"})

mapping = {'Asia-Pacific' : 1, 'Africa' : 2, 'North America' : 3, 'South America' : 4, 'Europe' : 5, 'Australia' : 6}

def get_countries_from_region(region:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM CountryDetails WHERE RegionID = ?""", (mapping[region],))
    data = cursor.fetchall()
    return data

# Gets the next available UserID (also does garbage collection)
def get_next_count_id():

    user_id = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    data = list(cursor.execute('select * from CountryDetails'))
    conn.commit()
    conn.close()
    if not data:
        return 1
    
    else:
        for line in data:
            user_id.append(line[0])
        
        for i in range(1, max(user_id)+1):
            if i not in user_id:
                return i
            else:
                set = True

        if set:
            return max(user_id) + 1