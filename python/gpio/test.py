import RPi.GPIO as GPIO
import time

GPIO.setmode (GPIO.BOARD)
led=16
counter = 10
while True:
 GPIO.setup(led,GPIO.OUT)
 print ("LED On")
 GPIO.output(led, True)
 time.sleep(2)
 print ("LED Off")
 GPIO.output(led, False)
 time.sleep(2)
 counter = counter - 1
 if counter == 0 :
  break

GPIO.cleanup()
