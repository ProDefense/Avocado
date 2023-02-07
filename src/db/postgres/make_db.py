import psycopg2
import os
import subprocess
#import sqlalchemy
#import sqlalchemy.orm
import uuid
import datetime
#FIRST CHANGE - Added new imports from docs.sqlalchemy.org
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import cast, select, String, TIMESTAMP
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


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
tablespace_path = os.getcwd() + '/data'
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

# Declare database models
#SECOND CHANGE - RJ: Establishing a declarative base with class Base
class Base(DeclarativeBase):
    pass
Base.metadata

#THIRD CHANGE - RJ: Declaring mapped classes with the appropriate ORM format.
class implantRecords(Base):
    __tablename__ = "Implants"
    Implant_UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    OS: Mapped[str] = mapped_column(String(64))
    Arch: Mapped[str] =  mapped_column(String(64))
    Arch: Mapped[str] =  mapped_column(String(64))
    IPv4: Mapped[str] = mapped_column(String(64))
    Hostname: Mapped[str] = mapped_column(String(64))
    Username: Mapped[str] = mapped_column(String(64))
    PID: Mapped[int] = mapped_column
    ImplantUpTime: Mapped[datetime.datetime] = TIMESTAMP(timezone = True)
class lootRecords(Base):
    __tablename__ = "Loot"
    Loot_UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Loot_Type: Mapped[str] = mapped_column(String(64))
    Implant_UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("Implants.Implant_UUID"), nullable = False, default=uuid.uuid4)
    Operator_UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("Operators.Operator_UUID"), nullable = False, default=uuid.uuid4)
    CreatedAt: Mapped[datetime.datetime] = TIMESTAMP(timezone = True)

class operatorRecords(Base):
    __tablename__ = "Operators"

    Operator_UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    User: Mapped[str] = mapped_column(String(64))
    Password: Mapped[str] = mapped_column(String(64))

# create tables
Base.metadata.create_all(engine)
print("Tables created")

# Close connection
conn.close()
