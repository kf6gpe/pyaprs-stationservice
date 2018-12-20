#!/bin/sh
chdir /home/kf6gpe/Projects/Python/pyaprs-stationservice
echo -n "stationservice starting..."
PYTHONPATH=. /usr/bin/twistd -n web --port tcp:8080 --wsgi stationservice.app > stationservice.log & 
echo "... started!"


