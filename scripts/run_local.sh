#!/usr/bin/env bash

# Script to run the Django server in a development environment

python3 manage.py migrate
sleep 15
echo y | python3 manage.py search_index --rebuild
python3 manage.py runserver 0.0.0.0:8001