# All the sql queries for the users table will be defined here
import sqlite3
import os
import pandas as pd

# Get the path to the current databasefile
script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, '..', 'databasefile.db')
db_path = os.path.abspath(db_path)



# Adds an entry to the Users table in the databasefile and then commits it (permanent)
def add_entry(UserID:int, Name:str, Role:str, Email:str, Password:str, AccessedRegions:str):
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Users(UserID, Name, Role, Email, Password, AccessedRegions)
        VALUES(?, ?, ?, ?, ?, ?)""", (int(UserID), str(Name), str(Role), str(Email), str(Password), str(AccessedRegions)))
        conn.commit()
        conn.close()
        return None

    except Exception as e:
        return (f"Error : {e}")


        
# Retrieves an entry based on Email
def get_by_email(Email:str):
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM Users 
        WHERE Email = ?""", (Email,))
        entry = cursor.fetchone()
        conn.close()

        if entry:
            return entry
        
        else:
            return (f"Error : User with Email {Email} not found")
            
        
    except Exception as e:
        return {f"Error occured : {e}"}


# Updates an entry by its Email and then commits it
def update_by_mail(Name:str, Role:str, Email:str, Password:str, AccessedRegions:str):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Users WHERE Email = ?""",(Email,))
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
            WHERE Email = ?""", 
            (str(Name), str(Role), str(Email), str(Password), str(AccessedRegions), str(Email)))
            conn.commit()
            conn.close()

        except Exception as e:
            print({f"Error occured : {e}"})

    else:
        return (f"Error : User with Email {Email} not found")


# Deletes an entry based on its Email
def  delete_by_mail(Email:str):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Users WHERE Email = ?""",(Email,))
    entry = cursor.fetchone()
    
    if entry:
       
        try:
            cursor.execute("""
            DELETE FROM Users 
            WHERE Email = ?""", (Email,))
            conn.commit()
            conn.close()
            return None

        except Exception as e:
            return (f"Error occured : {e}")
    
    else:
        return (f"Error : User with Email {Email} not found")


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


# Gets the next available UserID (also does garbage collection)
def get_next_id():

    user_id = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    data = list(cursor.execute('select * from Users'))
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

