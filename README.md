# iot-raspberry-pi
Demonstration for connecting Raspberry Pi to AEP platform. You should already have a login/password to log into the Connecthing platform. If not, please contact your local administrator or support@davra.io.

### Get Started
You just need a Raspberry Pi, any version should do. It should be connected to the power supply and the network. The easiest way to connect to the network is to plug an ethernet cable in but you can also use a wifi connection. When the Raspbeery Pi boots up and you have the HDMI cable connected to a tv or monitor, it will show what it's IP address is. 

### Typing in to the Raspberry Pi
- Option 1: Connect a keyboard to the Raspberry Pi and you can type directly into the Raspberry Pi and see it on-screen.
- Option 2: If you know the IP address you can "ssh" to that IP. If you are using Windows or Mac, you can use the program "putty". 

### Download and install the basic programs
Type the following commands at the prompt:
```
git clone https://github.com/Davra/iot-raspberry-pi.git
cd iot-raspberry-pi
python setup.py
```
This setup program will ask you what the server address it. You should type in the location of your server (eg. demo.connecthing.io). Then it will ask what your device name is. You should type in something which you recognise (e.g. your own name). Then it will ask for a username and password. These are what you use to connect to the Connecthing server.

### Run the basic program
Type the following command at the prompt:
```
python pi-iot.py
```
This program will find out some statistics about your Raspberry Pi, such as the temperature of the CPU and how long the Pi has been powered on for then upload that data to the Connecthing server.

### Create a dashboard on Connecthing to see your data
On your computer, use a browser to navigate to the Connecthing server (eg demo.connecthing.io) and log in with your username and password. 
- Go to the "Applications" link on the left menu. Click "Add Application"; give it a name and click "Create".
- Select the "Single Line Graph" option. In the settings page for this graph, choose to graph the metric "piUptime". Save the settings (right side of page) then click the "finish" button. The chart will now be in your dashboard and hopefully displaying at least 1 datapoint from your Raspberry Pi.
- Add another graph in a similar way to the previous graph, one for each of the metrics "piCpuload", "piCpuTemp" and "piRamFree".
You should now have a dashboard showing 4 aspects of data streaming every 30 seconds from your Raspberry Pi device to the Connecthing server.

### Add an Air Sensor to the Pi
Connect the 3 pins of the air sensor "AD2032". This sensor measures the temperature and humidity of the air. Connect the pins as follows:
- GND on sensor to Ground pin on Pi (pin 6).
- VCC on sensor to 3.3V pin on pi (pin 1).
- SIG on sensor to GPIO 4 on Pi (pin 7).

### Run program to read air sensor
On the Raspberry Pi prompt, type the following:
```
sudo dht-install.sh
```
That will install the DHT (Digital Humidity and Temperature) program so that it the Pi can understand the readings coming from the sensor. It may take a minute or 2 to complete and may ask you to approve the installation of more files. If so, type "y" without the quotes to approve the request. Then type the following at the Raspberry Pi prompt:
```
python pi-dht.py
```
This program will keep running, reading the temperature and pressure at 30 second intervals and uploading them to the Connecthing server.

### Create a dashboard to show temperature and pressure
On your computer, while logged in to the Connecthing server, add 2 more graphs on the dashboard to show the metrics "piTemperature" and "piHumidity".

### Add an LED to indicate temperature
Connect an LED to the Raspberry Pi. The short leg of the LED should be connected to Ground which is pin 9 on the raspberry Pi. The long leg of the LED should be connected to a 470 Ohm resistor and the other end of the resistor should be connected to GPIO 27 on the Raspberry Pi (pin 13).
If the pi-dht.py program is still running the LED will blink. It has 3 speeds: slow when the temperature is below 20 degrees Celcius, faster up to 25 degrees C and fastest when above 25 degrees C.


