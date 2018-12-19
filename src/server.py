#! /usr/bin/python3

import aprslib
import re
import yaml
import sys

def handlePacket(packet):
    m = re.match(stationsToMatch, packet['from'])
    if (m != None):
        print(packet)


# Read configuration
configFile = open("config.yaml")
config = yaml.load(configFile)

if not 'stations' in config or len(config['stations']) == 0:
    sys.exit("pyaprs-stationservice: must specify at least one callsign in configuration.");

if 'login' in config:
    login = config['login']
else:
    login = 'N0CALL'
if 'password' in config:
    password =  config['password']
else:
    password = ''

# Convert station list to regular expression and compile.
stationExpression = ''
for station in config['stations']:
    stationExpression = stationExpression + station + '|'
stationExpression = stationExpression[:-1]

stationsToMatch = re.compile(stationExpression, re.I)    

# Start the server to monitor the APRS feed.
AIS = aprslib.IS(login, passwd = password)
AIS.connect()
AIS.consumer(handlePacket)
