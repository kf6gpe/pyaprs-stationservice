#! /usr/bin/python3

import aprslib
import json
import logging
import re
import sys
from threading import Thread
import time
import yaml

from flask import Flask
from flask_restful import Api, Resource, reqparse

class Station(Resource):
    def get(self, callsign):
        if callsign in _stationList:
            return _stationList[callsign], 200
        else:
            return 'callsign not cached', 404
        
    def post(self, name):
        return 'operation not supported', 403
        
    def put(self, name):
        return 'operation not supported', 403
    
    def delete(self, name):
        return 'operation not supported', 403
        
_stationList = {}

def handlePacket(packet):
    m = re.match(stationsToMatch, packet['from'])
    if (m != None):
        packet['timestamp'] = time.time()
        packet['result'] = 'OK'
        if packet['from'] in _stationList:
            _stationList[packet['from']].update(packet)
        else:
            _stationList[packet['from']] = packet
        print(packet['from'])

def runAprsMonitor():
    while True:
        try:
            AIS = aprslib.IS(login, passwd = password)
            print('- Connecting to APRS-IS...')
            AIS.connect()
            print('- Connected! Handling incoming packets.')
            AIS.consumer(handlePacket)
        except:
            print('- APRS server socket failure... reconnecting in 3 seconds')
            time.sleep(3)
            
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

# logging.basicConfig(level=logging.DEBUG)

# Start the server to monitor the APRS feed.
serverMonitorThread = Thread(target=runAprsMonitor)
serverMonitorThread.start()

# Start the REST server
app = Flask(__name__)
api = Api(app)
api.add_resource(Station, '/callsign/<string:callsign>')
app.run(host='10.0.1.126',port=8080,debug=True)

print('*** TERMINATING!')
