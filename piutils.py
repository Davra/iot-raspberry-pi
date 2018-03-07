# Utility functions for other programs
#
import RPi.GPIO as GPIO
import subprocess
import os, sys
import time, requests, os.path
from requests.auth import HTTPBasicAuth
import json 
from pprint import pprint
import datetime

utilsConfigFilename = "config.json"

# Load configuration if it already exists
utilsConfigData = {}
if(os.path.isfile(utilsConfigFilename) == True):
    with open(utilsConfigFilename) as data_file:
        utilsConfigData = json.load(data_file)



def createMetricOnServer(metricName, metricUnits, serverAddress, serverUsername, serverPassword):
    contents = '[{ "name": "' + metricName + '", "'\
        + '"label": "' + metricName + '", '\
        + '"semantics": "metric" }]'
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    #print('Sending data to server: ' + contents)
    r = requests.post(serverAddress + '/api/v1/iotdata/meta-data', data=contents, \
        headers=headers, auth=HTTPBasicAuth(serverUsername, serverPassword))
    if(r.status_code == 200):
        #print(r.content)
        print("Metric created on server: " + metricName)
    else:
        print("Failed to create metric on server: " + metricName + ' : ' + str(r.status_code))
        sys.exit()
    return



def sendDataToServer(dataToSend, serverAddress):
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    r = requests.put(serverAddress + '/api/v1/iotdata', data=json.dumps(dataToSend), headers=headers)
    if (r.status_code == 200):
        #print(r.content)
        print("Data sent ok: " + str(dataToSend['name']) + ': '+ str(dataToSend['value']))
    else:
        print("Issue while sending data to server. " + str(r.status_code) + ': ' + r.content)



def getLanIpAddress():
    # Returns the current LAN IP address.
    arg = "ip route list"
    p = subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    ipaddr = split_data[split_data.index("src")+1]
    return ipaddr


def getWanIpAddress():
    # Returns the current WAN IP address, as calls to internet server perceive it
    arg = "curl -s http://whatismyip.akamai.com/"
    p = subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    return data[0]


def getLatLong():
    # Use IP address to guess location from geoIp
    wanIpAddress = getWanIpAddress()
    # Make call to GeoIP server to find out location from WAN IP
    print('Getting Lat/Long from WAN IP: ' + wanIpAddress)
    r = requests.get('https://freegeoip.net/json/' + wanIpAddress)
    if(r.status_code == 200):
        #country = r.content.country_name
        jsonContent = json.loads(r.content)
        latitude = jsonContent['latitude']
        longitude = jsonContent['longitude']
        return (latitude, longitude)
    else:
        print("Cannot reach server. " + str(r.status_code))
        return (0,0)
        

def blinkLed(blinksPerSecond, secondsToBlinkFor):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
    ledMode = GPIO.LOW
    countBlinks = 0.0
    while countBlinks < (blinksPerSecond * secondsToBlinkFor):
        if(ledMode == GPIO.LOW):
            ledMode = GPIO.HIGH
        else:
            ledMode = GPIO.LOW
        print("Setting LED " + str(ledMode))
        GPIO.output(27, ledMode)
        time.sleep(0.5 / blinksPerSecond)
        countBlinks += 0.5

