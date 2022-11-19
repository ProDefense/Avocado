####################################################################################################################
# Description: make_db.py uses sqlite3 to connect to a local, in-memory database file "test_db".
#              The tables implantRecords and lootRecords are created if they don't
#              already exist in memory.
#
#     Authors: Jacqueline and RJ
#        Date: 10/8/22
####################################################################################################################

import sqlite3

# Establish connection to sqlite3 and create a local, in-memory database
# in the current working directory called "test_db"
c2db = sqlite3.connect(
    'test_db'
)

c2Cursor =  c2db.cursor()

# If the tables do not exist, create the tables w/ their columns 
# NOTE: removed AUTO INCREMENT (refer to https://www.sqlite.org/autoinc.html)
implantRecords = """CREATE TABLE IF NOT EXISTS Implants (
                    [Implant_UUID] STRING PRIMARY KEY, 
                    [OS] TEXT,
                    [Arch.] TEXT,
                    [IPv4] TEXT,
                    [Hostname] TEXT,
                    [Username] TEXT, 
                    [PID] INTEGER, 
                    [ImplantUpTime] NUMERIC)""" # Numeric data type allows for access to the date and time functions
                                                # (refer to https://www.sqlite.org/datatype3.html 
                                                # section 2.2, 3.1.1, 3.4)   

lootRecords = """ CREATE TABLE IF NOT EXISTS Loot (
                  [Loot_UUID] STRING PRIMARY KEY,
                  [Loot_Type] TEXT,
                  [Implant_UUID] TEXT,
                  [CreatedAt] NUMERIC)""" 

operatorRecords = """ CREATE TABLE Operators (
                  [User] STRING PRIMARY KEY,
                  [Password] STRING,
                  [Public_Key] STRING)"""       # not decided if we are going with password or public key based       

# create tables in db
c2Cursor.execute(implantRecords)
c2Cursor.execute(lootRecords)
c2Cursor.execute(operatorRecords)

# close database
c2db.close()
