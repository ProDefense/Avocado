import psycopg2
import os
import subprocess
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.dialects.postgresql import UUID
import uuid

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
engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:password@localhost:5432/test_db')

# Declare database models
Base = sqlalchemy.orm.declarative_base()
class implantRecords(Base):
    __tablename__ = "Implants"

    Implant_UUID = sqlalchemy.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    OS = sqlalchemy.Column(sqlalchemy.String(64))
    Arch = sqlalchemy.Column(sqlalchemy.String(64))
    IPv4 = sqlalchemy.Column(sqlalchemy.String(64))
    Hostname = sqlalchemy.Column(sqlalchemy.String(64))
    Username = sqlalchemy.Column(sqlalchemy.String(64))
    PID = sqlalchemy.Column(sqlalchemy.Integer)
    ImplantUpTime = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())

class lootRecords(Base):
    __tablename__ = "Loot"

    Loot_UUID = sqlalchemy.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Loot_Type = sqlalchemy.Column(sqlalchemy.String(64))
    Implant_UUID = sqlalchemy.Column(UUID(as_uuid=True), sqlalchemy.ForeignKey("Implants.Implant_UUID"), nullable = False, default=uuid.uuid4)
    Operator_UUID = sqlalchemy.Column(UUID(as_uuid=True), sqlalchemy.ForeignKey("Operators.Operator_UUID"), nullable = False, default=uuid.uuid4)
    CreatedAt = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())

class operatorRecords(Base):
    __tablename__ = "Operators"

    Operator_UUID = sqlalchemy.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    User = sqlalchemy.Column(sqlalchemy.String(64))
    Password = sqlalchemy.Column(sqlalchemy.String(64))

# create tables
Base.metadata.create_all(engine)
print("Tables created")

# Close connection
conn.close()
