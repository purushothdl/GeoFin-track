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
#     (1, 'Asia-Pacific', 1000000000.00, 250000000.00),
#     (2, 'Africa', 500000000.00, 120000000.00),
#     (3, 'North America', 2000000000.00, 450000000.00),
#     (4, 'South America', 700000000.00, 180000000.00),
#     (5, 'Europe', 1500000000.00, 350000000.00),
#     (6, 'Australia', 800000000.00, 200000000.00);""")
# conn.commit()

# cursor.execute("SELECT * FROM RegionLimits")
data = cursor.fetchall()
for line in data:
    print(line)


## sample data entered in the country_details table

# sql = """
# INSERT INTO CountryDetails (
#     CountryID, RegionID, CountryName, GFILimit, GFIInstitue, TradeLimits, 
#     TradeOS, TreasuryLimits, TreasuryOS, TotalLimit, TotalOSLimit) VALUES

#     (1, 1, 'China', 500000000.00, 100000000.00, 200000000.00, 50000000.00, 150000000.00, 30000000.00, 850000000.00, 200000000.00),
#     (2, 1, 'Japan', 300000000.00, 60000000.00, 150000000.00, 40000000.00, 120000000.00, 25000000.00, 620000000.00, 150000000.00),
#     (3, 1, 'India', 200000000.00, 40000000.00, 100000000.00, 25000000.00, 80000000.00, 15000000.00, 380000000.00, 100000000.00),
#     (4, 1, 'Singapore', 200000000.00, 40000000.00, 100000000.00, 25000000.00, 80000000.00, 15000000.00, 320000000.00, 70000000.00),
#     (5, 1, 'South Korea', 120000000.00, 24000000.00, 60000000.00, 15000000.00, 50000000.00, 10000000.00, 230000000.00, 55000000.00),

 
#     (6, 2, 'Nigeria', 80000000.00, 16000000.00, 50000000.00, 12000000.00, 40000000.00, 8000000.00, 140000000.00, 30000000.00),
#     (7, 2, 'South Africa', 60000000.00, 12000000.00, 40000000.00, 10000000.00, 35000000.00, 7000000.00, 115000000.00, 27000000.00),
#     (8, 2, 'Kenya', 50000000.00, 10000000.00, 30000000.00, 8000000.00, 25000000.00, 5000000.00, 85000000.00, 20000000.00),
#     (9, 2, 'Egypt', 70000000.00, 14000000.00, 45000000.00, 11000000.00, 30000000.00, 6000000.00, 115000000.00, 25000000.00),
#     (10, 2, 'Morocco', 40000000.00, 8000000.00, 25000000.00, 6000000.00, 20000000.00, 4000000.00, 65000000.00, 14000000.00),

   
#     (11, 3, 'United States', 1000000000.00, 200000000.00, 600000000.00, 150000000.00, 500000000.00, 100000000.00, 2200000000.00, 450000000.00),
#     (12, 3, 'Canada', 300000000.00, 60000000.00, 150000000.00, 40000000.00, 120000000.00, 25000000.00, 620000000.00, 150000000.00),
#     (13, 3, 'Mexico', 200000000.00, 40000000.00, 100000000.00, 25000000.00, 80000000.00, 15000000.00, 380000000.00, 100000000.00),
#     (14, 3, 'Guatemala', 50000000.00, 10000000.00, 20000000.00, 5000000.00, 15000000.00, 3000000.00, 35000000.00, 8000000.00),
#     (15, 3, 'Colombia', 40000000.00, 8000000.00, 15000000.00, 3000000.00, 12000000.00, 2500000.00, 27000000.00, 5500000.00),

#     (16, 4, 'Brazil', 70000000.00, 14000000.00, 35000000.00, 8000000.00, 25000000.00, 5000000.00, 80000000.00, 19000000.00),
#     (17, 4, 'Argentina', 60000000.00, 12000000.00, 40000000.00, 10000000.00, 30000000.00, 6000000.00, 100000000.00, 18000000.00),
#     (18, 4, 'Chile', 50000000.00, 10000000.00, 30000000.00, 7000000.00, 20000000.00, 4000000.00, 80000000.00, 17000000.00),
#     (19, 4, 'Peru', 40000000.00, 8000000.00, 25000000.00, 6000000.00, 15000000.00, 3000000.00, 65000000.00, 13000000.00),
#     (20, 4, 'Venezuela', 30000000.00, 6000000.00, 20000000.00, 5000000.00, 10000000.00, 2000000.00, 50000000.00, 11000000.00),

