import psycopg2
import os
import subprocess

# Establish connection
conn = psycopg2.connect(
    database = "postgres", user='postgres', password='password', host='127.0.0.1', port='5432'
)
conn.autocommit = True

# Create cursor object using cursor() method
cursor = conn.cursor()

# Create tablespace folder with correct ownership 

# mkdir ./data
# chown postgres:postgres ./data
# Query to create that tablespace in server
tablespace_path = os.getcwd() + "/data"
os.mkdir(tablespace_path)
os.chown(tablespace_path, uid = 10, gid = -1) # change ownership of "./data" to postgres user (uid = 10)
print("created tablespace path at: {tablespace_path}")

cursor.execute('''CREATE TABLESPACE db_tablespace
                  OWNER postgres
                  LOCATION %s''',
            (tablespace_path))

# Query to create database
query = '''CREATE DATABASE test_db
           TABLESPACE db_tablespace''';
cursor.execute(query)

# Query to initialize tables


# Close connection
conn.close()
