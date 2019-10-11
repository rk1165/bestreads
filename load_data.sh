#!/bin/bash

. db.config

db_url="${database}://${username}:${password}@${hostname}/${dbname}"
echo "DB URL = ${db_url}"

export DATABASE_URL=${db_url}

python3 create.py
python3 import.py