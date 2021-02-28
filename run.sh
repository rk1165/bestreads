#!/bin/bash

echo "Please enter the following details"

echo -n "Database : "
read -r database
echo -n "Username : "
read -r username
echo -n "Password : "
read -r -s password
echo
echo -n "Hostname : "
read -r hostname
echo -n "DB name  : "
read -r dbname

db_url="${database}://${username}:${password}@${hostname}/${dbname}"
echo "${db_url}"


python3 create.py
python3 import.py

export FLASK_APP=application.py
export DATABASE_URI=${db_url}

flask run