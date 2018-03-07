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


def get_ram():
    #Returns a tuple (total ram, available ram) in megabytes.
    try:
        s = subprocess.check_output(["free", "-m"])
        lines = s.split("\n")
        return ( int(lines[1].split()[1]), int(lines[2].split()[3]) )
    except:
        return 0

def get_process_count():
    #Returns the number of processes.
    try:
        s = subprocess.check_output(["ps","-e"])
        return len(s.split("\n"))
    except:
        return 0

def get_up_stats():
    #Returns a tuple (uptime, 1 min load average).
    try:
        s = subprocess.check_output(["uptime"])
        load_split = s.split("load average: ")
        load_one = float(load_split[1].split(",")[0])
        up = load_split[0]
        up_pos = up.rfind(",", 0, len(up)-4)
        up = up[:up_pos].split("up ")[1]
        return (up, load_one)
    except:
        return ("", 0)

def get_proc_uptime():
    # Returns uptime in seconds
    try:
        s = subprocess.check_output(["cat", "/proc/uptime"])
        return int(float(s.split(" ")[0]))
    except:
        return 0

def get_proc_idletime():
    # Returns idle cpu time in seconds
    try:
        s = subprocess.check_output(["cat", "/proc/uptime"])
        return int(float(s.split(" ")[1]))
    except:
        return 0

def get_connections():
    #Returns the number of network connections.
    try:
        s = subprocess.check_output(["netstat", "-tun"])
        return len([x for x in s.split() if x == "ESTABLISHED"])
    except:
        return 0

def get_cpu_temperature():
    #Returns the temperature in degrees C.
    try:
        s = subprocess.check_output(["/opt/vc/bin/vcgencmd", "measure_temp"])
        return float(s.split("=")[1][:-3])
    except:
        return 0



# piRamFree: str(get_ram()[1])
# ramTotal: str(get_ram()[0])
# processes: str(get_process_count())
# piCpuTemp: str(get_cpu_temperature())
# lanIpAddress: piutils.getLanIpAddress()
# piUptime: str(get_proc_uptime())
# piCpuLoad: str(get_up_stats()[1])

(piLatitude, piLongitude) = piutils.getLatLong()
print('Latitude/Longitude found as ' + str(piLatitude) + ", " + str(piLongitude))

dataToSend = { 
    "UUID": filedata['UUID'],
    "name": "piUptime",
    "value": get_proc_uptime(),
    "msg_type": "datum",
    "latitude": piLatitude,
    "longitude": piLongitude
}

while True:
    # Inform user of the overall data being sent for a single metric
    print('Sending data to server: ' + filedata['server'])
    print(json.dumps(dataToSend, indent=4))
    #
    # Send CPU uptime as metric piUptime to server
    dataToSend['name'] = 'piUptime'
    dataToSend['value'] = get_proc_uptime()
    piutils.sendDataToServer(dataToSend, filedata['server'])
    #
    dataToSend['name'] = 'piCpuTemp'
    dataToSend['value'] = get_cpu_temperature()
    piutils.sendDataToServer(dataToSend, filedata['server'])
    #
    dataToSend['name'] = 'piCpuLoad'
    dataToSend['value'] = get_up_stats()[1]
    piutils.sendDataToServer(dataToSend, filedata['server'])
    #
    dataToSend['name'] = 'piRamFree'
    dataToSend['value'] = get_ram()[1]
    piutils.sendDataToServer(dataToSend, filedata['server'])
    #
    print(str(datetime.datetime.now()) + ' Pausing for 30 seconds...\n')
    time.sleep(30)