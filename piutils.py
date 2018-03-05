# Utility functions for other programs
#
import time, requests, os.path
from requests.auth import HTTPBasicAuth
import json 
from pprint import pprint
import datetime

configFilename = "config.json"

# Load configuration if it already exists
configdata = {}
if(os.path.isfile(configFilename) == True):
    with open(configFilename) as data_file:
        configdata = json.load(data_file)

