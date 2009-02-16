#!/bin/bash

python manage.py dumpdata sites > front/fixtures/sites.json
python manage.py dumpdata auth > front/fixtures/auth.json
python manage.py dumpdata front > front/fixtures/front.json
