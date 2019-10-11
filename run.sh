#!/bin/bash

. db.config

db_url="${database}://${username}:${password}@${hostname}/${dbname}"
export DATABASE_URL=${db_url}

export FLASK_APP=application.py

flask run