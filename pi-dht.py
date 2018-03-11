# Please run as root. Eg. sudo python pi-dht.py
import RPi.GPIO as GPIO
import subprocess
import os, sys
import time, requests, os.path
from requests.auth import HTTPBasicAuth
import json 
from pprint import pprint
import datetime
import piutils as piutils

configFilename = "config.json"

# Load configuration 
filedata = {}
if(os.path.isfile(configFilename) == True):
    with open(configFilename) as data_file:
        filedata = json.load(data_file)
# Confirm configuration available
if('server' not in filedata or 'UUID' not in filedata):
    print("Configuration incomplete. Please run setup.py first.")
    sys.exit()


def get_dht():
    # Get the temperature and Humidiy from air sensor. Returns a tubple (Temp, humidity)
    try:
        s = subprocess.check_output([os.getcwd() + "/Adafruit_Python_DHT/examples/AdafruitDHT.py", "2302", "4"])
        print("Sensor measurement returned " + s) # E.g.  Temp=19.8*  Humidity=41.5%
        lines = s.split("  ")
        if(len(lines) > 1):
            tmpTemp = lines[0].split("=")[1].replace('*','')
            tmpHum = lines[1].split("=")[1].replace('%','')
            return (float(tmpTemp), float(tmpHum))
        else:
            return ("Failed to read Temperature and Pressure from sensor")
    except:
        print("Error encountered while trying to read DHT")
        return 0

(piLatitude, piLongitude) = piutils.getLatLong()
print('Latitude/Longitude found as ' + str(piLatitude) + ", " + str(piLongitude))

dataToSend = { 
    "UUID": filedata['UUID'],
    "msg_type": "datum",
    "latitude": piLatitude,
    "longitude": piLongitude
}

while True:
    #
    # Send metric to server and inform user via console
    piTemperature = get_dht()[0]
    dataToSend['name'] = 'piTemperature'
    dataToSend['value'] = piTemperature
    print('Sending data to server: ' + filedata['server'])
    print(json.dumps(dataToSend, indent=4))
    piutils.sendDataToServer(dataToSend, filedata['server'])
    #
    piHumidity = get_dht()[1]
    dataToSend['name'] = 'piHumidity'
    dataToSend['value'] = piHumidity
    print('Sending data to server: ' + filedata['server'])
    print(json.dumps(dataToSend, indent=4))
    piutils.sendDataToServer(dataToSend, filedata['server'])
    #
    print(str(datetime.datetime.now()) + ' Pausing for 30 seconds...\n')
    #time.sleep(30)
    # Blink the LED at a rate slow to fast, indicating the temperature range
    if(piTemperature <= 20):
        piutils.blinkLed(1, 30)
    if(piTemperature > 20 and piTemperature < 25):
        piutils.blinkLed(3, 30)
    if(piTemperature >= 25):
        piutils.blinkLed(6, 30)