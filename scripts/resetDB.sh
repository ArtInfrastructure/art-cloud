#!/bin/bash

sudo mysql -e "drop database artcloud; create database artcloud; grant all on artcloud.* to 'trevor'@'localhost';"
echo "Done!"

