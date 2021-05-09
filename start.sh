#!/bin/sh
# chdir /home/kf6gpe/Projects/Code/pyaprs-stationservice
chdir /home/kf6gpe/pyaprs-stationservice
echo -n "stationservice starting..."
PYTHONPATH=. /usr/bin/twist3 web --port tcp:8080 --wsgi stationservice.app > stationservice.log &

echo "... started!"


