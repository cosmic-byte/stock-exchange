#!/usr/bin/env bash

sleep 15

echo "Running migrations..."
python3 ./manage.py migrate

echo "Rebuilding elastic indexes..."
echo y | python3 ./manage.py search_index --rebuild

pytest ./portal/tests/
