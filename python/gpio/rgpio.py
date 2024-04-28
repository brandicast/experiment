from gpiozero import LED

from time import sleep

import os

#factory = PiGPIOFactory(host='192.168.68.54')
os.environ["PIGPIO_ADDR"] = "192.168.68.54"
os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

#red = LED(10,pin_factory=factory)
red = LED (10)

counter = 3

while True:
 red.on()
 print ("led on")
 sleep(1)
 red.off()
 print ("led off")
 sleep(1)
 counter = counter -1 
 if counter == 0:
  break
 
