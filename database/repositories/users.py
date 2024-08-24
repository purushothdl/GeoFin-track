# All the sql queries for the users table will be defined here
import sqlite3
import os
import pandas as pd

# Get the path to the current databasefile
script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, '..', 'databasefile.db')
db_path = os.path.abspath(db_path)

# Establish a connection to the databasefile


# Adds an entry to the Users table in the databasefile and then commits it (permanent)
def add_entry(UserID:int, Name:str, Role:str, Email:str, Password:str, AccessedRegions:str):
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Users(UserID, Name, Role, Email, Password, AccessedRegions)
        VALUES(?, ?, ?, ?, ?, ?)""", (UserID, Name, Role, Email, Password, AccessedRegions))
        conn.commit()
        conn.close()
        return None

    except Exception as e:
        return (f"Error : {e}")


# Retreives an entry based on its ID
def  get_entry(UserID:int):
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM Users 
        WHERE UserID = ?""", (UserID,))
        entry = cursor.fetchone()
        conn.close()

        if entry:
            return entry
        
        else:
            return (f"Error : User with ID {UserID} not found")
            
        
    except Exception as e:
        return {f"Error occured : {e}"}
        


# Updates an entry by its RegionID and then commits it
def update_entry(UserID:int, Name:str, Role:str, Email:str, Password:str, AccessedRegions:str):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Users WHERE UserID = ?""",(UserID,))
    entry = cursor.fetchone()

    if entry:
        
        try:
            cursor.execute("""
            UPDATE Users
            SET Name = ?,
                Role = ?, 
                Email = ?, 
                Password = ?, 
                AccessedRegions = ?
            WHERE UserID = ?""", 
            (Name, Role, Email, Password, AccessedRegions, UserID))
            conn.commit()
            conn.close()

        except Exception as e:
            print({f"Error occured : {e}"})

    else:
        return (f"Error : User with ID {UserID} not found")
  

# Deletes an entry based on its ID
def  delete_entry(UserID:int):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Users WHERE UserID = ?""",(UserID,))
    entry = cursor.fetchone()
    
    if entry:
       
        try:
            cursor.execute("""
            DELETE FROM Users 
            WHERE UserID = ?""", (UserID,))
            conn.commit()
            conn.close()
            return None

        except Exception as e:
            return (f"Error occured : {e}")
    
    else:
        return (f"Error : User with ID {UserID} not found")


# Prints all the entries present in the Users table
def get_all():
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM Users""")
        data = cursor.fetchall()
        return data
    
    except Exception as e :
        return (f"Error occured' : {e}")



data = pd.DataFrame(get_entry(5)).values.reshape(1, -1)
data = pd.DataFrame(data, columns = ['id', 'name', 'role', 'email', 'password', 'region'])

print(data)
