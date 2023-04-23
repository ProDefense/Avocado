--CREATE TABLESPACE db
 --   OWNER CURRENT_USER
  --  LOCATION '/home/avocado/src/db/postgres/data';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE Implants 
(
    Implant_UUID UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    OS VARCHAR(64),
    Arch VARCHAR(64),
    IPv4 VARCHAR(64),
    Hostname VARCHAR(64),
    Username VARCHAR(64),
    PID INTEGER,
    ImplantUpTime TIMESTAMP WITH TIME ZONE
);

CREATE TABLE Operators 
(
    Operator_UUID UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    "User" VARCHAR(64),
    Passwrd VARCHAR(64)
);

CREATE TABLE Loot 
(
    Loot_UUID UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    Loot_Type VARCHAR(64),
    Implant_UUID UUID NOT NULL REFERENCES Implants(Implant_UUID),
    Operator_UUID UUID NOT NULL REFERENCES Operators(Operator_UUID),
    CreatedAt TIMESTAMP WITH TIME ZONE
);
