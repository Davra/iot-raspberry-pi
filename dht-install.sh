#!/bin/bash

cd `dirname $0`

git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo apt-get upgrade
sudo apt-get install build-essential python-dev
sudo python setup.py install
cd examples
echo " -- Starting to run the read operation for the digital air sensor..."
sudo ./AdafruitDHT.py 2302 4
