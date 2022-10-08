# Establish connection to MySQL database
import sqlite3

c2db = sqlite3.connect(
    'test_db'
)

# getting the cursor by cursor() method
c2Cursor =  c2db.cursor()

# creating database - remote version - not applicable in sprint1
# c2Cursor.execute("CREATE DATABASE C2Database")

# establish the entities w/ their characteristics 
# TODO: fix queries for sqlite3
# RESOLVED: fixed the queries, removed AUTO INCREMENT (refer to https://www.sqlite.org/autoinc.html)
implantRecords = """CREATE TABLE IF NOT EXISTS Implants (
                    [Implant_UUID] INTEGER PRIMARY KEY, 
                    [OS] TEXT,
                    [Arch.] TEXT,
                    [IPv4] TEXT,
                    [Hostname] TEXT,
                    [Username] TEXT, 
                    [PID] INTEGER, 
                    [ImplantUpTime] NUMERIC)""" #Numeric data type allows for access to the date and time functions(refer to https://www.sqlite.org/datatype3.html section 2.2, 3.1.1, 3.4)   

lootRecords = """ CREATE TABLE Loot (
                  [Loot_UUID] INT PRIMARY KEY,
                  [Loot_Type] TEXT,
                  [Implant_UUID] TEXT,
                  [CreatedAt] NUMERIC)"""           

#create tables in db
c2Cursor.execute(implantRecords)
c2Cursor.execute(lootRecords)

#close database
c2db.close()