#     (21, 5, 'Germany', 900000000.00, 180000000.00, 500000000.00, 120000000.00, 400000000.00, 80000000.00, 1700000000.00, 260000000.00),
#     (22, 5, 'France', 800000000.00, 160000000.00, 450000000.00, 110000000.00, 350000000.00, 70000000.00, 1200000000.00, 230000000.00),
#     (23, 5, 'United Kingdom', 700000000.00, 140000000.00, 400000000.00, 100000000.00, 300000000.00, 60000000.00, 1000000000.00, 200000000.00),
#     (24, 5, 'Italy', 600000000.00, 120000000.00, 350000000.00, 90000000.00, 250000000.00, 50000000.00, 900000000.00, 170000000.00),
#     (25, 5, 'Spain', 500000000.00, 100000000.00, 300000000.00, 80000000.00, 200000000.00, 40000000.00, 800000000.00, 140000000.00),

#     (26, 6, 'Australia', 150000000.00, 30000000.00, 70000000.00, 20000000.00, 60000000.00, 12000000.00, 290000000.00, 70000000.00);"""

# cursor.execute(sql)
# conn.commit()

cursor.execute("SELECT * FROM CountryDetails")
data = cursor.fetchall()
for line in data:
    print(line)


## sample data entered in the Users table

# cursor.execute("""
# INSERT INTO Users(UserID, Name, Role, Email, Password, AccessedRegions) VALUES
#     (1, 'Alice', 'user', 'alice.smith@example.com', 'alicepass123', '["North America", "Europe"]'),
#     (2, 'Bob', 'admin', 'bob.jones@example.com', 'bobpass456', '["North America", "Australia"]'),
#     (3, 'Charlie', 'user', 'charlie.brown@example.com', 'charliepass789', '["Europe", "Asia-Pacific"]'),
#     (4, 'Diana', 'user', 'diana.prince@example.com', 'dianapass101', '["Australia", "Asia-Pacific"]'),
#     (5, 'Ethan', 'user', 'ethan.hunt@example.com', 'ethanpass202', '["Europe", "Africa"]'),
#     (6, 'Fiona', 'user', 'fiona.glenanne@example.com', 'fionapass303', '["Europe", "North America"]'),
#     (7, 'George', 'user', 'george.smith@example.com', 'georgepass404', '["Asia-Pacific", "North America"]'),
#     (8, 'Hannah', 'user', 'hannah.montana@example.com', 'hannahpass505', '["Europe", "Australia"]'),
#     (9, 'Isaac', 'admin', 'isaac.newton@example.com', 'isaacpass606', '["North America", "Africa", "Australia"]'),
#     (10, 'Jasmine', 'user', 'jasmine.lee@example.com', 'jasminepass707', '["Asia-Pacific", "Europe"]'),
#     (11, 'Liam', 'admin', 'liam.connor@example.com', 'liampass808', '["North America", "Africa"]'),
#     (12, 'Mia', 'user', 'mia.williams@example.com', 'miapass909', '["South America", "Asia-Pacific"]'),
#     (13, 'Noah', 'user', 'noah.johnson@example.com', 'noahpass1010', '["North America", "South America"]'),
#     (14, 'Olivia', 'user', 'olivia.martin@example.com', 'oliviapass1111', '["Europe", "Asia-Pacific"]'),
#     (15, 'Parker', 'admin', 'parker.james@example.com', 'parkerpass1212', '["Europe", "North America"]'),
#     (16, 'Quinn', 'user', 'quinn.rodriguez@example.com', 'quinnpass1313', '["Australia", "South America"]'),
#     (17, 'Ryan', 'user', 'ryan.smith@example.com', 'ryanpass1414', '["Asia-Pacific", "Africa"]'),
#     (18, 'Sophia', 'user', 'sophia.garcia@example.com', 'sophiapass1515', '["North America", "Asia-Pacific"]'),
#     (19, 'Tyler', 'user', 'tyler.brown@example.com', 'tylerpass1616', '["South America", "Europe"]'),
#     (20, 'Uma', 'admin', 'uma.kumar@example.com', 'umapass1717', '["Australia", "Africa", "Europe"]');""")
# conn.commit()


cursor.execute("SELECT * FROM Users")
data = cursor.fetchall()
for line in data:
    print(line)


