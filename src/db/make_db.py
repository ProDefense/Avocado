import psycopg2
import os
import subprocess
from sqlalchemy import create_engine
from typing import List
from typing import Optional
from schema import Base


#allow for user input if they have postgres setup on their personal device
username = input("Please enter your postgres username, if no user associated please enter 'postgres' for username: ")
print(username)
user_password = input("Please enter your postgres password, if no user associated please enter 'password' for password: ")

# Establish connection
conn = psycopg2.connect(
    database = "postgres", user=username, password=user_password, host='127.0.0.1', port='5432'
)
conn.autocommit = True
cursor = conn.cursor()

# Run make_directories.sh to create tablespace folder with correct ownership
os.chmod('./make_directories.sh', 0o755)
proces = subprocess.call("./make_directories.sh")

# Create tablespace in server
tablespace_path = os.getcwd() + '/postgres/data'
SQL = '''CREATE TABLESPACE db_tablespace
         OWNER postgres
         LOCATION %s'''
data = (tablespace_path, )
try:
    cursor.execute(SQL, data)
except Exception as error:
    print ("An exception occured: ", error)


# Create database
try: 
    cursor.execute('''CREATE DATABASE test_db
                  TABLESPACE db_tablespace''')
except Exception as error:
    print ("An exception occured: ", error)


# Connect to SQLAlchemy engine
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/test_db')

# create tables
Base.metadata.create_all(engine)
print("Tables created")

# Close connection
conn.close()
