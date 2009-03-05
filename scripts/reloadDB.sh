#!/bin/bash

echo "drop database artcloud; create database artcloud; grant all on database artcloud to postgres;" | psql -U postgres

python manage.py syncdb --noinput

python manage.py syncdb --noinput
python manage.py loaddata front/fixtures/sites.json
python manage.py loaddata front/fixtures/auth.json
echo "delete from front_userprofile;" | psql -U postgres artcloud
python manage.py loaddata front/fixtures/front.json
python manage.py loaddata front/fixtures/wiki.json
echo "Done!"

