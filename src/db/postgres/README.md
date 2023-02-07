Install the following dependencies, in the Build prerequisites section, for using psycopg2: https://www.psycopg.org/docs/install.html#install-from-source
Install SQLAlchemy: https://docs.sqlalchemy.org/en/14/intro.html#installation

To create database, run "python3 make_db.py"

Change to postgres user and enter postgres shell by typing: sudo -u postgres psql
Here you can query the database interactively by following https://www.postgresql.org/docs/current/app-psql.html 
Change to postgres user and enter postgres shell by typing: sudo -u postgres psql
Here you can query the database interactively by following https://www.postgresql.org/docs/current/app-psql.html

For testing purposes, if you're running make_db.py multiple times, you will need to connect to the database using psql and type the following commands:
DROP DATABASE test_db;
DROP TABLESPACE db_tablespace;
Then you will be able to regenerate the database by running make_db.py.