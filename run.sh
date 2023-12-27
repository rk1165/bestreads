#!/bin/bash

db_url="sqlite:///books.db"
export DATABASE_URL=${db_url}

export FLASK_APP=application.py

python3 -m flask run