import RPi.GPIO as GPIO
import subprocess
import os, sys
import time, requests, os.path
from requests.auth import HTTPBasicAuth
import json 
from pprint import pprint
import datetime
import piutils

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
    #Returns a tuple (uptime in seconds, idle seconds).
    try:
        s = subprocess.check_output(["cat", "/proc/uptime"])
        return (s.split(" "))
    except:
        return ("", 0)

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

def get_ipaddress():
    #Returns the current IP address.
    arg = "ip route list"
    p = subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    ipaddr = split_data[split_data.index("src")+1]
    return ipaddr


print(" { ramFree: " + str(get_ram()[1])\
    + ", ramTotal: " +str(get_ram()[0])\
    + ", processes: " + str(get_process_count())\
    + ", cpuTemp: " + str(get_cpu_temperature())\
    + ", ipAddress: " + get_ipaddress()\
    + ", uptime: " + str(get_proc_uptime()[0])\
    + ", cpuLoad: " + str(get_up_stats()[1])\
    + " } ")


dataToSend = '{ "UUID": "' + filedata['UUID'] + '", '\
    + ' "name": "43040_101", '\
    + ' "value": ' + str(get_up_stats()[1]) + ', '\
    + ' "msg_type": "datum" '\
    + ' } '
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
print('Sending data to server: ' + dataToSend)
r = requests.put(filedata['server'] + '/api/v1/iotdata', data=dataToSend, headers=headers)
if (r.status_code == 200):
    print(r.content)
    print("Device data sent ok")
else:
    print("Cannot reach server. " + str(r.status_code))
    
