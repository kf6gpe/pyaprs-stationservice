#!/bin/sh
chdir /home/kf6gpe/Projects/Python/pyaprs-stationservice

PYTHONPATH=. /home/kf6gpe/.local/bin/twistd -n web --port tcp:8080 --wsgi stationservice.app > stationservice.log & 
