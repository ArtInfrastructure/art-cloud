#!/bin/bash

sudo mysql -e "drop database artcloud; create database artcloud; grant all on artcloud.* to 'trevor'@'localhost';"
python manage.py syncdb --noinput
python manage.py loaddata front/fixtures/sites.json
python manage.py loaddata front/fixtures/auth.json
mysql artcloud -e "delete from front_userprofile;"
python manage.py loaddata front/fixtures/front.json
echo "Done!"

