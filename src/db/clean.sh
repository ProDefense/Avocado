#!/bin/sh
# Before starting please create a role in the database with your corresponding linux username.
# Steps:
# 1) sudo -su postgres -H -- psql -c "CREATE ROLE <username> SUPERUSER LOGIN PASSWORD '<password>'" //this will create your role with admin like priv.

echo "start"
sudo -su postgres pg_dump --dbname=test_db > test.txt
sudo -u postgres -H -- psql -c 'DROP DATABASE test_db;' -c 'DROP tablespace db_tablespace;'
echo "Exported and cleaned."