import sqlite3

conn= sqlite3.connect('database/databasefile.db')
cursor = conn.cursor()

RegionLimits = """
CREATE TABLE IF NOT EXISTS RegionLimits( 
    RegionID INT PRIMARY KEY, 
    RegionName VARCHAR, 
    TotalLimitsUSD DECIMAL, 
    TotalOutstandingUSD DECIMAL)
"""

CountryDetails = """ 
CREATE TABLE IF NOT EXISTS CountryDetails(
    CountryID INT PRIMARY KEY, 
    RegionID INT, 
    CountryName VARCHAR, 
    GFILimit DECIMAL, 
    GFIInstitue DECIMAL,
    TradeLimits DECIMAL, 
    TradeOS DECIMAL, 
    TreasuryLimits DECIMAL,
    TreasuryOS DECIMAL, 
    TotalLimit DECIMAL, 
    TotalOSLimit DECIMAL,
    FOREIGN KEY(RegionID) REFERENCES RegionLimits(RegionID))
"""

Users = """
CREATE TABLE IF NOT EXISTS Users( 
    UserID INT PRIMARY KEY, 
    Name TEXT,
    Role TEXT, 
    Email VARCHAR UNIQUE,
    Password  VARCHAR, 
    AccessedRegions VARCHAR)
"""

# Creates table format
cursor.execute(RegionLimits)
cursor.execute(CountryDetails)
cursor.execute(Users)


## sample data entered in the region_limits table

# cursor.execute("""
# INSERT INTO RegionLimits(RegionID, RegionName, TotalLimitsUSD, TotalOutstandingUSD) VALUES
#     (1, 'North America', 1000000.00, 250000.00),
#     (2, 'Europe', 750000.00, 300000.00),
#     (3, 'Asia-Pacific', 1200000.00, 450000.00),
#     (4, 'South America', 500000.00, 150000.00),
#     (5, 'Middle East', 600000.00, 200000.00),
#     (6, 'Africa', 400000.00, 100000.00),
#     (7, 'Australia', 300000.00, 75000.00),
#     (8, 'China', 900000.00, 350000.00),
#     (9, 'India', 650000.00, 280000.00),
#     (10, 'Russia', 700000.00, 320000.00);""")
# conn.commit()

cursor.execute("SELECT * FROM RegionLimits")
data = cursor.fetchall()
for line in data:
    print(line)


## sample data entered in the country_details table

# sql = """
# INSERT INTO CountryDetails (
#     CountryID, RegionID, CountryName, GFILimit, GFIInstitue, TradeLimits, 
#     TradeOS, TreasuryLimits, TreasuryOS, TotalLimit, TotalOSLimit
# ) VALUES
#     (1, 1, 'United States', 500000.00, 100000.00, 300000.00, 80000.00, 100000.00, 50000.00, 900000.00, 180000.00),
#     (2, 1, 'Canada', 400000.00, 80000.00, 200000.00, 60000.00, 70000.00, 30000.00, 670000.00, 120000.00),
#     (3, 2, 'Germany', 450000.00, 90000.00, 250000.00, 50000.00, 80000.00, 40000.00, 780000.00, 130000.00),
#     (4, 2, 'France', 350000.00, 70000.00, 220000.00, 55000.00, 60000.00, 20000.00, 630000.00, 105000.00),
#     (5, 3, 'China', 600000.00, 120000.00, 350000.00, 100000.00, 90000.00, 30000.00, 1040000.00, 150000.00),
#     (6, 3, 'Japan', 500000.00, 100000.00, 280000.00, 70000.00, 70000.00, 20000.00, 850000.00, 120000.00),
#     (7, 4, 'Brazil', 350000.00, 70000.00, 180000.00, 50000.00, 50000.00, 15000.00, 580000.00, 115000.00),
#     (8, 4, 'Argentina', 250000.00, 50000.00, 150000.00, 40000.00, 40000.00, 10000.00, 440000.00, 80000.00),
#     (9, 5, 'Saudi Arabia', 300000.00, 60000.00, 180000.00, 50000.00, 40000.00, 20000.00, 520000.00, 80000.00),
#     (10, 5, 'United Arab Emirates', 250000.00, 50000.00, 140000.00, 30000.00, 30000.00, 10000.00, 420000.00, 60000.00);
# """

# cursor.execute(sql)
# conn.commit()

cursor.execute("SELECT * FROM CountryDetails")
data = cursor.fetchall()
for line in data:
    print(line)


## sample data entered in the Users table

# cursor.execute("""
# INSERT INTO Users(UserID, Name, Role, Email, Password, AccessedRegions) VALUES
#   (1, 'Alice', 'user', 'alice.smith@example.com', 'alicepass123', 'New York, USA'),
#   (2, 'Bob', 'admin', 'bob.jones@example.com', 'bobpass456', 'Toronto, Canada'),
#   (3, 'Charlie', 'user', 'charlie.brown@example.com', 'charliepass789', 'London, UK'),
#   (4, 'Diana', 'user', 'diana.prince@example.com', 'dianapass101', 'Sydney, Australia'),
#   (5, 'Ethan', 'user', 'ethan.hunt@example.com', 'ethanpass202', 'Berlin, Germany'),
#   (6, 'Fiona', 'user', 'fiona.glenanne@example.com', 'fionapass303', 'Dublin, Ireland'),
#   (7, 'George', 'user', 'george.smith@example.com', 'georgepass404', 'Paris, France'),
#   (8, 'Hannah', 'user', 'hannah.montana@example.com', 'hannahpass505', 'Rome, Italy'),
#   (9, 'Isaac', 'admin', 'isaac.newton@example.com', 'isaacpass606', 'Madrid, Spain'),
#   (10, 'Jack', 'admin', 'jack.doe@example.com', 'jackpass707', 'Riyadh, Saudi Arabia');""")
# conn.commit()


cursor.execute("SELECT * FROM Users")
data = cursor.fetchall()
for line in data:
    print(line)