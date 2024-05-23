from machine import Pin, Timer
import time


led = Pin(20, Pin.OUT, Pin.PULL_UP )




tim = Timer()
def tick(timer):
  global led
  led.toggle()

#tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)

led.value(1)

print (time.localtime())

