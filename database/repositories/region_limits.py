# All the sql queries for the region_limits table will be defined here
import sqlite3
import os


# Get the path to the current databasefile
script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, '..', 'databasefile.db')
db_path = os.path.abspath(db_path)



# Adds an entry to the region_limits table in the databasefile and then commits it (permanent)
def add_entry(RegionID:int,RegionName:str, TotalLimitsUSD:float, TotalOutstandingUSD:float ):
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO RegionLimits(RegionID, RegionName, TotalLimitsUSD, TotalOutstandingUSD)
            VALUES(?, ?, ?, ?)""", (int(RegionID), RegionName, float(TotalLimitsUSD), float(TotalOutstandingUSD)))
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error occured : {e}")
        return None


# Retreives an entry based on its ID
def get_entry(RegionName:str):

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM RegionLimits
            WHERE RegionName = ? """, (RegionName,))
        entry = cursor.fetchone()
        conn.close()

        if entry:
            return entry
        
        else:
            print({'Error' : f"Region with Name {RegionName} doesn't exist"})
            return None

    except Exception as e:
        print(f"Error occured : {e}")
        return None
    
    

# Updates an entry by its RegionID and then commits it
def update_entry(RegionName:str, TotalLimitsUSD:float, TotalOutstandingUSD:float):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM RegionLimits WHERE RegionName = ?""",(RegionName,))
    entry = cursor.fetchone()
    
    if entry:
           
            try:
                cursor.execute("""
                    UPDATE RegionLimits 
                    SET TotalLimitsUSD = ?,
                        TotalOutstandingUSD = ?
                    WHERE RegionName = ?""", 
                    (float(TotalLimitsUSD), float(TotalOutstandingUSD), RegionName))
                conn.commit()
                conn.close()
                return None

            except Exception as e:
                return (f"Error occured : {e}")           

    else:
        return (f"Error : Region with RegionName {RegionName} doesn't exist")
    

# Deletes an entry from the databasefile and then commits it 
def delete_entry(RegionID:int):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM RegionLimits WHERE RegionID = ?""",(RegionID,))
    entry = cursor.fetchone()
    
    if entry:
            
            try:
                cursor.execute("""
                    DELETE FROM RegionLimits WHERE RegionID = ? """, (RegionID,))
                conn.commit()
                conn.close()

            except Exception as e:
                print(f"Error occured : {e}")
                return None
    else:
        print({'Error' : f"RegionID with ID {RegionID} doesn't exist"})
        return None


# Prints all the entries present in the RegionLimits table
def get_all():
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM RegionLimits """)
        data = cursor.fetchall()
        conn.close()
        # data = [region[1] for region in data]
        return data
    except Exception as e:
        return (f"Error occured : {e}")
    
