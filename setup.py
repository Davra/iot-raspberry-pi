# Establish connection with the Connecthing server
# Save the location of the Connecthing server to config.json for use by other programs
# Optionally: Create this device on the Connecthing server
#
import time, requests, os.path
from requests.auth import HTTPBasicAuth
import json 
from pprint import pprint
import datetime, sys
import piutils

configFilename = "config.json"

# Load configuration if it already exists
filedata = {}
if(os.path.isfile(configFilename) == True):
    with open(configFilename) as data_file:
        filedata = json.load(data_file)

if('server' not in filedata):
    # No configuration info exists so get it from user and save
    filedata['server'] = raw_input("Server location? ")
    with open(configFilename, 'w') as outfile:
        json.dump(filedata, outfile, indent=4)

    


print("Establishing connection to Connecthing server... ")
# Confirm can reach the server
r = requests.get(filedata['server'])
if(r.status_code == 200):
    #print(r.content)
    print("Ok, can reach " + filedata['server'])
else:
    print("Cannot reach server. " + filedata['server'] + ' Response: ' + str(r.status_code))

# Create this device on server
if('deviceName' not in filedata):        
    filedata['deviceName'] = raw_input("Name for this device? ")
    serverUsername = raw_input('Username:')
    serverPassword = raw_input('Password:')
    contents = '{ "name": "' + filedata['deviceName'] + '", '\
        + '"serialNumber": "' + filedata['deviceName'] + '" }'
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    #print('Sending data to server: ' + contents)
    r = requests.post(filedata['server'] + '/api/v1/devices', data=contents, \
        headers=headers, auth=HTTPBasicAuth(serverUsername, serverPassword))
    if(r.status_code == 200):
        print(r.content)
        filedata['UUID'] = json.loads(r.content)[0]['UUID']
        print("Device created on server. New UUID: " + filedata['UUID'])
        # Save device info to config file
        with open(configFilename, 'w') as outfile:
            json.dump(filedata, outfile, indent=4)
    else:
        print(r.content)
        print("Cannot reach server. " + str(r.status_code))
        sys.exit()
    #
    # Create metrics on server    
    piutils.createMetricOnServer('piCpuLoad', '%', filedata['server'], serverUsername, serverPassword)
    piutils.createMetricOnServer('piUptime', 's', filedata['server'], serverUsername, serverPassword)
    piutils.createMetricOnServer('piCpuTemp', 'C', filedata['server'], serverUsername, serverPassword)
    piutils.createMetricOnServer('piRamFree', '%', filedata['server'], serverUsername, serverPassword)
    piutils.createMetricOnServer('piTemperature', 'C', filedata['server'], serverUsername, serverPassword)
    piutils.createMetricOnServer('piHumidity', '%', filedata['server'], serverUsername, serverPassword)
    

print("Finished setup.")

