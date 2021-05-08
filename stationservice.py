#! /usr/bin/python

import aprslib
import json
import logging
import re
import sys
from threading import Thread
import time
import yaml

from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

_stationList = {}
class Station(Resource):
    def get(self, callsign):
        global _stationList
        print('GET ' + callsign)
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
        
_startTime = time.clock()
_bytesRead = 0
_highwaterDelta = 1000000
_highwater = _highwaterDelta

def handlePacket(raw):
    global _stationList
    global _startTime 
    global _bytesRead
    global _highwater
    global _highwaterDelta

    if raw is None: return
    packet = aprslib.parse(raw)
    if packet is None: return
    m = re.match(stationsToMatch, packet['from'])
    if m != None:
        packet['timestamp'] = time.time()
        packet['result'] = 'OK'
        if packet['from'] in _stationList:
            _stationList[packet['from']].update(packet)
            if 'message_text' not in packet and 'message_text' in _stationList[packet['from']]:
                del _stationList[packet['from']]['message_text']
        else:
            _stationList[packet['from']] = packet
        # print('- heard ' + packet['from'])

    # Record how many bytes we've read...
    _bytesRead = _bytesRead + len(raw)
    # And checkpoint it to the log occasionally.
    if _bytesRead > _highwater:
        _highwater = _bytesRead + _highwaterDelta
        elapsed = time.clock() - _startTime;
        hours, rem = divmod(elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        print("- elapsed {:0>2}:{:0>2}:{:05.2f} read {}".format(int(hours),int(minutes),seconds,_bytesRead))
        # If we're going to overflow, reset the counter and elapsed timer.
        if sys.maxsize - _bytesRead < _highwaterDelta:
            _bytesRead = 0
            _highwater = highwater_delta
            _startTime = time.clock()
        
def runAprsMonitor():
    while True:
        try:
            if password is not None:
                AIS = aprslib.IS(login, passwd = password)
            else:
                AIS = aprslib.IS(login)
            print('- Connecting to APRS-IS...')
            AIS.connect()
            print('- Connected! Handling incoming packets.')
            AIS.consumer(handlePacket, raw=True)
        except Exception as e:
            print(e);
            print('- APRS server socket failure... reconnecting in 2 seconds')
            time.sleep(2)
            
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
    password = None

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
CORS(app)
api = Api(app)
api.add_resource(Station, '/callsign/<string:callsign>')
if __name__ == '__main__':
    app.run()
