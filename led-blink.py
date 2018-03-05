import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
ledMode = GPIO.LOW
while True:
    if(ledMode == GPIO.LOW):
        ledMode = GPIO.HIGH
    else:
        ledMode = GPIO.LOW
    print("Setting LED " + str(ledMode))
    GPIO.output(27, ledMode)
    time.sleep(1)
