# All the sql queries for the region_limits table will be defined here

# Add the sql queries for the region_limits table here
def create_region_limits_table(cursor):
    RegionLimits = """
    CREATE TABLE IF NOT EXISTS RegionLimits(
        RegionID INT PRIMARY KEY, 
        RegionName VARCHAR, 
        TotalLimitsUSD DECIMAL, 
        TotalOutstandingUSD DECIMAL)
    """
    cursor.execute(RegionLimits)

    cursor.execute("""
    INSERT INTO RegionLimits(RegionID, RegionName, TotalLimitsUSD, TotalOutstandingUSD) VALUES
        (1, 'North America', 1000000.00, 250000.00),
        (2, 'Europe', 750000.00, 300000.00),
        (3, 'Asia-Pacific', 1200000.00, 450000.00),
        (4, 'South America', 500000.00, 150000.00),
        (5, 'Middle East', 600000.00, 200000.00),
        (6, 'Africa', 400000.00, 100000.00),
        (7, 'Australia', 300000.00, 75000.00),
        (8, 'China', 900000.00, 350000.00),
        (9, 'India', 650000.00, 280000.00),
        (10, 'Russia', 700000.00, 320000.00);""")
    return cursor

# create few more files for fuctnions of diffrent tables
# should consist of CRUD operations
# create, read, update, delete