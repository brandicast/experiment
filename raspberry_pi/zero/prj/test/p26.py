import RPi.GPIO as GPIO
import time

GPIO.setmode (GPIO.BCM)
pin=26



GPIO.setup(pin,GPIO.OUT)

GPIO.output(pin, True)
time.sleep(60)
GPIO.output(pin, False)
 
GPIO.cleanup()
