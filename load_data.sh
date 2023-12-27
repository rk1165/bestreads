#!/bin/bash

rm -rf instance/

# Loads the data in instance/books.db

db_url="sqlite:///books.db"
echo "DB URL = ${db_url}"

export DATABASE_URL=${db_url}

python3 create.py
python3 import.py